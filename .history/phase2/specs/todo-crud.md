# Todo CRUD Feature Spec: Phase II

## Overview

This specification defines the Create, Read, Update, and Delete (CRUD) operations for Todo items in the Phase II full-stack web application. The feature enables users to manage their todo items through a web interface backed by persistent database storage.

## User Stories

### As a User, I want to create a new todo item
- **Story**: I should be able to add a new todo with a title and optional description
- **Acceptance Criteria**:
  - Can submit a new todo with required title field
  - Can optionally include description, due date, and initial completion status
  - Receive confirmation of successful creation with the new todo data
  - See the new todo appear in my todo list immediately

### As a User, I want to view all my todo items
- **Story**: I should be able to see a list of all my todo items with their current status
- **Acceptance Criteria**:
  - Can view all todos with title, description, completion status, and due date
  - Todos are displayed in a readable format with clear status indicators
  - Can see creation and update timestamps for each todo
  - List updates automatically when new todos are added

### As a User, I want to update an existing todo item
- **Story**: I should be able to modify the title, description, due date, or completion status of a todo
- **Acceptance Criteria**:
  - Can update the title field of an existing todo
  - Can update the description field of an existing todo
  - Can update the due date field of an existing todo
  - Can toggle the completion status of an existing todo
  - Receive confirmation of successful update with updated todo data

### As a User, I want to delete a todo item
- **Story**: I should be able to remove a todo item that I no longer need
- **Acceptance Criteria**:
  - Can delete a specific todo by its unique identifier
  - Receive confirmation of successful deletion
  - Deleted todo is removed from the todo list immediately
  - Cannot access the deleted todo after deletion

## API Endpoints

### Create Todo
- **Method**: `POST`
- **Path**: `/api/todos`
- **Description**: Creates a new todo item with the provided data

### View All Todos
- **Method**: `GET`
- **Path**: `/api/todos`
- **Description**: Retrieves all todo items for the current user

### View Single Todo
- **Method**: `GET`
- **Path**: `/api/todos/{id}`
- **Description**: Retrieves a specific todo item by its unique identifier

### Update Todo
- **Method**: `PUT`
- **Path**: `/api/todos/{id}`
- **Description**: Updates all fields of a specific todo item

### Partial Update Todo
- **Method**: `PATCH`
- **Path**: `/api/todos/{id}`
- **Description**: Updates specific fields of a todo item

### Delete Todo
- **Method**: `DELETE`
- **Path**: `/api/todos/{id}`
- **Description**: Deletes a specific todo item by its unique identifier

## Request/Response Schemas

### Todo Data Model
```
Todo {
  id: integer (auto-generated, unique)
  title: string (required, max 255 characters)
  description: string (optional, max 1000 characters)
  completed: boolean (default: false)
  due_date: datetime (optional, ISO 8601 format)
  created_at: datetime (auto-generated, ISO 8601 format)
  updated_at: datetime (auto-generated and updated, ISO 8601 format)
}
```

### Create Todo Request
```
POST /api/todos
Content-Type: application/json

{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "due_date": "string (optional, ISO 8601 datetime format)",
  "completed": "boolean (optional, default: false)"
}
```

### Create Todo Response (Success: 201 Created)
```
{
  "id": integer,
  "title": "string",
  "description": "string",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime format)",
  "created_at": "string (ISO 8601 datetime format)",
  "updated_at": "string (ISO 8601 datetime format)"
}
```

### View All Todos Response (Success: 200 OK)
```
{
  "todos": [
    {
      "id": integer,
      "title": "string",
      "description": "string",
      "completed": boolean,
      "due_date": "string (ISO 8601 datetime format)",
      "created_at": "string (ISO 8601 datetime format)",
      "updated_at": "string (ISO 8601 datetime format)"
    }
  ],
  "total_count": integer,
  "page": integer,
  "limit": integer
}
```

### View Single Todo Response (Success: 200 OK)
```
{
  "id": integer,
  "title": "string",
  "description": "string",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime format)",
  "created_at": "string (ISO 8601 datetime format)",
  "updated_at": "string (ISO 8601 datetime format)"
}
```

### Update Todo Request (PUT)
```
PUT /api/todos/{id}
Content-Type: application/json

{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean",
  "due_date": "string (optional, ISO 8601 datetime format)"
}
```

