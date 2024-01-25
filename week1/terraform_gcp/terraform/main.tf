terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.11.0"
    }
  }
}


provider "google" {
  project = "dtc-de-zoomcamp-2024"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_storage_bucket" "data-lake-bucket" {
  name     = "dtc-de-zoomcamp-2024-data-lake-bucket"
  location = "EU"

  # Optional, but recommended settings:
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = "bq_dataset"
  project    = "dtc-de-zoomcamp-2024"
  location   = "EU"
}
