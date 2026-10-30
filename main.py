from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/about')
def about(): 
    return {
        "Hello, this is the about page"
    }


#@app.get('/users')
#def users(): 
#    return {
#        "users" : [
#            'amit', 'mohit', 'rahul'
#        ]
#    }

@app.get("/user/{user_id}")
def get_user(user_id:int):
    return {
        "user": user_id
    }


@app.get('/users')
def users(name: str = None):
    return {
        "user": name
    }

@app.post('/create_user')
def create_user(name:str, age:int):
    return {
        "name":name, 
        "age": age
    }
