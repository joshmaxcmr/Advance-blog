# Directives



# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django 5.2.5 blog application named "monsite" with a single `blog` app. The project uses SQLite as the database and includes basic blog functionality with post listing and detail views.

## Development Commands

### Running the Development Server
```bash
python manage.py runserver
```

### Database Operations
```bash
# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser
```

### Django Management
```bash
# Start Django shell
python manage.py shell

# Collect static files (if needed)
python manage.py collectstatic
```

## Project Architecture

### Core Structure
- **Main Project**: `monsite/` - Contains settings, main URL configuration, WSGI/ASGI configs
- **Blog App**: `blog/` - Single Django app handling blog functionality
- **Templates**: `templates/blog/` - HTML templates with base template inheritance
- **Static Files**: `blog/static/css/` - CSS files for styling
- **Database**: SQLite database (`db.sqlite3`) for development

### Blog App Components
- **Models**: `blog/models.py` - `Post` model with status choices (Draft/Published), slug field unique for date
- **Views**: `blog/views.py` - Class-based views (`PostListView`, `PostDetailView`) with pagination
- **URLs**: Date-based URL pattern for post detail (`/year/month/day/slug/`)
- **Templates**: Uses template inheritance with `base.html`, includes list and detail views

### Key Model Details
- Post model has slug field with `unique_for_date='publish'` constraint
- Status choices using TextChoices (Draft/Published)
- Date-based URL routing with `get_absolute_url()` method
- Foreign key to User model via `settings.AUTH_USER_MODEL`

### Template Structure
- Base template at `templates/blog/base.html` with sidebar
- Template inheritance using `{% block %}` tags
- Static files loaded via `{% load static %}` and `{% static %}` tags

### URL Configuration
- Main URLs include blog app at root path (`''`)
- Blog app uses namespaced URLs (`app_name = 'blog'`)
- Admin interface available at `/admin/`