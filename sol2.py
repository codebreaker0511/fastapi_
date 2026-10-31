from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

projects = []
tasks = []

nxt_id = 1
tsk_id = 1

class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    owner: str

class Project(BaseModel):
    id: int
    name: str
    description: str
    owner: str


class taskData(BaseModel):
    title: str
    completed: bool = False
    priority: str = "medium"

class Task(BaseModel):
    id: int
    project_id: int
    title: str
    completed: bool
    priority: str

app = FastAPI()

#1st api endpoint
@app.post('/projects')
def create_project(project_data: ProjectCreate):
    global nxt_id
    if not project_data.name.strip() or not project_data.owner.strip():
        raise HTTPException(
            status_code=400,
            detail="Name and owner can't be left blank"
        )
    project = Project(
        id = nxt_id,
        name = project_data.name, 
        description=project_data.description,
        owner = project_data.owner
    )
    projects.append(project)
    nxt_id += 1
    return {
        "message": "Project Created Successfully",
        "project": project
    }

#2nd api endpoint
@app.get('/projects')
def get_projects(owner_name:str="", search: str = ""):
    retrieved_projects = []
    for project in projects: 
        owner_matches = (
            not owner_name or owner_name.lower() == project.owner.lower()
        )
        search_matches = (
            not search or search.lower() in project.name.lower()
        )

        if owner_matches and search_matches:
            retrieved_projects.append(project)

    return retrieved_projects
    

#3rd api endpoint
@app.get('/projects/{project_id}')
def get_specific_project(project_id:int):
    for project in projects: 
        if project.id == project_id:
            return project

    raise HTTPException(
        status_code=404,
        detail="Project doesn't exist"
    )

#4th api endpoint
@app.put('/projects/{project_id}')
def update_project(project_id:int, updated_Project: ProjectCreate):
    for index, project in enumerate(projects):
        if project.id == project_id:
            if not updated_Project.name.strip() or not updated_Project.owner.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Name and owner can't be blank"
                )
            updated_project = Project(
                id = project.id,
                name = updated_Project.name,
                description=updated_Project.description,
                owner = updated_Project.owner
            )
            projects[index] = updated_project
            return {
                "message": "Project updated successfully",
                "data": updated_project
            }
    raise HTTPException(
        status_code=404,
        detail="Project_id is invalid"
    )


#5th api endpoint
@app.delete('/projects/{project_id}')
def delete_project(project_id: int):
    for index, project in enumerate(projects):
        if(project.id == project_id):
            projects.pop(index)
            tasks[:] = [task for task in tasks if task.project_id != project_id]
            return {
                "message": "Project deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail='Project_id is invalid'
    )


#6th api endpoint
@app.post('/projects/{project_id}/tasks')
def create_task(project_id: int, task: taskData):
    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="title can't be valid"
        )
    global tsk_id
    for project in projects:
        if project.id == project_id:
            tsk_data = Task(
                id= tsk_id,
                project_id=project.id,
                title=task.title,
                completed=task.completed,
                priority=task.priority
            )
            tsk_id += 1
            tasks.append(tsk_data)
            return {
                "message": "Task added successfully",
                "task created": tsk_data
            }

    raise HTTPException(
        status_code=404,
        detail="Project_id is invalid"
    )

#7th api endpoint
@app.get('/projects/{project_id}/tasks')
def get_tasks(project_id: int, completed:bool=None, priority: str=None, limit: int = 10, offset:int = 0):
    task_retrieved = []
    for project in projects: 
        if project.id == project_id:
            task_retrieved = [task for task in tasks if project.id == task.project_id ]
            filtered_task = []

            for tsk in task_retrieved: 
                is_completed = (
                    completed is None or tsk.completed == completed
                )
                have_priority = (
                    not priority or priority.lower() == tsk.priority.lower()
                )
                if is_completed and have_priority:
                    filtered_task.append(tsk)

            return filtered_task[offset: offset+limit]
  
    raise HTTPException(
        status_code=404,
        detail="Project doesn't exist"
    )

#8th api endpoint
@app.get('/tasks/{task_id}')
def get_tasks(task_id:int):
    for task in tasks: 
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code= 404,
        detail="Task not found"
    )

#9th api endpoint
@app.put('/tasks/{task_id}')
def update_task(task_id: int, updated_tsk: taskData):
    if not updated_tsk.title.strip().lower():
        raise HTTPException(
            status_code=400,
            detail="Title can't be left blank"
        )

    for index, task in enumerate(tasks): 
        if task.id == task_id:
            new_tsk = Task(
                id=task.id,
                project_id=task.project_id,
                title=updated_tsk.title,
                completed=updated_tsk.completed,
                priority=updated_tsk.priority
            )
            tasks[index] = new_tsk
            return {
                "message": "Task updated successfully"
            }
        

    raise HTTPException(
        status_code=404,
        detail="Task doesn't exist"
    )
    

#10th api endpoint
@app.delete('/tasks/{task_id}')
def del_task(task_id: int):
    for index, task in enumerate(tasks): 
        if task.id == task_id: 
            tasks.pop(index)
            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException (
        status_code=404,
        detail="Task doesn't exist"
    )