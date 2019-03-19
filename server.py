
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Company, Job, app, company_schema, companies_schema, jobs_schema, job_schema




# Required to use Flask sessions and the debug toolbar
app.secret_key = "kjhdsf8234"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    jobs = Job.query.all()
    return render_template("index.html", jobs=jobs)


@app.route('/results', methods=['POST'])
def search_results():
	form_input = request.form["search"]
	search = '%' + form_input + '%'

	company_results = Job.query.filter(Job.company_name.ilike(search))
	job_title_results = Job.query.filter(Job.job_title.ilike(search),~Job.company_name.ilike(search))
	location_results = Job.query.filter(Job.job_location.ilike(search),~Job.company_name.ilike(search),~Job.job_title.ilike(search))

	isNone = False 
	total_results = len(company_results.all()) + len(job_title_results.all()) + len(location_results.all())
	
	if total_results == 0:
		isNone = True
	
	return render_template("searchresults.html",
							company_results=company_results,
							job_title_results=job_title_results,
							location_results=location_results,
							isNone=isNone,
							total_results=total_results)




# endpoint to show all companies
@app.route('/company', methods=['GET'])
def get_companies():
	companies = Company.query.all()
	result = companies_schema.dump(companies)
	return jsonify(result.data)

# endpoint to show all jobs
@app.route('/jobs', methods=['GET'])
def get_jobs():

	result = db.session.query(Job.id, Company.name, Job.company_id, Job.title, Job.location, Job.description, Job.link).join(Company).all()
	
	return jobs_schema.jsonify(result)

# endpoint to show all jobs at company
@app.route('/company/<id>', methods=["GET"])
def get_jobs_at_company(id):
	result = Job.query.filter(Job.company_id == id).all()
	return jobs_schema.jsonify(result)

# endpoint to show all jobs in location
@app.route('/jobs/<location>', methods=["GET"])
def get_jobs_at_location(location):
	result = Job.query.filter(Job.location == location)
	return jobs_schema.jsonify(result)

# endpoint to show all jobs with keywords in title
@app.route('/jobs/<keywords>',methods=["GET"])
def get_jobs_with_keywords(keywords):
	result = Job.query.filter(Job.title.ilike(keywords))
	return jobs_schema.jsonify(result)



if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
