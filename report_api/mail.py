import smtplib
from report_api.settings import get_settings, MAIL_TEMPLATE

settings = get_settings()


def send_email(subject, to_addr, link):
    """
    Send an email
    """

    BODY = "\r\n".join((
        "From: no-repty@physics.msu.ru",
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        MAIL_TEMPLATE.replace('{{url}}', link)
    ))

    from_addr = 'profcom@physics.msu.ru'
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(from_addr, settings.EMAIL_PASS)
    smtpObj.sendmail(from_addr, [to_addr], BODY)
    smtpObj.quit()
