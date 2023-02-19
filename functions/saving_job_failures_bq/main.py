import pathlib
from typing import Dict

import functions_framework
from google.cloud import bigquery


@functions_framework.cloud_event
def save_gcs_file_to_bq_function(cloud_event):
    data: Dict = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]

    table_id = "gb-poc-373711.monitoring.job_failure"

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")

    client = bigquery.Client()

    current_directory = pathlib.Path(__file__).parent
    schema_path = str(current_directory / "schema/job_failure.json")

    schema = client.schema_from_json(schema_path)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )

    uri = f"gs://{bucket}/{name}"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()

    print("#######The GCS file was correctly loaded to the BigQuery table#######")
