from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

projects = []
tasks = []

nxt_id = 1


class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    owner: str

class Project(BaseModel):
    id: int
    name: str
    description: str
    owner: str


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

tsk_id = 1

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
def get_tasks(project_id: int):
    for project in projects: 
        if project['id'] == project_id:
            pass


@app.put('/tasks/{task_id}')
def update_task(task_id: int):
    pass


@app.get('/tasks/{task_id}')
def get_tasks(task_id):
    pass


@app.delete('/tasks/{task_id}')
def del_task(task_id: int):
    pass