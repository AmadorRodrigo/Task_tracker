
import sys
import json
import os
from datetime import datetime
from typing import Dict, List, Any


TASKS_FILE = "tasks.json"

def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks JSON archive"""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error to load tasks: {e}")
            return []
    return []

def save_tasks(tasks: List[Dict[str, Any]]) -> bool:
    """Save tasks in archive JSON"""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error to save tasks: {e}")
        return False

def get_next_id(tasks: List[Dict[str, Any]]) -> int:
    """Generate id available for new task"""
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

def add_task(description: str):
    """Add a new tasks"""
    tasks = load_tasks()
    new_task = {
        'id': get_next_id(tasks),
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(new_task)
    
    if save_tasks(tasks):
        print(f"Task added successfully (ID: {new_task['id']})")
    else:
        print("Erro to save task")

def update_task(task_id: int, description: str):
    """Update a task description"""
    tasks = load_tasks()
    task_id = int(task_id)
    
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = description
            task['updatedAt'] = datetime.now().isoformat()
            
            if save_tasks(tasks):
                print(f"Task {task_id} updated successfully")
            else:
                print("Erro to save task")
            return
    
    print(f"Task {task_id} not found")

def delete_task(task_id: int):
    """Delete a task by id"""
    tasks = load_tasks()
    task_id = int(task_id)
    
    initial_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < initial_count:
        if save_tasks(tasks):
            print(f"Task {task_id} deleted successfully")
        else:
            print("Erro to save task")
    else:
        print(f"Task {task_id} not found")

def mark_status(task_id: int, status: str):
    """Mark a task as in-progress or done"""
    if status not in ['in-progress', 'done']:
        print("Invalid status. Use 'in-progress' or 'done'")
        return
    
    tasks = load_tasks()
    task_id = int(task_id)
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            
            status_name = "in progress" if status == 'in-progress' else "done"
            if save_tasks(tasks):
                print(f"Task {task_id} marked as {status_name}")
            else:
                print("Erro to save task")
            return
    
    print(f"Task {task_id} not found")

def list_tasks(filter_status: str = None):
    """List tasks, optionally filtered by status (todo, in-progress, done)"""
    tasks = load_tasks()
    
    if filter_status:
        tasks = [task for task in tasks if task['status'] == filter_status]
    
    if not tasks:
        status_msg = f"No {filter_status or 'tasks'} found" if filter_status else "No tasks found"
        print(status_msg)
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<4} {'Status':<12} {'Description':<40} {'Created':<19} {'Updated':<19}")
    print("="*80)
    
    for task in tasks:
        status = task['status'].replace('-', ' ').title()
        created = task['createdAt'][:19]
        updated = task['updatedAt'][:19]
        print(f"{task['id']:<4} {status:<12} {task['description']:<40} {created:<19} {updated:<19}")
    
    print("="*80)
    print(f"Total: {len(tasks)} tasks\n")

def print_help():
    """Shows the help commands"""
    help_text = """
Task Tracker CLI - Task Manager

Available commands:

`task-cli add "Task Description"`

Adds a new task

`task-cli update ID "New Description"`

Updates the description of a task

`task-cli delete ID`

Removes a task

`task-cli mark-in-progress ID`

`task-cli mark-in-progress ID`

`task-cli mark-done ID`

`task-cli list`

Lists all tasks

`task-cli list todo`

Lists pending tasks

`task-cli list in-progress`

`task-cli list done`

`task-cli list done`

"""
    print(help_text)

def main():
    """Main function to process command line arguments and execute corresponding actions"""
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    try:
        if command == "add" and len(sys.argv) == 3:
            add_task(sys.argv[2])
        
        elif command == "update" and len(sys.argv) == 4:
            update_task(int(sys.argv[2]), sys.argv[3])
        
        elif command == "delete" and len(sys.argv) == 3:
            delete_task(int(sys.argv[2]))
        
        elif command == "mark-in-progress" and len(sys.argv) == 3:
            mark_status(int(sys.argv[2]), "in-progress")
        
        elif command == "mark-done" and len(sys.argv) == 3:
            mark_status(int(sys.argv[2]), "done")
        
        elif command == "list":
            filter_status = sys.argv[2] if len(sys.argv) > 2 else None
            if filter_status not in [None, 'todo', 'in-progress', 'done']:
                print("Invalid filter. Use 'todo', 'in-progress', or 'done'")
                return
            list_tasks(filter_status)
        
        else:
            print_help()
    
    except ValueError:
        print("Invalid input. Please check your command and try again.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()