#!/bin/bash

# Step 1: Run the first docker-compose file (database and download)
docker compose -f docker-compose-download.yml build && docker compose -f docker-compose-download.yml up --abort-on-container-exit

# Check if the first compose file ran successfully
if [ $? -eq 0 ]; then
  echo "First Docker Compose (download) completed successfully."

  # Step 2: Run the second docker-compose file (report)
  docker compose -f docker-compose-report.yml build && docker compose -f docker-compose-report.yml up --abort-on-container-exit

  if [ $? -eq 0 ]; then
    echo "Second Docker Compose (report generation) completed successfully."
  else
    echo "Error: Report generation failed."
  fi
else
  echo "Error: First Docker Compose (db and download) failed."
fi
