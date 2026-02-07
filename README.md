# Fitness Tracker API

A comprehensive REST API for tracking fitness activities, managing user workouts, setting fitness goals, and monitoring progress. Built with Django and Django REST Framework.

## Features

### Core Features

- **User Management**: Complete CRUD operations with secure authentication
- **Activity Tracking**: Log, update, delete, and view fitness activities
- **Activity History**: View detailed activity logs with filtering and sorting
- **Activity Metrics**: Get comprehensive statistics and summaries
- **JWT Authentication**: Secure token-based authentication
- **Pagination & Sorting**: Efficient data retrieval for large datasets

### Stretch Features

- **Goal Setting**: Set and track fitness goals with progress monitoring
- **Activity Analytics**: Detailed insights and trends over time
- **Permission System**: Secure user-specific data access

## Technology Stack

- **Backend**: Django 4.2+
- **API Framework**: Django REST Framework 3.14+
- **Authentication**: Simple JWT
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Heroku / PythonAnywhere
- **Python**: 3.10+

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- PostgreSQL (for production)

### Local Development Setup

1. **Clone the repository**

```bash
git clone <repository-url>
cd fitness_tracker_api
```

2. **Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create a superuser**

```bash
python manage.py createsuperuser
```

7. **Run the development server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/fitness_tracker

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

## Running the Application

### Development

```bash
python manage.py runserver
```

### Run with specific settings

```bash
python manage.py runserver --settings=fitness_tracker.settings
```

### Create sample data

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from activities.models import Activity
from datetime import datetime, timedelta

# Create test user
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Create sample activities
Activity.objects.create(
    user=user,
    activity_type='Running',
    duration=30,
    distance=5.0,
    calories_burned=300,
    date=datetime.now().date()
)
```

## API Documentation

### Base URL

- Development: `http://localhost:8000/api/`
- Production: `https://your-app.herokuapp.com/api/`

### Authentication

All endpoints (except registration and login) require JWT authentication.

**Headers:**

```
Authorization: Bearer <access_token>
```

### Endpoints Overview

#### Authentication & Users

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| POST   | `/api/users/register/`      | Register a new user      |
| POST   | `/api/users/login/`         | Login and get JWT tokens |
| POST   | `/api/users/token/refresh/` | Refresh access token     |
| GET    | `/api/users/profile/`       | Get current user profile |
| PUT    | `/api/users/profile/`       | Update user profile      |

#### Activities

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| GET    | `/api/activities/`         | List all user activities |
| POST   | `/api/activities/`         | Create new activity      |
| GET    | `/api/activities/{id}/`    | Get activity details     |
| PUT    | `/api/activities/{id}/`    | Update activity          |
| PATCH  | `/api/activities/{id}/`    | Partial update activity  |
| DELETE | `/api/activities/{id}/`    | Delete activity          |
| GET    | `/api/activities/metrics/` | Get activity metrics     |

#### Goals

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/api/goals/`      | List all user goals |
| POST   | `/api/goals/`      | Create new goal     |
| GET    | `/api/goals/{id}/` | Get goal details    |
| PUT    | `/api/goals/{id}/` | Update goal         |
| DELETE | `/api/goals/{id}/` | Delete goal         |

### Detailed API Examples

#### 1. User Registration

**Request:**

```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "password_confirm": "securePassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

#### 2. User Login

**Request:**

```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securePassword123"
}
```

**Response (200 OK):**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### 3. Create Activity

**Request:**

```http
POST /api/activities/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "activity_type": "Running",
  "duration": 45,
  "distance": 7.5,
  "calories_burned": 450,
  "date": "2024-02-07",
  "notes": "Morning run in the park"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "user": 1,
  "activity_type": "Running",
  "duration": 45,
  "distance": 7.5,
  "calories_burned": 450,
  "date": "2024-02-07",
  "notes": "Morning run in the park",
  "created_at": "2024-02-07T08:30:00Z",
  "updated_at": "2024-02-07T08:30:00Z"
}
```

#### 4. List Activities with Filters

**Request:**

```http
GET /api/activities/?activity_type=Running&start_date=2024-02-01&end_date=2024-02-07&ordering=-date
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "user": 1,
      "activity_type": "Running",
      "duration": 45,
      "distance": 7.5,
      "calories_burned": 450,
      "date": "2024-02-07",
      "notes": "Morning run",
      "created_at": "2024-02-07T08:30:00Z",
      "updated_at": "2024-02-07T08:30:00Z"
    }
  ]
}
```

#### 5. Get Activity Metrics

**Request:**

