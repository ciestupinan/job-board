
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####################################################################
# Model definitions

class Company(db.Model):
    """Company on Job Board"""

    __tablename__ = "companies"

    company_name = db.Column(db.String(), nullable=False, primary_key=True)
    company_logo = db.Column(db.String(), nullable=True)

    def __repr__(self):

        return f"<Company name={self.name}>"


class Job(db.Model):
    """Job listing at a company"""

    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    job_title = db.Column(db.String(), nullable=False)
    company_name = db.Column(db.String, db.ForeignKey('companies.company_name'))
    job_description = db.Column(db.String(), nullable=False)
    job_location = db.Column(db.String(), nullable=False)
    job_link = db.Column(db.String(), nullable=False)

    company = db.relationship("Company",
                              backref=db.backref("jobs",
                                                order_by=company_name))

    def __repr__(self):

        return f"""<Job job_id={self.job_id} 
                   company_name={self.company_name} 
                   title={self.job_title}>"""


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jobs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
