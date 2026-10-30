from fastapi import FastAPI
from pydantic import BaseModel

projects = []
tasks = []

nxt_id = 0
tsk_id = 0

class Project(BaseModel):
    id: int = nxt_id
    name: str = ""
    description: str = ""
    owner: str = ""


class Task(BaseModel):
    id: int = tsk_id
    project_id: int = nxt_id
    title: str
    completed: bool
    priority: str

app = FastAPI()

#1st api endpoint
@app.post('/projects')
def create_project(project: Project):
    nxt_id += 1
    if project.name.strip() == "" or project.owner.strip() == "":
        return {
            "error": "Name / Owner can't be left blank"
        }
    return {
        "message": "Project Created Successfully",
        "project": project
    }

#2nd api endpoint
@app.get('/projects')
def get_projects(owner_name:str=""):
    pass


#3rd api endpoint
@app.get('/projects/{projects_id}')
def get_specific_project(project_id:int):
    for project in projects: 
        if project["id"] == project_id:
            return project

    return {
        "status_code": 404,
        "error": "Such a project doesn't exist"
    }

#4th api endpoint
@app.put('/projects/{project_id}')
def update_project(project_id: int, updated_project: Project):
    for index, project in projects: 
        if(project["id"] == project_id):
            projects[index] = updated_project
            return {
                "message": "Project Updated Successfully"
            }
    return {
        "error": "Such a project doesn't exist."
    }

#5th api endpoint
@app.delete('/projects/{project_id}')
def delete_project(project_id: int):
    for index, project in projects:
        if(project['id'] == project_id):
            #Pop any task related to this project
            for index, task in tasks:
                if task.project_id == project['id']:
                    tasks.pop(index)
            #Project deleted
            projects.pop(index)
            return {
                "message": "Project deleted successfully"
            }

    return {
        "error" : "Project doesn't exist"
    }


#6th api endpoint
@app.post('/projects/{project_id}/tasks')
def create_task(project_id: int, task: Task):
    for project in projects: 
        if project["id"] == project_id: 
            tasks.append(task)
            tsk_id += 1
            return {
                "message": "Task appended successfully"
            }

    return {
        "error": "Project with this project_id doesn't exist"
    }

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