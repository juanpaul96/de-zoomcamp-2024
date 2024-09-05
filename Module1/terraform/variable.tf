variable "project" {
  description = "Project"
  default     = "ny-rides-431120"
}
variable "location" {
  description = "Project Location"
  default     = "US"
}
variable "region" {
  description = "Region"
  default     = "us-central1"
}
variable "bq_datase_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}
variable "gcs_bucket_name" {
  description = "My BigQuery Bucket Name"
  default     = "ny-rides-431120-auto-expiring-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}