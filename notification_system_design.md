# Stage 1 - Notification System Design

## Notification Schema

```json
{
  "id": "123",
  "type": "Placement",
  "message": "Microsoft Hiring",
  "isRead": false,
  "createdAt": "2026-06-18T10:00:00Z"
}
```

## API Endpoints

### Get All Notifications

GET /notifications

Response

```json
{
  "success": true,
  "notifications": [
    {
      "id": "1",
      "type": "Placement",
      "message": "Microsoft Hiring",
      "isRead": false
    }
  ]
}
```

### Get Single Notification

GET /notifications/{id}

Response

```json
{
  "id": "1",
  "type": "Placement",
  "message": "Microsoft Hiring",
  "isRead": false
}
```

### Create Notification

POST /notifications

Request

```json
{
  "type": "Placement",
  "message": "Microsoft Hiring"
}
```

Response

```json
{
  "success": true,
  "message": "Notification Created"
}
```

### Mark Notification As Read

PATCH /notifications/{id}/read

Response

```json
{
  "success": true,
  "message": "Marked as Read"
}
```

### Delete Notification

DELETE /notifications/{id}

Response

```json
{
  "success": true,
  "message": "Deleted"
}
```

## Real Time Notification Design

Technology Used:

- WebSocket

Flow:

Admin
↓
Backend Server
↓
WebSocket
↓
Students
