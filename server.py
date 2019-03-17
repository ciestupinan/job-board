
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
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


@app.route('/search/<searchInput>',methods=['GET'])
def search():
	search_input = '%' + request.form["searchInput"] + '%'
	company_results = Job.query.filter_by(Job.commpany_name.like(search_input))
	job_title_results = Job.query.filter_by(Job.job_title.like(search_input))
	location_results = Job.query.filter_by(Job.job_location.like(search_input))

	return render_template("search_results.html",
							company_results=company_results,
							job_title_results=job_title_results,
							location_results=location_results)


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
