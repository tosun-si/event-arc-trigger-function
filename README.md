# Command to deploy the function with Event Arc

The Medium article for this use case : 

https://medium.com/@mazlum.tosun/event-driven-cloud-function-load-gcs-file-to-bigquery-with-event-arc-a1540c1d2055

## Before to begin, check this link : 

https://cloud.google.com/eventarc/docs/run/create-trigger-storage-gcloud#before-you-begin

Update `GCloud CLI` : 

```bash
gcloud components update
```

Grant the pubsub.publisher role to the Cloud Storage service account:

```bash
SERVICE_ACCOUNT="$(gsutil kms serviceaccount -p gb-poc-373711)"

gcloud projects add-iam-policy-binding gb-poc-373711 \
--member="serviceAccount:${SERVICE_ACCOUNT}" \
--role='roles/pubsub.publisher'
```

At the root of the project, trigger the following command : 

```bash
gcloud functions deploy saving-job-failures-bq \
  --gen2 \
  --region=europe-west1 \
  --runtime=python310 \
  --source=functions/saving_job_failures_bq \
  --entry-point=save_gcs_file_to_bq_function \
  --run-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=event-arc-trigger-function" \
  --trigger-location=europe-west1 \
  --trigger-service-account=sa-cloud-functions-dev@gb-poc-373711.iam.gserviceaccount.com
```

## Deploy the function with Terraform and Cloud Build from local machine

### Set env vars in your Shell

```shell
export PROJECT_ID={{your_project_id}}
export LOCATION={{your_location}}
export TF_STATE_BUCKET={{your_tf_state_bucket}}
export TF_STATE_PREFIX={{your_tf_state_prefix}}
export GOOGLE_PROVIDER_VERSION="= 4.47.0"
```

### Plan

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config terraform-plan-modules.yaml \
    --substitutions _ENV=dev,_TF_STATE_BUCKET=$TF_STATE_BUCKET,_TF_STATE_PREFIX=$TF_STATE_PREFIX,_GOOGLE_PROVIDER_VERSION=$GOOGLE_PROVIDER_VERSION \
    --verbosity="debug" .
```


### Apply

```shell
gcloud builds submit \
    --project=$PROJECT_ID \
    --region=$LOCATION \
    --config terraform-apply-modules.yaml \
    --substitutions _ENV=dev,_TF_STATE_BUCKET=$TF_STATE_BUCKET,_TF_STATE_PREFIX=$TF_STATE_PREFIX,_GOOGLE_PROVIDER_VERSION=$GOOGLE_PROVIDER_VERSION \
    --verbosity="debug" .
```

## Interesting links

Documentations : 

https://cloud.google.com/functions/docs/tutorials/storage#object_finalize
https://cloud.google.com/functions/docs/writing#directory-structure-python
https://cloud.google.com/functions/docs/deploy
https://cloud.google.com/eventarc/docs/reference/supported-events
https://cloud.google.com/functions/docs/calling/eventarc
https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-csv#loading_csv_data_into_a_table

Code : 

https://github.com/GoogleCloudPlatform/eventarc-samples
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/functions/v2/storage/main.py
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/functions/v2/storage/main_test.py