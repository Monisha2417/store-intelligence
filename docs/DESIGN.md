# Store Intelligence Platform - Design Document

## Overview

Store Intelligence is a retail analytics platform designed to ingest customer movement events and transform them into actionable business insights. The system tracks customer journeys through a store, computes analytics such as conversion funnels and zone traffic heatmaps, detects anomalies in store performance, and presents the results through a dashboard.

The primary goal is to help store managers understand customer behavior, identify operational issues, and improve store layout and conversion rates.

The system consists of three major layers:

1. Event Ingestion Layer
2. Analytics Layer
3. Dashboard Layer

These layers are designed to be loosely coupled so that analytics logic can evolve independently from data collection and visualization.

---

## System Architecture

The platform follows a service-oriented architecture centered around FastAPI.

Customer movement events are generated either by a detection pipeline or a simulated event generator. These events are submitted to the ingestion API and stored in a SQLite database.

Analytics endpoints process stored events and calculate metrics such as:

* Visitor counts
* Conversion funnels
* Zone heatmaps
* Anomaly detection results

The frontend dashboard periodically requests analytics data from the API and renders visualizations for business users.

Data Flow:

Detection Pipeline → Event Ingestion API → Database → Analytics Engine → Dashboard

---

## Ingestion Flow

The ingestion flow is responsible for accepting customer activity events and storing them in the database.

Each event contains information such as:

* Event ID
* Store ID
* Visitor ID
* Camera ID
* Event Type
* Zone ID
* Timestamp

When an event is received through the ingestion endpoint:

1. FastAPI validates the request schema.
2. Invalid requests are rejected with an appropriate error response.
3. Valid events are converted into database objects.
4. Events are stored in SQLite.
5. The API returns a success response.

The ingestion layer is intentionally lightweight and performs minimal business logic. This design keeps event acceptance fast and allows analytics to be computed separately.

---

## Analytics Flow

The analytics layer processes stored events and generates business metrics.

### Funnel Analytics

Customer journeys are grouped by visitor ID.

The funnel tracks progression through:

ENTRY → ZONE VISIT → BILLING → PURCHASE

The analytics engine calculates:

* Number of visitors at each stage
* Drop-off percentages
* Conversion rate

### Heatmap Analytics

Zone traffic is computed by counting customer interactions within store zones.

Examples:

* Entrance
* Snacks
* Dairy
* Beverages
* Checkout

The resulting counts are used by the dashboard to visualize traffic intensity.

### Anomaly Detection

The anomaly engine evaluates store performance metrics and identifies unusual conditions.

Examples include:

* Low conversion rates
* Underutilized zones
* Dead zones with minimal customer traffic

Detected anomalies include severity levels and suggested actions for store operators.

---

## Dashboard Flow

The dashboard acts as the presentation layer.

React components periodically request analytics data from backend endpoints.

Key dashboard sections include:

### Metrics Card

Displays:

* Total visitors
* Purchases
* Conversion rate
* Average dwell time

### Conversion Funnel

Visualizes customer progression through the shopping journey and highlights drop-off points.

### Store Heatmap

Displays traffic distribution across store zones using relative intensity levels.

### Anomaly Detection

Presents operational alerts and recommended actions.

The dashboard refreshes automatically at regular intervals to provide near real-time visibility.

---

## Database Design

SQLite was selected as the storage layer because it is lightweight, easy to deploy, and sufficient for the challenge scale.

The primary table stores event records.

Each row represents a single customer interaction.

Important fields include:

* event_id
* store_id
* visitor_id
* camera_id
* event_type
* zone_id
* timestamp
* is_staff

This schema supports future extensions such as multi-store deployments, additional event types, and more advanced analytics.

---

## AI-Assisted Decisions

Large language models were used during development to accelerate implementation and evaluate design alternatives.

### Decision 1: Analytics Computation Strategy

An AI assistant suggested computing funnel metrics dynamically from stored events instead of maintaining precomputed aggregates.

I agreed with this recommendation because the project dataset is relatively small and dynamic computation simplifies the architecture while avoiding synchronization issues.

### Decision 2: Endpoint Separation

An AI assistant suggested exposing separate endpoints for metrics, heatmaps, funnels, and anomalies rather than returning all analytics through a single endpoint.

I adopted this approach because it improves maintainability, reduces payload size, and allows frontend components to request only the data they require.

### Decision 3: Heatmap Classification

An AI assistant suggested using relative zone traffic thresholds instead of fixed thresholds for heatmap intensity levels.

I accepted this recommendation because relative thresholds adapt better to different store traffic volumes and provide more meaningful visualizations across datasets.
