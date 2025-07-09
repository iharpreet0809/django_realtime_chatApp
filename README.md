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
   ```
   git clone 
   cd django_realtime_chatApp
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy `.env.example` to `.env` and set your secrets.

5. **Apply migrations**
   ```
   python manage.py migrate
   ```

6. **Run Redis server**

   Make sure Redis is running locally (default: `localhost:6379`).

7. **Run the development server**
   ```
   python manage.py runserver
   ```

8. **Access the app**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

### Docker (Optional)

To run with Docker:

(will let you further,App in devlopment )
