terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = "python-ops-mvp-kaz-2026"
  region  = "asia-northeast1"
}

resource "google_storage_bucket" "cleaned_data_bucket" {
  name                        = "python-ops-mvp-kaz-2026-cleaned-data"
  location                    = "ASIA-NORTHEAST1"
  uniform_bucket_level_access = true
  force_destroy               = true
}
