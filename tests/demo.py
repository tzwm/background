from background.tasks import TASKS

def run():
    msg = TASKS['demo'].send('tzwm')

    print(msg.message_id)


    # (TASKS['bilibili_download_video']
    #  .send(url='https://www.bilibili.com/video/BV1XuxYeKEgT'))
