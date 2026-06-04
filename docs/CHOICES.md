# Store Intelligence Platform - Design Choices

## Decision 1: Detection Model Choice

### Problem

The platform requires customer activity events that represent movement through different store zones. A key design decision was determining how these events would be generated.

### Options Considered

#### Option A: YOLOv8

YOLOv8 is a modern object detection model capable of detecting people in video streams with low latency. It could be combined with tracking algorithms to follow customers across store zones.

Pros:

* High detection accuracy
* Real-time performance
* Large community support

Cons:

* Requires additional tracking logic
* Increased implementation complexity
* More infrastructure requirements

#### Option B: Grounding DINO / Vision-Language Models

Vision-language models can classify objects and scenes using prompts and may be useful for zone recognition and staff identification.

Pros:

* Flexible prompting
* Strong semantic understanding

Cons:

* Higher computational cost
* More complex deployment
* Not necessary for the analytics-focused goals of this challenge

#### Option C: Synthetic Event Generation

Instead of implementing a complete computer vision pipeline, customer movement events are generated programmatically and inserted into the database.

Pros:

* Fast implementation
* Deterministic testing
* Focus remains on analytics and system architecture

Cons:

* Does not represent real-world detection accuracy
* Limited realism

### AI Suggestion

The AI assistant initially suggested using YOLOv8 because it is widely adopted and suitable for retail analytics scenarios.

### Final Choice

Synthetic Event Generation.

### Reason

The primary objective of this project is demonstrating ingestion, analytics, anomaly detection, and dashboard functionality. Implementing a full computer vision pipeline would significantly increase complexity while providing limited additional value for the challenge requirements.

Because of this, synthetic event generation was selected as the most practical solution.

---

## Decision 2: Event Schema Design

### Problem

The system requires a standardized event structure that can support analytics while remaining simple and extensible.

### Options Considered

#### Option A: Minimal Schema

Example:

```json
{
  "visitor_id": "123",
  "event_type": "ENTRY"
}
```

Pros:

* Very simple
* Small payload size

Cons:

* Insufficient for analytics
* No multi-store support
* Limited future extensibility

#### Option B: Rich Event Schema

Example:

```json
{
  "event_id": "uuid",
  "store_id": "STORE_BLR_002",
  "visitor_id": "VISITOR_001",
  "camera_id": "CAM_1",
  "event_type": "ZONE_ENTER",
  "zone_id": "SNACKS",
  "timestamp": "2026-06-01T12:00:00"
}
```

Pros:

* Supports analytics
* Supports multiple stores
* Enables auditing and debugging
* Easy future expansion

Cons:

* Slightly larger payloads

### AI Suggestion

The AI assistant recommended a richer schema containing identifiers, timestamps, and location information to support future analytics requirements.

### Final Choice

Rich Event Schema.

### Reason

Analytics such as funnels, heatmaps, and anomaly detection depend on contextual information. The richer schema enables these features while remaining easy to understand and maintain.

---

## Decision 3: API Architecture

### Problem

The platform needed an API structure capable of serving multiple analytics views efficiently.

### Options Considered

#### Option A: Single Analytics Endpoint

Example:

```text
GET /stores/{store_id}/analytics
```

Returns all metrics, funnel data, heatmap data, and anomalies together.

Pros:

* Fewer API routes
* Simple backend implementation

Cons:

* Larger payloads
* Less flexible frontend usage
* Harder to maintain

#### Option B: Separate Analytics Endpoints

Examples:

```text
GET /stores/{store_id}/metrics
GET /stores/{store_id}/heatmap
GET /stores/{store_id}/funnel
GET /stores/{store_id}/anomalies
```

Pros:

* Smaller responses
* Better separation of concerns
* Easier maintenance
* Independent scaling of analytics features

Cons:

* More endpoints to manage

### AI Suggestion

The AI assistant recommended separating analytics functionality into dedicated endpoints.

### Final Choice

Separate Analytics Endpoints.

### Reason

Each dashboard component requests only the information it needs. This reduces unnecessary data transfer, improves maintainability, and aligns with common REST API design practices.

---

## Vision-Language Model Evaluation

No vision-language model was used in the final implementation.

The possibility of using a VLM for zone classification and staff detection was considered during design discussions. However, the challenge focus was determined to be analytics infrastructure rather than computer vision accuracy.

For this reason, synthetic event generation was chosen instead of a VLM-based pipeline.

If a future version introduces video analytics, a vision-language model could be evaluated for:

* Zone classification
* Staff identification
* Customer activity recognition

The current architecture has been designed so that such models can be integrated without significant changes to the analytics layer.
