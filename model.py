
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


db = SQLAlchemy()
app = Flask(__name__)
ma = Marshmallow(app)


#####################################################################
# Model definitions

class Company(db.Model):
    """Company on Job Board"""

    __tablename__ = "companies"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    logo = db.Column(db.String(), nullable=False)


    def __init__(self, name, logo):
        self.name = name
        self.logo = logo
    
    def __repr__(self):
        return f"<Company name={self.name} id={self.id}>"



class CompanySchema(ma.Schema):
    class Meta:
        fields = ('name','logo')

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)






class Job(db.Model):
    """Job listing at a company"""

    __tablename__ = "jobs"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    description = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    link = db.Column(db.String(), nullable=False)

    company = db.relationship("Company",
                              backref=db.backref("jobs",
                              order_by=company_id))

    
    def __init__(self, title, company_id, company_name, description, location, link):
        self.title = title
        self.company_id = company_id
        self.description = description
        self.location = location
        self.link = link

    def __repr__(self):

        return f"""<Job id={self.id} 
                   company_id={self.company_id} 
                   title={self.title}>"""



class JobSchema(ma.Schema):
    class Meta:
        fields = ('title','company_id','description','location','link')


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    connect_to_db(app)
    print("Connected to DB.")
