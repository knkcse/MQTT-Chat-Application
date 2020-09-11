import paho.mqtt.client as mqtt
import os


#This functions is mqtt callback on connect
def on_connect(client, userdata, flags, rc):
	#prin("\n")
    print("\n"+s_id+" Connected to the broker with result code "+str(rc)+"\n")

    
#This functions is mqtt callback on message receive
def on_message(client, userdata, msg):
    print("\n"+msg.topic+"[You] <-- "+str(msg.payload.encode('utf-8'))+"\n")
    

#This functions is mqtt callback on subscribe
def on_subscribe(client, userdata, mid, qos):
	prin("\n")
	print(userdata['clientId']+" subscribed to topic "+userdata['topic']+"\n")


#This functions is mqtt callback on publish
def on_publish(client, userdata, mid):
	prin("\n")
	print(userdata['clientId']+" --> "+userdata['topic']+" -- "+userdata['msg']+"\n")


#This functions is mqtt callback on unsubscribe
def on_unsubscribe(client, userdata, mid):
	prin("\n")
	print(userdata['clientId']+" "+userdata['msg']+" "+userdata['topic']+"\n")



#This functions is  writing the subscrbed groups in user's specific file
def writeData(username,groupList):
	if(len(groupList)==0):
		return
	f=open("userfiles/"+username+"_user.txt","w")
	data=groupList[0]
	for i in range(1,len(groupList)):
	    data=data+"\t"+groupList[i]
	f.write(data)
	f.close()	


#This function will remove the user details from our data base file (users.txt) when he/she wants to disconnect
def removeUser(username):
	f=open("users.txt","r")
	data=f.readlines()
	f.close()

	f=open("users.txt","w")
	for line in data:
		ch=line.split("\t")
		if(ch[2]!=username):
			f.write(line)
	f.close()




#The actual chat application starts here	
def chatBox(username,mobile):

	s_id=username

	client = mqtt.Client(client_id=username,clean_session = False,transport="tcp")
	client.will_set(s_id,payload="> unseen messages",qos=2)
	client.on_connect = on_connect
	client.on_message = on_message
	#client.on_subscribe=on_subscribe
	#client.on_publish=on_publish
	client.on_unsubscribe=on_unsubscribe

	client.connect("localhost", 1883, 60)

	client.loop_start()


	"""
	client.user_data_set({
	            'clientId': "You",
	            'topic':s_id
	        	})"""


	client.subscribe(s_id,qos=2);
	print("\nYou subscribed for topic "+ s_id)
	
	
	groupList=list()
	if(not os.path.isfile("userfiles/"+username+"_user.txt")):
		print("Creating file for new username")
		f=open("userfiles/"+username+"_user.txt","w+")
		f.close()

	f=open("userfiles/"+username+"_user.txt","r")
	data=f.read();
	f.close()
	
	#groupList=data;
	if(data!=""):
		ext_data=data.split('\t')
		for i in ext_data:
			client.subscribe(i,qos=2)
			if(i!=""):
				groupList.append(i)

		groupList[len(groupList)-1]=groupList[len(groupList)-1].rstrip("\n\r")
		print("Your subscribed groups are "+str(groupList))

	
	

	print("\n\n")
	print("*** Note: ***\nPlease read the README.txt file to know about the input format\n")

	print("1. TO SUBSCRIBE TO GROUP \nsub/group/groupName\n\n")
	print("2. TO PUBLISH MESSAGE TO GROUP\npub/group/groupName/Message\n\n")
	print("3. TO PUBLISH MESSAGE TO INDIVIDUAL\npub/topicName/Message\n\n")
	print("4. TO  EXIT FROM THE PROGRAM (not disconnecting to the broker)\nexit\n\n")
	print("5. TO DISCONNECT (TO DIACTIVATE)\ndisconnect\n\n")
	print("6. TO UNSUBSCRIBE THE GROUP\nunsub/group/groupName\n\n")

	while(True):
	        intext = raw_input();
	        txt=intext.split('/')

	        if(txt[0]=="sub"):
	        	test=txt[1]
	        	if(test=='group'):
	        		topic=txt[2]
	        		if(topic==""):
	        			print("\n* Warnig: * You entered invalid options\n")
	        		elif(topic in groupList):
	        			print("\n* Warnig: * You Already subscribed to this group\n")
	        		else:
		        		"""client.user_data_set({
		            		'clientId':  s_id,
		            		'topic':topic
		        		})"""
		        		print("\nYou subscribed to the group "+topic+"\n")
		        		client.subscribe(topic,qos=2)
		        		groupList.append(topic)
		        		message=s_id+" is subscribed to the group "+topic
		        		client.publish(topic,message,qos=2)
		        else:
		        	print("\nYou have to register to the groups\n")
			        print("\n*Warning: * You have entered invalid format of the input. Please check once:\n")
	        	
	        	#Any message that you want to display
	        elif(txt[0]=="pub"):
	        	group=txt[1]#group
	        	if(group=="group"):
	        		#need to check whether the subscriber is in the group or not
	        		if(txt[2] in groupList):
			        	# Set the credentials and save the user data
			        	topic=txt[2]#identifier
			        	message=s_id+": "+txt[3]#message
			        	
			        	print("\nYou--> "+topic+": "+txt[3]+"\n")
			        	client.publish(topic,message,qos=2)
			        else:
			        	print("\n*Warning:* You are not subscribed to this group. Please subscribe to this group first\n")
		        else:
		        	if(len(txt)==3):
			        	topic=txt[1]
			        	message=txt[2]#message
			        	
				        print("\nYou--> "+topic+": "+message+"\n")
				        message=s_id+": "+message
			        	client.publish(topic,message,qos=2)
			        else:
			        	print("\n*Warning:* You are not subscribed to this group. Please subscribe to this group first\n")


			

	        else:
	        	if(txt[0]=="unsub"):
	        		if(txt[1]=="group"):
	        			groupId=txt[2]
	        			if(groupId in groupList):
	        				groupList.remove(groupId)
	        				message=" left the group "
	        				client.user_data_set({
	        					'clientId':s_id,
	        					'topic':groupId,
	        					'msg':message
	        					})

	        				writeData(username,groupList)

	        				client.unsubscribe(groupId)
	        				print("\nYou unsubscribed the group "+groupId+"\n")
	        				client.publish(groupId,s_id+" left the group",qos=2)
	        			else:
	        				print("\nYou haven't subscribed to the group "+groupId+"\n")
	        		else:
	        			if(len(txt)==2):
	        				topic=txt[1]
	        				#print("\nYou unsubscribed the topic "+topic+"\n")
	        				#client.unsubscribe(topic)
	        				#client.publish(topic,s_id+" unsubscribed the topic "+topic+"\n",qos=2)
	        				print("\nYou only able to unsubscribe to the gorups. Please follow the input rules\n\n")
	        			else:
	        				print("\nWarning: * You have entered invalid input type. Pleae check once\n")
	        	else:
	        		if(txt[0]=="exit"):
	        			writeData(username,groupList)
	        			#client.disconnect()
	        			print("\nYou have exit the program\n")
	        			break
	        		elif(txt[0]=="disconnect"):

	        			for i in groupList:
	        				client.unsubscribe(i)
	        			client.unsubscribe(username)
	        			client.disconnect()
	        			os.remove("userfiles/"+username+"_user.txt")

	        			#removeUser(username)

	        			client.loop_stop()
	        			break
	        		
	        		else:	
	        			print("\n*Warning: * You have entered invalid format of the input. Please check once:\n")
