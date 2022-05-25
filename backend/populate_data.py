import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from host import Ticket
from faker import Faker


fake = Faker()
DATABASE_URL = os.environ['DATABASE_URL']
buildSession = sessionmaker()
engine = create_engine(DATABASE_URL)
buildSession.configure(bind=engine)
session = buildSession()


def generate_data():
    title = fake.name()
    info = fake.text()
    created_date = fake.date()
    modified_date = fake.date()
    creator = fake.name()
    status = 'Open'

    return Ticket(title, info, created_date, modified_date, creator, status)


for i in range(0, 50):
    session.add(generate_data())

session.commit()
session.close()
