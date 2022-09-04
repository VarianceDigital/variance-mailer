from variancemailer import create_app
import os

#SET THESE FOR DEBUGGING PURPOSES
os.environ["SENDER_NAME"]="Your Name"
os.environ["SESSION_SECRET"]="MySessionSecret" 

os.environ["JWT_MAILER_SECRET"]="MyMailerJWTSecret" 
#MUST BE THE EXACT COPY OF THAT OF THE SENDER APP

app = create_app()
app.run()
