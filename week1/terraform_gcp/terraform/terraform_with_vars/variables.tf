variable "credentials" {
  description = "My credentials"
  default     = "../../keys/dtc-de-zoomcamp-2024-9e862cc7c6aa.json"
}

variable "project" {
  description = "Project"
  default     = "dtc-de-zoomcamp-2024"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "zone" {
  description = "Zone"
  default     = "us-central1-c"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "bq_dataset"
}

variable "gcs_bucket_name" {
  description = "MY GCS bucket name"
  default     = "dtc-de-zoomcamp-2024-data-lake-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "uniform_bucket_level_access" {
  description = "Uniform bucket level access"
  default     = true
}
