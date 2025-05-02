# posts-manager-api

This project is an API client developed with Django Rest Framework (DRF) to consume an external API for a technical assessment, enabling post management through RESTful endpoints.
A companion frontend was developed by my friend Breno to take advantage of the bonus features of this backend. You can find the frontend repository here:
[Frontend Repository](https://github.com/breno-aredes/codeleap-project)

> ⚠️ Attention: The backend is deployed and available for testing. However, in Branch: Main-2, it consumes a free third-party API that automatically goes to sleep after 15 minutes
> of inactivity. As a result, you may experience a slight delay on the first request while the external API is being reactivated.

The frontend for this project is also deployed and available at: https://codeleap-project2.vercel.app/

## About The Assessment

This project was developed as part of a technical assessment with specific requirements to keep it simple and focused. The implementation intentionally avoids complex architectural
patterns or over-engineering, as the assessment emphasized creating a straightforward API client that consumes the specified external API. The project demonstrates the ability to
implement the core functionality while maintaining clean, readable code that meets all the specified requirements. With permission from the recruiter, the project was further
developed beyond its original scope. All extended features and improvements can be found in the **main-2** branch, which includes authentication using Firebase, additional
endpoints (such as login, post and comment likes, comment CRUD operations), and a complete refactor of the project structure and database (migrated from SQLite to Firebase).

The original scope, along with a few bonus features, remains available in the **main-1** branch for reference.

**Bonus Features:**  
In addition to the required features, some extra functionalities were implemented to enhance the project:

- CRUD operations for comments
- Mentioning users in comments
- Search posts by username, title, or content
- Unit tests
- Authentication via Firebase (login, registration, token validation)
- Post likes
- Comment likes
- Integration with Firebase as a database

## About the Project

The posts-manager-api acts as an abstraction layer for the external API, receiving standardized endpoints:

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
- Firebase Authentication
- Firebase Realtime Database

## Installation and Setup

### Prerequisites

- Python 3.x installed
- pip (Python package manager)
- Firebase account (with a configured project and service key)

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
│   ├── middleware
│       └── auth_middleware.py
│   ├── migrations
│       └── __init__.py
│   ├── models
│       ├── __init__.py
│       ├── comment_like.py
│       ├── firebase_init.py
│       ├── post_comment.py
│       ├── post_like.py
│       ├── post.py
│       └── user.py
│   ├── serializers
│       ├── __init__.py
│       ├── comment_like_serializer.py
│       ├── post_comment_serializer.py
│       ├── post_like_serializer.py
│       ├── post_serializer.py
│       └── user_serializer.py
│   ├── tests
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_firebase_auth.py
│   ├── utils
│       ├── api_utils.py
│       ├── firebase_utils.py
│       └── utils.py
│   ├── views
│       ├── __init__.py
│       ├── auth_views.py
│       ├── comment_like_views.py
│       ├── comment_views.py
│       ├── like_views.py
│       └── post_views.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py             # API URL configuration
│   └── utils.py            # Utility functions to assist
├── codeleap_careers/       # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project URLs
│   ├── firebase_config.py
│   └── wsgi.py
├── manage.py
├── requirements.txt        # Project dependencies
├── serviceAccountKey.json
└── README.md
```

## API Endpoints

### Register & Login

```http
GET /api/careers/register/
```

Register user

```http
GET /api/careers/login/
```

Login user

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
  "content": "This is a great post! @mentioned_user, what do you think?"
}
```

### (Bonus) Search Posts

```http
GET /api/careers/?search={query}
```

Searches for posts by username, title, or content matching the given query string.

### (Bonus) Like a comment

```http
POST /api/careers/comments/{comment_id}/like/
```

## Tests

The project includes unit and integration tests to verify correct endpoint functionality, including:

- Post management
- Likes
- Comments

⚠️ Please note: These tests are fully implemented only in the main branch. The main-2 branch is still under active development and may not yet include complete test coverage for
posts, likes, and comments.

To run the tests:

```bash
python manage.py test
```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.
