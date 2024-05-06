# from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from django.conf import settings
# settings.configure()
def send_account_activatoin_email(email, email_token):
    try:
        # Create a MIMEMultipart message object
        message = MIMEMultipart()

        print(settings.EMAIL_HOST, settings.EMAIL_PORT,'-----------------')
        # Set the subject
        message["Subject"] = "Your account needs to be verified"

        # Set the sender email address
        message["From"] = "demo735060@gmail.com"

        # Set the recipient email address
        message["To"] = email

        # Set the message content
        message_content = f"Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}"

        # Attach the message content
        message.attach(MIMEText(message_content, "plain"))

        # Convert the message to a string
        msg_body = message.as_string()

        # Connect to the SMTP server
        server = SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(server,'-----------------')

        # Start TLS encryption
        server.starttls()

        # Login to the SMTP server
        print("just above login -----------")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Send the email
        server.sendmail(message["From"], message["To"], msg_body)

        print('yes mail sends----------')

        # Quit the SMTP server
        server.quit()

        # try:
        #     subject = "Your account needs to be verfied"
        #     email_from = "demo735060@gmail.com"
        #     meassage = f"Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}"
        #     print("inside send_account_activatoin_email")
        #     print(email,"email-----------")
        #     print(email_from,"emailfrom -----------")
        #     send_mail(subject,meassage,email_from,[email])
        # except  Exception as e:
        #     raise e
    except Exception as e:
        raise e

# send_account_activatoin_email("suntake23@gmail.com", "1237821lkjhh123")
