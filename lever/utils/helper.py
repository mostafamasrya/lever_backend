from django.utils.translation import gettext as _
import phonenumbers as pn
import re
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings.base import SMTP_FROM,SMTP_SERVER,SMTP_PASSWORD,SMTP_PORT,SMTP_USERNAME, env
import threading


def check_required_fileds(required_fields,data):
    for field in required_fields:
        if field not in data or not data[field]:
            msg = _("required")
            message = _(field) + " " + msg
            # message = {"message":message}
            return message
    return ""


def default_success_response(data=[],status_code=200,message="success",error_code=1000):
    return {
        "status": "success",
        "status_code": status_code,
        "error_code": error_code,

        "message": message,
        "data": data,
    }

def default_error_response(data=[],status_code=400,message="error",error_code=1000):
    return {
        "status": "error",
        "status_code": status_code,
        "error_code": error_code,
        "message": message,
        "data": data,
    }      



def valid_phone_number(phone):
    try:
        valid_phone_number = pn.parse(phone, None)
        valid = pn.is_valid_number(valid_phone_number)
        if not valid:
            return False
        else:
            return True
    except Exception as e:
        return False
    


def validate_email(email):
    pattern = r'^(?![-.])[a-zA-Z0-9._+-]+(?<![-.])@[a-zA-Z0-9.]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        # Ensure no consecutive periods in the local part
        local_part = email.split('@')[0]
        if '..' in local_part:
            return False
        return True
    else:
        return False
    

def validate_password(password):
    # Regular expression for password validation
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$"
    
    # Match the password with the pattern
    if re.match(pattern, password):
        return True
    else:
        return False
    




# def default_email_func(email,subject,message):
#     smtp_server = SMTP_SERVER
#     smtp_port = SMTP_PORT
#     smtp_username = SMTP_USERNAME
#     smtp_password = SMTP_PASSWORD

#     email_msg = message

#     msg = MIMEMultipart('alternative')
#     msg['From'] = SMTP_FROM
#     msg['To'] = email
#     msg['Subject'] = subject

#     # Create HTML part of the email
#     html_part = MIMEText(email_msg, 'html')
#     msg.attach(html_part)

#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as smtp:
#             smtp.connect(smtp_server,smtp_port)
#             smtp.ehlo()
#             smtp.starttls()
#             smtp.ehlo()
#             smtp.login(smtp_username, smtp_password)
#             smtp.sendmail(msg['From'], msg['To'], msg.as_string())
#             return True
#     except Exception as e:
#         print(e)
#         return False
