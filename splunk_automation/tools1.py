from langchain.tools import tool
import splunklib.client as client
import splunklib.results as results
import os
import os.path
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
USERNAME=os.environ["SPLUNK_USER"]
PASSWORD=os.environ["SPLUNK_PASSWORD"]

def connect_splunk():
    """ connect to splunk"""
    service=client.connect(
        host="localhost",
        port=8089,
        username=USERNAME,
        password=PASSWORD
    )
    return service

@tool
def get_failed_login_attempts()->str:
    """
    Fetches IPs, hosts, and accounts with failed login attempts from Splunk.
    Returns a JSON string of failed login events for analysis.
    """
    service=connect_splunk()
    serach_query="""
    search index="main" action="LogonFailed"
    """
    job=service.jobs.create(serach_query,exec_mode="normal")
    while not job.is_done():
        job.refresh()
    reader=results.ResultsReader(job.results())
    failed_records=[i for i in reader if isinstance(i,dict)]
    df=pd.DataFrame(failed_records)
    return df.to_json(orient="records")



