from app import app, db
from app.models import User, Post, Resort, Conditions
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User': User, 'Post': Post,'Resort' : Resort, 'Conditions' : Conditions}
