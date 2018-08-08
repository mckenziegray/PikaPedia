from flask import Flask, render_template, url_for, request
import os

app = Flask(__name__)

@app.route("/testpage")
def birthdays():
    dates = {"bulbasaur": 1, "ivysaur": 2, "venusaur": 3, "charmander": 4, "charmeleon": 5, "charizard": 6, "squirtle": 7, "wartortle": 8, "blastoise": 9}
    x = int(100)
    return render_template("testpage.html", dates=dates, x=x)

@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	return render_template('ProjectHomepage.html')

@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

@app.route('/results/', methods=['GET', 'POST'])
def results():
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')
	print("You searched for: " + query)
	firstName = ['Ben','Sarah', 'Xandar', 'Ellewyn']
	lastName = ['McCamish', 'G', 'Quazar', 'Sabbeth']
	return render_template('results.html', query=query, results=zip(firstName, lastName))

#Found at URL: http://flask.pocoo.org/snippets/40/
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)	

if __name__ == '__main__':
	app.run(debug=True)