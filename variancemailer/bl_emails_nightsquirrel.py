from flask import Blueprint, render_template                                                                                                          
from .layoutUtils import *                                                                                                                          
from .auth import *                                                                                                                                   
import jwt                                                                                                                                            
import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

bp = Blueprint('bl_emails_nightsquirrel', __name__, url_prefix='/emailservice-ntsqr')


# ── Shared SMTP send logic ──────────────────────────────────────

def _send_email(recipient_email, recipient_name, subject, body_plain, body_html):
    """Single place for all SMTP send logic."""
    mailertogo_host     = os.environ.get('MAILERTOGO_SMTP_HOST')
    mailertogo_port     = os.environ.get('MAILERTOGO_SMTP_PORT', 587)
    mailertogo_user     = os.environ.get('MAILERTOGO_SMTP_USER')
    mailertogo_password = os.environ.get('MAILERTOGO_SMTP_PASSWORD')
    mailertogo_domain   = os.environ.get('MAILERTOGO_DOMAIN')

    sender_user = 'noreply'
    sender_email = "@".join([sender_user, mailertogo_domain])
    sender_name = os.environ.get('SENDER_NAME')

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['To'] = email.utils.formataddr((recipient_name, recipient_email))
    message.attach(MIMEText(body_plain, 'plain'))
    message.attach(MIMEText(body_html, 'html'))

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


# ── Auth email senders ───────────────────────────────────────────

def send_signup_email(user_email, user_aut_key, email_link_url, email_link_token):
    sender_name = os.environ.get('SENDER_NAME')

    subject = 'Confirm and access Night Squirrel'

    body_plain = ("Hi there,\n"
        "please cut and paste link below to confirm your Night Squirrel registration!\n"
        + email_link_url + email_link_token + "\n\n"
        "To login, use your email with this access key:\n"
        + user_aut_key + "\n\n"
        "Enjoy!\n"
        "-" + sender_name + "\n"
    )

    body_html = f'''<html>
                        <head></head>
                        <body>
                            <p>Hi there, </p>
                            <p>please click on the link below to confirm your <i>Night Squirrel</i> registration<br>
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

    return _send_email(user_email, 'Night Squirrel User', subject, body_plain, body_html)


def send_change_email(user_email, user_aut_key, email_link_url, email_link_token):
    sender_name = os.environ.get('SENDER_NAME')

    subject = 'Confirm changed email/login'

    body_plain = ("Hi there,\n"
        "please cut and paste link below to confirm your Night Squirrel changed email!\n"
        + email_link_url + email_link_token + "\n\n"
        "To login, use your new email with this access key:\n"
        + user_aut_key + "\n\n"
        "Enjoy!\n"
        "-" + sender_name + "\n"
    )

    body_html = f'''<html>
                        <head></head>
                        <body>
                            <p>Hi there, </p>
                            <p>please click on the link below to confirm your <i>Night Squirrel</i> changed email<br>
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

    return _send_email(user_email, 'Night Squirrel User', subject, body_plain, body_html)


def send_reset_email(user_email, user_otp):
    sender_name = os.environ.get('SENDER_NAME')

    subject = 'Reset access key for Night Squirrel'

    body_plain = ("Hi there,\n"
        "you asked to reset your lost access key!\n"
        "(If it was not you, forget about this email)\n\n"
        "To set a new access key, use the OTP code below:\n"
        + user_otp + "\n\n"
        "Enjoy!\n"
        "-" + sender_name + "\n"
    )

    body_html = f'''<html>
                        <head></head>
                        <body>
                            <p>Hi there, </p>
                            <p>you asked to reset your lost access key!<br>
                            (If it was not you, forget about this email)
                            </p><br>
                            <p>To set a new access key, use the OTP code below:<br>
                            {user_otp}
                            </p>
                            <p>Enjoy!</p>
                            <p>-{sender_name}</p>
                        </body>
                    </html>'''

    return _send_email(user_email, 'Night Squirrel User', subject, body_plain, body_html)


#***********************
#   MAILER ENDPOINTS   *
#***********************

@bp.route('/signup/<incoming_token>')
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


@bp.route('/resetkey/<incoming_token>')
def resetkeyEmailservice(incoming_token):

    error =0
    msg = "All ok"
    #RECEIVING OTP THIS TIME :)
    user_email, user_otp,  \
    email_link_url, email_link_token = get_data_from_token(incoming_token)
    #No email link this time, the last two parameters are not used.

    if len(user_email)>0:
        error, msg = send_reset_email(user_email, user_otp)
    else:
        error = 1
        msg = "Problem with token"

    return { "error": error, "msg":msg }


# ── Notification helpers ─────────────────────────────────────────

def get_notification_data(incoming_token):
    mailersecret = os.environ["JWT_MAILER_SECRET"]
    return jwt.decode(incoming_token, mailersecret, algorithms=['HS256'])


