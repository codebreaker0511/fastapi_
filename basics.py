prices = {"book": 100, "pen": 20, "bag": 800}

discounted = {
    item: price*0.9 for item,price in prices.items()
}

print(discounted)

todos = [
    {"id": 3, "title": "Study Python"},
    {"id": 1, "title": "Learn SQL"},
    {"id": 2, "title": "Build API"}
]

todo_sorted = sorted(todos, key = lambda todo: todo["id"])
print(todo_sorted)

#1
nums = [10, 15, 20, 25, 30, 35]
evn = [num for num in nums if num % 2 == 0]

#2
student = {
    "name": "Rahul",
    "age": 21,
    "branch": "CSE"
}

student["cgpa"] = 8.5
student["age"] = 22

print(student.get("name"))
print(student)

#3
todos = [
    {"id": 1, "title": "Python", "completed": True},
    {"id": 2, "title": "SQL", "completed": False},
    {"id": 3, "title": "FastAPI", "completed": False},
    {"id": 4, "title": "Git", "completed": True}
]

titles = [todo["title"] for todo in todos if todo["completed"]]
print(titles)

#4
for todo in todos:
    if todo.get("id") == 2: 
        todo["title"] = "PSQL"

print(todos)

numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

counts = {}
for num in numbers: 
    if num in counts: 
        counts[num] += 1

    else: 
        counts[num] = 1