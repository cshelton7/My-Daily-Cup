# pylint: disable=no-member
"""Functions to display and delete entries from user journals"""
from models import db, Entry


def get_entries(user_id):
    """Function to display entries from user's journal"""
    entries = Entry.query.filter_by(user=user_id).all()
    return entries


def delete_Entry(entry_id):
    """Function to delete entry from user journal"""
    entry = Entry.query.filter_by(id=entry_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
