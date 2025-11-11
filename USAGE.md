# Task Planning Service - Usage Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Workflow](#basic-workflow)
3. [Advanced Features](#advanced-features)
4. [API Examples](#api-examples)
5. [Python SDK Examples](#python-sdk-examples)

## Getting Started

### Start the Service

Using Docker Compose (recommended):
```bash
docker-compose up -d
```

Or manually:
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Run migrations
alembic upgrade head

# Start API server
uvicorn src.task_planner.api.main:app --reload
```

Access the API documentation at: http://localhost:8000/docs

## Basic Workflow

### 1. Create a Team

```bash
curl -X POST "http://localhost:8000/api/v1/teams/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Backend Team",
    "description": "Backend development team"
  }'
```

Response:
```json
{
  "id": 1,
  "name": "Backend Team",
  "description": "Backend development team",
  "is_active": true,
  "created_at": "2025-10-21T10:00:00",
  "updated_at": null
}
```

### 2. Add Team Members

```bash
curl -X POST "http://localhost:8000/api/v1/people/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "role": "Senior Developer",
    "team_id": 1,
    "skills": {
      "python": 5,
      "sql": 4,
      "api_design": 5
    },
    "max_concurrent_tasks": 3
  }'
```

### 3. Add Resources (Optional)

```bash
curl -X POST "http://localhost:8000/api/v1/resources/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Development Server",
    "resource_type": "compute",
    "capacity": 1.0,
    "is_renewable": true,
    "properties": {
      "cpu": "8 cores",
      "ram": "32GB"
    }
  }'
```

### 4. Create Tasks

```bash
# Task 1
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Database schema design",
    "duration": 4.0,
    "description": "Design the database schema for user management",
    "team_id": 1,
    "priority": 3,
    "required_skills": {"sql": 4}
  }'

# Task 2 (depends on Task 1)
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Implement API endpoints",
    "duration": 8.0,
    "description": "Implement REST API endpoints",
    "team_id": 1,
    "priority": 3,
    "predecessor_id": 1,
    "deadline": "2025-10-30T17:00:00Z",
    "required_skills": {"python": 4, "api_design": 4}
  }'
```

### 5. Create a Schedule

```bash
curl -X POST "http://localhost:8000/api/v1/schedules/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sprint 1 - Week 1",
    "start_date": "2025-10-21T09:00:00Z",
    "end_date": "2025-10-28T17:00:00Z",
    "team_id": 1
  }'
```

Response includes:
- Schedule ID
- Optimization results
- Solver used
- Solve time

### 6. View Assignments

```bash
curl "http://localhost:8000/api/v1/schedules/1/assignments"
```

### 7. Check for Exceptions

```bash
curl "http://localhost:8000/api/v1/schedules/1/exceptions?resolved=false"
```

### 8. Generate Reports

```bash
# JSON report
curl "http://localhost:8000/api/v1/reports/1/json" > report.json

# HTML report
curl "http://localhost:8000/api/v1/reports/1/html" -o report.html

# CSV timeline
curl "http://localhost:8000/api/v1/reports/1/csv/timeline" -o timeline.csv
```

## Advanced Features

### Rescheduling

When tasks are delayed or people become unavailable:

```bash
# Mark person as unavailable
curl -X PATCH "http://localhost:8000/api/v1/people/1" \
  -H "Content-Type: application/json" \
  -d '{"is_available": false}'

# Reschedule
curl -X POST "http://localhost:8000/api/v1/schedules/1/reschedule"
```

### Handling Exceptions

```bash
# Resolve an exception
curl -X POST "http://localhost:8000/api/v1/schedules/exceptions/1/resolve" \
  -H "Content-Type: application/json" \
  -d '{
    "resolution_notes": "Assigned additional resources",
    "reschedule": true
  }'
```

### Task Dependencies

Create a dependency chain:

```bash
# Task A
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -d '{"name": "Task A", "duration": 4.0, "team_id": 1}'

# Task B (depends on A)
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -d '{"name": "Task B", "duration": 6.0, "team_id": 1, "predecessor_id": 1}'

# Task C (depends on B)
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -d '{"name": "Task C", "duration": 8.0, "team_id": 1, "predecessor_id": 2}'
```

### Filtering and Queries

```bash
# List only pending tasks
curl "http://localhost:8000/api/v1/tasks/?status=pending"

