# The Muse Coding Challenge #
#### 19 March 2019 ####

![gif](https://media.giphy.com/media/2njsPW20xdovXTpcNu/giphy.gif)

## Prompt ##

Build a web app that allows users to learn information about a job and links them to be able to apply when they’re interested.
 

* Ensure you that it contains at least the following fields:
	* Company name
	* Company logo
	* Location
	* Job title
	* Job description
	* Link to apply
* Create APIs to pull data from the database
* Web frontend should call the appropriate APIs to get the proper data for a given job and display it to a user



* There is no specific design to develop towards - just create something you find clean and attractive that you would like to use. Feel free to take inspiration from design elements within the Muse or, if you prefer, to show off if this is an area in which you shine
* You’re welcome to use whatever technologies with which you feel most comfortable showing off your best work. If you’re curious what we work most with, our standard stack is Python/Django, React, and Postgres
* You may also include other information, 3rd party embeds (i.e. Twitter feed, Facebook timeline, YouTube video), etc. you think would be useful and relevant to the user. Feel free to experiment and show off

## How to Run ##

These are instructions assuming you have Python3 installed on your machine. It is recommended that you use Google Chrome as your browser.
1. Create virtualenv

```$ virtualenv env```

2. Install requirements

```$ pip3 install -r requirements.txt```

3. Create jobs database and seed it with seed data provided

```$ createdb jobs
$ python3 model.py
$ python3 seed.py
```

4. Run server.py. In the terminal, it will tell you the address where the server is running. Visit that address in a browser. I recommend using incognito mode with Google Chrome.

```$ python3 server.py```

## Resources ##
Bootstrap theme https://bootswatch.com/