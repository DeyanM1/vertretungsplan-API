# FastAPI Docker Project

This project is a FastAPI application running inside a Docker container. It exposes two GET endpoints: `/classes` and `/plan`, each accepting two query parameters.

## Prerequisites

- Docker
- Docker Compose
- Python (for local development if needed)

## Getting Started

Clone the repository:

```bash
git clone https://github.com/DeyanM1/vertretungsplan-API
cd vertretungsplan-API
```

### Running the Project

Start the application using Docker Compose:

```bash
docker compose up -d
```

This will build the Docker image and start the FastAPI server in detached mode.

### Stopping the Project

```bash
docker compose down
```

### Accessing the API

By default, the FastAPI app runs on port `9090`. You can access it at:

```
http://localhost:9090
```

The automatic API documentation is available at:

```
http://localhost:9090/docs
```

## API Endpoints

### 1. `/classes`

Retrieve all available classes.

**Method:** GET

**Example Request:**

```
GET /classes
```

**Response:**

```json
{
   "result":{
      "05":1,
      "05A":2,
      "05B":3
   }
}
```

---


### 2. `/plan`

Retrieve the schedule for a specific class based on the class name and week number.

**Method:** GET  
**Query Parameters:**  
- `className`: name of the class, must match one of the available class names from `/classes`  
- `weekNum`: number of the week  
  - `1-52`: specific week of the year  
  - `-1`: current week  
  - `-2`: all weeks  
  - `-3`: current and next week  

**Example Requests:**

```
GET /plan?className=09F&weekNum=1
GET /plan?className=08a&weekNum=-1
GET /plan?className=05c&weekNum=-3
```

**Response:**

```json
{
   "result":[
      {
         "Montag":{},
         "Dienstag":{},
         "Mittwoch":{},
         "Donnerstag":{  },
         "Freitag":{
            "0":{
               "klasse":"09F",
               "hour":"5 - 6",
               "vertreter":"Fr. Schmidt",
               "fach":"E 2.FS",
               "fachNeu":"E 2.FS",
               "raum":"---",
               "art":"Entfall",
               "text":""
            }
         }
      }
   ]
}
```