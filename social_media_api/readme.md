# Django Custom User Authentication & Social Media API

This Django project implements a **custom user model** with additional fields (`bio`, `profile_picture`, `following`) and provides **user registration, login, and token-based authentication** using Django REST Framework (DRF).  
Additionally, it includes **Posts and Comments functionality**, as well as a **follow system and dynamic feed**, allowing users to follow others and see posts from followed users.

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
- API endpoints fully documented for follow/unfollow actions and feed retrieval

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
