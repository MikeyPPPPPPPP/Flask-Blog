from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date


def get_date():
	d = date.today()
	return d


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class posts(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    entry = db.Column(db.String(1000))
    date = db.Column(db.String(100))

    def __init__(self, entry, date):
        self.entry = entry
        self.date = date
        
@app.route("/")
def home():
	return render_template('home.html', values=posts.query.all())

@app.route("/add", methods=["POST", "GET"])
def addtoblog():
	if request.method == "POST":

		entry = request.form["Entry"]

		current_date = get_date()
		new_post = posts(entry.strip(), str(current_date))

		db.session.add(new_post)
		db.session.commit()

		return render_template('home.html', values=posts.query.all())
	else:
		return render_template('addtoblog.html')

	return render_template('addtoblog.html')

if __name__ == '__main__':
	db.create_all()
	app.run()