# List people in a specific team
curl "http://localhost:8000/api/v1/people/?team_id=1"

# List available people only
curl "http://localhost:8000/api/v1/people/?available_only=true"

# List active schedules
curl "http://localhost:8000/api/v1/schedules/?status=active"
```

## Python SDK Examples

### Using the Services Directly

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from src.task_planner.models.database import Base
from src.task_planner.services import (
    TeamService,
    PersonService,
    TaskService,
    SchedulingService,
)
from src.task_planner.models import TaskPriority

# Setup database
engine = create_engine("postgresql://postgres:postgres@localhost:5432/task_planner")
Session = sessionmaker(bind=engine)
db = Session()

# Create team
team_service = TeamService(db)
team = team_service.create_team(
    name="Development Team",
    description="Our awesome dev team"
)

# Add team members
person_service = PersonService(db)
alice = person_service.create_person(
    name="Alice",
    email="alice@example.com",
    team_id=team.id,
    skills={"python": 5, "javascript": 4}
)

bob = person_service.create_person(
    name="Bob",
    email="bob@example.com",
    team_id=team.id,
    skills={"python": 4, "devops": 5}
)

# Create tasks
task_service = TaskService(db)
task1 = task_service.create_task(
    name="Setup CI/CD",
    duration=8.0,
    team_id=team.id,
    priority=TaskPriority.HIGH,
    required_skills={"devops": 4}
)

task2 = task_service.create_task(
    name="Implement authentication",
    duration=12.0,
    team_id=team.id,
    priority=TaskPriority.CRITICAL,
    deadline=datetime.now() + timedelta(days=3),
    required_skills={"python": 4}
)

# Create schedule
scheduling_service = SchedulingService(db)
schedule = scheduling_service.create_schedule(
    name="Sprint 1",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=14),
    team_id=team.id
)

print(f"Schedule created: {schedule.name}")
print(f"Objective value: {schedule.objective_value}")
print(f"Solve time: {schedule.solve_time}s")

# Get assignments
assignments = scheduling_service.get_assignments(schedule.id)
for assignment in assignments:
    print(f"Task {assignment.task_id} -> Person {assignment.person_id}")
    print(f"  Start: {assignment.scheduled_start}")
    print(f"  End: {assignment.scheduled_end}")

# Check exceptions
exceptions = scheduling_service.get_exceptions(schedule.id, resolved=False)
print(f"Unresolved exceptions: {len(exceptions)}")
```

### Generating Reports

```python
from src.task_planner.reports import ReportGenerator, ScheduleReport

# Get schedule data
schedule = scheduling_service.get_schedule(1)
assignments = scheduling_service.get_assignments(1)
exceptions = scheduling_service.get_exceptions(1)

# Get tasks and people
from src.task_planner.models import Task, Person
task_ids = [a.task_id for a in assignments]
tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()
person_ids = [a.person_id for a in assignments if a.person_id]
people = db.query(Person).filter(Person.id.in_(person_ids)).all()

# Generate report
report = ScheduleReport(schedule, assignments, tasks, people, exceptions)
report_data = report.generate_full_report()

# Save as JSON
generator = ReportGenerator()
json_path = generator.generate_json_report(report_data, "my_report.json")
print(f"JSON report saved to: {json_path}")

# Save as HTML
html_path = generator.generate_html_report(report_data, "my_report.html")
print(f"HTML report saved to: {html_path}")

# Save timeline as CSV
timeline = report.generate_task_timeline()
csv_path = generator.generate_csv_report(timeline, "timeline.csv")
print(f"CSV timeline saved to: {csv_path}")
```

## Tips and Best Practices

1. **Always set deadlines for critical tasks** - This helps the scheduler prioritize them

2. **Use task dependencies** - Define predecessor relationships to maintain logical order

3. **Monitor exceptions** - Regularly check for unresolved exceptions and handle them

4. **Reschedule when needed** - Don't hesitate to reschedule when constraints change

5. **Use appropriate priorities** - HIGH and CRITICAL for urgent tasks, LOW for nice-to-haves

6. **Set realistic durations** - Include buffer time for unexpected issues

7. **Track skills accurately** - Helps the scheduler assign tasks to appropriate people

8. **Monitor person utilization** - Use reports to identify over/under-utilized team members

9. **Review generated schedules** - Always review before finalizing

10. **Keep resources updated** - Mark resources as unavailable when they're not accessible
