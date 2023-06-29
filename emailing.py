import smtplib
from email.message import EmailMessage
import imghdr


def sending_email(image_with_object):
    password = "rcjqsbclbtkymqqm"
    sender = "lovelakhwani181@gmail.com"
    email_message = EmailMessage()
    email_message["Subject"] = "INTRUDER DETECTED"
    email_message.set_content("We have detected the an Object Entering your Area")
    with open(image_with_object, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, sender, email_message.as_string())
    gmail.quit()
