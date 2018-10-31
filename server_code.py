import socket
import time
from functions import *
import sqlite3

def create():
    try:
        c.execute("""CREATE TABLE chatLog(name, text)""")
    except:
        pass

def insert(name, text):
    c.execute("""INSERT INTO chatLog (name, text)
              values(?, ?)""", (name, text))

def select(verbose=True):
    sql = "SELECT * FROM mytable"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print (row)


db_path = r'database.db'
conndb = sqlite3.connect(db_path)
c = conndb.cursor()

    
fullChatString=""
strName=""
strAddress=""
boolSent=False
lstPossibilities=list()
stage=0
boolSent=False
#possibilitiesList=[]

#Give ChatBot server an IP address and port
host = "127.0.0.1"
port = 5001
#Create Socket and bind server to socket           
thisSocket = socket.socket()
thisSocket.bind((host,port))
#Listen for clients     
thisSocket.listen(1)
#Connect to client
conn, addr = thisSocket.accept()
#print Connect ip address
print ("The Connection ip is : " + str(addr))

#Main loop
while True:
  #Receive info from client
  receiveMess = conn.recv(1024).decode()
  #if no info from client end loop
  if not receiveMess:    
    break
  #Print info from client
  if(stage==0):
    print("stage 0")
    #asking victim info including name and address
    if(not boolSent):
      print("asking for name...")
      returnMess="Please insert your name."
      boolSent=True
    else:         
      boolSent=False
      strName=receiveMess
      print("recieved name: "+strName)
      print("asking address...")
      returnMess=strName+ ", please insert your address as best as possible."
      stage=1
      print("done")
  elif(stage==1):
    #asking what the situation is and looking for keywords that would give clues on the possibilities
    strAddress=receiveMess
    print("recieved address: "+strAddress)
    print("stage 1")
    if(not boolSent):
      print("if")
      returnMess=strName+ ", please describe the situation as best as possible."
      boolSent=True      
    else:
      print("else")
      lstPossibilities=CheckWords(receiveMess)
      stage=2
      idx=-1
      cnt=0
  if(stage==2):
    #asking exact questions to try and confirm the situations present in the lstPossibilities         
    if(receiveMess.lower()=="no"):
      lstPossibilities[idx]=0
    elif(idx!=-1):
      print("cnt++")
      cnt+=1
    print("idx= "+str(idx))
    idx+=1
    if(idx<25):
      print("starting cicle")
      for i in range(idx, 25):
        print("i= "+str(i))
        if(lstPossibilities[i]==1):
          if(i==0):
            returnMess=AllergicReaction()
            break
          elif(i==1):
            returnMess=AnimalBite()
            break
          elif(i==2):
            returnMess=AssaultInjured()
            break
          elif(i==3):
            returnMess=AttemptedSuicide()
            break
          elif(i==4):
            returnMess=BackPain()
            break
          elif(i==5):
            returnMess=BreathingDifficulty()
            break
          elif(i==6):
            returnMess=CoInhalation()
            break
          elif(i==7):
            returnMess=CardiacArrest()
            break
          elif(i==8):
            returnMess=ChestPain()
            break
          elif(i==9):
            returnMess=Choking()
            break
          elif(i==10):
            returnMess=Diabetic()
            break
          elif(i==11):
            returnMess=FallInjured()
            break
          elif(i==12):
            returnMess=Headache()
            break
          elif(i==13):
            returnMess=HeatColdExposure()
            break
          elif(i==14):
            returnMess=Hemorrhage()
            break
          elif(i==15):
            returnMess=Laceration()
            break
          elif(i==16):
            returnMess=Overdose()
            break
          elif(i==17):
            returnMess=Pain()
            break
          elif(i==18):
            returnMess=Pregnancy()
            break
          elif(i==19):
            returnMess=Seizure()
            break
          elif(i==20):
            returnMess=Shooting()
            break
          elif(i==21):
            returnMess=Stabbing()
            break
          elif(i==22):
            returnMess=UnconsciousPerson()
            break
          elif(i==23):
            returnMess=Unknown()
            break
          elif(i==24):
            returnMess=VehicleAccidents()
            break
        elif(i==24): 
          print("1st ending")
          if(cnt==0):
            returnMess= strName+ ", unfortunately we couldnt identify the problem.\nPlease try again (type: ok)."
            stage=1
            boolSent=False
          else:
            #sendinfo via email
            returnMess=strName+ ", help is on the way.\n ending con."
            fullChatString+=receiveMess+"\n"
            fullChatString+=returnMess+"\n"
            sendEmail(fullChatString)        
            makeCall(fullChatString)
            sendSMS(fullChatString)
            insert(strName, fullChatString)
            conndb.commit()
            conn.send(returnMess.encode())
            conn.close()
            quit()                          
      idx=i    
    else:
      print("2st ending")
      if(cnt==0):
        returnMess= strName+ ", unfortunately we couldnt identify the problem.\nPlease try again. (type: ok)"
        stage=1
        boolSent=False
      else:
        #sendinfo via email
        returnMess=strName+ ", help is on the way.\nending con."
        fullChatString+=receiveMess+"\n"
        fullChatString+=returnMess+"\n"
        sendEmail(fullChatString)
        makeCall(fullChatString)
        sendSMS(fullChatString)
        insert(strName, fullChatString)
        conndb.commit()
        conn.send(returnMess.encode())
        conn.close()
        quit()
        
  print ("Message from User to Chatbot : " + str(receiveMess + "."))
  #set return message
  fullChatString+=receiveMess+"\n"
  fullChatString+=returnMess+"\n"
  sendEmail(fullChatString)
  insert(strName, fullChatString)
  conndb.commit()
  conn.send(returnMess.encode())
  returnMess="blank"
  #end cycle
conn.close()                

def saveToDatabase():
    
    c = conndb.cursor()
    
    # Insert a row of data
    query = [strName, fullChatString]
    c.execute("INSERT INTO chatLog(name, fullChatString) values (?, ?)", query)
    
    # Save (commit) the changes
    conndb.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conndb.close()
#def CheckForAnswer(): #FUNCTION TO FIND OUT THE QUESTIONS FOR THE BOT TO SEND
