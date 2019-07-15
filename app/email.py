#from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail
from app.common.file import put_to_file

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body='', html_body=''):
    if (current_app.config['IS_LOGGING_MAIL']):
        body = html_body if len(html_body) > 0 else text_body
        debug_email(subject, sender, recipients, body)
        return

    msg = Message(subject, sender=sender, recipients=recipients)

    if len(text_body) > 0:
        msg.body = text_body
    if len(html_body) > 0:
        msg.html = html_body

    mail.send(msg)
    #Thread(target=send_async_email, args=(current_app, msg)).start()
    #if (current_app.config['IS_LOGGING_MAIL']):
    #    debug_email(subject, sender, recipients, text_body)

def send_sample_email(email_to):
    send_email('[{}] Sample mail'.format(current_app.config['FBD_SITE_NAME']),
               sender=current_app.config['FBD_ADMIN_MAIL'],
               recipients=[email_to],
               text_body=render_template('email/sample.txt',
                                            email_to=email_to),
               html_body=render_template('email/sample.html',
                                            email_to=email_to))

def debug_email(subject, sender, recipients, body):
    data = '\n-----------------------------\n'
    data += 'to: {}\nfrom: {}\nsubject: {}\n'.format(', '.join(recipients),
                                                        sender, subject)
    data += '---------------\n'
    data += body
    data += '\n-----------------------------\n'
    put_to_file('logs/mail.log', data)