# ── Notification email senders ───────────────────────────────────

def send_answer_delivered_email(data):
    recipient_email = data["user_email"]
    user_name = data.get("user_name", "there")
    qtn_title = data.get("qtn_title", "your question")
    tkt_id = data.get("tkt_id", "")

    subject = "Your answer is ready - Night Squirrel"

    body_plain = (
        f"Hi {user_name},\n\n"
        f"Great news! The answer to your question \"{qtn_title}\" (ticket #{tkt_id}) "
        f"has been delivered.\n\n"
        f"Log in to Night Squirrel to view it.\n\n"
        f"Enjoy!\n"
    )

    body_html = f'''<html><body>
        <p>Hi {user_name},</p>
        <p>Great news! The answer to your question <b>"{qtn_title}"</b>
        (ticket #{tkt_id}) has been delivered.</p>
        <p>Log in to Night Squirrel to view it.</p>
        <p>Enjoy!</p>
    </body></html>'''

    return _send_email(recipient_email, user_name, subject, body_plain, body_html)


def send_payer_quote_accepted_email(data):
    recipient_email = data["user_email"]
    payer_name = data.get("user_name", "there")
    student_name = data.get("student_name", "A student")
    qtn_title = data.get("qtn_title", "a question")
    amount_cents = data.get("tkt_quote_cents", 0)
    currency = data.get("tkt_currency", "EUR")
    amount = f"{amount_cents / 100:.2f}" if amount_cents else "0.00"

    subject = "Quote accepted - Night Squirrel"

    body_plain = (
        f"Hi {payer_name},\n\n"
        f"{student_name} has accepted a quote for the question \"{qtn_title}\".\n"
        f"The amount of {amount} {currency} will be charged to your PayPal "
        f"when the answer is delivered.\n\n"
        f"Enjoy!\n"
    )

    body_html = f'''<html><body>
        <p>Hi {payer_name},</p>
        <p><b>{student_name}</b> has accepted a quote for the question
        <b>"{qtn_title}"</b>.</p>
        <p>The amount of <b>{amount} {currency}</b> will be charged to your
        PayPal when the answer is delivered.</p>
        <p>Enjoy!</p>
    </body></html>'''

    return _send_email(recipient_email, payer_name, subject, body_plain, body_html)


def send_payment_failed_email(data):
    recipient_email = data["user_email"]
    tkt_id = data.get("tkt_id", "?")
    student_name = data.get("student_name", "unknown")
    payer_email = data.get("payer_email", "unknown")
    amount_cents = data.get("amount_cents", 0)
    currency = data.get("currency", "EUR")
    error_msg = data.get("error_msg", "unknown error")
    amount = f"{amount_cents / 100:.2f}" if amount_cents else "0.00"

    subject = f"Payment FAILED for ticket #{tkt_id} - Night Squirrel"

    body_plain = (
        f"Payment failed after delivery.\n\n"
        f"Ticket: #{tkt_id}\n"
        f"Student: {student_name}\n"
        f"Payer: {payer_email}\n"
        f"Amount: {amount} {currency}\n"
        f"Error: {error_msg}\n\n"
        f"Please investigate and resolve manually.\n"
    )

    body_html = f'''<html><body>
        <h3>Payment failed after delivery</h3>
        <table>
            <tr><td><b>Ticket:</b></td><td>#{tkt_id}</td></tr>
            <tr><td><b>Student:</b></td><td>{student_name}</td></tr>
            <tr><td><b>Payer:</b></td><td>{payer_email}</td></tr>
            <tr><td><b>Amount:</b></td><td>{amount} {currency}</td></tr>
            <tr><td><b>Error:</b></td><td>{error_msg}</td></tr>
        </table>
        <p>Please investigate and resolve manually.</p>
    </body></html>'''

    return _send_email(recipient_email, "Admin", subject, body_plain, body_html)


# ── Notification endpoints ───────────────────────────────────────

@bp.route('/answer_delivered/<incoming_token>')
def answerDeliveredEmailservice(incoming_token):
    try:
        data = get_notification_data(incoming_token)
        error, msg = send_answer_delivered_email(data)
    except Exception as e:
        error, msg = 1, str(e)
    return {"error": error, "msg": msg}


@bp.route('/payer_quote_accepted/<incoming_token>')
def payerQuoteAcceptedEmailservice(incoming_token):
    try:
        data = get_notification_data(incoming_token)
        error, msg = send_payer_quote_accepted_email(data)
    except Exception as e:
        error, msg = 1, str(e)
    return {"error": error, "msg": msg}


@bp.route('/payment_failed/<incoming_token>')
def paymentFailedEmailservice(incoming_token):
    try:
        data = get_notification_data(incoming_token)
        error, msg = send_payment_failed_email(data)
    except Exception as e:
        error, msg = 1, str(e)
    return {"error": error, "msg": msg}
