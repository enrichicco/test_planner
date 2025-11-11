# Migration Guide: Customer Database Schema Integration

## Overview

This document describes the migration from the original simple task planning schema to the customer's comprehensive a2rp (project management) schema.

## What Has Been Completed

### 1. Schema Analysis ✅
- Analyzed all 32 tables in the customer's SQL dump
- Documented table relationships and dependencies
- Created schema analysis document: `docs/SCHEMA_ANALYSIS.md`

### 2. SQLAlchemy Models Created ✅

All models have been created in `src/task_planner/models/a2rp/`:

#### Lookup Tables (`lookups.py`)
- ProjectStatus, ProjectType
- TaskStatus
- ResourceStatus, ResourceType
- ProcessingOrderStatus, ProcessingOrderType
- CostType
- Job, NtAccount, Property

#### Organizational Tables (`organizational.py`)
- CostCenter, CostItem
- Customer
- Imputation
- OrganizationalUnit
- TechnicalFeature
- WorkBreakdownStructure (WBS)
- ResourceBreakdownStructure (RBS)

#### Core Entities (`core.py`)
- **Project** - Main project entity with ~90 columns including EVM metrics
- **Task** - Work breakdown structure tasks with ~100+ columns
- **Resource** - People and equipment with ~35 columns
- **Assignment** - Task-resource assignments with ~40 columns
- **AssignmentByMonth** - Monthly assignment aggregation

#### Supporting Tables (`supporting.py`)
- ProcessingOrder
- HistoricalProjectSummary, HistoricalProjectSummaryResource
- ProjectToPlan, ProjectToPlanOrganizationalUnit
- TaskToPlan, TaskToPlanOrganizationalUnit

### 3. Database Configuration ✅
- Created dedicated database module: `models/a2rp/database.py`
- Updated settings with connection documentation
- All models use `schema="a2rp"` for proper schema isolation

## Database Connection Setup

### Environment Configuration

Update your `.env` file with the customer's database credentials:

```env
DATABASE_URL=postgresql://username:password@hostname:port/database_name
DATABASE_ECHO=false
```

Example:
```env
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/a2rp_production
DATABASE_ECHO=false
```

### Testing Connection

```python
from task_planner.models.a2rp.database import test_connection

if test_connection():
    print("Connected to customer database successfully!")
else:
    print("Connection failed - check your DATABASE_URL")
```

## Using the New Models

### Basic Usage

```python
from task_planner.models.a2rp.database import get_db_context
from task_planner.models.a2rp import Project, Task, Resource, Assignment

# Query projects
with get_db_context() as db:
    projects = db.query(Project).filter(
        Project.project_status_id == 1
    ).all()

    for project in projects:
        print(f"Project: {project.name}")
        print(f"  Status: {project.project_status.name}")
        print(f"  Tasks: {len(project.tasks)}")

# Query tasks with assignments
with get_db_context() as db:
    tasks = db.query(Task).join(Assignment).filter(
        Task.is_milestone == True
    ).all()

    for task in tasks:
        print(f"Milestone: {task.name}")
        print(f"  Assignments: {len(task.assignments)}")
```

### Querying Resources

```python
from task_planner.models.a2rp import Resource, ResourceStatus

with get_db_context() as db:
    active_resources = db.query(Resource).join(ResourceStatus).filter(
        Resource.is_active == True
    ).all()

    for resource in active_resources:
        print(f"Resource: {resource.name} ({resource.resource_type.name})")
        print(f"  Email: {resource.mail_address}")
        print(f"  Org Unit: {resource.organizational_unit.name if resource.organizational_unit else 'N/A'}")
```

## Key Differences from Old Schema

| Feature | Old Schema | New Schema (a2rp) |
|---------|-----------|-------------------|
| **Complexity** | Simple, 5-8 tables | Enterprise, 32 tables |
| **Domain** | Generic task scheduling | MS Project-like PM system |
| **Projects** | Not supported | Full hierarchical projects with EVM |
| **Resources** | Basic Person model | Comprehensive Resource with org structure |
| **Cost Tracking** | None | Extensive cost and budget tracking |
| **Baselines** | None | Multiple baselines (0, 1, 6, 10) |
| **Work Tracking** | Basic duration | Detailed work, overtime, material work |
| **Organization** | None | Full org units, cost centers, WBS, RBS |

## What Still Needs To Be Done

### 1. Update Services 🔄
The old service layer needs to be rewritten to work with the new models:

**Old services to update/replace:**
- `services/task_service.py` → needs Task model adaptation
- `services/resource_service.py` → needs Resource model adaptation
- `services/person_service.py` → replace with Resource queries
- `services/team_service.py` → replace with OrganizationalUnit
- `services/planning.py` → adapt to new Project/Task models
- `services/scheduling_service.py` → adapt to Assignment model

**New services to create:**
- `services/a2rp/project_service.py` - Project CRUD and queries
- `services/a2rp/assignment_service.py` - Assignment management
- `services/a2rp/cost_tracking_service.py` - Cost and EVM calculations
- `services/a2rp/organizational_service.py` - Org structure queries

