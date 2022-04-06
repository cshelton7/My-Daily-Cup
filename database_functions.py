from models import db, Joes, Entry


def get_entries(user_id):
    entries = Entry.query.filter_by(user=user_id).all()
    return entries


def deleteEntry(entry_id):
    entry = Entry.query.filter_by(id=entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
