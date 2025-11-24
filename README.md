---

# Privue Vendor Service

A backend microservice to onboard vendors, ingest performance metrics, compute and track vendor score, and provide APIs to query vendor performance.

---

## 🚀 Live Deployment

* **Base URL:** [https://privue-vendor-service.onrender.com](https://privue-vendor-service.onrender.com)
* **Swagger API Docs:** [https://privue-vendor-service.onrender.com/docs](https://privue-vendor-service.onrender.com/docs)

---

## 📌 Features

✔ Vendor registration
✔ Submit performance metrics
✔ Compute vendor score (0–100)
✔ Return latest score in vendor detail API
✔ View vendor score history
✔ Recompute score endpoint (cron-trigger-compatible)
✔ Migration support with Alembic
✔ Public deployment + testable APIs

---

## 🧩 Tech Stack

| Component  | Technology                           |
| ---------- | ------------------------------------ |
| Framework  | FastAPI                              |
| Language   | Python 3.x                           |
| ORM        | SQLModel          		    |
| Database   | PostgreSQL			    |
| Migrations | Alembic                              |
| Deployment | Render                               |
| Docs       | Swagger UI                           |

---

## 🔍 API Endpoints Overview

| Method | Endpoint                  | Description                          |
| ------ | ------------------------- | ------------------------------------ |
| POST   | `/vendors`                | Create a new vendor                  |
| POST   | `/vendors/{id}/metrics`   | Submit performance metrics           |
| GET    | `/vendors/{id}`           | Vendor details + latest score        |
| GET    | `/vendors/{id}/scores`    | Score history (pagination supported) |
| POST   | `/admin/recompute-scores` | Recompute all vendor scores          |
| GET    | `/health`                 | Health check                         |

---

## 🧪 Example Usage with cURL (Working Commands)

> For testing purposes, please use vendor ID = **1** (already created in database)

---

### 1️⃣ Create Vendor

```bash
curl -X 'POST' \
  'https://privue-vendor-service.onrender.com/vendors/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Acme Pvt Ltd",
  "category": "supplier"
}'
```

---

### 2️⃣ Submit Vendor Metrics

```bash
curl -X 'POST' \
  'https://privue-vendor-service.onrender.com/metrics/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "on_time_delivery_rate": 100,
  "complaint_count": 0,
  "missing_documents": true,
  "compliance_score": 100,
  "timestamp": "2025-11-24T17:03:19.440Z"
}'
```

---

### 3️⃣ Get Vendor Details (includes latest score)

```bash
curl -X 'GET' \
  'https://privue-vendor-service.onrender.com/vendors/1' \
  -H 'accept: application/json'
```

---

### 4️⃣ Get Vendor Score History

```bash
curl -X 'GET' \
  'https://privue-vendor-service.onrender.com/scores/1?limit=10&offset=0' \
  -H 'accept: application/json'
```

---

### 5️⃣ Trigger Score Recalculation (Admin API)

```bash
curl -X 'POST' \
  'https://privue-vendor-service.onrender.com/admin/recompute-scores' \
  -H 'accept: application/json' \
  -d ''
```

---

### 6️⃣ Health Check

```bash
curl -X 'GET' \
  'https://privue-vendor-service.onrender.com/health' \
  -H 'accept: application/json'
```

---

## 📊 Vendor Scoring Logic

A vendor's score is recalculated every time new metrics are submitted.

### Weighted Metric Breakdown

| Metric                | Weight           | Impact                       |
| --------------------- | ---------------- | ---------------------------- |
| On-time delivery rate | 40%              | Higher is better             |
| Compliance score      | 40%              | Higher is better             |
| Complaint count       | 10%              | Higher is worse (normalized) |
| Missing documents     | Flat -10 penalty | Negative event               |

---

### 🔹Complaint Normalization

```
MAX_COMPLAINTS = 10
complaint_normalized = max(0, 1 - complaint_count / MAX_COMPLAINTS)
complaint_score = complaint_normalized * 100
```

### ✔ Final Score Formula

```
Score =
  0.4 × on_time_delivery_rate +
  0.4 × compliance_score +
  0.1 × complaint_score −
  (10 if missing_documents else 0)
```

* Score is clamped within **0–100**
* Rounded to **2 decimal places**

---

## 🔄 Score Recalculation Strategy

Vendor scores remain fresh by recomputation.
Instead of embedding cron logic inside the app (infra-specific), a trigger endpoint is provided:

```
POST /admin/recompute-scores
```

This endpoint can be called by:

* Render Scheduler (cron jobs)
* CI/CD pipelines
* Event schedulers like AWS EventBridge

➡ This design keeps infrastructure concerns decoupled from business logic
➡ Flexible to change schedule frequency without redeployment
➡ Supports **on-demand** recalculation

---

## 🛠 Local Setup

```bash
git clone https://github.com/ProGrammar404/privue-vendor-service.git
cd privue-vendor-service
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Set DB configuration in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://privue_user:privue_password@localhost:5432/privue_db
```

Run migrations:

```bash
alembic upgrade head
```

Start application:

```bash
uvicorn app.main:app --reload
```

Swagger Docs:

```
http://localhost:8000/docs
```

---

## 🧪 Testing

Run test suite:

```bash
pytest
```

Includes:

* Scoring logic tests
* Input validation tests
* API behavior tests

---

## 📌 Assumptions & Notes

* Authentication not included (scope-limited assignment)
* Latest metric timestamp used for current score display
* All records stored for historical score analysis

---

## 🚧 Future Enhancements

* RBAC authentication for admin operations
* Configurable scoring weights (database driven)
* Dashboard support with score charts
* Docker support + CI/CD pipeline
* Metadata for paginated endpoints

---

## 🏁 Conclusion

A scalable and cloud-ready vendor performance evaluation service — complete with real-time scoring, score history, deployment, and public API testing support.

> Fully aligned with assignment requirements.
> Designed with real-world architecture principles.

---
