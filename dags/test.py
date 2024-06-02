from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    # 'start_date': datetime(2023, 5, 27),
    # 'retries': 1,
}

# Define the DAG
dag = DAG(
    'extract_data_from_postgres',
    default_args=default_args,
    description='A simple DAG to extract data from PostgreSQL running in Docker',
    # schedule_interval='@daily',
)

# Define the PostgreSQL connection details
POSTGRES_CONN_ID = 'postgres_main'

# Function to extract data from PostgreSQL
def extract_data_from_postgres():
    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sample_retail")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    # Process the records if necessary
    for record in records:
        print(record)

# Define the PythonOperator task
extract_data_task = PythonOperator(
    task_id='extract_data_task',
    python_callable=extract_data_from_postgres,
    dag=dag,
)

# Set task dependencies
extract_data_task