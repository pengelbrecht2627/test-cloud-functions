provider "google" {
  credentials = file("account.json")
  project     = "eta-testing-239509"
  region      = var.gcp.region
  version     = "~> 3.15"
}

data "google_client_config" "current" {
}