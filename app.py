from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import db, URL
from flask_mail import Mail, Message
from flask_restful import Api, Resource
from crawler import crawl_url
from ocr import ocr_image

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'
mail = Mail(app)

# Configure Flask-RESTful API
api = Api(app)

@app.route('/')
def index():
    return 'Welcome to the Demo Project!'

@app.route('/crawl')
def crawl():
    url = request.args.get('url')
    html_content = crawl_url(url)
    if html_content:
        return html_content
    else:
        return 'Failed to crawl URL'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return 'No image file uploaded'
    image = request.files['image']
    ocr_text = ocr_image(image)
    if ocr_text:
        return ocr_text
    else:
        return 'Failed to perform OCR'

@app.route('/add_url', methods=['POST'])
def add_url():
    url = request.form.get('url')
    hash_value = request.form.get('hash_value')
    new_url = URL(url=url, hash_value=hash_value)
    db.session.add(new_url)
    db.session.commit()
    return 'URL added successfully'

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form.get('recipient')
    subject = request.form.get('subject')
    body = request.form.get('body')
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
    return 'Email sent successfully'

class URLs(Resource):
    def get(self):
        # Retrieve URLs from database and return as JSON
        return {'urls': [{'url': url.url, 'hash_value': url.hash_value} for url in URL.query.all()]}

api.add_resource(URLs, '/urls')

if __name__ == '__main__':
    app.run(debug=True)
