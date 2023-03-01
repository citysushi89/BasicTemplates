from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv

load_dotenv()

env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

def get_data():
    data = []
    data.append(
        {
         "movies": [
             {         
                 "title": 'Terminator',
                 "description": 'One soldier is sent back to protect her from the killing machine. He must find Sarah before the Terminator can carry out its mission.'
             },
             {                 
                 "title": 'Seven Years in Tibet',
                 "description": 'Seven Years in Tibet is a 1997 American biographical war drama film based on the 1952 book of the same name written by Austrian mountaineer Heinrich Harrer on his experiences in Tibet.'
             },
             {               
                 "title": 'The Lion King',
                 "description": 'A young lion prince is born in Africa, thus making his uncle Scar the second in line to the throne. Scar plots with the hyenas to kill King Mufasa and Prince Simba, thus making himself King. The King is killed and Simba is led to believe by Scar that it was his fault, and so flees the kingdom in shame.'
             }
         ]
         })
    return data


def send_mail(bodyContent):
    to_email = os.getenv('TO_EMAIL')
    print(to_email)
    from_email = os.getenv('FROM_EMAIL')
    print(from_email)
    subject = 'This is a email from Python with a movies list!'
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email

    message.attach(MIMEText(bodyContent, "html"))
    msgBody = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, os.getenv('FROM_EMAIL_PASSWORD'))
    print(os.getenv('FROM_EMAIL_PASSWORD'))
    server.sendmail(from_email, to_email, msgBody)

    server.quit()


def send_movie_list():
    json_data = get_data()
    template = env.get_template('child.html')
    output = template.render(data=json_data[0])
    send_mail(output)    
    return "Mail sent successfully."

send_movie_list()