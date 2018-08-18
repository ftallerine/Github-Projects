import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class BaseEmailer(object):
    def __init__(self, Recipient):
        self.FROM = 'franktallerine@gmail.com'
        self.TO = Recipient
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.message = MIMEMultipart()
        self.message['From'] = self.FROM
        self.message['To'] = self.TO

    def SetUp(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.login("franktallerine@gmail.com" ,"$.q6pVN/6M\(&!,@G5}u")

    def SendMessage(self, Subject, text):
        self.message['Subject'] = Subject
        self.message.attach(MIMEText(text, 'plain'))
        self.server.sendmail(self.FROM ,self.TO, self.message.as_string())
        self.Quit()

    def Quit(self):
        self.server.close()

class HTMLEmailer(BaseEmailer):
    def __init__(self,Reciptient):
        super(HTMLEmailer, self).__init__(Recipient=Reciptient)


    def SetUp(self):
        super(HTMLEmailer, self).SetUp()

    def SendMessage(self, Subject, text,  html):
        self.message['Subject'] = Subject
        self.message.attach(MIMEText(text, 'plain'))
        self.message.attach(MIMEText(html, 'html'))
        self.server.sendmail(self.FROM, self.TO, self.message.as_string())
        self.Quit()
    def Quit(self):
        super(HTMLEmailer, self).Quit()

if __name__ == '__main__':
    '''
    print("this is a test.")
    tester = BaseEmailer("franktallerine@gmail.com")
    tester.SetUp()
    tester.SendMessage("testing","Yo dawg, hey")

    tester2 = HTMLEmailer("franktallerine@gmail.com")
    tester2.SetUp()
    tester2.SendMessage("Test2","words yo","<p>Fried</p>")
    '''
    