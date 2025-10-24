# django_realtime_chatApp
A modern real-time chat application built with Django, Django Channels, and WebSockets.

## Features

- **User Registration & Authentication**: Secure sign up and login with custom forms.
- **Real-Time Messaging**: Instant chat using WebSockets (Django Channels).
<!-- - **Multiple Chat Rooms**: Join different chat rooms by name. -->
- **Responsive UI**: Styled with Tailwind CSS for a modern look.
<!-- - **Persistent Message History**: (Optional, if implemented) Messages are stored and loaded per room. -->

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Redis (for Channels layer)
- Docker (optional, for containerized setup)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd django_realtime_chatApp
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On Linux/Mac:
   source env/bin/activate
   ```

3. **Configure environment variables**
   
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your database credentials and settings.

4. **Quick Setup (Recommended)**
   ```bash
   python setup_dev.py
   ```
   
   Or manual setup:

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Setup Database**
   
   Make sure MySQL is running and create the database:
   ```sql
   CREATE DATABASE chatrca;
   ```

7. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run Redis server**
   
   Make sure Redis is running locally (default: `localhost:6379`).
   ```bash
   # On Windows (if Redis is installed):
   redis-server
   # On Linux/WSL:
   sudo service redis-server start
   # On Mac:
   brew services start redis
   ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

11. **Access the app**
    
    - Main app: [http://localhost:8000](http://localhost:8000)
    - Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)
    - API documentation: [http://localhost:8000/swagger](http://localhost:8000/swagger)

### Docker (Optional)

To run with Docker:

(will let you further,App in devlopment )
