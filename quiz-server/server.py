from flask import Flask
from flask import render_template, redirect, url_for
from flask import request, session
import pythonquiz as quiz
quiz.load_quiz() # load the database to be available to users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard-to-guess-string'

@app.route ("/")
def root():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    print("ROUTE /login")
    reply = request.query_string.decode()
    print("query_string...", reply)
    if reply:
        name = reply.replace("name=","")
        name = request.args.get("name")
        print("name", name)
        session["user_name"] = name
        print("session is...", session)
        return redirect(url_for("start") ) ### ( 2 ) ###
    else:
        return render_template("login.html") ### ( 1 ) ###

@app.route("/start")
def start():
    print("ROUTE /start")
    name = session.get("user_name", None)
    if request.query_string: # ο χρήστης έχει πατήσει "Εναρξη"
        questions = quiz.draw_questions()
        print(questions)
        new_question = questions.pop()
        session["questions"] = questions
        session["score"] = 0
        session["count"] = 0
        return redirect(url_for("question", id = new_question)) ### ( 3 ) ### send first question
    else:
        return render_template("start.html", button= "Έναρξη", 
            name=name, history=quiz.player_history(name)) ###( 2 ) ###

@app.route("/end")
def end():
    print("ROUTE /end")
    name = session.get("user_name", None)
    score = session.get("score", None)
    return render_template("end.html", button="Νέα προσπάθεια", \
        score = "{:.2f}".format(score), name=name, history=quiz.player_history(name))
        ###### ( 6 ) ######

@app.route('/q/<id>')
def question(id):
    print("ROUTE /quiz", id)
    # ανάκτησε από το session την κατάσταση...
    name = session.get("user_name", None)
    score = session.get("score", 0)
    count = session.get("count",0)
    questions = session.get("questions", [])
    if id == "end":
        session["user_name"] = name
        quiz.save_game(name, score)
        return redirect(url_for("end")) ##### ( 5 ) #####

    q = quiz.show_question(id)
    print(name, questions, score, q)

    if request.query_string: # ο χρήστης απάντησε
        reply = request.args.get("answer")
        new_score = quiz.question_score(id, reply)
        score += new_score
        print('score is...', new_score)
        if new_score == 1: feedback = "Σωστή απάντηση"
        else: feedback = "Προσοχή! Η σωστή απάντηση είναι η {}".format(q["correct"])
        if questions: 
            next_question = questions.pop()
        else: next_question = "end"
        session["user_name"] = name
        session["score"] = score
        session["questions"] = questions
        ## να δώσουμε ανάδραση για την απάντηση και σκορ
        return render_template('question.html', question = q["question"], \
            id = id, user_name=name, replies = q["replies"],
            feedback = feedback, next_question = next_question, button="Επόμενη",
            disabled = "disabled") ####### ( 4 ) ########

    else: # πρέπει να στείλουμε στον χρήστη την ερώτηση
        session["user_name"] = name
        session["score"] = score
        session["questions"] = questions
        session["count"] = count + 1
        return render_template('question.html', question = q["question"], \
            id = id, user_name=name, replies = q["replies"], button="Υποβολή")
            ##### ( 3 ) ########

if __name__ == "__main__":
    app.run(debug=True)