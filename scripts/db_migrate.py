from background.models import Task

def create():
    Task.create_table()
    print('migrated')
