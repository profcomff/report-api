import smtplib
from report_api.settings import MAIL_CONFERENCE_END_TEMPLATE, MAIL_PASSWORD_TEMPLATE, get_settings, MAIL_CONFIRMATION_TEMPLATE

settings = get_settings()


def send_confirmation_email(subject, to_addr, link):
    """
    Send confirmation email
    """
    from_addr = 'profcom@physics.msu.ru'

    BODY = "\r\n".join((
        f"From: {from_addr}",
        f"To: {to_addr}",
        f"Subject: {subject}",
        "Content-Type: text/html; charset=utf-8;",
        "",
        MAIL_CONFIRMATION_TEMPLATE.replace('{{url}}', link)
    ))

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY.encode('utf-8'))
    smtpObj.quit()


def send_password_email(subject, to_addr, name, password):
    """
    Send password email
    """
    from_addr = 'profcom@physics.msu.ru'

    BODY = "\r\n".join((
        f"From: {from_addr}",
        f"To: {to_addr}",
        f"Subject: {subject}",
        "Content-Type: text/html; charset=utf-8;",
        "",
        MAIL_PASSWORD_TEMPLATE.replace('{{name}}', name)
        .replace('{{email}}', to_addr).replace('{{password}}', password)
    ))

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY.encode('utf-8'))
    smtpObj.quit()


def send_conference_end_email(subject, to_addr):
    """
    Send conference end email
    """
    from_addr = 'profcom@physics.msu.ru'

    BODY = "\r\n".join((
        f"From: {from_addr}",
        f"To: {to_addr}",
        f"Subject: {subject}",
        "Content-Type: text/html; charset=utf-8;",
        "",
        MAIL_CONFERENCE_END_TEMPLATE
    ))

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY.encode('utf-8'))
    smtpObj.quit()
