from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

# CKEditor
ckeditor = CKEditor(app)

# Bootstrap
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    ## Geting all posts from db

    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>", methods=["GET"])
def show_post(index):
    ##TODO: "posts = db.session.query(BlogPost).all()" - 2times ;/
    posts = db.session.query(BlogPost).all()
    requested_post = None

    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post

    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["POST", "GET"])
def new_post():
    form = CreatePostForm()
    if request.method == 'POST' and form.validate_on_submit():
        body = request.form.get('body')

        data_now = datetime.now().strftime("%B %d, %Y")

        new_entry = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=data_now,
            body=body,
            author=form.author.data,
            img_url=form.img_url.data
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect("/")

    edit = False

    return render_template("make-post.html", form=form, edit=edit)


@app.route("/edit_post/<post_id>", methods=["POST", "GET"])
def edit_post(post_id):
    edit = True

    post = db.session.query(BlogPost).get(post_id)
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    if request.method == "POST" and form.validate_on_submit():
        body = request.form.get('body')
        data_now = datetime.now().strftime("%B %d, %Y")

        edit_entry = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=data_now,
            body=body,
            author=form.author.data,
            img_url=form.img_url.data
        )
        db.session.uo
        db.session.add(edit_entry)
        db.session.commit()

    return render_template("make-post.html", form=form, edit=edit)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
