from fastapi import FastAPI, HTTPException
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel
import json

import background.main
from background.tasks import TASKS
from background.models import Task

app = FastAPI()


@app.get('/up')
def up():
    return 'pong'


class CreateTaskRequest(BaseModel):
    task_name: str
    data: dict

@app.post('/tasks')
def create_task(req: CreateTaskRequest):
    if req.task_name not in TASKS:
        raise HTTPException(status_code=404, detail="task name not found")


    task = Task.get_or_none(
        actor_name=req.task_name,
        args=json.dumps({
            'args': [],
            'kwargs': req.data,
        }, ensure_ascii=False),
        status='successed',
    )

    if task:
        return { 'task_id': task.uuid }
    else:
        actor = TASKS[req.task_name]
        msg = actor.send(**req.data)
        return { 'task_id': msg.message_id }


@app.get('/tasks/{id}')
def get_task(id):
    task = Task.get_or_none(Task.uuid == id)
    if task == None:
        raise HTTPException(status_code=404, detail="task not found")

    res = model_to_dict(task)
    res.pop('id')

    return res
