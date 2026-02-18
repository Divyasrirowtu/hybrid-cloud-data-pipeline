resource "google_cloudfunctions_function" "processor" {
  name        = "pubsub-processor"
  runtime     = "python39"
  entry_point = "process_pubsub"
  source_directory = "${path.module}/../src/processor_function"
  trigger_topic = google_pubsub_topic.localstack_events.name
  region       = var.gcp_region
}
