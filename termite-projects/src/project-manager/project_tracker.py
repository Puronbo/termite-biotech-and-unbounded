#!/usr/bin/env python3
"""
Termite Research Project Tracker

A comprehensive project management tool for tracking
the three termite research projects.

Author: Termite Research Team
Date: June 2026
Version: 1.0
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ProjectEncoder(json.JSONEncoder):
    """JSON encoder that handles ProjectStatus and Priority enums."""
    def default(self, obj):
        if isinstance(obj, (ProjectStatus, Priority)):
            return obj.value
        return super().default(obj)


class ProjectStatus(Enum):
    """Project status enumeration."""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"


class Priority(Enum):
    """Priority levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class Task:
    """Task data class."""
    id: str
    name: str
    description: str
    status: ProjectStatus
    priority: Priority
    start_date: str
    end_date: str
    assigned_to: str
    dependencies: List[str]
    notes: str = ""


@dataclass
class Milestone:
    """Milestone data class."""
    id: str
    name: str
    description: str
    due_date: str
    status: ProjectStatus
    tasks: List[str]


@dataclass
class Project:
    """Project data class."""
    id: str
    name: str
    description: str
    status: ProjectStatus
    start_date: str
    end_date: str
    budget: float
    spent: float
    tasks: List[Task]
    milestones: List[Milestone]
    notes: str = ""


