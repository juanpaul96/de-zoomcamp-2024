terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"

    }
  }
}
provider "google" {
  credentials = "./keys/my-creds.json"
  project     = var.project
  region      = "us-central1"
}

resource "google_storage_bucket" "auto-expire" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_datase_name
  location   = var.location
}