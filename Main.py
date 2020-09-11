
import string
import re
import getpass
import ChatBox as obj

RE_phone = re.compile("^[0-9]{3}-[0-9]{3}-[0-9]{4}$")


#This function will check whether the username is exists or not
def checkUsername(username):
	f=open('users.txt','r')

	while  True:
		text=f.readline()
		if not text:
			break
		txt=text.split('\t')
		if(txt[2]==username):
			return True
	f.close()
	return False


#This function validates login credentials

def validateUser(username,password):
	f=open('users.txt','r')

	while  True:
		text=f.readline()
		if not text:
			break
		txt=text.split('\t')
		if(txt[2]==username and txt[3]==password):
			return True
	f.close()
	return False


#This function shows interface to user login
def loginSubscriber():
	print("********** USER LOGIN **********")
	while True:
		username=raw_input("\nEnter subscriber id /username: ")
		if(username==""):
			print("\nPlease enter subscriber id/username\n")
		else:
			break;
	while True:
		password=getpass.getpass("\nEnter your password: ")
		if(password==""):
			print("\nPlease enter the password\n")
		else:
			break
	if(validateUser(username,password)):
		f=open('users.txt','r')
		mobile=""
		while  True:
			text=f.readline()
			if not text:
				break
			txt=text.split('\t')
			if(txt[2]==username):
				mobile=txt[2] #getting mobile number from the file
		f.close()
		
		#print("Enter to the chat box now\n")

		obj.chatBox(username,mobile)
	else:
		
		print("\nYou have entered invalid user/password\nPlease try again\n")
		start()



#This function shows registration interface to user
def registerSubscriber():
	print("********** REGISTRATION **********")
	F=True
	while(F):
		name=raw_input("\nEnter your name: ")
		if(name==""):
			print("\nPlease enter the name\n")
		else:
			F=False
	F=True


	while(F):
		phone_number=raw_input("\nEnter mobile number in the format XXX-XXX-XXXX: ")
		if(RE_phone.match(phone_number)):
		#if(phone_number!=""):
			break
		else:
			print("\nMobile number is in invalid format\n")


	while True:
		sub_id=raw_input("\nEnter subscriber id /username: ")
		if(sub_id==""):
			print("\nPlease enter subscriber id/username\n")
		else:
			break;


	while True:
		password=getpass.getpass("\nEnter password: ")
		if(password==""):
			print("\nPlease enter the password\n")
		else:
			break


	if(checkUsername(sub_id)):#if username already exists
		print("\nusername/subscriber "+sub_id +" already exist. Please login...\n")
		loginSubscriber()
	else:
		f = open("users.txt", "a")
		record=name+"\t"+phone_number+"\t"+sub_id+"\t"+password+'\t'+"\n"
		f.write(record)
		print("\nPlease Login using your credentials\n")

		f=open("userfiles/"+sub_id+"_user.txt","w+")
		f.close()
		loginSubscriber()
		#obj.chatBox(username,mobile)


def start():
	print("********** APPLICATION **********")	
	flag=True
	while(flag):
		print("Choose your choice:\n1.Register\n2.Login\n")
		ch=raw_input()
		if(ch=="1"):
			registerSubscriber()
			break
		elif(ch=="2"):
			loginSubscriber()
			break
		else:
			print("\nYou have entered invalid option\nPlease enter again\n")

start();