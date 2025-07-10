# API Request/Response Logging System

This system automatically logs all API requests and responses to the database for monitoring, debugging, and analytics purposes.

## Features

- **Automatic Logging**: All API requests (to `/api/` endpoints) are automatically logged
- **Comprehensive Data**: Captures request/response headers, body, timing, user info, and more
- **Security**: Sensitive headers (authorization, cookies, CSRF tokens) are automatically filtered out
- **Performance**: Logging is done asynchronously to avoid blocking responses
- **Size Limits**: Request/response bodies are limited to 10KB to prevent database bloat
- **Admin Interface**: View logs through Django admin or REST API
- **Statistics**: Built-in analytics and filtering capabilities

## Database Schema

The `APILog` model stores:

### Request Information
- HTTP method (GET, POST, etc.)
- Request path
- Query parameters
- Request headers (filtered for sensitive data)
- Request body (limited to 10KB)
- User making the request
- Client IP address

### Response Information
- Response status code
- Response headers
- Response body (limited to 10KB)

### Timing Information
- Request timestamp
- Response timestamp
- Request duration in milliseconds

### Additional Metadata
- User agent
- Content type

## Usage

### 1. Setup

The logging system is automatically enabled when you add the middleware to your settings:

```python
MIDDLEWARE = [
    # ... other middleware
    'middlewares.api_logging.APILoggingMiddleware',
]
```

### 2. View Logs

#### Via Django Admin
1. Go to `/admin/`
2. Look for "Api logs" section
3. View, filter, and search through logs

#### Via REST API
- List logs: `GET /api/common/api-logs/`
- Get specific log: `GET /api/common/api-logs/{id}/`
- Get statistics: `GET /api/common/api-logs/stats/`

#### API Endpoints

**List API Logs**
```
GET /api/common/api-logs/
```

Query parameters for filtering:
- `method`: HTTP method (GET, POST, etc.)
- `path`: URL path (partial match)
- `response_status_code`: Status code
- `request_user`: User ID
- `date_from`: Start date (ISO format)
- `date_to`: End date (ISO format)
- `ordering`: Sort by field (-field for descending)

**Get Log Details**
```
GET /api/common/api-logs/{id}/
```

**Get Statistics**
```
GET /api/common/api-logs/stats/?days=7
```

Returns:
- Total requests
- Unique endpoints
- Unique users
- Average response time
- Status code distribution
- Method distribution
- Top endpoints

### 3. Cleanup Old Logs

Use the management command to clean up old logs:

```bash
# Delete logs older than 30 days (default)
python manage.py cleanup_api_logs

# Delete logs older than 7 days
python manage.py cleanup_api_logs --days 7

# Dry run to see what would be deleted
python manage.py cleanup_api_logs --dry-run
```

## Configuration

### Customizing Logging Behavior

You can customize the logging behavior by modifying the `APILog.log_request` method in `common/models.py`:

- Change the 10KB size limit for request/response bodies
- Add/remove sensitive headers to filter
- Modify which endpoints are logged (currently all `/api/` endpoints)

### Performance Considerations

- Logs are created synchronously but with error handling to prevent breaking requests
- Consider setting up a cron job to run `cleanup_api_logs` regularly
- Monitor database size as logs can accumulate quickly
- Consider using database partitioning for high-volume applications

### Security Notes

- Sensitive headers are automatically filtered out
- Request/response bodies are limited in size
- Only admin users can access the log viewing API endpoints
- Consider additional access controls for production environments

## Example Usage

### Making API Requests
All API requests to `/api/` endpoints are automatically logged:

```bash
# This request will be logged
curl -X GET http://localhost:8000/api/sample/hello/

# This request will also be logged
curl -X POST http://localhost:8000/api/sample/ \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
```

### Viewing Logs via API

```bash
# Get recent logs
curl http://localhost:8000/api/common/api-logs/

# Get logs for specific user
curl "http://localhost:8000/api/common/api-logs/?request_user=1"

# Get statistics for last 7 days
curl http://localhost:8000/api/common/api-logs/stats/?days=7
```

## Troubleshooting

### Logs Not Appearing
1. Check that the middleware is in `MIDDLEWARE` setting
2. Verify requests are to `/api/` endpoints
3. Check for errors in Django logs

### Performance Issues
1. Run cleanup command to remove old logs
2. Consider reducing the body size limit
3. Monitor database performance

### Memory Issues
1. Ensure cleanup command runs regularly
2. Consider archiving old logs instead of deleting
3. Monitor database size growth 