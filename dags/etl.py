from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago


## Define the DAG
with DAG(
    dag_id="nasa_apod_postgres",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    ## step 1: Create the table if it doesn't exist

    @task
    def create_table():
        # Initialize the PostgresHook
        hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        # SQL query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        # Run the SQL query to create the table
        hook.run(create_table_query)


    ## step 2 : Extract data from the API (Nasa APOD)
    extract_apod = SimpleHttpOperator(
        task_id="extract_apod",
        http_conn_id="nasa_api", ## connection id defined in airflow for nasa api
        endpoint=f"planetary/apod", ## nasa api endpoint for apod
        method="GET",
        data={"api_key":"{{conn.nasa_api.extra_dejson.api_key}}"}, ## use the connection id to get the api key
        response_filter=lambda response: response.json(), ## convert response to json
    )
 
    ## step 3 : Transform the data
    @task
    def transform_apod_data(response):
        apod_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", "")
        }
        return apod_data


    ## step 4 : Load the data into the database
    @task
    def load_data_to_db(apod_data):
        # initialize the postgreshook
        hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        # define the sql query
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type) VALUES (%s, %s, %s, %s, %s)
        """
        # run the sql query
        hook.run(insert_query, parameters=(apod_data["title"], apod_data["explanation"], apod_data["url"], apod_data["date"], apod_data["media_type"]))



    ## Step 5: Define the dependencies
    ## Extract
    create_table() >> extract_apod ## Ensure the table is created before the extraction 
    api_response = extract_apod.output
    ## Transform
    transformed_data = transform_apod_data(api_response) 
    ## Load
    load_data_to_db(transformed_data)



