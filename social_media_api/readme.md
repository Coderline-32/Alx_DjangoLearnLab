# Django Custom User Authentication API

This Django project implements a **custom user model** with additional fields (`bio`, `profile_picture`, `followers`) and provides **user registration, login, and token-based authentication** using Django REST Framework (DRF).

---

## Features

- Custom user model (`CustomUser`) extending `AbstractUser`
  - `bio` (optional text field)
  - `profile_picture` (optional image field)
  - `followers` (self-referential ManyToMany field)
- User registration endpoint
- User login endpoint with **token authentication**
- Retrieve user details
- Django REST Framework integration

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
