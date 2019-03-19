
import datetime
from sqlalchemy import func

from model import Company, Job, connect_to_db, db
from server import app


def load_data(file_list):
	Company.query.delete()
	Job.query.delete()

	for job_file in file_list:
		with open(job_file) as file:
			f = file.readlines()
			name = f[0].strip('\n')
			job_title = f[1].strip('\n')
			logo = f[2].strip('\n')
			job_location = f[3].strip('\n')
			job_link = f[4].strip('\n')
			jd = f[6:]
			job_description = ('').join(jd).replace('\n','<br>')

			company_exists = db.session.query(db.exists().where(Company.name == name)).scalar()
			if not company_exists:

				company = Company(name=name, logo=logo)

				db.session.add(company)
				db.session.commit()

			company_id = db.session.query(Company.id).filter(Company.name == name)

			job = Job(title=job_title,
					  company_id=company_id,
					  description=job_description,
					  location=job_location,
					  link=job_link)

			db.session.add(job)

			db.session.commit()



def set_val_company_id():
    """Set value for the next company id after seeding database"""

    # Get the Max company id in the database
    result = db.session.query(func.max(Company.id)).one()
    max_id = int(result[0])

    # Set the value for the next company id to be max_id + 1
    query = "SELECT setval('companies_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_job_id():
    """Set value for the next job id after seeding database"""

    # Get the Max job id in the database
    result = db.session.query(func.max(Job.id)).one()
    max_id = int(result[0])

    # Set the value for the next job id to be max_id + 1
    query = "SELECT setval('jobs_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
	connect_to_db(app)
	db.create_all()
	load_data(["seed_data/Nike  - Senior Director, Product Marketing, SNKRS.txt",
		"seed_data/Outdoor Voices - Front End Engineer.txt",
		"seed_data/Outdoor Voices - Payroll Specialist.txt",
		"seed_data/Wall Street Journal - iOS Software Engineer.txt",
		"seed_data/Wayfair - Product Manager, Mobile Apps.txt"])

	set_val_company_id()
	set_val_job_id()

