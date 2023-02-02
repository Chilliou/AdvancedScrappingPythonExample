
import time
import string
# importing webdriver from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import smtplib, ssl
from bs4 import BeautifulSoup


def mailSend(date):
	port = 587  # For starttls
	smtp_server = "smtp.gmail.com"
	sender_email = "xxxxx@gmail.com"    # Enter your Gmail address
	receiver_email = "xxxxx@gmail.com"  # Enter receiver address
	password = "wrrmbpbnskbnpcae"       # Enter your token Gmail
	message = """\
	Subject: Nouveau Rdv dispo

	Il y a un nouveau rdv dispo le """+str(date)

	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
	    server.ehlo()  # Can be omitted
	    server.starttls(context=context)
	    server.ehlo()  # Can be omitted
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)

	print("Email Envoyer")

d1 = datetime.datetime(2023,4,11)

url='http://rdv-mairie.lehavre.fr/eAppointment/appointment.do?preselectservice=CNI'
driver = webdriver.Chrome()
driver.get(url)

button = driver.find_element(By.ID,"nextButtonId")
button.click()
time.sleep(3)

button = driver.find_element(By.NAME,"selectedMotiveKeyList")
button.click()
time.sleep(3)

button = driver.find_element(By.ID,"nextButtonId")
button.click()
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
rdv = soup.find_all(class_="soonestText")


spliter = str(rdv).split(",")
no_digits = string.printable[10:]
lmois= ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre" ]
for mois in lmois:
	for date in spliter:
		if mois in date:
			trans = str.maketrans(no_digits, " "*len(no_digits))
			jour = date.translate(trans).split()[0]
			d2 = datetime.datetime(2023,lmois.index(mois)+1,int(jour))
			if d2 < d1:
				mailSend(d2)
			else:
				print("Pas de nouvelle date dispo")


