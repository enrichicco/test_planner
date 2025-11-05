# Quick Start Guide

This guide will help you get started with the Task Planner Service quickly.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://gitlab.othernet.boh:11443/testgroup/mcr_planner.git
   cd mcr_planner
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your environment**

   ```bash
   cp .env.example .env
   # Edit .env to configure your database connection
   ```

## Basic Usage

### 1. Initialize the Database

```python
from task_planner import init_db

# Initialize database tables
init_db()
```

### 2. Create Teams and People

```python
from task_planner import get_db_session, TeamService, PersonService

db = get_db_session()

# Create services
team_service = TeamService(db)
person_service = PersonService(db)

# Create a team
dev_team = team_service.create_team(
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

# Add person to team
team_service.add_member(dev_team.id, alice.id)

db.close()
```

### 3. Create and Schedule Tasks

```python
from task_planner import get_db_session, TaskService, PlanningService
from datetime import datetime

db = get_db_session()

task_service = TaskService(db)
planning_service = PlanningService(db)

# Create a task
task = task_service.create_task(
    name="Build feature X",
    description="Implement feature X",
    estimated_hours=16.0,
    priority=10,
    team_id=dev_team.id,
    assigned_person_id=alice.id
)

# Schedule the task
schedule = planning_service.create_schedule([task])

print(f"Task scheduled from {schedule[task.id][0]} to {schedule[task.id][1]}")

db.close()
```

### 4. Generate Reports

```python
from task_planner import get_db_session, ReportGenerator

db = get_db_session()
report_gen = ReportGenerator(db)

# Task summary
summary = report_gen.generate_task_summary()
print(f"Total tasks: {summary['total_tasks']}")
print(f"Total estimated hours: {summary['total_estimated_hours']}")

# Person workload
workload = report_gen.generate_person_workload_report()
for person in workload:
    print(f"{person['person_name']}: {person['total_estimated_hours']} hours")

db.close()
```

## Running the Example

Run the comprehensive example script:

```bash
python examples/basic_usage.py
```

This will demonstrate:

- Creating teams, people, and resources
- Adding skills to people
- Creating tasks with dependencies
- Scheduling tasks
- Recording exceptions
- Generating various reports

## Running Tests

```bash
pytest tests/ -v
```

## Common Tasks

### Add a dependency between tasks

```python
task_service.add_dependency(
    task_id=task2.id,
    depends_on_task_id=task1.id
)
```

### Record an exception

```python
exception = task_service.record_exception(
    task_id=task.id,
    exception_type="resource_unavailable",
    description="Developer on sick leave"
)
```

### Reschedule a task

```python
new_schedule = planning_service.reschedule_task(
    task_id=task.id,
    reason="Delay due to exception",
    new_start=datetime.now()
)
```

### Update task status

```python
task_service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
# ... work happens ...
task_service.update_task_status(task.id, TaskStatus.COMPLETED)
```

## Database Configuration

### SQLite (Development/Testing)

```env
DATABASE_URL=sqlite:///task_planner.db
```

### PostgreSQL (Production)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/task_planner
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [examples/](examples/) directory for more examples
- Check the [tests/](tests/) directory to see how to use each service
- Customize the models and services for your specific needs

## Support

For issues, questions, or contributions, please visit:
<https://gitlab.othernet.boh:11443/testgroup/mcr_planner>
