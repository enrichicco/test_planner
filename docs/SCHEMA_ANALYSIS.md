# Customer Database Schema Analysis

## Overview
- **Schema Name:** a2rp
- **Database:** PostgreSQL 17.5
- **Total Tables:** 32
- **Domain:** Enterprise Project Management & Resource Planning

## Table Categories

### 1. Lookup/Reference Tables (Status & Type)
- `project_status` - Project status values
- `project_type` - Types of projects
- `task_status` - Task status values
- `resource_status` - Resource availability status
- `resource_type` - Types of resources (human, material, etc.)
- `processing_order_status` - Processing order status
- `processing_order_type` - Types of processing orders
- `cost_type` - Types of costs

### 2. Core Entity Tables
- `project` - Main project entity with extensive EVM fields (~90 columns)
- `task` - Work breakdown structure tasks (~100+ columns)
- `resource` - People and equipment resources (~35 columns)
- `assignment` - Task-Resource assignments (~40 columns)
- `assignment_by_month` - Monthly assignment aggregation

### 3. Organizational Structure
- `organizational_unit` - Organizational hierarchy
- `cost_center` - Cost center management
- `customer` - Customer information
- `imputation` - Cost imputation/allocation

### 4. Breakdown Structures
- `work_breakdown_structure` - WBS definitions
- `resource_breakdown_structure` - RBS definitions

### 5. Processing & Planning
- `processing_order` - Work orders/requests
- `project_to_plan` - Projects in planning phase
- `project_to_plan_organizational_unit` - Planning org units
- `task_to_plan` - Tasks in planning phase
- `task_to_plan_organizational_unit` - Planning org units for tasks

### 6. Cost Management
- `cost_item` - Cost line items
- `historical_project_summary` - Historical project data
- `historical_project_summary_resource` - Historical resource data

### 7. Supporting Tables
- `job` - Job definitions
- `nt_account` - Windows NT account integration
- `property` - Generic properties
- `technical_feature` - Technical features

### 8. Chat/External
- `public.ckrgky205xwebcuq_chat_history` - Chat history table

## Key Relationships

### Project Hierarchy
```
project (parent_id) -> project
project -> project_status
project -> project_type
project -> customer
project -> work_breakdown_structure
project -> organizational_unit
project -> resource (multiple: author, owner, program_manager, project_manager)
```

### Task Structure
```
task -> project
task -> task_status
task (parent_id) -> task
task -> processing_order
task -> cost_center (multiple)
task -> organizational_unit
task -> work_breakdown_structure (multiple)
```

### Resource Management
```
resource -> resource_status
resource -> resource_type
resource -> organizational_unit (multiple)
resource -> resource_breakdown_structure (multiple)
resource -> cost_center (multiple)
resource -> nt_account
resource -> property
resource -> job
resource (timesheet_manager_id) -> resource
```

### Assignment Tracking
```
assignment -> task
assignment -> resource (multiple: resource_id, owner_id, manager_id)
assignment -> resource_type
assignment -> imputation
assignment -> cost_center
assignment -> organizational_unit
assignment -> work_breakdown_structure (multiple)
```

## Migration Strategy

### Phase 1: Lookup Tables (Simplest)
Create models for all status and type tables first - they have no dependencies.

### Phase 2: Organizational & Structure Tables
Create models for organizational_unit, cost_center, customer, WBS, RBS.

### Phase 3: Core Entity Base Models
Create base models for project, task, resource without all relationships.

### Phase 4: Complete Relationships
Add all foreign key relationships and complete the models.

### Phase 5: Supporting Tables
Create models for remaining tables (processing_order, assignments, etc.).

## Notes
- All tables use integer primary keys with sequences
- Extensive use of numeric type for financial/work calculations
- Many optional fields (nullable)
- Cascade deletes on foreign keys
- Schema prefix 'a2rp' must be specified in SQLAlchemy models
