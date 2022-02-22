import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailSender:
    def __init__(self, body=None, subject=None, to_email=None):
        load_dotenv()
        self.from_email = os.getenv('SENDGRID_SENDER')
        if body and subject and to_email:
            self.send_message(body, subject, to_email)

    def send_message(self, body, subject, to_email):
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=f'{subject}',
            html_content=f'<p>{body}</p>')
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.body)


if __name__ == '__main__':
    EmailSender('body', 'subject', 'mykola.kurenkov@data-ox.com')
