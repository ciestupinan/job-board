
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
			company_name = f[0].strip('\n')
			job_title = f[1].strip('\n')
			company_logo = f[2].strip('\n')
			job_location = f[3].strip('\n')
			job_link = f[4].strip('\n')
			jd = f[6:]
			job_description = ('').join(jd).replace('\n','<br>')

			company_exists = db.session.query(db.exists().where(Company.company_name == company_name)).scalar()
			if not company_exists:

				company = Company(company_name=company_name,
								  company_logo=company_logo)

				db.session.add(company)
				db.session.commit()

			job = Job(job_title=job_title,
					  company_name=company_name,
					  job_description=job_description,
					  job_location=job_location,
					  job_link=job_link)

			db.session.add(job)

			db.session.commit()




def set_val_job_id():
    """Set value for the next job_id after seeding database"""

    # Get the Max job_id in the database
    result = db.session.query(func.max(Job.job_id)).one()
    max_id = int(result[0])

    # Set the value for the next job_id to be max_id + 1
    query = "SELECT setval('jobs_job_id_seq', :new_id)"
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


	set_val_job_id()

