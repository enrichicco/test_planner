#!/usr/bin/env python3
"""
Example usage of the Task Planner Service using a2rp schema.

This script demonstrates:
- Setting up the database
- Creating projects, tasks, and resources
- Creating assignments
- Using the a2rp (MCR) schema
"""

from datetime import datetime, timedelta

from task_planner.models.a2rp.database import SessionLocal, init_db
from task_planner.services.a2rp import (
    AssignmentService,
    ProjectService,
    ResourceService,
    TaskService,
)


def main() -> None:
    """Run the example."""
    print("=" * 80)
    print("Task Planner Service - Example Usage (a2rp/MCR Schema)")
    print("=" * 80)
    print()

    # Initialize database
    print("1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    print()

    # Get database session
    db = SessionLocal()

    # Initialize services
    project_service = ProjectService(db)
    task_service = TaskService(db)
    resource_service = ResourceService(db)
    assignment_service = AssignmentService(db)

    try:
        # Note: In a real application, you would need to create lookup tables first
        # (project_type, project_status, task_status, resource_type, resource_status)
        # For this example, we assume they exist with IDs 1, 2, etc.

        # Create a project
        print("2. Creating project...")
        project = project_service.create_project(
            name="Web Application Development",
            description="Build a new web application",
            project_type_id=1,  # Assumes project_type exists
            project_status_id=1,  # Assumes status "Active" exists
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=90),
        )
        print(f"   ✓ Created project: {project.name}")
        print()

        # Create resources
        print("3. Creating resources...")
        alice = resource_service.create_resource(
            name="Alice Johnson",
            email="alice@example.com",
            resource_type_id=1,  # Assumes "Developer" type exists
            resource_status_id=1,  # Assumes "Available" status exists
        )
        bob = resource_service.create_resource(
            name="Bob Smith",
            email="bob@example.com",
            resource_type_id=1,
            resource_status_id=1,
        )
        charlie = resource_service.create_resource(
            name="Charlie Davis",
            email="charlie@example.com",
            resource_type_id=2,  # Assumes "QA" type exists
            resource_status_id=1,
        )
        print(f"   ✓ Created resource: {alice.name}")
        print(f"   ✓ Created resource: {bob.name}")
        print(f"   ✓ Created resource: {charlie.name}")
        print()

        # Create tasks
        print("4. Creating tasks...")
        task1 = task_service.create_task(
            name="Design database schema",
            description="Design and document the database schema",
            project_id=project.project_id,
            task_status_id=1,  # Assumes "Not Started" status exists
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=2),
            work=16.0,  # 16 hours
        )

        task2 = task_service.create_task(
            name="Implement user authentication",
            description="Implement user login and registration",
            project_id=project.project_id,
            task_status_id=1,
            start_date=datetime.now() + timedelta(days=2),
            end_date=datetime.now() + timedelta(days=5),
            work=24.0,  # 24 hours
        )

        task3 = task_service.create_task(
            name="Create API endpoints",
            description="Create REST API endpoints",
            project_id=project.project_id,
            task_status_id=1,
            start_date=datetime.now() + timedelta(days=5),
            end_date=datetime.now() + timedelta(days=8),
            work=24.0,  # 24 hours
        )

        task4 = task_service.create_task(
            name="Test authentication flow",
            description="Write and run tests for authentication",
            project_id=project.project_id,
            task_status_id=1,
            start_date=datetime.now() + timedelta(days=8),
            end_date=datetime.now() + timedelta(days=10),
            work=16.0,  # 16 hours
        )

        print(f"   ✓ Created task: {task1.name} ({task1.work}h)")
        print(f"   ✓ Created task: {task2.name} ({task2.work}h)")
        print(f"   ✓ Created task: {task3.name} ({task3.work}h)")
        print(f"   ✓ Created task: {task4.name} ({task4.work}h)")
        print()

        # Create assignments
        print("5. Creating assignments...")
        assignment1 = assignment_service.create_assignment(
            task_id=task1.task_id,
            resource_id=alice.resource_id,
            work=16.0,
            start_date=task1.start_date,
            end_date=task1.end_date,
        )
        assignment_service.create_assignment(
            task_id=task2.task_id,
            resource_id=bob.resource_id,
            work=24.0,
            start_date=task2.start_date,
            end_date=task2.end_date,
        )
        assignment_service.create_assignment(
            task_id=task3.task_id,
            resource_id=alice.resource_id,
            work=24.0,
            start_date=task3.start_date,
            end_date=task3.end_date,
        )
        assignment_service.create_assignment(
            task_id=task4.task_id,
            resource_id=charlie.resource_id,
            work=16.0,
            start_date=task4.start_date,
            end_date=task4.end_date,
        )
        print(f"   ✓ Assigned {alice.name} to {task1.name}")
        print(f"   ✓ Assigned {bob.name} to {task2.name}")
        print(f"   ✓ Assigned {alice.name} to {task3.name}")
        print(f"   ✓ Assigned {charlie.name} to {task4.name}")
        print()

        # List all tasks for the project
        print("6. Listing all project tasks...")
        all_tasks = task_service.list_tasks(project_id=project.project_id)
        print(f"   ✓ Found {len(all_tasks)} tasks for project '{project.name}'")
        for t in all_tasks:
            print(f"      - {t.name} (Work: {t.work}h)")
        print()

        # List all assignments for a resource
        print("7. Listing assignments for Alice...")
        alice_assignments = assignment_service.list_assignments(resource_id=alice.resource_id)
        print(f"   ✓ Found {len(alice_assignments)} assignments for {alice.name}")
        print()

        # Update task status
        print("8. Updating task status...")
        updated_task = task_service.update_task(
            task_id=task1.task_id,
            task_status_id=2,  # Assumes "In Progress" exists
        )
        if updated_task:
            print(f"   ✓ Updated status for {updated_task.name}")
        print()

        # Update assignment with actual work
        print("9. Recording actual work...")
        updated_assignment = assignment_service.update_assignment(
            assignment_id=assignment1.assignment_id,
            actual_work=18.0,  # Took 18 hours
        )
        if updated_assignment:
            print(
                f"   ✓ Recorded {updated_assignment.actual_work}h actual work "
                f"(estimated: {updated_assignment.work}h)"
            )
        print()

        print("=" * 80)
        print("Example completed successfully!")
        print("=" * 80)
        print()
        print("NOTE: This example assumes lookup tables exist (project_type, ")
        print("      project_status, task_status, resource_type, resource_status).")
        print("      In production, you would need to populate these first.")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
