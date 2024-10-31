import datetime
from peewee import DateTimeField, Model, TextField, AutoField
import uuid

from background.config import db


class Task(Model):
    id = AutoField()
    uuid = TextField(
        unique=True,
        default=uuid.uuid4(),
    )

    # pending, running, successed, failed, skipped
    status = TextField(default='pending')

    actor_name = TextField()
    args = TextField()
    results = TextField(null=True)
    extra = TextField(null=True)

    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db
        table_name = 'tasks'
        indexes = (
            (('actor_name', 'args', 'status'), False),
        )
