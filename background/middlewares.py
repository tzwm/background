from dramatiq import Middleware
import json
from datetime import datetime

from dramatiq.middleware import SkipMessage

from background.models import Task


class Logger(Middleware):

    def before_process_message(self, broker, message):
        args = {
            'args': message.args,
            'kwargs': message.kwargs,
        }
        task, is_new = Task.get_or_create(
            actor_name=message.actor_name,
            args=json.dumps(args, ensure_ascii=False),
            defaults={
                'uuid': message.message_id,
                'status': 'running',
            },
        )
        if not is_new and task.status == 'successed':
            Task.create(
                uuid=message.message_id,
                status='skipped',
                actor_name=message.actor_name,
                args=json.dumps(args, ensure_ascii=False),
                extra=json.dumps({ 'skipped_by': task.uuid }, ensure_ascii=False),
                results=task.results,
            )
            print(f"[{message.message_id}] skipped")
            raise SkipMessage("[{message.message_id}] skipped")

        print(f"[{message.message_id}] is processing")


    def after_process_message(self, broker, message, *, result=None, exception=None):
        status = 'successed'

        if exception is not None:
            status = 'failed'
            result = str(exception)

        (Task
         .update(
            status=status,
            results=json.dumps(result, ensure_ascii=False),
            updated_at=datetime.now())
         .where(Task.uuid == message.message_id)
         .execute())

        print(f"[{message.message_id}] is done")
