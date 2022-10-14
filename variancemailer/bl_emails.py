from flask import Blueprint, render_template
from .layoutUtils import *
from .auth import *
import jwt
import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

bp = Blueprint('bl_emails', __name__, url_prefix='/emailservice')

def get_data_from_token(token):
    
    jwt_secret = os.environ["JWT_MAILER_SECRET"]

    #data that should be in token
    user_email = ''
    user_aut_key = ''
    email_link_url = ''
    email_link_token = ''

    if token and len(token)>0:
         
        #TRY DECODE 
        try:
            decoded = jwt.decode(token, jwt_secret, algorithms=['HS256'])
            user_email=decoded["user_email"]
            user_aut_key=decoded["user_aut_key"]
            email_link_url=decoded["email_link_url"]
            email_link_token=decoded["email_link_token"]
        except jwt.DecodeError:
            pass
        
    return user_email, user_aut_key, email_link_url, email_link_token


def send_test_email():
    
    mailertogo_host     = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port     = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user     = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain   = os.environ.get('MAILERTOGO_DOMAIN', "variancedigital.com")

    
    # sender
    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])
    sender_name = os.environ.get('SENDER_NAME')

    # recipient
    recipient_email = "beethovenreview@gmail.com" # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
    recipient_name = ''

    # subject
    subject = 'Dobbiamo cambiare qualcosa?'

    # text body
    body_plain = ("Ciao Rinaldo,\n"
        "Spero proprio che  Beethoven Sources\n"
        "dia i frutti sperati... \n\n"
        "-Rinaldo Nani \n"
    )

    # html body
    line_break = '\n' #used to replace line breaks with html breaks
    body_html = f'''<html>
                   <head></head>
                    <body>
                   {'<br/>'.join(body_plain.split(line_break))}
                    </body>
                    </html>'''

    # create message container
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))

    # prepare plain and html message parts
    part1 = MIMEText(body_plain, 'plain')
    part2 = MIMEText(body_html, 'html')

    # attach parts to message
    message.attach(part1)
    message.attach(part2)

    # send the message.
    try:
        server = smtplib.SMTP(mailertogo_host, mailertogo_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mailertogo_user, mailertogo_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
    except Exception as e:
        return 2, str(e)
    
    return 0, "Ok"
    

def send_signup_email(user_email, user_aut_key,email_link_url, email_link_token):
    
    mailertogo_host     = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port     = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user     = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain   = os.environ.get('MAILERTOGO_DOMAIN')

    
    # sender
    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])
    sender_name = os.environ.get('SENDER_NAME')

    # recipient
    recipient_email = user_email # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
    recipient_name = 'CatLoader user'

    # subject
    subject = 'Confirm and access CatLoader'

    # text body
    body_plain = ("Hi there,\n"
        "please cut and paste link below to confirm your CatLoader registration!\n"
        + email_link_url + email_link_token + "\n\n"
        "To login, use your email with this access key:\n"
        + user_aut_key + "\n\n"
        "Enjoy!\n"
        "-" + sender_name + "\n"
    )

    # html body
    body_html = f'''<html>
                        <head></head>
                        <body>
                            <p>Hi there, </p>
                            <p>please click on the link below to confirm your <i>CatLoader</i> registration<br>
                            <a href="{email_link_url + email_link_token}"><b>Confirm email</b></a>
                            </p><br>
                            <p>To login, use your email along with this access key:<br>
                            {user_aut_key}
                            </p>
                            <p>Enjoy!</p>
                            <p>-{sender_name}</p>
                            <p>P.S: if the link above does not work, please copy this url<br>
                            {email_link_url + email_link_token}<br>
                            and paste it into your browser's serch bar (and press enter).
                            </p>
                        </body>
                    </html>'''

    # create message container
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))

    # prepare plain and html message parts
    part1 = MIMEText(body_plain, 'plain')
    part2 = MIMEText(body_html, 'html')

    # attach parts to message
    message.attach(part1)
    message.attach(part2)

    # send the message.
    try:
        server = smtplib.SMTP(mailertogo_host, mailertogo_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mailertogo_user, mailertogo_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
    except Exception as e:
        return 2, str(e)
    
    return 0, "Ok"


def send_change_email(user_email, user_aut_key,email_link_url, email_link_token):
    
    mailertogo_host     = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port     = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user     = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain   = os.environ.get('MAILERTOGO_DOMAIN')

    
    # sender
    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])
    sender_name = os.environ.get('SENDER_NAME')

    # recipient
    recipient_email = user_email # change to recipient email. Make sure to use a real email address in your tests to avoid hard bounces and protect your reputation as a sender.
    recipient_name = 'CatLoader user'

    # subject
    subject = 'Confirm changed email/login'

    # text body
    body_plain = ("Hi there,\n"
        "please cut and paste link below to confirm your CatLoader changed email!\n"
        + email_link_url + email_link_token + "\n\n"
        "To login, use your new email with this access key:\n"
        + user_aut_key + "\n\n"
        "Enjoy!\n"
        "-" + sender_name + "\n"
    )

    # html body
    body_html = f'''<html>
                        <head></head>
                        <body>
                            <p>Hi there, </p>
                            <p>please click on the link below to confirm your <i>CatLoader</i> changed email<br>
                            <a href="{email_link_url + email_link_token}"><b>Confirm email</b></a>
                            </p><br>
                            <p>To login, use your email along with this access key:<br>
                            {user_aut_key}
                            </p>
                            <p>Enjoy!</p>
                            <p>-{sender_name}</p>
                            <p>P.S: if the link above does not work, please copy this url<br>
                            {email_link_url + email_link_token}<br>
                            and paste it into your browser's serch bar (and press enter).
                            </p>
                        </body>
                    </html>'''

    # create message container
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))

    # prepare plain and html message parts
    part1 = MIMEText(body_plain, 'plain')
    part2 = MIMEText(body_html, 'html')

    # attach parts to message
    message.attach(part1)
    message.attach(part2)

    # send the message.
    try:
        server = smtplib.SMTP(mailertogo_host, mailertogo_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mailertogo_user, mailertogo_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
    except Exception as e:
        return 2, str(e)
    
    return 0, "Ok"


@bp.route('/testemail',methods=('GET', 'POST'))
def testemail():
    mc = set_menu("testemail")

    error, teststr = send_test_email()

    return render_template('emails/emailsent.html', mc=mc, teststr=teststr)


@bp.route('/sugnup/<incoming_token>')
def signupEmailservice(incoming_token):

    error =0 
    msg = "All ok"
    user_email, user_aut_key,  \
    email_link_url, email_link_token = get_data_from_token(incoming_token)

    if len(user_email)>0:
        error, msg = send_signup_email(user_email, user_aut_key,email_link_url, email_link_token)
    else:
        error = 1
        msg = "Problem with token"

    return { "error": error, "msg":msg }

@bp.route('/change/<incoming_token>')
def changeEmailservice(incoming_token):

    error =0 
    msg = "All ok"
    user_email, user_aut_key,  \
    email_link_url, email_link_token = get_data_from_token(incoming_token)

    if len(user_email)>0:
        error, msg = send_change_email(user_email, user_aut_key,email_link_url, email_link_token)
    else:
        error = 1
        msg = "Problem with token"

    return { "error": error, "msg":msg }
    