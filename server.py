
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Company, Job


app = Flask(__name__)

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
	job_title_results = Job.query.filter(Job.job_title.ilike(search))
	location_results = Job.query.filter(Job.job_location.ilike(search))

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


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
