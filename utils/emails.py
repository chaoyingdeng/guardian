from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from smtplib import SMTP

SERVER = 'smtp.qq.com'
AUTH_CODE = 'rsabmlgwgcoebhfa'
SENDER = '406125295@qq.com'
RECEIVERS = '406125295@qq.com, dengchaoying18@gmail.com'


class Email:
    def __init__(self, sender, receivers, server, auth_code, title='Test Email', html=None, attachment_files=None):
        self.sender = sender
        self.receivers = receivers
        self.server = server
        self.auth_code = auth_code

        self.title = title
        self.html = html
        self.attachment_files = attachment_files
        self.msg = MIMEMultipart('related')

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receivers

        if self.html:
            self.msg.attach(MIMEText(self.html, 'html'))

        if self.attachment_files:
            for file_path in self.attachment_files:
                self._attach_file(file_path)

        smtp_server = SMTP(self.server)
        smtp_server.login(self.sender, self.auth_code)
        smtp_server.sendmail(self.sender, self.receivers.split(','), self.msg.as_string())
        smtp_server.quit()

    def _attach_file(self, file_path):
        if not Path(file_path).exists():
            raise FileNotFoundError(file_path)
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{Path(file_path).name}"')
        self.msg.attach(part)


class SendDailyReport(Email):
    template_path = Path(__file__).parent.parent / 'data' / 'report_related' / 'daily_template.html'
    summary_json = Path(__file__).parent.parent / 'data' / 'report_related' / 'report.json'
    detail_json = Path(__file__).parent.parent / 'data' / 'report_related' / 'origin_report.json'

    def daily_report_format(self):
        import json
        with open(self.summary_json, 'r', encoding='utf-8') as sj:
            summary = json.loads(sj.read())

        with open(self.detail_json, 'r', encoding='utf-8') as dj:
            detail = json.loads(dj.read())

        with open(self.template_path, 'r', encoding='utf-8') as f:
            details = ''
            for case, result in detail.items():
                details += f" <tr><td>{case}</td><td>{result}</td> </tr>"
            self.html = f.read().format(details=details, **summary)
        self.title = 'Guardian Daily Report'

    def send_daily_report(self):
        self.daily_report_format()
        self.send()


if __name__ == '__main__':
    SendDailyReport(
        sender=SENDER,
        receivers=RECEIVERS,
        server=SERVER,
        auth_code=AUTH_CODE
    ).send_daily_report()
