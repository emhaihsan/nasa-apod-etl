# NASA APOD ETL Pipeline

## Overview

This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from the NASA APOD API, transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.

## Key Components

1. **Airflow for Orchestration**: Airflow is used to define, schedule, and monitor the entire ETL pipeline. It manages task dependencies, ensuring that the process runs sequentially and reliably.
2. **Postgres Database**: A PostgreSQL database is used to store the extracted and transformed data. Postgres is hosted in a Docker container, making it easy to manage and ensuring data persistence through Docker volumes.
3. **NASA API (Astronomy Picture of the Day)**: The external API used in this project is NASA's APOD API, which provides data about the astronomy picture of the day.
4. **Airflow Hooks and Operators**: Airflow hooks and operators are used to handle the ETL process efficiently.

## Objectives

1. **Extract Data**: The pipeline extracts astronomy-related data from NASA's APOD API on a scheduled basis.
2. **Transform Data**: Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.
3. **Load Data into Postgres**: The transformed data is loaded into a Postgres database. The data can be used for further analysis, reporting, or visualization.

## Architecture and Workflow

The ETL pipeline is orchestrated in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. **Extract (E)**: The SimpleHttpOperator is used to make HTTP GET requests to NASA's APOD API. The response is in JSON format.
2. **Transform (T)**: The extracted JSON data is processed in the transform task using Airflow's TaskFlow API. This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database.
3. **Load (L)**: The transformed data is loaded into a Postgres table using PostgresHook. If the target table doesn't exist in the Postgres database, it is created automatically as part of the DAG.

## Additional Information

- NASA APOD API: <https://api.nasa.gov/planetary/apod>
- Postgres documentation: <https://www.postgresql.org/docs/>
- Airflow documentation: <https://airflow.apache.org/docs/>
