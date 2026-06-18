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

# Stage 4 - Performance Improvement

## Problem

Notifications are fetched from the database every time a student opens the application.

This causes:

- High database load
- Increased response time
- Poor user experience
- Scalability issues

## Proposed Solutions

### 1. Redis Caching

Store frequently accessed notifications in Redis.

Benefits:
- Faster response times
- Reduced database load

Tradeoff:
- Additional infrastructure required
- Cache invalidation complexity

### 2. Pagination

Instead of loading all notifications:

Example:

GET /notifications?page=1&limit=20

Benefits:
- Smaller responses
- Reduced memory usage

Tradeoff:
- Multiple API calls may be needed

### 3. Real-Time Notifications

Use WebSocket for instant notification delivery.

Benefits:
- Better user experience
- Reduced polling requests

Tradeoff:
- More complex implementation

### 4. Database Indexing

Use indexes on:

- studentID
- isRead
- createdAt

Benefits:
- Faster queries

Tradeoff:
- Slightly slower inserts and updates

## Recommended Architecture

Client
→ Redis Cache
→ PostgreSQL Database

Real-time updates delivered through WebSocket.

# Stage 5 - Notification Scalability

## Problems In Current Implementation

The current implementation sends email, saves to database, and pushes notifications one by one.

Issues:

- Slow execution for 50,000 students
- Failure of one operation may affect others
- No retry mechanism
- Not scalable
- High response time

## What If Email Fails For 200 Students?

The system should not stop processing.

Failed emails should be stored in a retry queue and processed later.

## Improved Architecture

HR
→ Notification Service
→ Message Queue (RabbitMQ / Kafka)

Workers:

- Email Worker
- Database Worker
- Push Notification Worker

Each worker processes jobs independently.

## Benefits

- Faster processing
- Better fault tolerance
- Easy retry mechanism
- Highly scalable

## Should Database Save And Email Send Happen Together?

No.

These tasks should be asynchronous.

Reason:

- Faster user response
- Better scalability
- Independent failure handling

## Revised Pseudocode

```text
function notify_all(student_ids, message):

    create_notification_job(student_ids, message)

    queue.publish(job)

worker:

    receive_job()

    save_notification_to_db()

    send_email()

    push_notification()

    if failure:
        retry()
```

## Recommended Technologies

- RabbitMQ
- Apache Kafka
- Redis Queue
- WebSocket
```