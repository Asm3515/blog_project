from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configure Flask Mail
app.config['MAIL_SERVER'] = os.environ.get('SMTP_HOST')
app.config['MAIL_PORT'] = int(os.environ.get('SMTP_PORT'))
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def send_email(mail_options):
    msg = Message(subject=mail_options['subject'],
                  sender=mail_options['from'],
                  recipients=mail_options['to'])
    msg.body = mail_options['text_body']
    msg.html = mail_options['html_body']

    with app.app_context():
        mail.send(msg)
        print(f"Message sent to {', '.join(mail_options['to'])}")

if __name__ == '__main__':
    app.run(debug=True)
