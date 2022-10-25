import functools
from flask import current_app
from flask import (
    Blueprint, g, redirect, request, session
)

import os
import jwt

bp = Blueprint('auth', __name__, url_prefix='/auth')


#IMPORTANT! Called for every request
@bp.before_app_request
def pre_operations(): 

    #ALL STATIC REQUESTS BYPASS!!!
    if request.endpoint == 'static':
        return

    #REDIRECT http -> https
    if 'DYNO' in os.environ:
        current_app.logger.critical("DYNO ENV !!!!")
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
            

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
            user_aut_key=decoded["user_aut_key_or_otp"]
            email_link_url=decoded["email_link_url"]
            email_link_token=decoded["email_link_token"]
        except jwt.DecodeError:
            pass
        
    return user_email, user_aut_key, email_link_url, email_link_token
