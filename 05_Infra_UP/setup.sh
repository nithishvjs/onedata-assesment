#!/bin/bash

echo "Starting infrastructure..."
docker compose pull    
docker compose build    
docker compose up -d    
echo "All services are running!"
