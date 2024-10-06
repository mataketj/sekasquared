from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/session')
def session():
    return render_template('session.html')


if __name__ == '__main__':
    app.run(debug=True)