class ProjectTracker:
    """Main project tracking class."""
    
    def __init__(self, data_file: str = "project_data.json"):
        """Initialize project tracker."""
        self.data_file = data_file
        self.projects: Dict[str, Project] = {}
        self.load_data()
    
    def load_data(self):
        """Load project data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Convert dictionaries back to objects
                    for project_id, project_data in data.get('projects', {}).items():
                        tasks = [Task(**{k: ProjectStatus(v) if k == 'status' else Priority(v) if k == 'priority' else v for k, v in task_data.items()}) for task_data in project_data.get('tasks', [])]
                        milestones = [Milestone(**milestone_data) for milestone_data in project_data.get('milestones', [])]
                        project = Project(
                            id=project_id,
                            name=project_data['name'],
                            description=project_data['description'],
                            status=ProjectStatus(project_data['status']),
                            start_date=project_data['start_date'],
                            end_date=project_data['end_date'],
                            budget=project_data['budget'],
                            spent=project_data['spent'],
                            tasks=tasks,
                            milestones=milestones,
                            notes=project_data.get('notes', '')
                        )
                        self.projects[project_id] = project
                print(f"Loaded {len(self.projects)} projects from {self.data_file}")
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            print("No existing data file found. Creating new projects.")
            self.create_default_projects()
    
    def save_data(self):
        """Save project data to file."""
        data = {
            'last_updated': datetime.now().isoformat(),
            'projects': {}
        }
        
        for project_id, project in self.projects.items():
            project_data = {
                'name': project.name,
                'description': project.description,
                'status': project.status.value,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'budget': project.budget,
                'spent': project.spent,
                'tasks': [asdict(task) for task in project.tasks],
                'milestones': [asdict(milestone) for milestone in project.milestones],
                'notes': project.notes
            }
            data['projects'][project_id] = project_data
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, cls=ProjectEncoder)
            print(f"Data saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def create_default_projects(self):
        """Create default project structures with actual experimental data."""
        # Biofuel Research Project
        biofuel_tasks = [
            Task(
                id="BIO-001",
                name="Termite Collection",
                description="Collect termite colonies from Southern Luzon, Philippines",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-01-06",
                end_date="2026-01-20",
                assigned_to="Field Team",
                dependencies=[],
                notes="3 colonies collected: M. gilvus, N. luzonensis, C. gestroi"
            ),
            Task(
                id="BIO-002",
                name="Bacterial Isolation",
                description="Isolate cellulolytic bacteria from termite gut",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-01-20",
                end_date="2026-02-15",
                assigned_to="Lab Team",
                dependencies=["BIO-001"],
                notes="7 isolates (TF-001 through TF-007) with cellulase activity"
            ),
            Task(
                id="BIO-003",
                name="16S rRNA Identification",
                description="Molecular identification of bacterial isolates",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-02-10",
                end_date="2026-02-28",
                assigned_to="Lab Team",
                dependencies=["BIO-002"],
                notes="Identified: Bacillus, Cellulomonas, Enterobacter, Pseudomonas, Paenibacillus, Streptomyces, Klebsiella"
            ),
            Task(
                id="BIO-004",
                name="Cellulase Assay",
                description="Quantify cellulase enzyme activity of isolates",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-03-01",
                end_date="2026-03-15",
                assigned_to="Lab Team",
                dependencies=["BIO-003"],
                notes="TF-001: 85.2 U/mg highest; all strains 15.2-85.2 U/mg"
            ),
            Task(
                id="BIO-005",
                name="Enzyme Cocktail Optimization",
                description="Optimize enzyme ratios for maximum cellulose conversion",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-03-15",
                end_date="2026-03-31",
                assigned_to="Research Team",
                dependencies=["BIO-004"],
                notes="C-5 formulation: 89.4% conversion (35% EG, 35% CBH, 30% BG)"
            ),
            Task(
                id="BIO-006",
                name="Fermentation Trials",
                description="Batch ethanol fermentation experiments",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-04-01",
                end_date="2026-04-30",
                assigned_to="Research Team",
                dependencies=["BIO-005"],
                notes="TF-001+TF-006 co-culture: 10.8 g/L ethanol (24% improvement)"
            ),
            Task(
                id="BIO-007",
                name="Agricultural Waste Testing",
                description="Test hydrolysis on rice straw, bagasse, corn stover, coconut coir",
                status=ProjectStatus.COMPLETED,
                priority=Priority.MEDIUM,
                start_date="2026-05-01",
                end_date="2026-05-20",
                assigned_to="Research Team",
                dependencies=["BIO-006"],
                notes="Rice straw: 81.2% conversion (NaOH pretreatment, 48h)"
            ),
            Task(
                id="BIO-008",
                name="5L Bioreactor Validation",
                description="Scale up fermentation to 5L benchtop bioreactor",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-05-20",
                end_date="2026-06-05",
                assigned_to="Research Team",
                dependencies=["BIO-007"],
                notes="10.2 g/L ethanol with TF-001+TF-006 co-culture (96 h)"
            ),
            Task(
                id="BIO-009",
                name="Cost Analysis",
                description="Techno-economic analysis of scaled production",
                status=ProjectStatus.COMPLETED,
                priority=Priority.MEDIUM,
                start_date="2026-06-01",
                end_date="2026-06-15",
                assigned_to="Research Team",
                dependencies=["BIO-008"],
                notes="Enzyme: ₱4.20/L; ethanol breakeven at ₱23.23/L, 300,000 L/yr"
            ),
            Task(
                id="BIO-010",
                name="100L Pilot Scale-Up",
                description="Scale fermentation from 5L to 100L pilot bioreactor",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.CRITICAL,
                start_date="2026-07-01",
                end_date="2026-09-30",
                assigned_to="Research Team",
                dependencies=["BIO-008", "BIO-009"],
                notes="Target: Validate yield consistency at 10x scale"
            ),
            Task(
                id="BIO-011",
                name="Enzyme Purification & Immobilization",
                description="Purify and immobilize enzyme cocktail for reuse",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.HIGH,
                start_date="2026-08-01",
                end_date="2026-10-31",
                assigned_to="Research Team",
                dependencies=["BIO-005"],
                notes="Target: 5-cycle reuse with >80% activity retention"
            ),
            Task(
                id="BIO-012",
                name="Patent Filing",
                description="File patent applications for novel strains and process",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.HIGH,
                start_date="2026-10-01",
                end_date="2026-12-31",
                assigned_to="Legal Team",
                dependencies=["BIO-010"],
                notes="Priority: TF-001+Tf-006 co-culture method, C-5 cocktail formulation"
            )
        ]
        
        biofuel_milestones = [
            Milestone(
                id="BIO-M1",
                name="Strain Library Established",
                description="7 bacterial isolates identified and catalogued",
                due_date="2026-02-28",
                status=ProjectStatus.COMPLETED,
                tasks=["BIO-001", "BIO-002", "BIO-003"]
            ),
            Milestone(
                id="BIO-M2",
                name="Proof of Concept",
                description="10.8 g/L ethanol demonstrated in co-culture",
                due_date="2026-04-30",
                status=ProjectStatus.COMPLETED,
                tasks=["BIO-004", "BIO-005", "BIO-006"]
            ),
            Milestone(
                id="BIO-M3",
                name="Pilot Validation",
                description="5L bioreactor validated with agricultural waste",
                due_date="2026-06-05",
                status=ProjectStatus.COMPLETED,
                tasks=["BIO-007", "BIO-008"]
            ),
            Milestone(
                id="BIO-M4",
                name="Business Case Complete",
                description="Cost analysis confirms commercial viability",
                due_date="2026-06-15",
                status=ProjectStatus.COMPLETED,
                tasks=["BIO-009"]
            ),
            Milestone(
                id="BIO-M5",
                name="100L Pilot Scale Achieved",
                description="Successful scale-up to pilot production",
                due_date="2026-09-30",
                status=ProjectStatus.NOT_STARTED,
                tasks=["BIO-010"]
            ),
            Milestone(
                id="BIO-M6",
                name="IP Portfolio",
                description="Patent applications filed for core technologies",
                due_date="2026-12-31",
                status=ProjectStatus.NOT_STARTED,
                tasks=["BIO-011", "BIO-012"]
            )
        ]
        
        biofuel_project = Project(
            id="BIOFUEL-001",
            name="Biofuel Research Project",
            description="Develop biofuel production using termite-derived enzymes",
            status=ProjectStatus.IN_PROGRESS,
            start_date="2026-01-06",
            end_date="2028-06-01",
            budget=23000000,
            spent=8200000,
            tasks=biofuel_tasks,
            milestones=biofuel_milestones,
            notes="Phase 1 complete (Jan-Jun 2026): 7 strains isolated, 10.8 g/L ethanol, 89.4% conversion, cost validated at ₱23.23/L"
        )
        
        # Natural Pest Control Project
        pest_tasks = [
            Task(
                id="PEST-001",
                name="Neem Repellent Trial",
                description="Formulate and test neem oil repellent (Trial 1)",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-03-10",
                end_date="2026-03-15",
                assigned_to="Product Development",
                dependencies=[],
                notes="88% repellency against C. gestroi, 10L batch"
            ),
            Task(
                id="PEST-002",
                name="Essential Oil Blend Trial",
                description="Formulate and test clove-cinnamon-tea tree blend (Trial 2)",
                status=ProjectStatus.COMPLETED,
                priority=Priority.HIGH,
                start_date="2026-03-20",
                end_date="2026-03-25",
                assigned_to="Product Development",
                dependencies=[],
                notes="100% mortality at 250 µL/L, 5L batch"
            ),
            Task(
                id="PEST-003",
                name="Borate Bait Trial",
                description="Formulate and test borate bait granules (Trial 3)",
                status=ProjectStatus.COMPLETED,
                priority=Priority.MEDIUM,
                start_date="2026-04-01",
                end_date="2026-04-08",
                assigned_to="Product Development",
                dependencies=[],
                notes="92% mortality in 14-day feeding assay, 5 kg batch"
            ),
            Task(
                id="PEST-004",
                name="Nematode Suspension Trial",
                description="Test Steinernema carpocapsae suspension (Trial 4)",
                status=ProjectStatus.COMPLETED,
                priority=Priority.MEDIUM,
                start_date="2026-04-15",
                end_date="2026-04-22",
                assigned_to="Product Development",
                dependencies=[],
                notes="76% mortality in soil bioassay, 2L batch"
            ),
            Task(
                id="PEST-005",
                name="Field Trials",
                description="Conduct field efficacy trials in agricultural settings",
                status=ProjectStatus.IN_PROGRESS,
                priority=Priority.CRITICAL,
                start_date="2026-06-01",
                end_date="2026-08-31",
                assigned_to="Field Team",
                dependencies=["PEST-001", "PEST-002", "PEST-003", "PEST-004"],
                notes="Testing top 2 formulations at 3 trial sites"
            ),
            Task(
                id="PEST-006",
                name="FDA-DENR Certification",
                description="Obtain regulatory approvals for product launch",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.CRITICAL,
                start_date="2026-07-01",
                end_date="2026-12-31",
                assigned_to="Regulatory Affairs",
                dependencies=["PEST-005"],
                notes="FDA product registration + DENR pesticide permit"
            ),
            Task(
                id="PEST-007",
                name="Pilot Manufacturing",
                description="Set up small-scale manufacturing line",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.HIGH,
                start_date="2026-09-01",
                end_date="2026-11-30",
                assigned_to="Production Team",
                dependencies=["PEST-005"],
                notes="Target: 200 L/week capacity"
            )
        ]
        
        pest_milestones = [
            Milestone(
                id="PEST-M1",
                name="Formulations Tested",
                description="4 formulation trials completed with efficacy data",
                due_date="2026-04-30",
                status=ProjectStatus.COMPLETED,
                tasks=["PEST-001", "PEST-002", "PEST-003", "PEST-004"]
            ),
            Milestone(
                id="PEST-M2",
                name="Field Validated",
                description="Field trials confirm laboratory efficacy",
                due_date="2026-08-31",
                status=ProjectStatus.IN_PROGRESS,
                tasks=["PEST-005"]
            ),
            Milestone(
                id="PEST-M3",
                name="Regulatory Approved",
                description="FDA and DENR certifications obtained",
                due_date="2026-12-31",
                status=ProjectStatus.NOT_STARTED,
                tasks=["PEST-006"]
            )
        ]
        
        pest_project = Project(
            id="PEST-001",
            name="Natural Pest Control Project",
            description="Create eco-friendly termite control solutions",
            status=ProjectStatus.IN_PROGRESS,
            start_date="2026-03-10",
            end_date="2027-06-01",
            budget=3000000,
            spent=1800000,
            tasks=pest_tasks,
            milestones=pest_milestones,
            notes="4 formulations validated (88-100% efficacy). Essential oil blend shows 100% mortality at 250 µL/L."
        )
        
        # Termite Farming Project
        farm_tasks = [
            Task(
                id="FARM-001",
                name="Farm Design",
                description="Design farm layout based on Thailand model",
                status=ProjectStatus.IN_PROGRESS,
                priority=Priority.HIGH,
                start_date="2026-06-01",
                end_date="2026-07-31",
                assigned_to="Farm Manager",
                dependencies=[],
                notes="Studying Thailand's 742 sago palm weevil farms"
            ),
            Task(
                id="FARM-002",
                name="Construction",
                description="Build farm facilities and enclosures",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.HIGH,
                start_date="2026-08-01",
                end_date="2026-10-31",
                assigned_to="Construction Team",
                dependencies=["FARM-001"],
                notes="Phase 1: 5-acre initial plot"
            ),
            Task(
                id="FARM-003",
                name="Colony Establishment",
                description="Source and establish Macrotermes/Nasutitermes colonies",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.HIGH,
                start_date="2026-11-01",
                end_date="2027-01-31",
                assigned_to="Farm Manager",
                dependencies=["FARM-002"],
                notes="Target: 50+ colonies from Southern Luzon, Philippines region"
            ),
            Task(
                id="FARM-004",
                name="First Harvest",
                description="First commercial harvest for protein meal",
                status=ProjectStatus.NOT_STARTED,
                priority=Priority.MEDIUM,
                start_date="2027-02-01",
                end_date="2027-04-30",
                assigned_to="Farm Manager",
                dependencies=["FARM-003"],
                notes="Target: 50 kg processed product"
            )
        ]
        
        farm_milestones = [
            Milestone(
                id="FARM-M1",
                name="Farm Operational",
                description="Farm facilities completed and operational",
                due_date="2026-10-31",
                status=ProjectStatus.NOT_STARTED,
                tasks=["FARM-001", "FARM-002"]
            ),
            Milestone(
                id="FARM-M2",
                name="First Harvest",
                description="First commercial harvest for protein meal",
                due_date="2027-04-30",
                status=ProjectStatus.NOT_STARTED,
                tasks=["FARM-003", "FARM-004"]
            )
        ]
        
        farm_project = Project(
            id="FARM-001",
            name="Termite Farming Project",
            description="Establish commercial termite farming operations",
            status=ProjectStatus.IN_PROGRESS,
            start_date="2026-06-01",
            end_date="2027-06-01",
            budget=3200000,
            spent=300000,
            tasks=farm_tasks,
            milestones=farm_milestones,
            notes="Thailand production cost: ~3.4 USD/kg"
        )
        
        self.projects = {
            "BIOFUEL-001": biofuel_project,
            "PEST-001": pest_project,
            "FARM-001": farm_project
        }
        
        self.save_data()
        print("Default projects created successfully.")
    
    def get_project_summary(self, project_id: str) -> Dict:
        """Get summary of a specific project."""
        if project_id not in self.projects:
            return {"error": f"Project {project_id} not found"}
        
        project = self.projects[project_id]
        
        # Calculate task statistics
        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == ProjectStatus.COMPLETED)
        in_progress_tasks = sum(1 for task in project.tasks if task.status == ProjectStatus.IN_PROGRESS)
        
        # Calculate budget statistics
        budget_used_percent = (project.spent / project.budget * 100) if project.budget > 0 else 0
        
        # Calculate timeline
        start_date = datetime.strptime(project.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(project.end_date, "%Y-%m-%d")
        current_date = datetime.now()
        total_days = (end_date - start_date).days
        elapsed_days = (current_date - start_date).days
        timeline_percent = (elapsed_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "status": project.status.value,
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "completion_percent": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            },
            "budget": {
                "total": project.budget,
                "spent": project.spent,
                "remaining": project.budget - project.spent,
                "used_percent": budget_used_percent
            },
            "timeline": {
                "start_date": project.start_date,
                "end_date": project.end_date,
                "total_days": total_days,
                "elapsed_days": elapsed_days,
                "timeline_percent": timeline_percent
            },
            "milestones": len(project.milestones)
        }
    
    def get_all_projects_summary(self) -> List[Dict]:
        """Get summary of all projects."""
        summaries = []
        for project_id in self.projects:
            summaries.append(self.get_project_summary(project_id))
        return summaries
    
    def update_task_status(self, project_id: str, task_id: str, new_status: ProjectStatus):
        """Update status of a specific task."""
        if project_id not in self.projects:
            print(f"Project {project_id} not found")
            return False
        
        project = self.projects[project_id]
        for task in project.tasks:
            if task.id == task_id:
                task.status = new_status
                self.save_data()
                print(f"Task {task_id} status updated to {new_status.value}")
                return True
        
        print(f"Task {task_id} not found in project {project_id}")
        return False
    
    def add_task(self, project_id: str, task: Task):
        """Add a new task to a project."""
        if project_id not in self.projects:
            print(f"Project {project_id} not found")
            return False
        
        self.projects[project_id].tasks.append(task)
        self.save_data()
        print(f"Task {task.id} added to project {project_id}")
        return True
    
    def generate_report(self) -> str:
        """Generate a comprehensive project report."""
        report = []
        report.append("=" * 80)
        report.append("TERMITE RESEARCH PROJECTS - COMPREHENSIVE REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        for project_id, project in self.projects.items():
            summary = self.get_project_summary(project_id)
            
            report.append(f"\n{'='*80}")
            report.append(f"PROJECT: {project.name}")
            report.append(f"{'='*80}")
            report.append(f"Status: {summary['status']}")
            report.append(f"Timeline: {summary['timeline']['start_date']} to {summary['timeline']['end_date']}")
            report.append(f"Budget: ₱{summary['budget']['total']:,.2f}")
            report.append(f"Spent: ₱{summary['budget']['spent']:,.2f} ({summary['budget']['used_percent']:.1f}%)")
            
            report.append(f"\nTask Progress:")
            report.append(f"  Total: {summary['tasks']['total']}")
            report.append(f"  Completed: {summary['tasks']['completed']}")
            report.append(f"  In Progress: {summary['tasks']['in_progress']}")
            report.append(f"  Completion: {summary['tasks']['completion_percent']:.1f}%")
            
            report.append(f"\nTimeline Progress: {summary['timeline']['timeline_percent']:.1f}%")
            
            # List tasks
            report.append(f"\nTasks:")
            for task in project.tasks:
                report.append(f"  [{task.status.value}] {task.id}: {task.name}")
                if task.notes:
                    report.append(f"          Notes: {task.notes}")
        
        report.append(f"\n{'='*80}")
        report.append("END OF REPORT")
        report.append(f"{'='*80}")
        
        return "\n".join(report)
    
    def export_to_markdown(self, filename: str = "project_report.md"):
        """Export report to markdown file."""
        report = self.generate_report()
        
        # Convert to markdown format
        md_content = []
        md_content.append("# Termite Research Projects Report")
        md_content.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for project_id, project in self.projects.items():
            summary = self.get_project_summary(project_id)
            
            md_content.append(f"## {project.name}")
            md_content.append(f"\n**Status**: {summary['status']}")
            md_content.append(f"**Timeline**: {summary['timeline']['start_date']} to {summary['timeline']['end_date']}")
            md_content.append(f"**Budget**: ₱{summary['budget']['total']:,.2f}")
            md_content.append(f"**Spent**: ₱{summary['budget']['spent']:,.2f} ({summary['budget']['used_percent']:.1f}%)")
            
            md_content.append(f"\n### Task Progress")
            md_content.append(f"- Total: {summary['tasks']['total']}")
            md_content.append(f"- Completed: {summary['tasks']['completed']}")
            md_content.append(f"- In Progress: {summary['tasks']['in_progress']}")
            md_content.append(f"- Completion: {summary['tasks']['completion_percent']:.1f}%")
            
            md_content.append(f"\n### Tasks")
            for task in project.tasks:
                md_content.append(f"- [{task.status.value}] **{task.id}**: {task.name}")
                if task.notes:
                    md_content.append(f"  - Notes: {task.notes}")
            
            md_content.append(f"\n---\n")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("\n".join(md_content))
            print(f"Report exported to {filename}")
        except Exception as e:
            print(f"Error exporting report: {e}")


def main():
    """Main function to demonstrate the project tracker."""
    print("=" * 80)
    print("TERMITE RESEARCH PROJECT TRACKER")
    print("=" * 80)
    
    # Create project tracker instance
    tracker = ProjectTracker()
    
    # Generate and display report
    print("\nGenerating project report...")
    report = tracker.generate_report()
    print(report)
    
    # Export to markdown
    print("\nExporting report to markdown...")
    tracker.export_to_markdown("project_report.md")
    
    # Display summary of all projects
    print("\nProject Summaries:")
    summaries = tracker.get_all_projects_summary()
    for summary in summaries:
        print(f"\n{summary['project_name']}:")
        print(f"  Status: {summary['status']}")
        print(f"  Tasks: {summary['tasks']['completed']}/{summary['tasks']['total']}")
        print(f"  Budget: ₱{summary['budget']['spent']:,.2f}/{summary['budget']['total']:,.2f}")
        print(f"  Timeline: {summary['timeline']['timeline_percent']:.1f}%")
    
    print("\n" + "=" * 80)
    print("Project tracker initialized successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
