# Django Custom User Authentication & Social Media API

This Django project implements a **custom user model** with additional fields (`bio`, `profile_picture`, `following`) and provides **user registration, login, and token-based authentication** using Django REST Framework (DRF).  
Additionally, it includes **Posts, Comments, Follow System, Dynamic Feed, Likes, and Notifications**, allowing users to fully interact in a social media environment.

---

## Features

### User Authentication
- Custom user model (`CustomUser`) extending `AbstractUser`
  - `bio` (optional text field)
  - `profile_picture` (optional image field)
  - `following` (self-referential ManyToMany field)
- User registration endpoint
- User login endpoint with **token authentication**
- Retrieve user details
- Django REST Framework integration

### Social Media (Posts & Comments)
- **Posts**
  - Fields: `author` (ForeignKey to User), `title`, `content`, `created_at`, `updated_at`
  - CRUD operations (Create, Read, Update, Delete)
  - Pagination and filtering by `title` or `content`
- **Comments**
  - Fields: `post` (ForeignKey), `author` (ForeignKey to User), `content`, `created_at`, `updated_at`
  - CRUD operations for user comments
  - Permissions: Users can only edit or delete their own comments

### Follow System & Feed
- **Following**
  - Users can follow and unfollow other users
  - Self-referential ManyToMany relationship (`following`)
- **Feed**
  - Displays posts from users that the current user follows
  - Ordered by creation date (most recent first)
  - Accessible via `/feed/` endpoint

### Likes
- Users can **like and unlike posts**
- Prevents duplicate likes
- Endpoints:
  - `POST /posts/<id>/like/`
  - `POST /posts/<id>/unlike/`

### Notifications
- Users receive notifications when:
  - Someone follows them
  - Someone likes their post
  - Someone comments on their post
- Notifications include:
  - `recipient` (who gets notified)
  - `actor` (who performed the action)
  - `verb` (what happened, e.g., "liked your post")
  - `target` (object of the action, e.g., post or comment)
  - `timestamp`
- Endpoint: `/notifications/` (shows unread notifications prominently)

---

## Requirements

- Python 3.8+
- Django 4.x
- Django REST Framework
- Pillow (for `ImageField` support)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
