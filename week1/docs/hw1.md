### Q1: Which tag has the following text? - Automatically remove the container when it exits

docker run --help

Ans:

*--rm                             Automatically remove the container when it exits*

### Q2: What is version of the package wheel ?

Ans:
docker run -t -i --rm python:3.9 bash

pip list

*wheel      0.42.0*

### Q3: How many taxi trips were totally made on September 18th 2019?  (count records with condition)

Ans:
SELECT
COUNT(1)
FROM
public.green_taxi_trips
WHERE
DATE(lpep_pickup_datetime) = '2019-09-18'
AND DATE(lpep_dropoff_datetime) = '2019-09-18'

*result of the query: 15612*

### Q4: Which was the pick up day with the largest trip distance?

Ans:
SELECT
DATE(lpep_pickup_datetime)
FROM
public.green_taxi_trips
WHERE
trip_distance = (
SELECT
MAX(trip_distance)
FROM
public.green_taxi_trips
)

*result of the query: 2019-09-26*

### Q5: Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

Ans:
SELECT
CAST(t.lpep_dropoff_datetime AS DATE) AS day,
SUM(t.total_amount) AS sum,
zpu."Borough"
FROM
green_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
WHERE
CAST(t.lpep_dropoff_datetime AS DATE) = '2019-09-18'
GROUP BY
1,
3
HAVING
SUM(t.total_amount) > 50000

*result of the query: "Brooklyn", "Manhattan", "Queens"*

"day","sum","Borough"
"2019-09-18","95903.83999999963","Brooklyn"
"2019-09-18","92388.12000000033","Manhattan"
"2019-09-18","78788.35999999978","Queens"

### Q6: For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?

Ans:
SELECT
t.tip_amount,
zpu."Zone" as "pu_zone",
zdo."Zone" as "do_zone"
FROM
green_taxi_trips t
JOIN zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE
zpu."Zone" = 'Astoria'
ORDER BY
t.tip_amount DESC
LIMIT
1;

*Result of the query: "JFK Airport"*
"tip_amount","pu_zone","do_zone"
"62.31","Astoria","JFK Airport"

### Q7: Paste the output of this command (terraform apply ) into the homework submission form.

Ans.
Terraform used the selected providers to generate the following execution plan. Resource
actions are indicated with the following symbols:

+ create

Terraform will perform the following actions:

google_bigquery_dataset.dataset will be created

+ resource "google_bigquery_dataset" "dataset" {
  + creation_time              = (known after apply)
  + dataset_id                 = "bq-dataset"
  + default_collation          = (known after apply)
  + delete_contents_on_destroy = false
  + effective_labels           = (known after apply)
  + etag                       = (known after apply)
  + id                         = (known after apply)
  + is_case_insensitive        = (known after apply)
  + last_modified_time         = (known after apply)
  + location                   = "EU"
  + max_time_travel_hours      = (known after apply)
  + project                    = "dtc-de-zoomcamp-2024"
  + self_link                  = (known after apply)
  + storage_billing_model      = (known after apply)
  + terraform_labels           = (known after apply)
    }

google_storage_bucket.data-lake-bucket will be created

+ resource "google_storage_bucket" "data-lake-bucket" {
  + effective_labels            = (known after apply)
  + force_destroy               = true
  + id                          = (known after apply)
  + location                    = "EU"
  + name                        = "dtc-de-zoomcamp-2024-data-lake-bucket"
  + project                     = (known after apply)
  + public_access_prevention    = (known after apply)
  + rpo                         = (known after apply)
  + self_link                   = (known after apply)
  + storage_class               = "STANDARD"
  + terraform_labels            = (known after apply)
  + uniform_bucket_level_access = true
  + url                         = (known after apply)
  + lifecycle_rule {

    + action {
      + type = "Delete"
        }
    + condition {
      + age                   = 30
      + matches_prefix        = []
      + matches_storage_class = []
      + matches_suffix        = []
      + with_state            = (known after apply)
        }
        }
  + versioning {

    + enabled = true
      }
      }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.

Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/dtc-de-zoomcamp-2024/datasets/bq_dataset]
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc-de-zoomcamp-2024-data-lake-bucket]

*Apply complete! Resources: 2 added, 0 changed, 0 destroyed.*
