# posts-manager-api

This project is an API client developed with Django Rest Framework (DRF) to consume an external API for a technical assessment, allowing post management through RESTful endpoints.

## About The Assessment

This project was developed as part of a technical assessment with specific requirements to keep it simple and focused. The implementation intentionally avoids complex architectural
patterns or over-engineering, as the assessment emphasized creating a straightforward API client that consumes the specified external API. The project demonstrates the ability to
implement the core functionality while maintaining clean, readable code that meets all the specified requirements.

**Bonus Features:**  
In addition to the required features, some extra functionalities were implemented to enhance the project:

- Ability to like posts
- CRUD operations for comments
- Mentioning users in comments
- Search posts by username, title, or content
- Unit tests for like and comment functionalities

## About the Project

The posts-manager-api acts as an abstraction layer for the external API, providing standardized endpoints for:

- Listing posts
- Creating new posts
- Viewing specific posts
- Updating existing posts
- Deleting posts
- **(Bonus)** Liking posts
- **(Bonus)** Managing comments
- **(Bonus)** Mentioning users in comments
- **(Bonus)** Searching posts

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
   git clone https://github.com/IanBraga96/posts-manager-api.git
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

```plaintext
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
│   └── utils.py            # Utility functions to assist
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

```http
GET /api/careers/
```

Returns a list of all available posts.

### Create a New Post

```http
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

```http
GET /api/careers/{id}/
```

Returns details of a specific post.

### Update a Post

```http
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

```http
DELETE /api/careers/{id}/
```

---

### (Bonus) Like a Post

```http
POST /api/careers/{id}/like/
```

Likes the specified post.

### (Bonus) Comments on Posts

- **List Comments:**

  ```http
  GET /api/careers/{post_id}/comments/
  ```

- **Create a Comment:**

  ```http
  POST /api/careers/{post_id}/comments/
  ```

- **Update a Comment:**

  ```http
  PATCH /api/careers/comments/{comment_id}/
  ```

- **Delete a Comment:**

  ```http
  DELETE /api/careers/comments/{comment_id}/
  ```

### (Bonus) Mentioning Users in Comments

To mention users in a comment, simply use the @username syntax within the content field. The system will extract and store the mentioned users.

- Example of content with mentions:

```json
{
  "username": "usertest",
  "content": "This is a great post! @mentioned_user, what do you think?"
}
```

### (Bonus) Search Posts

```http
GET /api/careers/?search={query}
```

Searches for posts by username, title, or content matching the given query string.

## Tests

The project includes unit and integration tests to verify correct endpoint functionality, including:

- Post management
- Likes
- Comments

To run the tests:

```bash
python manage.py test
```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.
