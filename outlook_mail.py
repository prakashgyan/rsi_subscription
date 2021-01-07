# import the smtplib module. It should be included in Python by default
from calculator import get_table 
import smtplib
from tabulate import tabulate
import os

MY_ADDRESS = os.environ["MY_EMAIL_ADDRESS"]
PASSWORD = os.environ["MY_EMAIL_PASSWORD"]
# set up the SMTP server
s = smtplib.SMTP(host='smtp.office365.com', port=587)
s.starttls()
s.login(MY_ADDRESS, PASSWORD)

# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

# For each contact, send the email:
def read_text(filename1,filename2):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename1, 'r', encoding='utf-8') as template_file:
        template_file_content1 = template_file.read()
        # print(template_file_content)
    with open(filename2, 'r', encoding='utf-8') as template_file:
        template_file_content2 = template_file.read()
    return (template_file_content1),(template_file_content2)

def send_mail(data):
    text, html = read_text('template.txt','template.html')
    text = text.format(table=tabulate(data, headers=['S.No', 'YahooCD','Vol_Ratio','VR Purchase'],
            tablefmt="grid",colalign=("center","center","center","center")))
    html = html.format(table=tabulate(data, headers=['S.No', 'YahooCD','Vol_Ratio','VR Purchase'],
            tablefmt="html",colalign=("center","center","center","center")))
    # message_template = read_template('template.txt','template.html')
    msg = MIMEMultipart('alternative', None, [MIMEText(text), MIMEText(html,'html')])       # create a message
    mailing_list = open('mailing_list.txt','r')
    # add in the actual person name to the message template
    # message_template = 'sdhashhgdj hsgajs adhjasa jshdjasd'
    # message = message_template.substitute(PERSON_NAME='Subscriber_007')
    # message = message_template.substitute()
    for to_email in mailing_list:
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=to_email
        msg['Subject']="Recent Stock Chnages"

        # add in the message body
        # msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.sendmail(MY_ADDRESS, to_email, msg.as_string())
        print(f'Email Sent to {to_email}')

    del msg