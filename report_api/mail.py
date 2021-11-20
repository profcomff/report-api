import smtplib
from report_api.settings import MAIL_PASSWORD_TEMPLATE, get_settings, MAIL_CONFIRMATION_TEMPLATE

settings = get_settings()


def send_confirmation_email(subject, to_addr, link):
    """
    Send confirmation email
    """

    BODY = "\r\n".join((
        "From: no-repty@physics.msu.ru",
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "Content-Type: text/html;",
        "",
        MAIL_CONFIRMATION_TEMPLATE.replace('{{url}}', link)
    ))

    from_addr = 'profcom@physics.msu.ru'
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY.encode('utf-8'))
    smtpObj.quit()


def send_password_email(subject, to_addr, name, password):
    """
    Send password email
    """

    BODY = "\r\n".join((
        "From: no-repty@physics.msu.ru",
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "Content-Type: text/html;",
        "",
        MAIL_PASSWORD_TEMPLATE.replace('{{name}}', name)
        .replace('{{email}}', to_addr).replace('{{password}}', password)
    ))

    from_addr = 'profcom@physics.msu.ru'
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY.encode('utf-8'))
    smtpObj.quit()
