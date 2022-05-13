#!/usr/bin/env python3
import os
import datetime

import flask
import flask_admin
import flask_admin.contrib.sqla
import flask_sqlalchemy

ERROR_HTML = '<h1 style="text-align:center">{}</h1><h3 style="max-width:1200px; margin:auto; text-align:center">{}</h3>'
ENV_KEYS = ['AZURE_SQL_USER', 'AZURE_SQL_PASSWORD', 'AZURE_SQL_SERVER', 'AZURE_SQL_PORT', 'AZURE_SQL_DATABASE']

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://{}:{}@{}:{}/{}".format(*[os.getenv(key) for key in ENV_KEYS])
app.secret_key = b'test'
db = flask_sqlalchemy.SQLAlchemy(app)
try:
    db.create_all()
except:
    pass

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255))
    modified_date = db.Column(db.DateTime, nullable = False, default = datetime.datetime.utcnow)

admin = flask_admin.Admin(app)
admin.add_view(flask_admin.contrib.sqla.ModelView(Todo, db.session))

@app.route('/')
def index():
    for key in ENV_KEYS:
        if not os.getenv(key):
            return ERROR_HTML.format('Invalid Arguments', 'Unable to get environment variable of "{}"'.format(key)), 400
    try:
        db.create_all()
    except Exception as e:
        return ERROR_HTML.format('Connection Failure', e), 400
    return flask.redirect('admin/', 302)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
