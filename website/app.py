import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
from flask_mail import Mail, Message

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key from the environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Set your Gmail email as an environment variable
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Set your Gmail password (or app-specific password) as an environment variable
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#create a form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name? for real", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SessionForm(FlaskForm):
    first_name = StringField("Your First Name", validators=[DataRequired()])
    last_name = StringField("Your Last Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    company_url = StringField("Company Website/URL", validators=[DataRequired()])
    company_size = IntegerField("Company Size", validators=[DataRequired()])
    comment = TextAreaField("Tell us about your Interests..", validators=[DataRequired()])

    submit = SubmitField("Submit")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# @app.route('/session', methods = ['GET', 'POST'])
# def session():
#     form = SessionForm()
#     #Validate Form
#     if form.validate_on_submit():
#         form.first_name.data = ''
#         form.last_name.data = ''
#         form.email.data = ''
#         form.company_name.data = ''
#         form.company_url.data = ''
#         form.company_size.data = ''
#         form.comment.data = ''
#     return render_template('session.html',
#                            form = form)

@app.route('/session', methods=['GET', 'POST'])
def session():
    form = SessionForm()
    if form.validate_on_submit():
        # Email content
        subject = f"New Session Request from {form.first_name.data} {form.last_name.data}"
        sender_email = form.email.data
        message_body = f"""
        First Name: {form.first_name.data}
        Last Name: {form.last_name.data}
        Email: {form.email.data}
        Company Name: {form.company_name.data}
        Company URL: {form.company_url.data}
        Company Size: {form.company_size.data}
        Comments: {form.comment.data}
        """

        # Sending the email
        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])  # Send to your own business email
        msg.body = message_body

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Error: {str(e)}', 'danger')

        # # Clear form data (optional)
        # form.first_name.data = ''
        # form.last_name.data = ''
        # form.email.data = ''
        # form.company_name.data = ''
        # form.company_url.data = ''
        # form.company_size.data = ''
        # form.comment.data = ''

        return redirect(url_for('session'))

    return render_template('session.html', form=form)

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#create name page
@app.route('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
    return render_template('name.html',
                           name = name,
                           form = form
                           )

if __name__ == '__main__':
    app.run()
