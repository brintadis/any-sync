from flask_mail import Message, Mail

from webapp import create_app


app = create_app()
mail = Mail(app)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
