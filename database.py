import os
import psycopg2
import urlparse
import sys

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("postgres://lcgigjguzxyusa:Fl-W3fEmvP5mmgRSgoYiEF63Ro@ec2-54-197-230-210.compute-1.amazonaws.com:5432/dekjsm7qjhos9c")



# Table Format: cur.execute("CREATE TABLE Users(Stage INTEGER, Username VARCHAR(22), PhoneNumber INT)")
# New Table Format: cur.execute("CREATE TABLE UserDB(hasGivenPhoneNum BOOLEAN, hasProvidedMessageBody BOOLEAN, Username VARCHAR(22), PhoneNumber INT)")


#See if a given user is already in the database
def lookUpUser(username):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()
	cur.execute("SELECT Username from UserDB")
	rows = cur.fetchall()
	for row in rows:
		if row[0] == username:
			conn.close()
			return True
		
	conn.close()
	return False


#Add user to database
def addUser(givenNum, givenMessage, username, phoneNumber):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("INSERT INTO UserDB VALUES(%s, %s, %s, %s)", (givenNum, givenMessage, username, phoneNumber))
	
	conn.commit()

	conn.close()


#Check if a user has given a phone number
def hasGivenNum(username):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("SELECT Username, hasGivenPhoneNum from UserDB")
	rows = cur.fetchall()
	for row in rows:
		if row[0] == username:
			return row[1]


	conn.close() #Needed?



def hasGivenMessage(username):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("SELECT Username, hasProvidedMessageBody from UserDB")
	rows = cur.fetchall()
	for row in rows:
		if row[0] == username:
			return row[1]


	conn.close() #Needed?


#Change whether user has provided a phone number or not
def setGivenNum(username, newVal):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("UPDATE UserDB SET hasGivenPhoneNum=%s WHERE Username=%s", (newVal, username))   


	conn.commit()

	conn.close()



#Change whether user has provided a message body or not
def setGivenMessage(username, newVal):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("UPDATE UserDB SET hasProvidedMessageBody=%s WHERE Username=%s", (newVal, username))   


	conn.commit()

	conn.close()

def storePhoneNum(username, phoneNumber):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("UPDATE UserDB SET PhoneNumber=%s WHERE Username=%s", (phoneNumber, username))   


	conn.commit()

	conn.close()

def getPhoneNumber(username):

	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("SELECT Username, PhoneNumber from UserDB")
	rows = cur.fetchall()
	for row in rows:
		if row[0] == username:
			return row[1]


	conn.close() #Needed?



def alterTable():
	conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
	)  

	cur = conn.cursor()

	cur.execute("ALTER TABLE UserDB ALTER COLUMN PhoneNumber TYPE VARCHAR(20)")

	
	conn.commit()

	conn.close()





if __name__ == '__main__':
	alterTable()
   






