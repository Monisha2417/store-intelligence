## ARCHITECTURE

Retail Cameras / Sensors
          |
          v
     Event API
          |
          v
     FastAPI Backend
          |
          v
       SQLite
          |
          v
 Analytics Engine
          |
          v
 React Dashboard


 ## Ingestion Flow

 The ingestion layer is responsible for collecting raw store events and storing them in the database.

 Store Cameras / Sensors
          │
          ▼
      POST /events
          │
          ▼
     FastAPI Backend
          │
          ▼
      Validation
          │
          ▼
       SQLite DB

## Analytics Flow

The analytics layer transforms raw events into business insights

Stored Events
      │
      ▼
 Analytics Engine
      │
      ├── Funnel Analysis
      ├── Heatmap Analysis
      ├── Metrics Analysis
      └── Anomaly Detection
      │
      ▼
 Analytics APIs

After events are stored:

Funnel Analysis- Tracks customer progression:

ENTRY
  ▼
ZONE VISIT
  ▼
BILLING
  ▼
PURCHASE

Calculates:

1.Entry count
2.Billing count
3.Purchase count
4.Conversion rate
5.Drop-off percentages
6.Heatmap Analysis
7.Counts traffic in each zone.

Example:

SNACKS      120 visits
DAIRY       80 visits
BEVERAGES   45 visits
CHECKOUT    30 visits

Used to identify:

->High traffic areas
->Low traffic areas
->Dead zones
->Metrics Analysis
->Computes overall store KPIs.

Examples:

Total visitors
Total purchases
Average dwell time
Conversion rate
Anomaly Detection

Identifies unusual patterns.

Examples:

Low conversion rate
Dead checkout area
Traffic spike

Generates recommendations:

Review product placement
Inspect customer flow

## Dashboard Flow

The dashboard visualizes analytics in real time.

Flow
React Dashboard
        │
        ▼
 REST API Calls
        │
        ▼
 FastAPI Analytics Endpoints
        │
        ▼
 Analytics Results
        │
        ▼
 Dashboard Cards


1.React loads the dashboard.
2.Components make API requests.

Examples:

/stores/{store_id}/funnel
/stores/{store_id}/heatmap
/stores/{store_id}/anomalies
/metrics

3.FastAPI computes analytics from stored events.
4.Results are returned as JSON.
5.React updates:
Funnel Card
Heatmap Card
Metrics Card
Anomaly Card

Dashboard refreshes every 5 seconds to simulate real-time monitoring.

New Purchase Event
        │
        ▼
Database Updated
        │
        ▼
Funnel Recomputed
        │
        ▼
Dashboard Refresh
        │
        ▼
Conversion Rate Updated



# End-to-End Summary

Customer Activity
        │
        ▼
Event Generated
        │
        ▼
FastAPI Ingestion
        │
        ▼
SQLite Storage
        │
        ▼
Analytics Engine
        │
        ▼
REST APIs
        │
        ▼
React Dashboard
        │
        ▼
Business Insights

