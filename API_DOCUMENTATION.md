# API Documentation

## Base URL

http://localhost:8000

---

# Health Endpoint

## GET /health

Checks whether the backend service is running and responsive.

### Purpose

Used by monitoring systems, Docker health checks, and developers to verify that the API is operational.

### Request

GET /health


### Example Response

json
{
  "status": "healthy"
}


### Status Codes

| Code | Description        |
| ---- | ------------------ |
| 200  | Service is healthy |

---

# Metrics Endpoint

## GET /metrics

Returns overall store-level performance metrics.

### Purpose

Provides a high-level summary of store activity and customer behavior.

### Request

http
GET /metrics


### Example Response

json
{
  "store_id": "STORE_BLR_002",
  "total_visitors": 300,
  "total_purchases": 82,
  "conversion_rate": 27.33
}


### Response Fields

| Field           | Description                    |
| --------------- | ------------------------------ |
| store_id        | Unique store identifier        |
| total_visitors  | Number of unique visitors      |
| total_purchases | Number of completed purchases  |
| conversion_rate | Purchase-to-visitor percentage |

### Status Codes

| Code | Description                   |
| ---- | ----------------------------- |
| 200  | Metrics returned successfully |

---

# Funnel Endpoint

## GET /stores/{store_id}/funnel

Returns customer progression through the retail conversion funnel.

### Purpose

Measures how customers move through the shopping journey.

### Request

GET /stores/STORE_BLR_002/funnel


### Example Response

json
{
  "store_id": "STORE_BLR_002",
  "entry": 300,
  "zone_visits": 250,
  "billing": 120,
  "purchase": 82,
  "dropoffs": {
    "entry_to_zone": 16.67,
    "zone_to_billing": 52.0,
    "billing_to_purchase": 31.67
  },
  "conversion_rate": 27.33
}


### Response Fields

| Field           | Description                         |
| --------------- | ----------------------------------- |
| entry           | Visitors entering store             |
| zone_visits     | Visitors entering at least one zone |
| billing         | Visitors reaching billing           |
| purchase        | Visitors completing purchase        |
| dropoffs        | Percentage lost between stages      |
| conversion_rate | Final conversion percentage         |

### Status Codes

| Code | Description                   |
| ---- | ----------------------------- |
| 200  | Funnel generated successfully |
| 404  | Store not found               |

---

# Heatmap Endpoint

## GET /stores/{store_id}/heatmap

Returns traffic distribution across store zones.

### Purpose

Identifies highly visited and low-traffic areas inside the store.

### Request

GET /stores/STORE_BLR_002/heatmap


### Example Response

json
{
  "store_id": "STORE_BLR_002",
  "heatmap": {
    "SNACKS": 120,
    "DAIRY": 90,
    "BEVERAGES": 65,
    "CHECKOUT": 35
  }
}


### Response Fields

| Field    | Description         |
| -------- | ------------------- |
| store_id | Store identifier    |
| heatmap  | Zone traffic counts |

### Status Codes

| Code | Description                    |
| ---- | ------------------------------ |
| 200  | Heatmap generated successfully |
| 404  | Store not found                |

---

# Anomalies Endpoint

## GET /stores/{store_id}/anomalies

Detects unusual store behavior and operational issues.

### Purpose

Provides actionable insights for store managers.

### Request

GET /stores/STORE_BLR_002/anomalies


### Example Response
json
{
  "store_id": "STORE_BLR_002",
  "conversion_rate": 17.28,
  "anomalies": [
    {
      "type": "CONVERSION_DROP",
      "severity": "WARN",
      "metric": 17.28,
      "suggested_action": "Review product placement and billing experience"
    },
    {
      "type": "DEAD_ZONE",
      "zone": "CHECKOUT",
      "severity": "INFO",
      "suggested_action": "Inspect visibility, merchandising, and customer flow"
    }
  ]
}

### Response Fields

| Field            | Description                   |
| ---------------- | ----------------------------- |
| conversion_rate  | Current store conversion rate |
| anomalies        | List of detected anomalies    |
| severity         | Alert importance level        |
| suggested_action | Recommended next step         |

### Status Codes

| Code | Description                     |
| ---- | ------------------------------- |
| 200  | Analysis completed successfully |
| 404  | Store not found                 |

---

# Event Ingestion Endpoint

## POST /events

Ingests a new store activity event.

### Purpose

Accepts real-time customer activity from cameras, sensors, or simulated event generators.

### Request

POST /events


### Example Payload

json
{
  "event_id": "evt_001",
  "store_id": "STORE_BLR_002",
  "visitor_id": "VISITOR_123",
  "camera_id": "CAM_1",
  "event_type": "ZONE_ENTER",
  "zone_id": "SNACKS",
  "timestamp": "2026-06-02T10:30:00",
  "is_staff": false
}


### Request Fields

| Field      | Description                |
| ---------- | -------------------------- |
| event_id   | Unique event identifier    |
| store_id   | Store identifier           |
| visitor_id | Visitor identifier         |
| camera_id  | Camera or sensor source    |
| event_type | Event category             |
| zone_id    | Zone associated with event |
| timestamp  | Event timestamp            |
| is_staff   | Staff activity flag        |

### Supported Event Types

ENTRY
REENTRY
ZONE_ENTER
ZONE_DWELL
BILLING
BILLING_QUEUE_JOIN
PURCHASE
EXIT


### Example Response

json
{
  "message": "Event ingested successfully"
}


### Status Codes

| Code | Description               |
| ---- | ------------------------- |
| 200  | Event stored successfully |
| 422  | Validation error          |
| 500  | Internal server error     |


