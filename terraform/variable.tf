variable "credentials" {
  description = "My Credentials"
  default     = "/home/vscode/.gcp/dtc-de-course-485513-cc4073dc69b5.json"
}

variable "project" {
  description = "Project"
  default     = "dtc-de-course-485513"
}

variable "region" {
  description = "Region"
  default     = "europe-west3"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "de_zoomcamp_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "dtc-de-course-fh-2026-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}