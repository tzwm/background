import time

import httpx

from background.models import Task


def get_result(message_id: str, timeout: int = 60) -> Task | None:
    attempt_sec = 0
    t: Task = Task.get_or_none(Task.uuid == message_id)
    while attempt_sec < timeout:
        if t and t.status in ['successed', 'failed']:
            return t

        attempt_sec += 1
        t = Task.get_or_none(Task.uuid == message_id)

        time.sleep(0.5)

    if t is None:
        raise Exception(f"[{message_id}] task is not found in get_result")
    else:
        raise Exception(f"[{message_id}] task is running timeout")


async def dify_completion_messages(api_key: str, inputs: dict):
    DIFY_BASE_URL = 'https://dify.ai2cc.com/v1/completion-messages'

    data = {
      'user': 'background',
      'response_mode': 'blocking',
      'inputs': inputs,
    }
    res = await httpx.AsyncClient().post(
        url=DIFY_BASE_URL,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {api_key}",
        },
        json=data,
        timeout=120,
    )

    return res.json()['answer']
