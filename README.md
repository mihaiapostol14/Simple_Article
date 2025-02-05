# Simple Article - Django Project

## Description
**Simple Article** is a Django-based web application that allows users to register, log in, manage their profiles, and export user data in various formats. The project is designed to provide a minimal yet functional authentication system with user-friendly features.

## Features
- **User Registration**: Users can create an account.
- **User Login & Logout**: Secure authentication and logout functionality.
- **User Profile Management**: Users can view and update their profile.
- **Export User Data**: Users can export their data in:
  - **JSON**
  - **CSV**
  - **PDF**
- **Django Authentication System**: Built-in security features.
- **Minimal & Clean UI**: A simple interface for ease of use.

## Technologies Used
- **Python Django**: Backend framework.
- **Django Authentication**: User authentication and management.
- **Django Templates**: Frontend rendering.
- **CSV, JSON, and PDF Libraries**: Data export functionality.
- **Bootstrap**: Styling and UI design.

## Installation & Setup

**Steps by run project**

1. Cloning project or download archive
```bash
git clone https://github.com/mihaiapostol14/Simple_Article.git
```


2.  Creating virtual environment and install requirements
 * [creating virtual environment on windows](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)
 * [creating virtual environment on linux](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/)
 * [install requirements](https://www.geeksforgeeks.org/how-to-install-python-packages-with-requirements-txt/)

3. move to project directory using command ``cd MyWebSite`` and run command :arrow_down:

which is responsible for applying and unapplying migrations.
````bash
python manage.py migrate
````

running local testing server
````bash
python manage.py runserver
````


it can be helped **Django Resources**
* [Django Start](https://www.djangoproject.com/start/)
* [Django Static Files](https://docs.djangoproject.com/en/5.0/howto/static-files/)
* [Django Media Files](https://docs.djangoproject.com/en/5.0/howto/static-files/)
* [Django Customizing AuthenticationForm](https://medium.com/@iamalisaleh/customizing-authenticationform-for-custom-login-policy-in-django-e006029b9971)
* [Django Class Views](https://ccbv.co.uk/)