### Partial Update Todo Request (PATCH)
```
PATCH /api/todos/{id}
Content-Type: application/json

{
  "title": "string (optional, 1-255 characters)",
  "description": "string (optional, 0-1000 characters)",
  "completed": "boolean (optional)",
  "due_date": "string (optional, ISO 8601 datetime format)"
}
```

### Update Todo Response (Success: 200 OK)
```
{
  "id": integer,
  "title": "string",
  "description": "string",
  "completed": boolean,
  "due_date": "string (ISO 8601 datetime format)",
  "created_at": "string (ISO 8601 datetime format)",
  "updated_at": "string (ISO 8601 datetime format)"
}
```

### Delete Todo Response (Success: 204 No Content)
```
Status Code: 204 No Content
Body: Empty
```

## Validation Rules

### Create Todo Validation
- `title` is required and must be between 1-255 characters
- `description` is optional and must be between 0-1000 characters if provided
- `completed` must be a boolean value (true/false)
- `due_date` must be in ISO 8601 datetime format (YYYY-MM-DDTHH:MM:SS.sssZ) if provided
- `due_date` cannot be in the past relative to creation time (optional business rule)
- All string fields must not contain control characters

### Update Todo Validation
- `id` in URL path must correspond to an existing todo item
- `title` must be between 1-255 characters if provided
- `description` must be between 0-1000 characters if provided
- `completed` must be a boolean value if provided
- `due_date` must be in ISO 8601 datetime format if provided
- All string fields must not contain control characters

### General Validation
- All API requests must include proper authentication headers
- Requests must have Content-Type: application/json for POST/PUT/PATCH
- Request body size must not exceed 1MB
- All datetime fields must be in UTC timezone

## Error Cases

### 400 Bad Request
- **Cause**: Invalid request format, missing required fields, or invalid field values
- **Response**:
```
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "string",
      "message": "string"
    }
  ]
}
```
- **Examples**:
  - Missing required `title` field when creating a todo
  - `title` exceeding 255 characters
  - Invalid datetime format for `due_date`
  - Invalid boolean value for `completed` field

### 401 Unauthorized
- **Cause**: Missing or invalid authentication credentials
- **Response**:
```
{
  "detail": "Authentication required"
}
```
- **Examples**:
  - Missing authentication token
  - Expired authentication token
  - Invalid authentication token

### 403 Forbidden
- **Cause**: User attempting to access resources they don't own
- **Response**:
```
{
  "detail": "Access forbidden"
}
```
- **Examples**:
  - Attempting to access another user's todos
  - Attempting to modify another user's todo

### 404 Not Found
- **Cause**: Requested todo item does not exist
- **Response**:
```
{
  "detail": "Todo not found"
}
```
- **Examples**:
  - Requesting a todo with non-existent ID
  - Updating a todo with non-existent ID
  - Deleting a todo with non-existent ID

### 409 Conflict
- **Cause**: Operation conflicts with current state (rare for Todo CRUD)
- **Response**:
```
{
  "detail": "Operation conflict"
}
```
- **Examples**:
  - Attempting to create duplicate todo (if uniqueness constraint exists)

### 422 Unprocessable Entity
- **Cause**: Semantic errors in request content
- **Response**:
```
{
  "detail": "Unprocessable entity",
  "errors": [
    {
      "field": "string",
      "message": "string"
    }
  ]
}
```
- **Examples**:
  - Business logic validation failures
  - Constraint violations

### 500 Internal Server Error
- **Cause**: Unexpected server-side error
- **Response**:
```
{
  "detail": "Internal server error"
}
```
- **Examples**:
  - Database connection failures
  - Unexpected exceptions in server code
  - Server resource exhaustion

## Business Rules

### Data Integrity
- Each todo must have a unique identifier assigned by the database
- Creation timestamp is set only once upon creation
- Update timestamp is updated on every modification
- Completed status can be toggled freely by the user

### Access Control
- Users can only access their own todo items
- Users can only modify their own todo items
- Users can only delete their own todo items

### Data Lifecycle
- Todo items are permanently deleted upon DELETE request
- No soft delete mechanism is implemented
- Deleted todo items cannot be recovered