```http
GET /api/activities/metrics/?start_date=2024-02-01&end_date=2024-02-07
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Response (200 OK):**

```json
{
  "total_activities": 15,
  "total_duration": 675,
  "total_distance": 85.5,
  "total_calories": 5250,
  "average_duration": 45,
  "average_distance": 5.7,
  "average_calories": 350,
  "activity_breakdown": {
    "Running": 8,
    "Cycling": 5,
    "Weightlifting": 2
  },
  "period": {
    "start_date": "2024-02-01",
    "end_date": "2024-02-07"
  }
}
```

#### 6. Create Goal

**Request:**

```http
POST /api/goals/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "title": "Run 100km in February",
  "description": "Complete 100 kilometers of running this month",
  "goal_type": "distance",
  "target_value": 100.0,
  "activity_type": "Running",
  "start_date": "2024-02-01",
  "end_date": "2024-02-29"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "user": 1,
  "title": "Run 100km in February",
  "description": "Complete 100 kilometers of running this month",
  "goal_type": "distance",
  "target_value": 100.0,
  "current_value": 0.0,
  "progress_percentage": 0.0,
  "activity_type": "Running",
  "start_date": "2024-02-01",
  "end_date": "2024-02-29",
  "is_completed": false,
  "created_at": "2024-02-01T10:00:00Z"
}
```

### Query Parameters

#### Activities List

- `activity_type`: Filter by activity type (e.g., Running, Cycling)
- `start_date`: Filter activities from this date (YYYY-MM-DD)
- `end_date`: Filter activities until this date (YYYY-MM-DD)
- `ordering`: Sort by field (prefix with `-` for descending)
  - Options: `date`, `-date`, `duration`, `-duration`, `calories_burned`, `-calories_burned`
- `page`: Page number for pagination
- `page_size`: Number of results per page (default: 10, max: 100)

#### Activity Metrics

- `start_date`: Start of period (YYYY-MM-DD)
- `end_date`: End of period (YYYY-MM-DD)
- `activity_type`: Filter metrics by specific activity type

### Error Responses

#### 400 Bad Request

```json
{
  "error": "Invalid data",
  "details": {
    "duration": ["This field is required."]
  }
}
```

#### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found

```json
{
  "detail": "Not found."
}
```

## Deployment

### Heroku Deployment

1. **Install Heroku CLI**

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**

```bash
heroku login
```

3. **Create Heroku app**

```bash
heroku create fitness-tracker-api-your-name
```

4. **Add PostgreSQL**

```bash
heroku addons:create heroku-postgresql:mini
```

5. **Set environment variables**

```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='fitness-tracker-api-your-name.herokuapp.com'
```

6. **Deploy**

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

7. **Run migrations**

```bash
heroku run python manage.py migrate
```

8. **Create superuser**

```bash
heroku run python manage.py createsuperuser
```

### PythonAnywhere Deployment

1. **Create account** at https://www.pythonanywhere.com

2. **Clone repository**

```bash
git clone <repository-url>
cd fitness_tracker_api
```

3. **Create virtual environment**

```bash
mkvirtualenv --python=/usr/bin/python3.10 fitness-env
pip install -r requirements.txt
```

4. **Configure web app**

- Go to Web tab
- Add new web app
- Choose Manual configuration
- Select Python 3.10
- Set source code directory
- Set virtualenv path

5. **Configure WSGI file**

```python
import sys
import os

path = '/home/yourusername/fitness_tracker_api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'fitness_tracker.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. **Set environment variables**

- Go to Web tab
- Add environment variables in the virtualenv section

7. **Run migrations**

```bash
python manage.py migrate
python manage.py createsuperuser
```

8. **Collect static files**

```bash
python manage.py collectstatic
```

## Testing

### Run all tests

```bash
python manage.py test
```

### Run specific app tests

```bash
python manage.py test users
python manage.py test activities
python manage.py test goals
```

### Run with coverage

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test API with curl

**Register user:**

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123","password_confirm":"test123"}'
```

**Login:**

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'
```

**Create activity:**

```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"activity_type":"Running","duration":30,"distance":5,"calories_burned":300,"date":"2024-02-07"}'
```

## Project Structure

```
fitness_tracker_api/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version for deployment
├── Procfile                 # Heroku deployment configuration
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── manage.py                # Django management script
│
├── fitness_tracker/         # Main project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── users/                   # User management app
│   ├── models.py            # User models (extends Django User)
│   ├── serializers.py       # User serializers
│   ├── views.py             # Authentication & profile views
│   ├── urls.py              # User endpoints
│   ├── permissions.py       # User permissions
│   └── tests.py             # User tests
│
├── activities/              # Activity tracking app
│   ├── models.py            # Activity model
│   ├── serializers.py       # Activity serializers
│   ├── views.py             # Activity CRUD & metrics views
│   ├── urls.py              # Activity endpoints
│   ├── filters.py           # Activity filtering
│   ├── permissions.py       # Activity permissions
│   └── tests.py             # Activity tests
│
├── goals/                   # Goal tracking app
│   ├── models.py            # Goal model
│   ├── serializers.py       # Goal serializers
│   ├── views.py             # Goal CRUD views
│   ├── urls.py              # Goal endpoints
│   └── tests.py             # Goal tests
│
└── static/                  # Static files
```

## Key Features Explained

### Permission System

- Users can only access and modify their own data
- Implemented using custom permission classes
- JWT tokens ensure secure authentication

### Activity Metrics

- Real-time calculation of statistics
- Aggregated data by activity type
- Customizable date ranges
- Average calculations

### Pagination

- Configurable page size (default: 10, max: 100)
- Efficient for large datasets
- Consistent API responses

### Filtering & Sorting

- Django Filter Backend integration
- Multiple filter options
- Multi-field sorting
- Case-insensitive searches

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

- Lenny Beto - Backend Developer - Fitness Tracker API

## Support

For issues and questions:

- Create an issue in the repository
- Check existing documentation
- Review API examples

## Future Enhancements

- [ ] Workout Plans features
- [ ] Activity Sharing capabilities
- [ ] Leaderboards system
- [ ] Push notifications
- [ ] Wearable device integration
- [ ] Social features
- [ ] Advanced analytics dashboard
- [ ] Export data functionality

## Acknowledgments

- Django & Django REST Framework documentation
- JWT authentication best practices
- RESTful API design principles

---

**Happy Tracking! 🏃‍♂️🚴‍♀️💪**
