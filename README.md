# Task Planner Service

A comprehensive task planning service built with Python, using PyJobShop for intelligent scheduling and PostgreSQL for data persistence.

## Features

- **Team Management**: Create and manage teams with multiple members
- **People Management**: Track individuals, their skills, availability, and workload
- **Resource Management**: Manage equipment, materials, skills, and facilities
- **Task Management**: Create tasks with dependencies, resource requirements, and assignments
- **Intelligent Scheduling**: Automatic task scheduling using PyJobShop optimization
- **Exception Handling**: Track and manage task exceptions and delays
- **Rescheduling**: Automatically reschedule tasks when exceptions occur
- **Comprehensive Reports**: Generate various reports for workload, resources, schedules, and performance

## Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL database

### Setup

1. Clone the repository:

    ```bash
    git clone https://gitlab.othernet.boh:11443/testgroup/mcr_planner.git
    cd mcr_planner
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    # or
    pip install -e .
    ```

3. Configure the database:

   Copy `.env.example` to `.env` and update the database URL:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/task_planner
   DEBUG=False
   MAX_PLANNING_HORIZON_DAYS=90
   DEFAULT_WORKING_HOURS_PER_DAY=8
   ```

4. Initialize the database:

   ```python
   from task_planner import init_db
   init_db()
   ```

## Quick Start

```python
from task_planner import (
    init_db,
    get_db_session,
    TeamService,
    PersonService,
    TaskService,
    PlanningService,
    ReportGenerator,
)
from task_planner.models import ResourceType

# Initialize database
init_db()

# Get database session
db = get_db_session()

# Initialize services
team_service = TeamService(db)
person_service = PersonService(db)
task_service = TaskService(db)
planning_service = PlanningService(db)

# Create a team
team = team_service.create_team(
    name="Development Team",
    description="Software development team"
)

# Create people
alice = person_service.create_person(
    name="Alice Johnson",
    email="alice@example.com",
    role="Developer",
    availability_hours_per_day=8.0
)

# Add to team
team_service.add_member(team.id, alice.id)

# Create tasks
task1 = task_service.create_task(
    name="Build feature X",
    estimated_hours=16.0,
    team_id=team.id,
    assigned_person_id=alice.id
)

# Schedule tasks
schedule = planning_service.create_schedule([task1])

# Generate reports
report_gen = ReportGenerator(db)
summary = report_gen.generate_task_summary()
print(summary)
```

## Project Structure

```text
mcr_planner/
├── src/
│   └── task_planner/
│       ├── __init__.py          # Main package exports
│       ├── config.py             # Configuration management
│       ├── models/
│       │   └── __init__.py       # Database models
│       ├── services/
│       │   ├── __init__.py       # Service layer exports
│       │   ├── team.py           # Team management
│       │   ├── person.py         # Person management
│       │   ├── resource.py       # Resource management
│       │   ├── task.py           # Task management
│       │   ├── planning.py       # Scheduling with PyJobShop
│       │   └── exceptions.py     # Custom exceptions
│       ├── reports/
│       │   └── __init__.py       # Report generation
│       └── utils/
│           ├── __init__.py       # Utilities exports
│           └── database.py       # Database utilities
├── examples/
│   └── basic_usage.py            # Example usage script
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
└── README.md                     # This file
```

## Core Concepts

### Teams

Teams are groups of people working together. A person can belong to multiple teams.

### People

Individuals with skills, availability, and task assignments. Track their workload and utilization.

### Resources

Equipment, materials, skills, or facilities needed for tasks. Monitor availability and utilization.

### Tasks

Work items with:

- Estimated and actual hours
- Priority levels
- Status tracking (pending, scheduled, in progress, completed, etc.)
- Dependencies on other tasks
- Resource requirements
- Team and person assignments

### Scheduling

Creates optimal schedules considering:

- Task dependencies
- Resource availability
- Person availability
- Time constraints

**Note**: The current implementation uses a simple dependency-aware sequential scheduler. PyJobShop is included as a dependency and can be integrated for more advanced optimization scenarios (multi-resource constraints, complex precedence relationships, etc.).

### Exceptions

Track issues that affect task execution:

- Resource unavailability
- Delays
- Scope changes
- Can trigger rescheduling

## Services

### TeamService

- `create_team()` - Create a new team
- `get_team()` - Get team by ID
- `add_member()` - Add person to team
- `remove_member()` - Remove person from team
- `update_team()` - Update team info
- `delete_team()` - Delete team

### PersonService

- `create_person()` - Create a new person
- `get_person()` - Get person by ID
- `add_skill()` - Add skill to person
- `remove_skill()` - Remove skill from person
- `update_person()` - Update person info
- `delete_person()` - Soft delete person

### ResourceService

- `create_resource()` - Create a new resource
- `get_resource()` - Get resource by ID
- `get_all_resources()` - List all resources
- `update_resource()` - Update resource info
- `delete_resource()` - Delete resource

### TaskService

- `create_task()` - Create a new task
- `get_task()` - Get task by ID
- `add_resource_requirement()` - Add resource to task
- `add_dependency()` - Add task dependency
- `record_exception()` - Record task exception
- `resolve_exception()` - Resolve exception
- `update_task_status()` - Update task status
- `update_task()` - Update task info
- `delete_task()` - Delete task

### PlanningService

- `create_schedule()` - Create optimized schedule for tasks
- `reschedule_task()` - Reschedule task and dependencies
- `validate_schedule()` - Validate schedule for conflicts

### ReportGenerator

- `generate_task_summary()` - Task statistics and status
- `generate_person_workload_report()` - Person utilization
- `generate_resource_utilization_report()` - Resource usage
- `generate_team_performance_report()` - Team metrics
- `generate_schedule_report()` - Schedule for date range
- `generate_exception_report()` - Exception tracking

## Examples

See the `examples/basic_usage.py` file for a comprehensive example demonstrating all features.

Run it with:

```bash
python examples/basic_usage.py
```

## Database Models

The service uses SQLAlchemy ORM with the following models:

- **Team**: Team information and relationships
- **Person**: Individual people with skills and availability
- **Resource**: Equipment, materials, skills, facilities
- **Task**: Work items with scheduling and dependencies
- **TaskResource**: Association between tasks and resources
- **TaskDependency**: Dependencies between tasks
- **TaskException**: Exception tracking for tasks
- **Schedule**: Schedule snapshots

## Configuration

Configure via environment variables or `.env` file:

- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Enable debug mode (default: False)
- `MAX_PLANNING_HORIZON_DAYS`: Maximum days for planning (default: 90)
- `DEFAULT_WORKING_HOURS_PER_DAY`: Default working hours (default: 8)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
