from models import db, Joes, Entry, Task


def get_entries(user_id):
    entries = Entry.query.filter_by(user=user_id).all()
    return entries


def deleteEntry(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()

def deleteTaskList(task_list_id):
    taskList = Task.query.filter_by(id=task_list_id).first()
    if taskList:
        db.session.delete(taskList)
        db.session.commit
        

