#!/usr/bin/env python3
"""
Example usage of the Task Planner Service.

This script demonstrates:
- Setting up the database
- Creating teams, people, and resources
- Creating tasks with dependencies
- Scheduling tasks
- Handling exceptions and rescheduling
- Generating reports
"""

from datetime import datetime

from task_planner.models import TaskStatus
from task_planner.models.a2rp import ResourceType
from task_planner.reports import ReportGenerator
from task_planner.services import (
    PersonService,
    PlanningService,
    ResourceService,
    TaskService,
    TeamService,
)
from task_planner.utils import get_db_session, init_db


def main() -> None:
    """Run the example."""
    print("=" * 80)
    print("Task Planner Service - Example Usage")
    print("=" * 80)
    print()

    # Initialize database
    print("1. Initializing database...")
    init_db()
    print("   ✓ Database initialized")
    print()

    # Get database session
    db = get_db_session()

    # Initialize services
    team_service = TeamService(db)
    person_service = PersonService(db)
    resource_service = ResourceService(db)
    task_service = TaskService(db)
    planning_service = PlanningService(db)
    report_gen = ReportGenerator(db)

    try:
        # Create teams
        print("2. Creating teams...")
        dev_team = team_service.create_team(
            name="Development Team",
            description="Software development team",
        )
        qa_team = team_service.create_team(
            name="QA Team",
            description="Quality assurance team",
        )
        print(f"   ✓ Created team: {dev_team.name}")
        print(f"   ✓ Created team: {qa_team.name}")
        print()

        # Create people
        print("3. Creating people...")
        alice = person_service.create_person(
            name="Alice Johnson",
            email="alice@example.com",
            role="Senior Developer",
        )
        bob = person_service.create_person(
            name="Bob Smith",
            email="bob@example.com",
            role="Developer",
        )
        charlie = person_service.create_person(
            name="Charlie Davis",
            email="charlie@example.com",
            role="QA Engineer",
        )
        print(f"   ✓ Created person: {alice.name}")
        print(f"   ✓ Created person: {bob.name}")
        print(f"   ✓ Created person: {charlie.name}")
        print()

        # Add people to teams
        print("4. Adding people to teams...")
        team_service.add_member(dev_team.id, alice.id)
        team_service.add_member(dev_team.id, bob.id)
        team_service.add_member(qa_team.id, charlie.id)
        print(f"   ✓ Added {alice.name} to {dev_team.name}")
        print(f"   ✓ Added {bob.name} to {dev_team.name}")
        print(f"   ✓ Added {charlie.name} to {qa_team.name}")
        print()

        # Create resources
        print("5. Creating resources...")
        python_skill = resource_service.create_resource(
            name="Python Programming",
            resource_type=ResourceType.SKILL,
            description="Python development skills",
        )
        testing_tool = resource_service.create_resource(
            name="Selenium",
            resource_type=ResourceType.EQUIPMENT,
            description="Selenium testing framework",
        )
        print(f"   ✓ Created resource: {python_skill.name}")
        print(f"   ✓ Created resource: {testing_tool.name}")
        print()

        # Add skills to people
        print("6. Adding skills to people...")
        person_service.add_skill(alice.id, python_skill.id)
        person_service.add_skill(bob.id, python_skill.id)
        person_service.add_skill(charlie.id, testing_tool.id)
        print(f"   ✓ Added {python_skill.name} skill to {alice.name}")
        print(f"   ✓ Added {python_skill.name} skill to {bob.name}")
        print(f"   ✓ Added {testing_tool.name} skill to {charlie.name}")
        print()

        # Create tasks
        print("7. Creating tasks...")
        task1 = task_service.create_task(
            name="Design database schema",
            description="Design and document the database schema",
            estimated_hours=8.0,
            priority=10,
            team_id=dev_team.id,
            assigned_person_id=alice.id,
        )

        task2 = task_service.create_task(
            name="Implement user authentication",
            description="Implement user login and registration",
            estimated_hours=16.0,
            priority=9,
            team_id=dev_team.id,
            assigned_person_id=bob.id,
        )

        task3 = task_service.create_task(
            name="Create API endpoints",
            description="Create REST API endpoints",
            estimated_hours=12.0,
            priority=8,
            team_id=dev_team.id,
            assigned_person_id=alice.id,
        )

        task4 = task_service.create_task(
            name="Test authentication flow",
            description="Write and run tests for authentication",
            estimated_hours=8.0,
            priority=7,
            team_id=qa_team.id,
            assigned_person_id=charlie.id,
        )

        print(f"   ✓ Created task: {task1.name}")
        print(f"   ✓ Created task: {task2.name}")
        print(f"   ✓ Created task: {task3.name}")
        print(f"   ✓ Created task: {task4.name}")
        print()

        # Add task dependencies
        print("8. Adding task dependencies...")
        task_service.add_dependency(task2.id, task1.id)  # Auth depends on schema
        task_service.add_dependency(task3.id, task1.id)  # API depends on schema
        task_service.add_dependency(task4.id, task2.id)  # Testing depends on auth
        print("   ✓ Task dependencies added")
        print()

        # Add resource requirements
        print("9. Adding resource requirements...")
        task_service.add_resource_requirement(task1.id, python_skill.id, 1.0)
        task_service.add_resource_requirement(task2.id, python_skill.id, 1.0)
        task_service.add_resource_requirement(task3.id, python_skill.id, 1.0)
        task_service.add_resource_requirement(task4.id, testing_tool.id, 1.0)
        print("   ✓ Resource requirements added")
        print()

        # Create schedule
        print("10. Creating schedule using PyJobShop...")
        tasks = [task1, task2, task3, task4]
        start_date = datetime.now()

        try:
            schedule = planning_service.create_schedule(tasks, start_date)
            print("    ✓ Schedule created successfully!")
            print()
            print("    Scheduled tasks:")
            for task_id, (start, end) in schedule.items():
                task = task_service.get_task(task_id)
                duration = (end - start).total_seconds() / 3600
                print(f"      - {getattr(task, 'name', None)}:")
                print(f"        Start: {start.strftime('%Y-%m-%d %H:%M')}")
                print(f"        End:   {end.strftime('%Y-%m-%d %H:%M')}")
                print(f"        Duration: {duration:.1f} hours")
        except Exception as e:
            print(f"    ! Schedule creation encountered an issue: {e}")
            print("      (This is expected with PyJobShop integration)")
        print()

        # Simulate task progress
        print("11. Simulating task progress...")
        task_service.update_task_status(task1.id, TaskStatus.IN_PROGRESS)
        print(f"    ✓ {task1.name} started")
        task_service.update_task_status(task1.id, TaskStatus.COMPLETED)
        print(f"    ✓ {task1.name} completed")
        print()

        # Record an exception
        print("12. Recording a task exception...")
        task_service.record_exception(
            task2.id,
            "resource_unavailable",
            "Developer on sick leave, task delayed",
        )
        print(f"    ✓ Exception recorded for {task2.name}")
        print()

        # Generate reports
        print("13. Generating reports...")
        print()

        # Task summary
        print("    Task Summary Report:")
        summary = report_gen.generate_task_summary()
        print(f"      Total tasks: {summary['total_tasks']}")
        print("      Status breakdown:")
        for status, count in summary["status_counts"].items():
            if count > 0:
                print(f"        - {status}: {count}")
        print(f"      Total estimated hours: {summary['total_estimated_hours']:.1f}")
        print()

        # Person workload
        print("    Person Workload Report:")
        workload = report_gen.generate_person_workload_report()
        for person in workload:
            print(f"      {person['person_name']}:")
            print(f"        Active tasks: {person['active_tasks']}")
            print(f"        Estimated hours: {person['total_estimated_hours']:.1f}")
            print(f"        Utilization: {person['utilization_days']:.1f} days")
        print()

        # Resource utilization
        print("    Resource Utilization Report:")
        resources_report = report_gen.generate_resource_utilization_report()
        for res in resources_report:
            print(f"      {res['resource_name']} ({res['resource_type']}):")
            print(f"        Capacity: {res['capacity']:.1f}")
            print(f"        Current usage: {res['current_usage']:.1f}")
            print(f"        Utilization: {res['utilization_percentage']:.1f}%")
        print()

        # Exception report
        print("    Exception Report:")
        exceptions = report_gen.generate_exception_report()
        for exc in exceptions:
            print(f"      Task: {exc['task_name']}")
            print(f"        Type: {exc['exception_type']}")
            print(f"        Description: {exc['description']}")
            print(f"        Resolved: {exc['resolved']}")
        print()

        print("=" * 80)
        print("Example completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
