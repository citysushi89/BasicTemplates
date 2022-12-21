import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
MY_FROM_EMAIL = os.getenv("MY_FROM_EMAIL")
PASSWORD = os.getenv("MY_PASSWORD")
MY_TO_EMAIL = os.getenv("MY_TO_EMAIL")

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = MY_FROM_EMAIL
msg['To'] = MY_TO_EMAIL

# Create the body of the message (a plain-text and an HTML version).
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
email_html = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(email_html)
# Send the message via local SMTP server.
mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login(MY_FROM_EMAIL, PASSWORD)
mail.sendmail(MY_FROM_EMAIL, MY_TO_EMAIL, msg.as_string())
mail.quit()