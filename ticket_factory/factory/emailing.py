# Send an email with HTMl as the body
# This is used in the factory module to send the URL ticket to the user

# To access to the environment variable
import os
from os.path import join, dirname
from dotenv import load_dotenv
# To send the email
import smtplib
# Used to secure connections
import ssl 
# Used to format HTML in the email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Get the app pasword to login to mitorruco@gmail.com
def get_email_password() -> str:
	# The .env file is located in the root of the project
	dotenv_path = join(dirname(dirname(__file__)), '.env')
	load_dotenv(dotenv_path)
	APP_EMAIL_PASSWORD = os.getenv("APP_EMAIL_PASSWORD")
	return APP_EMAIL_PASSWORD

# Send the email to the reciver, specifying the URL to send, using an hyperlink
# The email sender is 'mitorruco@gmail.com' by defect
def send_email(receiver: str, url: str, receiver_name: str) -> bool:
	email_sender = 'mitorruco@gmail.com'
	email_password = get_email_password()
	email_receiver = receiver

	# TODO: make sure 'receiver' is a valid email and 'url' a valid URL

	# The message object represents the email to send
	message = MIMEMultipart()

	# Settings
	message['From'] = email_sender
	message['To'] = email_receiver
	message['Subject'] = 'Boleto digital de Ticket Factory'

	html_content = f"""
	<html>
		<body>
			<p>{receiver_name}, aquí está tu boleto digital</p>
			<p>Para visualizar su boleto, <a href="{url}">presione aquí</a>.</p>
			<p>Más instrucciones e información</p>
		</body>
	</html>
	"""

	# Create the object that represents the HTML
	html = MIMEText(html_content, 'html')

	# Attach the HTMl content
	message.attach(html)

	# Add SSL (layer of security)
	context = ssl.create_default_context()

	try:
		# Create a secure SMTP connection, from the port 465
		with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
			# Log in and send the email
			smtp.login(email_sender, email_password)
			smtp.sendmail(email_sender, email_receiver, message.as_string())
			return True
	except smtplib.SMTPException as e:
		return False