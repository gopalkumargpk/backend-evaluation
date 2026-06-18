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

# Stage 2 - Database Design

## Recommended Database

PostgreSQL

### Why PostgreSQL?

- ACID Compliance
- Strong Consistency
- Efficient Indexing
- High Scalability
- Reliable Transactions

## Database Schema

### Students Table

| Column | Type |
|----------|----------|
| id | UUID |
| name | VARCHAR |
| email | VARCHAR |
| created_at | TIMESTAMP |

### Notifications Table

| Column | Type |
|----------|----------|
| id | UUID |
| student_id | UUID |
| type | VARCHAR |
| message | TEXT |
| is_read | BOOLEAN |
| created_at | TIMESTAMP |

## Challenges

- Large notification volume
- Slow queries
- Increased storage usage

## Solutions

- Indexing
- Pagination
- Redis Caching
- Table Partitioning

## Sample Query

```sql
SELECT *
FROM notifications
WHERE student_id = '123'
ORDER BY created_at DESC;
```

# Stage 3 - Query Optimization

## Current Query

```sql
SELECT *
FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC;
```

## Is This Query Accurate?

Yes, the query correctly fetches unread notifications for a student and sorts them by newest first.

## Why Is It Slow?

The database contains:

- 50,000 students
- 5,000,000 notifications

Without proper indexing, the database may perform a full table scan, which is expensive and slow.

## Optimization

Create a composite index:

```sql
CREATE INDEX idx_notifications_student_read_created
ON notifications(studentID, isRead, createdAt DESC);
```

Benefits:

- Faster filtering by studentID
- Faster filtering by isRead
- Faster sorting by createdAt

## Computational Cost

Without Index:
- O(N)

With Index:
- O(log N)

## Should We Add Indexes On Every Column?

No.

Reasons:

- Increased storage usage
- Slower INSERT operations
- Slower UPDATE operations
- More maintenance overhead

Indexes should only be added on frequently queried columns.

## Query For Placement Notifications In Last 7 Days

```sql
SELECT *
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```