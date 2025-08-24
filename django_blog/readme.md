# Django Blog Project

This project is part of the **Alx_DjangoLearnLab** repository and serves as a hands-on learning path for building a fully functional blog using Django.  
The project progresses step by step, adding core functionalities such as setup, authentication, and blog post management.

---

## 📌 Project Information

- **Repository**: `Alx_DjangoLearnLab`
- **Directory**: `django_blog`
- **Framework**: Django (Python)
- **Database**: SQLite (default, but configurable to PostgreSQL/MySQL)
- **Objective**: Build a blog with authentication, CRUD functionality for posts, and user profile management.

---

## 🚀 Tasks & Implementations

### 0. Initial Setup and Project Configuration
**Objective**: Establish the Django environment and create the base setup for the blog.

- Installed Django and created a new project: `django_blog`
- Created a blog app: `blog`
- Registered the app in `INSTALLED_APPS`
- Configured database (default: SQLite, extendable to PostgreSQL)
- Created the `Post` model with fields:
  - `title` (CharField)
  - `content` (TextField)
  - `published_date` (DateTimeField, auto_now_add)
  - `author` (ForeignKey → Django User)
- Ran migrations to apply models to the database
- Set up directories for **templates** and **static files**
- Verified setup by running the Django development server

✅ Deliverables:
- Project structure with `blog` app
- `models.py` containing `Post` model
- Static and template directories with initial files

---

### 1. Implementing the Blog's User Authentication System
**Objective**: Enable user registration, login, logout, and profile management.

- Used Django’s built-in authentication system for login/logout
- Extended `UserCreationForm` for registration (added email field)
- Created templates for:
  - Login
  - Logout
  - Registration
  - Profile management
- Defined authentication URL patterns in `blog/urls.py`
- Built profile management view:
  - Users can view/edit profile details
  - Optional extension with profile picture and bio
- Security implemented:
  - CSRF tokens
  - Password hashing (default Django authentication)
- Documentation provided for setup and testing authentication flows

✅ Deliverables:
- Authentication views and forms
- HTML templates for login, logout, registration, and profile
- Documentation explaining the authentication process

---

### 2. Creating Blog Post Management Features
**Objective**: Add CRUD (Create, Read, Update, Delete) operations for blog posts.

- Implemented **class-based views** for posts:
  - `ListView` → display all posts
  - `DetailView` → view single post
  - `CreateView` → create new post (authenticated users only)
  - `UpdateView` → edit existing posts (author only)
  - `DeleteView` → delete posts (author only)
- Created **ModelForm** for `Post` to handle create/update
- Designed templates for:
  - Listing posts
  - Viewing post details
  - Post creation form
  - Post update form
  - Post deletion confirmation
- Configured URLs for CRUD operations in `blog/urls.py`
- Implemented permissions:
  - Only logged-in users can create posts
  - Only authors can edit/delete their posts
  - List/Detail views accessible to all users
- Thorough testing for navigation, permissions, and form submissions

✅ Deliverables:
- Updated `views.py`, `forms.py`, `urls.py`
- Templates for all CRUD operations
- Documentation of features and permissions

---

## 🛠️ How to Run the Project

1. **Clone Repository**
   ```bash
   git clone https://github.com/<your-username>/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/django_blog
