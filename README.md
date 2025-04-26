# posts-manager-api

This project is an API client developed with Django Rest Framework (DRF) to consume an external API for a technical assessment, allowing post management through RESTful endpoints.

## About The Assessment

This project was developed as part of a technical assessment with specific requirements to keep it simple and focused. The implementation intentionally avoids complex architectural
patterns or over-engineering, as the assessment emphasized creating a straightforward API client that consumes the specified external API. The project demonstrates the ability to
implement the core functionality while maintaining clean readable code that meets all the specified requirements.

## About the Project

The posts-manager-api acts as an abstraction layer for the external API, providing standardized endpoints for:

- Listing posts
- Creating new posts
- Viewing specific posts
- Updating existing posts
- Deleting posts

## Technologies Used

- Python 3.x
- Django 4.x
- Django Rest Framework
- Requests (for communication with the external API)

## Installation and Setup

### Prerequisites

- Python 3.x installed
- pip (Python package manager)

### Steps

1. Clone the repository:

   ```bash
   git https://github.com/IanBraga96/posts-manager-api.git
   cd posts-manager-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run Django migrations (not necessary):

   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

The server will be running at `http://127.0.0.1:8000/`.

## Project Structure

```
posts-manager-api/
├── posts/                  # Main app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Data models definition
│   ├── serializers.py      # Data serializers
│   ├── tests.py            # Automated tests
│   ├── urls.py             # API URL configuration
│   └── views.py            # API views
├── codeleap_careers/       # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project URLs
│   └── wsgi.py
├── manage.py
├── requirements.txt        # Project dependencies
└── README.md
```

## API Endpoints

### List All Posts

```
GET /api/careers/
```

Returns a list of all available posts.

### Create a New Post

```
POST /api/careers/
```

Request body:

```json
{
  "username": "string",
  "title": "string",
  "content": "string"
}
```

### View a Specific Post

```
GET /api/careers/{id}/
```

Returns details of a specific post.

### Update a Post

```
PATCH /api/careers/{id}/
```

Request body:

```json
{
  "title": "string",
  "content": "string"
}
```

### Delete a Post

```
DELETE /api/careers/{id}/
```

## Tests

The project includes unit and integration tests to verify correct endpoint functionality.

To run the tests:

```bash
python manage.py test
```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.
