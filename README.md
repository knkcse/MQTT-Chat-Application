# To run  application

step1: You have to run your hivemq (install before hand, install mqtt in python) 

step2: python Main.py


 Read the instructions displayed by the program after running it and give proper input to the program
 
 
Once the chat application is opened after completing the registration and login, we should follow some rules to give the input to the program


1. TO SUBSCRIBE TO GROUP
   sub/group/groupName
   
   [Note: Here groupName is any name that we want to create group chat. No predefined groups are exist. I imagened WhatsApp
   groups. So we have subscribe for a new group name]
   
   
2. TO PUBLISH MESSAGE TO GROUP
   pub/group/groupName/Message
   
   [Note: groupName is name of groups that user subscribed]
   
3. TO PUBLISH MESSAGE TO INDIVIDUAL (topicName could be individual or group)
   pub/topicName/Message
   
4. TO  EXIT FROM THE PROGRAM (not disconnecting to the broker, kind of offline)
   exit


5. TO DISCONNECT (TO DIACTIVATE)
   disconnect
   
6. TO UNSUBSCRIBE THE GROUP
   unsub/group/groupName


# *Details about files and folders*
1. userfiles folder contains files for each user to maintain their subscribed groups list. So that, when they go offline and come back then we can display the groups and messages for those groups .

2.users.txt file is used to maintain our registered users. 

3. ChatBox.py contains all the code that is responsible to implement the given application

4. Main.py contains first interface of registration and login, which is used to get users registered and login to the application
   
  
