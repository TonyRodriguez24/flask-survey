from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top_secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
toolbar = DebugToolbarExtension(app)



responses = []

@app.route("/")
def home():
   session.pop("responses", None)

   survey = surveys["satisfaction"]
   title = survey.title
   instructions = survey.instructions
   return render_template("home.html", title = title, instructions = instructions)

@app.route("/start-survey", methods = ["POST"])
def start_survey():
   # we initialize the response in the session
   session["responses"] = []
   #setting session equal to an empty array
   return redirect(url_for("questions", id = 0))


@app.route("/questions/<int:id>")
def questions(id):
   survey = surveys['satisfaction']
   responses = session.get("responses", [])

   if id != len(responses):
      flash("Trying to access invalid question", "error")
      return redirect(url_for("questions", id = len(responses)))
   
   if id >= len(survey.questions):
      return redirect(url_for("thank_you"))

   question = survey.questions[id]

   choices = survey.questions[id].choices
   return render_template("questions.html", question = question, choices = choices, id =id)

@app.route("/answer/<int:id>", methods = ["POST"])
def answers(id):
   answer = request.form.get("answer")

   next_question_id = id + 1

   responses = session.get("responses", [])
   responses.append(answer)

   session["responses"] = responses
   # for url_for first parameter passed should match the name of the function passed and any paramenters passed to it
   return redirect(url_for("questions", id = next_question_id))


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")