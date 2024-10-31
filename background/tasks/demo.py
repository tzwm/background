import dramatiq

@dramatiq.actor(max_retries=3, time_limit=10*60*1000)
def hi(text: str):
    ret = 'hi ' + text
    print(ret)

    return ret
