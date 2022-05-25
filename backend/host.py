from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi.flask import Schema  # Relationship
from flask_rest_jsonapi import (Api, ResourceList, ResourceDetail)
# from flask_rest_jsonapi import (
# ResourceDetail, ResourceList, ResourceRelationship )
from marshmallow_jsonapi import fields
# from sqlalchemy import UniqueConstraint
import uuid
import os


# Create a new Flask application
app = Flask(__name__)


# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    info = db.Column(db.String)
    created_date = db.Column(db.Date)
    modified_date = db.Column(db.Date)
    creator = db.Column(db.String)
    status = db.Column(db.String)

    def __init__(self, title, info, created_date,
                 modified_date, creator, status):
        self.title = title
        self.info = info
        self.created_date = created_date
        self.modified_date = modified_date
        self.creator = creator
        self.status = status


# Create the table
db.create_all()


class TicketSchema(Schema):
    class Meta:
        type_ = 'ticket'
        self_view = 'ticket_single'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'ticket_many'

    id = fields.Integer()
    title = fields.Str(required=True)
    info = fields.Str(required=False)
    created_date = fields.Date(required=True)
    modified_date = fields.Date(required=False)
    creator = fields.Str(required=True)
    status = fields.Str(required=True)


class TicketMany(ResourceList):
    schema = TicketSchema
    data_layer = {'session': db.session,
                  'model': Ticket}


class TicketSingle(ResourceDetail):
    schema = TicketSchema
    data_layer = {'session': db.session,
                  'model': Ticket}


@app.route('/')
def get_uuid():
    """Return random UUID"""
    return str(uuid.uuid4())


api = Api(app)
api.route(TicketMany, 'ticket_many', '/api')
api.route(TicketSingle, 'ticket_single', '/api/<int:id>')


# main loop to run app in debug mode
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8080
    )
