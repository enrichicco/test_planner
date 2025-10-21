# Task Planning Service

A comprehensive task planning and scheduling service built with Python, PyJobShop, and PostgreSQL.

## Features

- **Team Management**: Organize people into teams
- **Person Management**: Track people with skills and availability
- **Resource Management**: Manage equipment, tools, and other resources
- **Task Management**: Create and track tasks with dependencies, deadlines, and constraints
- **Intelligent Scheduling**: Uses PyJobShop (constraint programming) for optimal scheduling
- **Exception Handling**: Track and resolve scheduling conflicts and issues
- **Rescheduling**: Automatically reschedule when exceptions occur
- **Report Generation**: Generate reports in JSON, HTML, and CSV formats
- **REST API**: Complete FastAPI-based REST API

## Technology Stack

- **Python 3.10+**
- **PyJobShop**: Constraint programming for scheduling
- **SQLAlchemy 2.0**: ORM and database management
- **PostgreSQL**: Database
- **FastAPI**: REST API framework
- **Alembic**: Database migrations
- **Pydantic**: Data validation
- **Jinja2**: Report templating

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start PostgreSQL (using Docker):
```bash
docker-compose up -d postgres
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the API server:
```bash
uvicorn src.task_planner.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Using Docker Compose

Run the entire stack:
```bash
docker-compose up -d
```

This will start PostgreSQL and the API server.

## Documentation

- See [USAGE.md](USAGE.md) for detailed usage examples
- API documentation available at `/docs` endpoint
- Interactive API testing at `/docs` (Swagger UI)

## API Endpoints

### Core Entities
- Teams: `/api/v1/teams/`
- People: `/api/v1/people/`
- Resources: `/api/v1/resources/`
- Tasks: `/api/v1/tasks/`
- Schedules: `/api/v1/schedules/`
- Reports: `/api/v1/reports/`

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Formatting
```bash
black src/ tests/
ruff src/ tests/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## License

MIT License
