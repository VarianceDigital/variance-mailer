from variancemailer import create_app
import os

#SET THESE FOR DEBUGGING PURPOSES
os.environ["SENDER_NAME"]="Your Name"
os.environ["SESSION_SECRET"]="MySessionSecret" 

os.environ["JWT_MAILER_SECRET"]="MyMailerJWTSecret" 
#MUST BE THE EXACT COPY OF THAT OF THE SENDER APP

os.environ['MAILERTOGO_SMTP_HOST']="YourMailerToGoValueHere"
os.environ['MAILERTOGO_SMTP_PORT']="YourMailerToGoValueHere"
os.environ['MAILERTOGO_SMTP_USER']="YourMailerToGoValueHere"
os.environ['MAILERTOGO_SMTP_PASSWORD']="YourMailerToGoValueHere"
os.environ['MAILERTOGO_DOMAIN']="YourMailerToGoValueHere"

app = create_app()
app.run()
