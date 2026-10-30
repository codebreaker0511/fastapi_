from fastapi import FastAPI
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    title: str
    completed: bool

todos = []

app = FastAPI()

@app.get('/tasks')
def get_tasks():
    return {
        "todos": todos
    }

@app.get('/tasks/{task_id}')
def get_task(task_id:int):
    for index,todo in enumerate(todos):
        if todo.id == task_id:
            return todo

    return {
        "message": "Todo doesn't exist"
    }


@app.post('/tasks')
def post_task(todo: Todo):
    todos.append(todo)
    return {
        "message": "Todo added successfully"
    }

@app.put('/tasks/{task_id}')
def update_todo(task_id: int, updated_Todo: Todo):
    for index, todo in enumerate(todos):
        if task_id == todo.id:
            todos[index] = updated_Todo
            return {
                "message": "Todo updated successfully"
            }
    return {
        "message": "such a task_id doesn't exist"
    }


@app.delete('/tasks/{task_id}')
def delete_todo(task_id: int):
    for index,todo in enumerate(todos):
        if todo.id == task_id: 
            todos.pop(index)
            return {
                "message": "deleted successfully"
            }

    return {
        "message": "such a todo doesn't exist"
    }