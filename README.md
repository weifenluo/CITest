# CITest

CI Testing with Windows Runner and Linux Container Database

## Overview

This repository demonstrates how to run CI tests using GitHub Actions with:
- **Windows runners** (windows-latest)
- **Linux container databases** (PostgreSQL, MySQL)

## Architecture

GitHub Actions Windows runners come with Docker Desktop pre-installed, which allows running Linux containers on Windows using WSL2 (Windows Subsystem for Linux). This enables:
1. Running your test code on a Windows environment
2. Using Linux-based database containers for integration testing
3. Seamless communication between Windows host and Linux containers via port mapping

## Workflows

### 1. PostgreSQL Database (`windows-with-db.yml`)
- **Runner**: `windows-latest`
- **Database**: PostgreSQL 15 (Alpine Linux)
- **Port**: 5432
- **Test**: Python script with psycopg2

### 2. MySQL Database (`windows-with-mysql.yml`)
- **Runner**: `windows-latest`
- **Database**: MySQL 8.0 (Linux)
- **Port**: 3306
- **Test**: Python script with mysql-connector

## How It Works

1. **Checkout Code**: Pulls the repository code
2. **Docker Setup**: Verifies Docker is available (pre-installed on Windows runners)
3. **Start Database Container**: 
   - Pulls Linux database image
   - Runs container with environment variables
   - Maps container port to Windows host
4. **Install Dependencies**: Sets up Python and required database drivers
5. **Run Tests**: Executes connection tests and database operations
6. **Cleanup**: Stops and removes containers

## Test Scripts

### `test_db_connection.py` (PostgreSQL)
Tests PostgreSQL connectivity with:
- Connection verification with retries
- Table creation
- Data insertion
- Query execution

### `test_mysql_connection.py` (MySQL)
Tests MySQL connectivity with:
- Connection verification with retries
- Table creation
- Data insertion
- Query execution

## Running Locally

To test the setup locally on Windows with Docker Desktop:

### PostgreSQL Test
```powershell
# Start PostgreSQL container
docker run -d --name postgres-db -e POSTGRES_PASSWORD=testpass123 -e POSTGRES_USER=testuser -e POSTGRES_DB=testdb -p 5432:5432 postgres:15-alpine

# Install Python dependencies
pip install psycopg2-binary

# Run test
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="testdb"
$env:DB_USER="testuser"
$env:DB_PASSWORD="testpass123"
python test_db_connection.py

# Cleanup
docker stop postgres-db
docker rm postgres-db
```

### MySQL Test
```powershell
# Start MySQL container
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=rootpass123 -e MYSQL_DATABASE=testdb -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpass123 -p 3306:3306 mysql:8.0

# Install Python dependencies
pip install mysql-connector-python

# Run test
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_NAME="testdb"
$env:DB_USER="testuser"
$env:DB_PASSWORD="testpass123"
python test_mysql_connection.py

# Cleanup
docker stop mysql-db
docker rm mysql-db
```

## Key Features

✅ **Cross-platform testing**: Windows runner with Linux containers
✅ **Automated setup**: No manual database installation required
✅ **Isolated tests**: Each workflow run uses fresh database containers
✅ **Multiple database support**: PostgreSQL and MySQL examples
✅ **Retry logic**: Handles container startup delays
✅ **Comprehensive testing**: Connection, CRUD operations verification
✅ **Automatic cleanup**: Containers removed after tests

## Requirements

- GitHub repository with Actions enabled
- No additional setup required (Windows runners have Docker pre-installed)

## Notes

- Windows runners use Docker Desktop with WSL2 for Linux container support
- Container startup may take 10-30 seconds depending on the database
- Port mapping allows Windows processes to connect to Linux containers via localhost
- Both workflows can run in parallel or independently