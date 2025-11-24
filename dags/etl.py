from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task 
from airflow.providers.postgres.hooks.postgres import PostgresHook 
import json
from airflow.utils.dates import days_ago

##Defining the DAG

with DAG(
    dag_id='nasa_apod_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    ## step1: Create the table if it does not exists

    @task
    def create_table():
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")


        ##SQL query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data(
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        explanation TEXT,
        url TEXT,
        
        data DATE,
        media_type VARCHAR(50));

        """
        ##Execute the above query
        postgres_hook.run(create_table_query)


    ##Step2: extract APOD data (Extract Pipeline)
    extract_apod=SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={'api_key':"{{conn.nasa_api.extra_dejson.api_key}}"},
        response_filter=lambda response:response.json(),
    )
    ##step3: Transform the data
    @task
    def transform_apod_data(response):
        apod_data={
          'title':response.get('title',''),
          'explanation':response.get('explanation',''),
          'url':response.get('url',''),
          'date':response.get('date',''),
          'media_type':response.get('media_type','')  
        }
        return apod_data
    
    ##step4: Load the data into PostgreSQL
    @task
    def load_data_to_postgres(apod_data):
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        insert_query="""
        INSERT INTO     apod_data (title, explanation, url, data, media_type)
        VALUES (%s,%s,%s,%s,%s);
        """


        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']

        ))
    ##step 5 : verify the data using DBViewer
    ##step 6: define the task dependencies
    create_table() >> extract_apod  ##Enusre the tables is created before extraction
    api_response=extract_apod.output
    transformed_data=transform_apod_data(api_response)
    load_data_to_postgres(transformed_data)