### 2. Update API Endpoints 🔄
FastAPI endpoints need to be updated:

**Old endpoints** (`api/routers/`):
- `tasks.py` - Update to use new Task model
- `resources.py` - Update to use new Resource model
- `people.py` - Deprecate or map to Resource
- `teams.py` - Map to OrganizationalUnit
- `schedules.py` - Update to use new Assignment/Project

**New endpoints to create:**
- `api/routers/a2rp/projects.py` - Project management
- `api/routers/a2rp/assignments.py` - Assignment tracking
- `api/routers/a2rp/costs.py` - Cost reporting
- `api/routers/a2rp/reports.py` - EVM and progress reports

### 3. Update Pydantic Schemas 🔄
Create new Pydantic schemas for API validation:

```python
# api/schemas/a2rp/
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_type_id: int
    project_status_id: int
    # ... other fields

class ProjectResponse(ProjectBase):
    project_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    # ... relationships

    class Config:
        from_attributes = True
```

### 4. Update Tests 🔄
Adapt existing tests and create new ones:

```python
# tests/test_a2rp_models.py
def test_project_creation(db_session):
    project = Project(
        name="Test Project",
        project_type_id=1,
        project_status_id=1
    )
    db_session.add(project)
    db_session.commit()

    assert project.project_id is not None
    assert project.name == "Test Project"
```

### 5. Data Migration Considerations 🔄

**Important:** The customer database already has data!

- **DO NOT** run `init_db()` carelessly - it may try to create tables
- **DO NOT** drop or truncate any tables
- **READ-ONLY first**: Start with read-only queries to understand the data
- Test with a database backup or development copy first

## Migration Strategy

### Phase 1: Read-Only Integration (Recommended First Step)
1. Configure database connection to customer DB
2. Test reading existing data
3. Create simple query services
4. Build read-only API endpoints
5. Validate data relationships

### Phase 2: Service Layer Replacement
1. Create new service modules for a2rp
2. Gradually replace old services
3. Keep old models for backward compatibility if needed
4. Update business logic to work with new schema

### Phase 3: API Modernization
1. Create new API endpoints for a2rp
2. Update Pydantic schemas
3. Deprecate old endpoints or create adapters
4. Update API documentation

### Phase 4: Full Integration
1. Update scheduler to work with new Assignment model
2. Integrate reporting with EVM metrics
3. Complete test coverage
4. Performance optimization

## Example: Creating a New Service

```python
# src/task_planner/services/a2rp/project_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from ...models.a2rp import Project, ProjectStatus, Task

class ProjectService:
    """Service for managing projects in the a2rp schema."""

    def __init__(self, db: Session):
        self.db = db

    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self.db.query(Project).filter(
            Project.project_id == project_id
        ).first()

    def list_projects(
        self,
        status_id: Optional[int] = None,
        limit: int = 100
    ) -> List[Project]:
        """List projects with optional filtering."""
        query = self.db.query(Project)

        if status_id:
            query = query.filter(Project.project_status_id == status_id)

        return query.limit(limit).all()

    def get_project_with_tasks(self, project_id: int) -> Optional[Project]:
        """Get project with all tasks loaded."""
        return self.db.query(Project).filter(
            Project.project_id == project_id
        ).join(Project.tasks).first()

    def calculate_project_progress(self, project_id: int) -> dict:
        """Calculate project progress metrics."""
        project = self.get_project(project_id)
        if not project:
            return None

        return {
            "project_id": project.project_id,
            "name": project.name,
            "percent_completed": project.percent_completed,
            "cost": float(project.cost) if project.cost else 0,
            "actual_cost": float(project.actual_cost) if project.actual_cost else 0,
            "cpi": float(project.cpi) if project.cpi else None,
            "spi": float(project.spi) if project.spi else None,
        }
```

## Testing Checklist

Before deploying to production:

- [ ] Database connection works
- [ ] Can query all major tables (Project, Task, Resource, Assignment)
- [ ] Relationships load correctly (no N+1 queries)
- [ ] Read-only operations don't modify data
- [ ] All foreign key relationships are valid
- [ ] Performance is acceptable for large datasets
- [ ] Error handling works for missing/invalid IDs
- [ ] API endpoints return correct data
- [ ] Pydantic schemas validate correctly
- [ ] Tests pass with real database

## Rollback Plan

If issues occur:

1. Keep old models in `task_planner/models/` (legacy)
2. Git tag before major changes
3. Use feature flags to toggle between old/new
4. Keep database backups
5. Have rollback scripts ready

## Getting Help

For questions or issues:

1. Check schema analysis: `docs/SCHEMA_ANALYSIS.md`
2. Review SQL dump: `mcr_sql_schemas/dump_20251111_1530_full_db.sql`
3. Check model definitions in `src/task_planner/models/a2rp/`
4. Test queries in Python REPL before using in code

## Next Steps

1. Configure your database connection
2. Test connection with `test_connection()`
3. Try basic queries to understand the data
4. Plan which services to update first
5. Create new API endpoints incrementally
6. Write tests as you go

Good luck with the migration!
