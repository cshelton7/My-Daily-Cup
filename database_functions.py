from models import db, Joes, Entry, Task
"""Functions to display and delete entries from user journals"""
from models import db, Joes, Entry


def get_entries(user_id):
    """Function to display entries from user's journal"""
    entries = Entry.query.filter_by(user=user_id).all()
    return entries


def deleteEntry(entry_id):
    """Function to delete entry from user journal"""
    entry = Entry.query.filter_by(id=entry_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()


def deleteTaskList(task_list_id):
    ''' function to delete task list from databse'''
    taskList = Task.query.filter_by(id=task_list_id).first()
    if taskList:
        db.session.delete(taskList)
        db.session.commit


def getTaskLists(user_id):
    '''function to get tasklists from database by user ID'''
    
    taskLists = Task.query.filter_By(user=user_id).all()
    return taskLists
