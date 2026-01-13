# API Contract: Next.js Frontend ↔ FastAPI Backend

## Overview

This document defines the API contract between the Next.js frontend application and the FastAPI backend service. The contract specifies the endpoints, request/response formats, and error handling patterns that both systems must adhere to for seamless integration.

## Base URL

All API endpoints are prefixed with `/api` and follow REST conventions with JSON request/response bodies.

## Common Headers

### Request Headers
- `Content-Type: application/json` - Required for POST, PUT, PATCH requests
- `Accept: application/json` - Expected response format
- `Authorization: Bearer <token>` - Required for authenticated endpoints

### Response Headers
- `Content-Type: application/json` - All responses return JSON
- `X-Request-ID: <uuid>` - Unique identifier for each request (for debugging)

## Authentication

Authentication endpoints provide user registration, login, and user information retrieval. Most endpoints require authentication via JWT token in the Authorization header.

### Register User
- **Method**: `POST`
- **Path**: `/api/auth/register`
- **Auth Required**: No
- **Description**: Register a new user account

#### Request
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "username": "string (required, 1-50 characters, unique)",
  "email": "string (required, 1-100 characters, unique email format)",
  "password": "string (required, minimum 8 characters)",
  "confirm_password": "string (required, must match password)"
}
```

#### Response (Success: 200 OK)
```json
{
  "id": integer,
  "username": "string",
  "email": "string",
  "role": "string (user|admin)",
  "is_active": boolean,
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

### Login User
- **Method**: `POST`
- **Path**: `/api/auth/login`
- **Auth Required**: No
- **Description**: Authenticate user and return access token

#### Request
- **Headers**: `Content-Type: application/x-www-form-urlencoded`
- **Body** (form data):
```
username=<username>&password=<password>
```

#### Response (Success: 200 OK)
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (typically 'bearer')",
  "user": {
    "id": integer,
    "username": "string",
    "email": "string"
  }
}
```

### Get Current User
- **Method**: `GET`
- **Path**: `/api/auth/me`
- **Auth Required**: Yes
- **Description**: Retrieve information about the authenticated user

#### Request
- **Headers**: `Authorization: Bearer <token>`

#### Response (Success: 200 OK)
```json
{
  "id": integer,
  "username": "string",
  "email": "string",
  "role": "string (user|admin)",
  "is_active": boolean,
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

### Logout User
- **Method**: `POST`
- **Path**: `/api/auth/logout`
- **Auth Required**: No (client-side cleanup)
- **Description**: Logout user (client-side cleanup required)

#### Response (Success: 200 OK)
```json
{
  "message": "Successfully logged out"
}
```

## Protected Endpoints

All other endpoints (todos, health check) require authentication via JWT token in the Authorization header except for the health check endpoint.

## API Endpoints

### Health Check
- **Method**: `GET`
- **Path**: `/api/health`
- **Auth Required**: No
- **Description**: Verify API service availability

#### Request
- **Headers**: None required
- **Body**: None

#### Response (Success: 200 OK)
```json
{
  "status": "healthy",
  "timestamp": "string (ISO 8601 datetime)",
  "version": "string"
}
```

### Todo Management

#### Get All Todos
- **Method**: `GET`
- **Path**: `/api/todos`
- **Auth Required**: Yes
- **Description**: Retrieve all todos for the authenticated user

#### Request
- **Headers**: Authorization: Bearer <token>
- **Query Parameters**:
  - `limit`: integer (optional, default: 50, max: 100)
  - `offset`: integer (optional, default: 0)
  - `completed`: boolean (optional, filter by completion status)

#### Response (Success: 200 OK)
```json
{
  "todos": [
    {
      "id": integer,
      "title": "string (1-255 characters)",
      "description": "string (0-1000 characters, optional)",
      "completed": boolean,
      "due_date": "string (ISO 8601 datetime, optional)",
      "created_at": "string (ISO 8601 datetime)",
      "updated_at": "string (ISO 8601 datetime)"
    }
  ],
  "total_count": integer,
  "limit": integer,
  "offset": integer
}
```

#### Get Single Todo
- **Method**: `GET`
- **Path**: `/api/todos/{id}`
- **Auth Required**: Yes
- **Description**: Retrieve a specific todo by ID

#### Request
- **Headers**: Authorization: Bearer <token>
- **Path Parameters**:
  - `id`: integer (required, todo identifier)

#### Response (Success: 200 OK)
```json
{
  "id": integer,
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters, optional)",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime, optional)",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

#### Create Todo
- **Method**: `POST`
- **Path**: `/api/todos`
- **Auth Required**: Yes
- **Description**: Create a new todo item

#### Request
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Body**:
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean (optional, default: false)",
  "due_date": "string (optional, ISO 8601 datetime)"
}
```

#### Response (Success: 201 Created)
```json
{
  "id": integer,
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters, optional)",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime, optional)",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

#### Update Todo (Full)
- **Method**: `PUT`
- **Path**: `/api/todos/{id}`
- **Auth Required**: Yes
- **Description**: Update all fields of a specific todo

#### Request
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Path Parameters**:
  - `id`: integer (required, todo identifier)
- **Body**:
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean",
  "due_date": "string (optional, ISO 8601 datetime)"
}
```

#### Response (Success: 200 OK)
```json
{
  "id": integer,
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters, optional)",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime, optional)",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

#### Update Todo (Partial)
- **Method**: `PATCH`
- **Path**: `/api/todos/{id}`
- **Auth Required**: Yes
- **Description**: Update specific fields of a todo

#### Request
- **Headers**: Authorization: Bearer <token>, Content-Type: application/json
- **Path Parameters**:
  - `id`: integer (required, todo identifier)
- **Body**:
```json
{
  "title": "string (optional, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean (optional)",
  "due_date": "string (optional, ISO 8601 datetime)"
}
```

#### Response (Success: 200 OK)
```json
{
  "id": integer,
  "title": "string (1-255 characters)",
  "description": "string (0-1000 characters, optional)",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime, optional)",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

#### Delete Todo
- **Method**: `DELETE`
- **Path**: `/api/todos/{id}`
- **Auth Required**: Yes
- **Description**: Delete a specific todo

#### Request
- **Headers**: Authorization: Bearer <token>
- **Path Parameters**:
  - `id`: integer (required, todo identifier)

#### Response (Success: 204 No Content)
- **Status**: 204 No Content
- **Body**: Empty

## Error Responses

### Common Error Format
All error responses follow the same structure:

```json
{
  "detail": "string (error message)",
  "error_code": "string (machine-readable error code)",
  "timestamp": "string (ISO 8601 datetime)",
  "request_id": "string (corresponds to X-Request-ID header)"
}
```

### 400 Bad Request
- **Cause**: Invalid request format, missing required fields, or invalid field values
- **Error Code**: `VALIDATION_ERROR`
- **Example Response**:
```json
{
  "detail": "Validation error",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345",
  "errors": [
    {
      "field": "title",
      "message": "Field required"
    }
  ]
}
```

### 401 Unauthorized
- **Cause**: Missing or invalid authentication credentials
- **Error Code**: `UNAUTHORIZED`
- **Example Response**:
```json
{
  "detail": "Authentication required",
  "error_code": "UNAUTHORIZED",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345"
}
```

### 403 Forbidden
- **Cause**: User attempting to access resources they don't own
- **Error Code**: `FORBIDDEN`
- **Example Response**:
```json
{
  "detail": "Access forbidden",
  "error_code": "FORBIDDEN",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345"
}
```

### 404 Not Found
- **Cause**: Requested resource does not exist
- **Error Code**: `NOT_FOUND`
- **Example Response**:
```json
{
  "detail": "Todo not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345"
}
```

### 409 Conflict
- **Cause**: Operation conflicts with current state
- **Error Code**: `CONFLICT`
- **Example Response**:
```json
{
  "detail": "Operation conflict",
  "error_code": "CONFLICT",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345"
}
```

### 422 Unprocessable Entity
- **Cause**: Semantic errors in request content
- **Error Code**: `UNPROCESSABLE_ENTITY`
- **Example Response**:
```json
{
  "detail": "Unprocessable entity",
  "error_code": "UNPROCESSABLE_ENTITY",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345",
  "errors": [
    {
      "field": "due_date",
      "message": "Date cannot be in the past"
    }
  ]
}
```

### 500 Internal Server Error
- **Cause**: Unexpected server-side error
- **Error Code**: `INTERNAL_ERROR`
- **Example Response**:
```json
{
  "detail": "Internal server error",
  "error_code": "INTERNAL_ERROR",
  "timestamp": "2026-01-07T10:00:00Z",
  "request_id": "req-12345"
}
```

## Data Types and Formats

### String Formats
- **Date/Time**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ)
- **Text Fields**: UTF-8 encoded, no control characters
- **Identifiers**: Positive integers only

### Field Requirements
- **Required**: Field must be present and non-null
- **Optional**: Field may be omitted or null
- **Default**: Field may be omitted, server provides default value

## Rate Limiting

- All endpoints are subject to rate limiting (100 requests per minute per user)
- Exceeding limits returns 429 Too Many Requests with `Retry-After` header

## Versioning

- API versioning is handled through URL path (current version: `/api/v1/`)
- Backward compatibility is maintained for 6 months after new version release
- Deprecation notices are provided 3 months before removal of endpoints