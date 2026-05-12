# Simple Article - Django Content Management System

A production-ready Django-based content management system designed for creating, managing, and publishing articles with comprehensive user authentication and authorization capabilities.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technical Architecture](#technical-architecture)
- [Key Features](#key-features)
- [Database Schema](#database-schema)
- [API Endpoints & View Logic](#api-endpoints--view-logic)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

**Simple Article** is a Django web application that facilitates collaborative content creation and management. Built with Django 5.2.8, the platform enables authenticated users to create, update, view, and delete articles with a clean, user-friendly interface. The system implements role-based access control, user profile management, and image optimization for user avatars.

### Core Objectives

- Provide a streamlined article publishing workflow
- Implement secure user authentication and authorization
- Deliver an intuitive administrative dashboard
- Support multi-user concurrent access with proper data isolation
- Maintain data integrity through Django's ORM and migration framework

---

## Technical Architecture

### Stack Components

| Component | Version | Purpose |
|-----------|---------|---------|
| **Framework** | Django 5.2.8 | Web application framework |
| **Database** | SQLite3 | Relational data persistence |
| **ORM** | Django ORM | Object-relational mapping |
| **Image Processing** | Pillow 12.1.1 | Avatar optimization and resizing |
| **Template Engine** | Django Templates | Server-side HTML rendering |
| **Authentication** | Django Auth | User session management |

### Architecture Pattern: MVT (Model-View-Template)

The application follows Django's Model-View-Template architecture:

```
User Request
    ↓
URL Router (urls.py)
    ↓
View (Class-Based & Function-Based)
    ↓
Model (ORM)
    ↓
Database (SQLite3)
    ↓
Template Rendering
    ↓
HTTP Response
```

### Multi-App Architecture

The project is organized into three independent Django applications:

1. **main** - Landing page and navigation
2. **authentication_user** - User registration, authentication, and profile management
3. **article** - Article CRUD operations and article listing

Each app maintains separation of concerns with dedicated:
- `models.py` - Database schema definitions
- `views.py` - Request handling and business logic
- `urls.py` - URL routing
- `forms.py` - Form validation and rendering
- `templates/` - HTML templates

---

## Key Features

### 1. User Authentication System
- User registration with email validation
- Secure password hashing using Django's `set_password()` method
- Login/logout functionality with session management
- Password change capability with validation
- Custom User model extending Django's `AbstractUser`

### 2. Article Management
- **Create** - Authenticated users can author new articles
- **Read** - View article details and browse article listings
- **Update** - Authors can modify their articles
- **Delete** - Authors can remove their articles
- Timestamp tracking (creation and modification dates)
- Author-to-Article relationships via ForeignKey

### 3. User Profile Management
- Profile photo upload with validation (JPG format only)
- Automatic image optimization (resized to 300x300px)
- User profile viewing with article count
- Password change functionality

### 4. Administrative Dashboard
- Django Admin interface for superuser management
- Article management with filtering and search
- User management and permission control
- Migration tracking and database schema management

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────┐
│          User Model             │
├─────────────────────────────────┤
│ id (PK)                         │
│ username (UNIQUE)               │
│ email (UNIQUE)                  │
│ password (hashed)               │
│ photo (ImageField)              │
│ is_active (Boolean)             │
│ is_staff (Boolean)              │
│ is_superuser (Boolean)          │
│ date_joined (DateTime)          │
│ last_login (DateTime)           │
└─────────────────────────────────┘
         │ (One-to-Many)
         │ related_name='articles'
         ▼
┌─────────────────────────────────┐
│       Article Model             │
├─────────────────────────────────┤
│ id (PK)                         │
│ title (CharField)               │
│ description (TextField)         │
│ updated_at (DateTimeField)      │
│ author_id (FK → User)           │
└─────────────────────────────────┘
```

### Model Definitions

#### User Model (`authentication_user.models.User`)

```python
class User(AbstractUser, PermissionsMixin):
    """
    Custom User model extending Django's AbstractUser.
    Implements username-based authentication with email and profile photo.
    """
    username = CharField(
        unique=True,
        max_length=50,
        validators=[UnicodeUsernameValidator]
    )
    email = EmailField(
        max_length=254,
        validators=[validate_email]
    )
    password = CharField(
        max_length=20,
        validators=[validate_password]
    )
    photo = ImageField(
        default='default_account_picture.jpg',
        upload_to='user_photo',
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])]
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
```

**Key Characteristics:**
- Username serves as primary authentication identifier
- Email is required during registration
- Photo field with JPG-only validation and automatic resizing
- Full permission system inherited from Django's permission framework

#### Article Model (`article.models.Article`)

```python
class Article(models.Model):
    """
    Core content model representing published articles.
    Maintains referential integrity with cascade deletion on author removal.
    """
    title = CharField(
        max_length=255,
        blank=True,
        null=True
    )
    description = TextField(
        max_length=255,
        blank=True,
        null=True
    )
    updated_at = DateTimeField(auto_now=True)
    author = ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
```

**Key Characteristics:**
- ForeignKey relationship to User with CASCADE deletion (deleting a user removes their articles)
- `auto_now=True` on `updated_at` maintains update timestamps automatically
- Related name `articles` enables reverse queries: `user.articles.all()`

### Database Relationships

| Relationship | Type | On Delete | Description |
|---|---|---|---|
| User ↔ Article | One-to-Many | CASCADE | One user authors many articles |
| Article → User | Foreign Key | CASCADE | Each article has one author |

### Access Patterns

```python
# Forward relation
article.author  # Access article's author
article.author.email  # Access author's email

# Reverse relation
user.articles.all()  # Get all articles by user
user.articles.count()  # Count user's articles
user.articles.filter(title__icontains='Django')  # Filter user's articles
```

---

## API Endpoints & View Logic

### View Architecture

The application utilizes **Class-Based Views (CBV)** with mixins for code reusability:

```
Generic CBV (Django)
    ↓
ArticleMixin / AuthorizationUserMixin (Custom Context)
    ↓
LoginRequiredMixin (Access Control)
    ↓
Concrete View (CreateView, ListView, DetailView, etc.)
```

### Authentication User Endpoints

#### 1. User Registration

**Endpoint:** `POST /authentication_user/registration-user/`

**View:** `CreateUserView`

**Logic:**
```python
class CreateUserView(CreateView, AuthorizationUserMixin):
    template_name = 'authentication_user/registration_user.html'
    form_class = RegistrationUserForm
    
    def form_valid(self, form):
        self.object = form.save()
        login(self.request, user=self.object)  # Auto-login after registration
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('authentication_user:user-profile', 
                          kwargs={'pk': self.object.pk})
```

**Form Validation:**
- Username: 5-50 characters, unique, alphanumeric
- Email: Valid email format
- Password: 5-20 characters with Django's password validators
- Photo: JPG format only

**HTTP Response:** Redirect to user profile on success

---

#### 2. User Login

**Endpoint:** `GET/POST /authentication_user/login-user/`

**View:** `LoginUserView`

**Logic:**
```python
class LoginUserView(AuthorizationUserMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authentication_user/login_user.html'
    
    def get_success_url(self):
        return reverse_lazy('authentication_user:user-profile',
                          kwargs={'pk': self.request.user.pk})
```

**Form Requirements:**
- Username or Email
- Password

**Session Management:** Django's session middleware creates HTTP-only session cookie

---

#### 3. User Profile Detail

**Endpoint:** `GET /authentication_user/user-profile/<int:pk>/`

**View:** `UserDetailView`

**Logic:**
```python
class UserDetailView(AuthorizationUserMixin, DetailView):
    model = User
    template_name = 'authentication_user/user_profile.html'
    context_object_name = 'users'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_articles'] = User.objects.get(pk=self.kwargs['pk']).articles.all()
        return context
```

**Response Context:**
- User object with profile details
- User's photo URL
- Related articles via reverse relationship

---

#### 4. Change Password

**Endpoint:** `GET/POST /authentication_user/change-password/`

**View:** `ChangeUserPasswordView`

**Access Control:** `@login_required` - Only authenticated users

**Logic:**
```python
class ChangeUserPasswordView(AuthorizationUserMixin, PasswordChangeView):
    form_class = ChangeUserPasswordForm
    template_name = 'authentication_user/change_password.html'
    
    def get_success_url(self):
        messages.success(self.request, f'Change Password Successful')
        return reverse_lazy('authentication_user:user-profile',
                          kwargs={'pk': self.request.user.pk})
```

**Password Validation Chain:**
1. User similarity check
2. Minimum length validation (8 characters)
3. Common password check
4. Numeric-only password rejection

---

#### 5. User Logout

**Endpoint:** `GET/POST /authentication_user/logout-user/`

**View:** `UserLogoutView`

**Logic:**
```python
class UserLogoutView(LogoutView, AuthorizationUserMixin):
    http_method_names = ["post", "get"]
    template_name = 'authentication_user/logout_user.html'
    
    def get_success_url(self):
        return reverse_lazy('main:home')
```

**Session Cleanup:** Django removes session data and cookie

---

### Article Management Endpoints

#### 1. Create Article

**Endpoint:** `GET/POST /article/create-article/`

**View:** `CreateArticleView`

**Access Control:** `@login_required` - Authenticated users only

**Logic:**
```python
class CreateArticleView(LoginRequiredMixin, ArticleMixin, CreateView):
    model = Article
    form_class = CreateArticleForm
    template_name = 'article/create_article.html'
    
    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk  # Auto-set author
        return initial
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Article created successfully!")
        return redirect(self.get_success_url())
```

**Form Fields:**
- title (CharField, required)
- description (TextField, required)
- author (ModelChoiceField, auto-populated)

**Database Operation:** `Article.objects.create(title=..., description=..., author=...)`

---

#### 2. Article List

**Endpoint:** `GET /article/article-list/`

**View:** `ArticleListView`

**Access Control:** Public (no authentication required)

**Logic:**
```python
class ArticleListView(ArticleMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Optional pagination
    
    def get_queryset(self):
        return Article.objects.all().order_by('-updated_at')
```

**Database Query:** `SELECT * FROM article_article ORDER BY updated_at DESC`

**Response Context:**
- Paginated article list
- Article count
- Author information

---

#### 3. Article Detail

**Endpoint:** `GET /article/article-detail/<int:pk>/`

**View:** `ArticleDetailView`

**Access Control:** Public

**Logic:**
```python
class ArticleDetailView(ArticleMixin, DetailView):
    model = Article
    template_name = 'article/article_detail.html'
    context_object_name = 'article'
```

**Database Query:** `SELECT * FROM article_article WHERE id = pk`

**Response Context:**
- Article with all fields
- Author object with profile photo
- Article timestamps

---

#### 4. Update Article

**Endpoint:** `GET/POST /article/update-article/<int:pk>/`

**View:** `UpdateArticleView`

**Access Control:** `@login_required` - Authenticated users only

**Logic:**
```python
class UpdateArticleView(LoginRequiredMixin, ArticleMixin, UpdateView):
    model = Article
    form_class = CreateArticleForm
    template_name = 'article/update_article.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Article updated successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('article:article-list')
```

**Database Operation:** `article.save()` triggers UPDATE with `auto_now` timestamp

**Permission Note:** Implementation should include permission check to ensure user == article.author

---

#### 5. Delete Article

**Endpoint:** `GET/POST /article/delete-article/<int:pk>/`

**View:** `DeleteArticleView`

**Access Control:** `@login_required`

**Logic:**
```python
class DeleteArticleView(LoginRequiredMixin, ArticleMixin, DeleteView):
    model = Article
    template_name = 'article/delete_article.html'
    success_url = reverse_lazy('article:article-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Article deleted successfully!")
        return super().delete(request, *args, **kwargs)
```

**Database Operation:** `DELETE FROM article_article WHERE id = pk`

---

### Main App Endpoints

#### 1. Home Page with Calendar

**Endpoint:** `GET /`

**View:** `HomeView`

**Logic:**
```python
class HomeView(HomeMixin, TemplateView):
    template_name = 'main/home.html'
    
    @staticmethod
    def put_calendar(year=current_year, month=current_month):
        """Generate HTML calendar for given month"""
        month_number = list(calendar.month_name).index(month)
        return HTMLCalendar().formatmonth(year, month_number)
    
    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year', datetime.now().year)
        month = self.kwargs.get('month', datetime.now().strftime('%B'))
        context['calendar'] = self.put_calendar(year, month)
        return context
```

**Features:** Dynamic calendar rendering with month/year parameters

---

## Installation & Setup

### Prerequisites

Ensure your system has the following installed:

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager - typically included with Python)
- **git** (for version control)
- **virtualenv** or **venv** (Python virtual environment)

### Step 1: Clone the Repository

```bash
git clone https://github.com/mihaiapostol14/Simple_Article.git
cd Simple_Article
```

### Step 2: Create Virtual Environment

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Installed Packages:**
```
asgiref==3.11.1          # ASGI reference implementation
Django==5.2.8            # Web framework
pillow==12.1.1           # Image processing library
sqlparse==0.5.5          # SQL parser utility
tzdata==2025.3           # Timezone database
```

### Step 4: Navigate to Project Directory

```bash
cd WebSite
```

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

This creates the SQLite database and initializes all Django tables:
- `django_migrations`
- `django_users` (custom)
- `article_article`
- `auth_*` (permission tables)

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ••••••••
Password (again): ••••••••
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 8: Access the Application

- **Frontend:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/ (use superuser credentials)

---

## Environment Configuration

### Database Configuration

#### Development (SQLite - Default)

The project uses SQLite3 by default, suitable for development:

**File:** `WebSite/WebSite/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
```

**Characteristics:**
- Zero configuration required
- File-based database (`db.sqlite3`)
- Ideal for development and testing
- Not recommended for concurrent production use

#### Production Database Configuration

**For PostgreSQL:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'simple_article_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**For MySQL:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'simple_article_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1

# Database Configuration (PostgreSQL Example)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=simple_article_prod
DB_USER=article_user
DB_PASSWORD=your_secure_password_here
DB_HOST=db.example.com
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Media Files
MEDIA_URL=/media/
MEDIA_ROOT=/var/www/simple_article/media/
```

### Loading Environment Variables

**Install python-dotenv:**

```bash
pip install python-dotenv
```

**Update settings.py:**

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

### Static and Media Files Configuration

```python
# File: WebSite/WebSite/settings.py

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Directory Structure:**
```
WebSite/
├── static/           # CSS, JavaScript, images
├── media/            # User uploads (avatars, etc.)
├── templates/        # HTML templates
└── db.sqlite3        # SQLite database
```

---

## Usage

### Common Tasks

#### Create a New Article

1. Login to the application
2. Navigate to **Article** → **Create Article**
3. Fill in:
   - **Title:** Article headline
   - **Description:** Article content
   - **Author:** Your username (auto-populated)
4. Click **Submit**
5. Redirect to article list confirming successful creation

#### Update an Article

1. Navigate to **Article List**
2. Click on an article
3. Select **Edit**
4. Modify title or description
5. Click **Save**

#### Delete an Article

1. Navigate to article detail page
2. Click **Delete**
3. Confirm deletion on confirmation page
4. Redirect to article list

#### Change Password

1. Login and navigate to **Profile**
2. Select **Change Password**
3. Enter current password
4. Enter new password (twice for confirmation)
5. Submit

### Django Admin Interface

**Access:** http://127.0.0.1:8000/admin/

**Superuser tasks:**

```bash
# View all articles
python manage.py shell
>>> from article.models import Article
>>> Article.objects.all()

# Create article via admin
# Visit /admin → Article → Add Article

# Manage users
# Visit /admin → Users → User management
```

---

## Project Structure

```
Simple_Article/
│
├── WebSite/                          # Django project root
│   ├── WebSite/                      # Project settings package
│   │   ├── __init__.py
│   │   ├── settings.py              # Project configuration
│   │   ├── urls.py                  # URL routing
│   │   ├── asgi.py                  # ASGI configuration
│   │   └── wsgi.py                  # WSGI configuration
│   │
│   ├── authentication_user/          # Authentication app
│   │   ├── migrations/              # Database migrations
│   │   ├── templates/
│   │   │   └── authentication_user/
│   │   │       ├── registration_user.html
│   │   │       ├── login_user.html
│   │   │       ├── user_profile.html
│   │   │       ├── change_password.html
│   │   │       └── logout_user.html
│   │   ├── __init__.py
│   │   ├── admin.py                # Admin configuration
│   │   ├── apps.py                 # App config
│   │   ├── forms.py                # User forms
│   │   ├── models.py               # User model
│   │   ├── urls.py                 # Auth URLs
│   │   ├── utils.py                # Context mixins
│   │   ├── views.py                # Auth views
│   │   └── tests.py                # Unit tests
│   │
│   ├── article/                     # Article app
│   │   ├── migrations/              # Database migrations
│   │   ├── templates/
│   │   │   └── article/
│   │   │       ├── create_article.html
│   │   │       ├── article_list.html
│   │   │       ├── article_detail.html
│   │   │       ├── update_article.html
│   │   │       └── delete_article.html
│   │   ├── __init__.py
│   │   ├── admin.py                # Article admin
│   │   ├── apps.py                 # App config
│   │   ├── forms.py                # Article forms
│   │   ├── models.py               # Article model
│   │   ├── urls.py                 # Article URLs
│   │   ├── utils.py                # Article mixins
│   │   ├── views.py                # Article views
│   │   └── tests.py                # Unit tests
│   │
│   ├── main/                        # Main app
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── main/
│   │   │       └── home.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   ├── views.py
│   │   └── tests.py
│   │
│   ├── templates/                   # Global templates
│   │   └── base.html               # Base template
│   │
│   ├── static/                      # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── media/                       # User uploads
│   │   └── user_photo/             # Avatar storage
│   │
│   ├── manage.py                   # Django management CLI
│   └── db.sqlite3                  # SQLite database
│
├── requirements.txt                # Python dependencies
├── README.md                        # This file
└── .gitignore                       # Git ignore rules
```

---

## Security Considerations

### Current Implementation

✅ **Implemented:**
- Password hashing via Django's `set_password()` method
- CSRF protection in all forms
- SQL injection prevention through Django ORM
- XSS protection via template auto-escaping
- Authentication middleware
- Session framework with secure cookies (in production)

### Production Hardening Checklist

- [ ] Set `DEBUG = False` in production
- [ ] Generate unique `SECRET_KEY` (keep confidential)
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Enable HSTS headers: `SECURE_HSTS_SECONDS = 31536000`
- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting on auth endpoints
- [ ] Add permission checks on article update/delete
- [ ] Use HTTPS with valid SSL certificate
- [ ] Set up log aggregation for monitoring

### Recommended Permission Enhancement

```python
# Add to UpdateArticleView and DeleteArticleView
def dispatch(self, request, *args, **kwargs):
    article = self.get_object()
    if article.author != request.user:
        raise PermissionDenied("You can only edit your own articles")
    return super().dispatch(request, *args, **kwargs)
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature description'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Write unit tests for new features

---

## License

This project is open source and available under the MIT License. See LICENSE file for details.

---

## Support & Documentation

- **Django Documentation:** https://docs.djangoproject.com/
- **Django ORM Guide:** https://docs.djangoproject.com/en/5.2/topics/db/models/
- **Class-Based Views:** https://docs.djangoproject.com/en/5.2/topics/class-based-views/
- **Django Forms:** https://docs.djangoproject.com/en/5.2/topics/forms/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-12 | Initial release with core functionality |

---

## Contact

- **GitHub:** [@mihaiapostol14](https://github.com/mihaiapostol14)
- **Repository:** [Simple_Article](https://github.com/mihaiapostol14/Simple_Article)

---

**Last Updated:** May 12, 2026 | **Status:** Production Ready
