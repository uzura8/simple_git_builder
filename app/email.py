#from threading import Thread
import boto3
from flask import current_app, render_template
from flask_mail import Message
from app import mail
from app.common.file import put_to_file

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body='', html_body=''):
    if (current_app.config['MAIL_USE_SES']):
        send_email_on_local(subject, sender, recipients, text_body, html_body)
    else:
        send_email_on_ses(subject, sender, recipients, text_body, html_body)


def send_email_on_local(subject, sender, recipients, text_body='', html_body=''):
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


def send_email_on_ses(subject, sender, recipients, text_body='', html_body=''):
    msg = {
        'Subject': {
            'Data': subject,
            'Charset': 'UTF-8'
        },
        'Body': {}
    }

    if len(text_body) > 0:
        msg['Body']['Text'] =  {
            'Data': text_body,
            'Charset': 'UTF-8'
        }
    if len(html_body) > 0:
        msg['Body']['Html'] =  {
            'Data': html_body,
            'Charset': 'UTF-8'
        }

    client = boto3.client('ses')
    response = client.send_email(
        Source=sender,
        Destination={
            'ToAddresses': recipients
        },
        Message=msg,
        ReplyToAddresses=[sender]
    )
    return response


def send_contact_email(email_to, subject, inputs):
    admin_name = current_app.config['CONTACT_EMAIL_FROM_NAME']
    admin_email = current_app.config['FBD_ADMIN_MAIL']
    send_email(
        subject,
        sender=(admin_name, admin_email),
        recipients=[email_to, admin_email],
        text_body=render_template(
            'email/contact.txt',
            email_to=email_to,
            inputs=inputs,
            company_name=current_app.config['FBD_ADMIN_COMPANY_NAME'],
            company_site_url=current_app.config['FBD_ADMIN_COMPANY_SITE_URL'],
        )
    )


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
    put_to_file('var/logs/mail.log', data)
