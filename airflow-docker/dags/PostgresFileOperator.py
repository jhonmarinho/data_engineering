from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook

#For sending email.
from airflow.models import Variable
from email.message import EmailMessage
import ssl
import smtplib

class PostgresFileOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self,
                operation,
                config={},
                *args,
                **kwargs):
        super(PostgresFileOperator, self). __init__(*args, **kwargs)
        self.operation = operation
        self.config = config
        self.postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
        
    def execute(self, context):
        if self.operation == "write":
            self.writeInTable()
            pass
        elif self.operation == "read":
            self.readTable()
            pass
        
    def writeInTable(self):
        self.postgres_hook.bulk_load(self.config.get('table_name'), '/opt/airflow/dags/tmp/file.tsv')
        
    def readTable(self):
        conn = self.postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.config.get('query'))
        data = [doc for doc in cursor]
        
        if data:
            #do something
            print(data)
            email_sender = 'pruebasdevdata@gmail.com'   
            email_password = Variable.get("EMAIL_PASSWORD")
            email_receiver = 'pruebasdevdata@gmail.com'

            title = "ALERTA ! Items con demasiadas ventas"
            body="""Hemos detectado nuevos items con demasiadas ventas {}""".format(data)

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = title
            em.set_content(body)

            context=ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())