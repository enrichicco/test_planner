"""Report generation for task planner."""
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from task_planner.models import Task, Person, Team, Resource, TaskStatus


class ReportGenerator:
    """Generate various reports for task planning."""
    
    def __init__(self, db: Session):
        """Initialize report generator with database session."""
        self.db = db
    
    def generate_task_summary(self, team_id: Optional[int] = None) -> Dict[str, Any]:
        """Generate a summary report of tasks."""
        query = self.db.query(Task)
        if team_id:
            query = query.filter(Task.team_id == team_id)
        
        tasks = query.all()
        
        # Count by status
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(1 for t in tasks if t.status == status)
        
        # Calculate total estimated vs actual hours
        total_estimated = sum(t.estimated_hours for t in tasks)
        total_actual = sum(t.actual_hours or 0 for t in tasks if t.actual_hours)
        
        # On-time completion rate
        completed_tasks = [t for t in tasks if t.status == TaskStatus.COMPLETED]
        on_time = sum(
            1 for t in completed_tasks
            if t.actual_end and t.scheduled_end and t.actual_end <= t.scheduled_end
        )
        on_time_rate = (on_time / len(completed_tasks) * 100) if completed_tasks else 0
        
        return {
            "total_tasks": len(tasks),
            "status_counts": status_counts,
            "total_estimated_hours": total_estimated,
            "total_actual_hours": total_actual,
            "on_time_completion_rate": round(on_time_rate, 2),
            "completed_tasks": len(completed_tasks),
        }
    
    def generate_person_workload_report(self) -> List[Dict[str, Any]]:
        """Generate workload report for all active people."""
        people = self.db.query(Person).filter(Person.is_active == True).all()
        
        report = []
        for person in people:
            # Get assigned tasks that are not completed
            active_tasks = [
                t for t in person.assigned_tasks
                if t.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            ]
            
            total_hours = sum(t.estimated_hours for t in active_tasks)
            
            report.append({
                "person_id": person.id,
                "person_name": person.name,
                "email": person.email,
                "active_tasks": len(active_tasks),
                "total_estimated_hours": total_hours,
                "availability_hours_per_day": person.availability_hours_per_day,
                "utilization_days": total_hours / person.availability_hours_per_day if person.availability_hours_per_day > 0 else 0,
            })
        
        # Sort by utilization (highest first)
        report.sort(key=lambda x: x["total_estimated_hours"], reverse=True)
        
        return report
    
    def generate_resource_utilization_report(self) -> List[Dict[str, Any]]:
        """Generate resource utilization report."""
        resources = self.db.query(Resource).all()
        
        report = []
        for resource in resources:
            # Get tasks using this resource
            active_requirements = [
                tr for tr in resource.task_requirements
                if tr.task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            ]
            
            total_quantity = sum(tr.quantity_required for tr in active_requirements)
            
            report.append({
                "resource_id": resource.id,
                "resource_name": resource.name,
                "resource_type": resource.type.value,
                "capacity": resource.capacity,
                "current_usage": total_quantity,
                "available": resource.available,
                "utilization_percentage": (total_quantity / resource.capacity * 100) if resource.capacity > 0 else 0,
            })
        
        # Sort by utilization (highest first)
        report.sort(key=lambda x: x["utilization_percentage"], reverse=True)
        
        return report
    
    def generate_team_performance_report(self) -> List[Dict[str, Any]]:
        """Generate performance report for all teams."""
        teams = self.db.query(Team).all()
        
        report = []
        for team in teams:
            tasks = team.tasks
            completed_tasks = [t for t in tasks if t.status == TaskStatus.COMPLETED]
            
            # Calculate average completion time vs estimate
            time_variance = []
            for task in completed_tasks:
                if task.actual_start and task.actual_end:
                    actual_duration = (task.actual_end - task.actual_start).total_seconds() / 3600
                    variance = actual_duration - task.estimated_hours
                    time_variance.append(variance)
            
            avg_variance = sum(time_variance) / len(time_variance) if time_variance else 0
            
            report.append({
                "team_id": team.id,
                "team_name": team.name,
                "total_members": len(team.members),
                "total_tasks": len(tasks),
                "completed_tasks": len(completed_tasks),
                "completion_rate": (len(completed_tasks) / len(tasks) * 100) if tasks else 0,
                "avg_time_variance_hours": round(avg_variance, 2),
            })
        
        return report
    
    def generate_schedule_report(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        """Generate schedule report for a date range."""
        # Get tasks scheduled in the date range
        tasks = (
            self.db.query(Task)
            .filter(
                Task.scheduled_start >= start_date,
                Task.scheduled_end <= end_date,
            )
            .all()
        )
        
        # Group by date
        schedule_by_date = {}
        for task in tasks:
            if task.scheduled_start:
                date_key = task.scheduled_start.date().isoformat()
                if date_key not in schedule_by_date:
                    schedule_by_date[date_key] = []
                
                schedule_by_date[date_key].append({
                    "task_id": task.id,
                    "task_name": task.name,
                    "status": task.status.value,
                    "assigned_person": task.assigned_person.name if task.assigned_person else None,
                    "team": task.team.name if task.team else None,
                    "scheduled_start": task.scheduled_start.isoformat(),
                    "scheduled_end": task.scheduled_end.isoformat() if task.scheduled_end else None,
                    "estimated_hours": task.estimated_hours,
                })
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_tasks": len(tasks),
            "schedule_by_date": schedule_by_date,
        }
    
    def generate_exception_report(self) -> List[Dict[str, Any]]:
        """Generate report of task exceptions."""
        from task_planner.models import TaskException
        
        exceptions = self.db.query(TaskException).all()
        
        report = []
        for exc in exceptions:
            report.append({
                "exception_id": exc.id,
                "task_id": exc.task_id,
                "task_name": exc.task.name,
                "exception_type": exc.exception_type,
                "description": exc.description,
                "occurred_at": exc.occurred_at.isoformat(),
                "resolved": exc.resolved,
                "resolved_at": exc.resolved_at.isoformat() if exc.resolved_at else None,
                "resolution_notes": exc.resolution_notes,
            })
        
        return report
