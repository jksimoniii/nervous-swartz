# nervous-swartz
A random project name

# Getting Started
## Requirements
  - Docker
  - GCP Keys + GCP Storage Bucket 
  
## Setup
### Configure Environment Variables
Copy the provided `.env.sample` to `.env` and fill in any blank values
with the appropriate variables.

### Configure GCP
Place your GCP credentials into `keys/gcp.json`

### Build and Run
```
docker build -t jksimoniii .
docker run -p 8000:8000 --env-file .env jksimoniii python manage.py runserver
```

## How to Use
### Workflow explained
  1) Because BigQuery responses may be large (and slow), the system will respond to a query
  request with a `job`. This `job` can be retrieved at anytime using the url returned in the response body (see [API](perform-bigquery-lookup)).
  2) When retrieving a job, the `finished` property will denote whether or not the job has finished
  executing. Once `finished=True`, a `resource_url` will become available to link you the externally stored document.
  This assumes the document is public in GCP.

### API Endpoints
#### Perform BigQuery lookup
```
GET /api/bigquery/:resource/:dataset/tables/:table/
```
Filtering is provided by query parameters, in the form `?field_name=value`

Here's an example, filtering BigQuery’s public BLS dataset for `?year=2018`
```
RESOURCE=bigquery-public-data
DATASET=bls
TABLE=unemployment_cps
curl -X GET 'http://localhost:8000/api/bigquery/$RESOURCE/$DATASET/tables/$TABLE/?year=2018' | jq
{
  "url": "http://localhost:8000/api/bigquery/jobs/f5e2617b-55c9-48f1-9439-3daef4c3bbcd/",
  "finished": false,
  "query": "SELECT * FROM bigquery-public-data.bls.unemployment_cps WHERE year=2018",
  "resource_url": null
}
```

#### Retrieve a Job
```
curl -X GET http://localhost:8000/api/bigquery/jobs/f5e2617b-55c9-48f1-9439-3daef4c3bbcd/
{
  "url": "http://localhost:8000/api/bigquery/jobs/f5e2617b-55c9-48f1-9439-3daef4c3bbcd/",
  "finished": true,
  "query": "SELECT * FROM bigquery-public-data.bls.unemployment_cps WHERE year=2018",
  "resource_url": "https://jksimoniii-bigquery.storage.googleapis.com/f5e2617b-55c9-48f1-9439-3daef4c3bbcd.csv"
}
```