from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from PostgresFileOperator import PostgresFileOperator

with DAG(
    
    dag_id="tecnica_postgres",
    start_date=datetime(2024,10,18),
    #schedule_interval='0 0 * * *'
    
    
    
) as dag:
    task_1=PostgresOperator(
        task_id="Crear_tabla",
        postgres_conn_id="postgres_localhost",
        sql="""CREATE TABLE IF NOT EXISTS productos_mercadolibre (
            
            id varchar(500),
            site_id varchar(500),
            title varchar (500),
            price varchar(500),
            available_quantity varchar(200),
            thumbnail varchar(500),
            DATE varchar(100)
            
            )"""
    )
    
    task_2 = BashOperator(
        task_id="Consultar_api",
        bash_command = "python /opt/airflow/dags/consult_api.py"
        
        )
    
    task_3 = PostgresFileOperator(
        
        task_id="Insertar_Data",
        operation="write",
        config={"table_name":"productos_mercadolibre"}
        
    )
    
    task_4 = PostgresFileOperator(
        
        task_id="Leer_Data",
        operation="read",
        config={"query":"SELECT id, site_id, title, price, available_quantity, thumbnail, date FROM public.productos_mercadolibre WHERE price != 'null' AND (cast(price as decimal)*cast(available_quantity as integer)) > 10000000"}
        
    )
    
    task_1 >> task_2 >> task_3 >> task_4

