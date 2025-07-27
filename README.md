# KPA Form Data API

A FastAPI backend for handling KPA form submissions, using MySQL for data storage. Implements endpoints for wheel specifications and bogie checksheet forms.

## Features
- Submit wheel specification forms (POST)
- Retrieve wheel specification forms with filters (GET)
- Submit bogie checksheet forms (POST)
- Data is stored in a MySQL database

## Tech Stack
- Python 3.8+
- FastAPI
- SQLAlchemy
- MySQL
- Uvicorn (for running the server)

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone this repo and navigate into it
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. MySQL Database Setup
- Ensure MySQL is running.
- Create a database named `kpa_forms`:
  ```sql
  CREATE DATABASE kpa_forms;
  ```
- The default credentials in `api.py` are:
  - user: `root`
  - password: `root7728`
  - host: `localhost`
  - port: `3306`
  - database: `kpa_forms`
- You can change these in the `DATABASE_URL` in `api.py` if needed.

### 4. Run the FastAPI App
```bash
uvicorn api:app --reload
```
- The API will be available at: [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### 1. Submit Wheel Specification (POST)
`POST /forms/wheel-specifications`

**Request Body Example:**
```json
{
  "formNumber": "WHEEL-2025-001",
  "submittedBy": "user_id_123",
  "submittedDate": "2025-07-03",
  "fields": {
    "treadDiameterNew": "915 (900-1000)",
    "lastShopIssueSize": "837 (800-900)",
    "condemningDia": "825 (800-900)",
    "wheelGauge": "1600 (+2,-1)"
  }
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Wheel specification submitted successfully.",
  "data": {
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "user_id_123",
    "submittedDate": "2025-07-03",
    "status": "Saved"
  }
}
```

---

### 2. Get Wheel Specifications (GET)
`GET /forms/wheel-specifications?formNumber=...&submittedBy=...&submittedDate=...`

**Query Parameters (all optional):**
- `formNumber`
- `submittedBy`
- `submittedDate`

**Success Response:**
```json
{
  "success": true,
  "message": "Filtered wheel specification forms fetched successfully.",
  "data": [
    {
      "formNumber": "WHEEL-2025-001",
      "submittedBy": "user_id_123",
      "submittedDate": "2025-07-03",
      "fields": {
        "treadDiameterNew": "915 (900-1000)",
        "lastShopIssueSize": "837 (800-900)",
        "condemningDia": "825 (800-900)",
        "wheelGauge": "1600 (+2,-1)"
      }
    }
  ]
}
```

---

### 3. Submit Bogie Checksheet (POST)
`POST /forms/bogie-checksheet`

**Request Body Example:**
```json
{
  "formNumber": "BOGIE-2025-001",
  "inspectionBy": "user_id_456",
  "inspectionDate": "2025-07-03",
  "bogieDetails": {
    "bogieNo": "BG1234",
    "makerYearBuilt": "RDSO/2018",
    "incomingDivAndDate": "NR / 2025-06-25",
    "deficitComponents": "None",
    "dateOfIOH": "2025-07-01"
  },
  "bogieChecksheet": {
    "bogieFrameCondition": "Good",
    "bolster": "Good",
    "bolsterSuspensionBracket": "Cracked",
    "lowerSpringSeat": "Good",
    "axleGuide": "Worn"
  },
  "bmbcChecksheet": {
    "cylinderBody": "WORN OUT",
    "pistonTrunnion": "GOOD",
    "adjustingTube": "DAMAGED",
    "plungerSpring": "GOOD"
  }
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Bogie checksheet submitted successfully.",
  "data": {
    "formNumber": "BOGIE-2025-001",
    "inspectionBy": "user_id_456",
    "inspectionDate": "2025-07-03",
    "status": "Saved"
  }
}
```

---

## Testing
- Use [Postman](https://www.postman.com/) or the FastAPI Swagger UI (`/docs`) to test the endpoints.
- Make sure your MySQL server is running and accessible.

## Notes
- You can extend the API to add more endpoints or connect to a frontend as needed.
- For production, update your database credentials and consider using environment variables for security. 