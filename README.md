# FastAPI Application with Redis Caching

## Overview

This application is a FastAPI service that fetches data from external APIs, caches results in Redis, and returns the data to the client. It's designed to demonstrate asynchronous requests and caching mechanisms.

## How to Run

### Building the Docker Container

To build the Docker container for the application, run the following command in your terminal:

```bash
docker build -t fastapi-redis-app .
```

### Running the Docker Container

To run the application inside a Docker container, execute:

```bash
docker run -d -p 8000:8000 fastapi-redis-app
```

This command will start the application and make it accessible at `http://localhost:8000`.

### Example Usage

Once the application is running, you can query it by accessing the following URL in your browser or using a tool like `curl`:

```
http://127.0.0.1:8000/8.8.8.8
```

This will fetch and return information about the IP address `8.8.8.8`. The response should look similar to this:

```json
{
  "raw_data": {
    "ip-api": [
      {
        "status": "success",
        "country": "United States",
        "countryCode": "US",
        "region": "VA",
        "regionName": "Virginia",
        "city": "Ashburn",
        "zip": "20149",
        "lat": 39.03,
        "lon": -77.5,
        "timezone": "America/New_York",
        "isp": "Google LLC",
        "org": "Google Public DNS",
        "as": "AS15169 Google LLC",
        "query": "8.8.8.8"
      }
    ]
  },
  "metrics": {
    "ip-api": [
      {
        "success": "true",
        "time": 0
      }
    ]
  }
}
```

This example response shows the data fetched from the external API for the IP address `8.8.8.8`, including geographic and ISP information, along with metrics indicating the success of the request and the time taken to process it.

### Additional Example
When we run the following request with multiple IP addresses:

```
http://127.0.0.1:8000/8.8.8.8,24.48.0.1
```

We receive the following response, showing information for both IP addresses:

```json
{
  "raw_data": {
    "ip-api": [
      {
        "status": "success",
        "country": "United States",
        "countryCode": "US",
        "region": "VA",
        "regionName": "Virginia",
        "city": "Ashburn",
        "zip": "20149",
        "lat": 39.03,
        "lon": -77.5,
        "timezone": "America/New_York",
        "isp": "Google LLC",
        "org": "Google Public DNS",
        "as": "AS15169 Google LLC",
        "query": "8.8.8.8"
      },
      {
        "status": "success",
        "country": "Canada",
        "countryCode": "CA",
        "region": "QC",
        "regionName": "Quebec",
        "city": "Montreal",
        "zip": "H1K",
        "lat": 45.6085,
        "lon": -73.5493,
        "timezone": "America/Toronto",
        "isp": "Le Groupe Videotron Ltee",
        "org": "Videotron Ltee",
        "as": "AS5769 Videotron Ltee",
        "query": "24.48.0.1"
      }
    ]
  },
  "metrics": {
    "ip-api": [
      {
        "success": "true",
        "time": 0
      },
      {
        "success": "true",
        "time": 0.14333224296569824
      }
    ]
  }
}
```

## Endpoints

`GET /{ip_addresses}`: Fetches data for given IP addresses, comma-separated. Caches results in Redis.