try:
    from flask import Flask

    from flask import Flask, request, render_template, redirect, url_for, session, send_file

    from flask_wtf import FlaskForm, RecaptchaField
    from wtforms import StringField, SubmitField, RadioField, DateTimeField, SelectField, TextAreaField

    from wtforms.validators import DataRequired

    from flask import session
    from spacy import displacy
    from flaskext.markdown import Markdown
    from arc_eager import Process
    import os

except Exception as e:
    print("Some Modules are Missing")

app = Flask(__name__)
Markdown(app)
app.config["SECRET_KEY"] = 'mysecretkey'


class Widgets(FlaskForm):

    Statement = StringField(label="STATEMENT")

    submit = SubmitField(label="Submit")


def foo(value):
    print("Work to be done")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    
@app.route("/", methods=["GET", "POST"])
def home():

    form = Widgets()
    if request.method == 'POST':
        if (form.validate_on_submit()):
            val = form.Statement.data
            print(val)
            session['data'] = val
            # return render_template('home.html', form=form)
            return redirect('/thanks')
    return render_template('home.html', form=form)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    val = session['data']
    txt, err = Process(val)
    txt = txt.split('\n')
    # newval = foo(val)
    ex = [{
        "words": [
            {"text": "This", "tag": "DT"},
            {"text": "is", "tag": "VBZ"},
            {"text": "a", "tag": "DT"},
            {"text": "sentence", "tag": "NN"}
        ],
        "arcs": [
            {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
            {"start": 2, "end": 3, "label": "det", "dir": "left"},
            {"start": 1, "end": 3, "label": "attr", "dir": "right"}
        ]
    }] 
    
    return render_template('thanks.html',user_image='/static/process.png',text=txt,show= not err)


if __name__ == "__main__":
    app.run(debug=True)
