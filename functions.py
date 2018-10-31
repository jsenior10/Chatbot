import ftplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import xml.etree.ElementTree as ET
import json
def CheckWords(sentence):
  print("function checkwords")
  print("checking sentence", sentence)
  #looks for keywords in sentence and creates a list with the possibilities
  with open('conf.json') as data_file:
    data = json.load(data_file)
  availableL=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  availableLaux=[]
  idx=0
  List = list(data["AMBULANCE"])
  List = sorted(List)
    
  for item in data["AMBULANCE"]:                            #Verify each list of the json inside the ambulance category.                             
    for item2 in data["AMBULANCE"][item]:                 #Verify each item inside each list inside the ambulance category.
      if item2 in sentence and item not in availableLaux:  #Verify if the sentece contains the word but the list doesn't contain its category.
        availableL[List.index(item)]=1                               #Append the list name to the new list.
        availableLaux.append(item)
    idx=idx+1
              
  for item in data["FIREDEP"]:                                 
    if item.lower() in sentence and item not in availableL:
      availableL.append("Fire")   
  
  return availableL


 #Every function returns confirmation question that is then sent to the user
def CoInhalation():   
    return "Has the victim inhalated CO2? yes/no: "

def AnimalBite():
    return "Was the victim bitten by an animal? yes/no: "

def Stabbing():
    return "Was the victim stabbed? yes/no: "

def Shooting():
    return "Was the victim shot? yes/no: "

def HeatColdExposure():
  return "Was the victim exposed to extreme cold/heat? yes/no: "

def AttemptedSuicide():
  return "Did the victim try to kill themself? yes/no: "

def Choking():
    return "Is the victim choking? yes/no: "

def Fire():
	return "Is there an active fire? yes/no: "
	
def Laceration():
	return "Does the victim have an injury/laceration? yes/no: "
	
def Headache():
	return "Does the victim have a strong headache? yes/no: "
	
def Pregnancy():
	return "Is the victim giving birth to a child? yes/no: "

def AllergicReaction():
	return "Is the victim having an allergic reaction? yes/no: "
	
def Assault():
	return "Is the victim under assault? yes/no: "
	
def BackPain():
	return "Is the victim suffering with back pain? yes/no: "

def CardiacArrest():
	return "Is the victim under cardiac arrest? yes/no: "
	
def Diabetic():
	return "Is the victim suffering from diabetes? yes/no: "

def Unknown():
	return "Is the victim having symptoms you do not recognize? yes/no: "

def Overdose():
	return "Is the victim having an overdose? yes/no: "
	
def Hemorrhage():
	return "Does the victim have a hemorrhage? yes/no: "

def Pain():
	return "Is the victim feeling any pain? yes/no: "
	
def Seizure():
	return "Is the victim having a seizure? yes/no: "

def UnconsciousPerson():
	return "Is the victim uncounscious? yes/no: "
	
def ChestPain():
	return "Is the victim having chest pain? yes/no: "
	
def VehicleAccidents():
	return "Is the victim in a vehicle accident? yes/no: "

def FallInjured():
	return "Did the victim fall or injure themself? yes/no: "

def BreathingDifficulty():
	return "Is the victim having difficulty breathing? yes/no: "



#communications functions

def sendEmail(fullChatString):
    emailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465) #connects to Gmails email server securely
    #emailReceiver = input("Who will receive the email?\n")
    emailReceiver = "jacobsenior4@gmail.com"
    emailServer.login("emailsendtestjeff@gmail.com", "Jeffjeffjeff") #logs in with provided email and password

    emergency = fullChatString
    msg = MIMEMultipart('alternative')   #sets up the email so it has correct formatting
    msg['Subject'] = "Emergency Alert"
    msg['From'] = "Emergency Alert"
    msg['To'] = emailReceiver
    textBody = emergency

    part1 = MIMEText(textBody, 'plain') #makes sure the email is in text format rather than HTML
    msg.attach(part1)

    emailServer.sendmail("emailsendtestjeff@gmail.com", emailReceiver, msg.as_string())
    print("Email sent.")
    return ""


def sendSMS(fullChatString):
    accountID = "AC2f6a06aafd4f136f623c0e53a489e408"
    authKey = "58f18f90b5161191a30ede8cbead1447" #account authentication for the SMS and phone call API
    client = Client(accountID, authKey)
    message = fullChatString
    client.api.account.messages.create(
    to = "+447460489566",
    from_ = "+447481345615",
    body = message)
    print("SMS sent.")
    return ""

def makeCall(fullChatString): #this function also edits the textToSpeech.xml file and uploads the file to a server via ftp so that the API is able to read it
    accountID = "AC2f6a06aafd4f136f623c0e53a489e408"
    authKey = "58f18f90b5161191a30ede8cbead1447" #account authentication for the SMS and phone call API
    client = Client(accountID, authKey)
    
    ftpConnection = ftplib.FTP("jacobsenior.coventry.domains", "jacobsen", "WtYm76iy47") #establishes the connection to the server via FTP with the details provided
    question = fullChatString
    tree = ET.parse('textToSpeech.xml')
    root = tree.getroot()
    for say in root.iter('Say'):
        newSay = question
        say.text = newSay
    tree.write('textToSpeech.xml')
    remotePath = "/www/"
    ftpConnection.cwd(remotePath)
    fh = open("textToSpeech.xml", 'rb')
    ftpConnection.storbinary('STOR textToSpeech.xml', fh)
    fh.close

    makeCall = client.api.account.calls.create(
    to = "+447460489566", #sends to my phone number right now, could be easily changed to send to others but the API requires phone numbers to be verified when using a free account
    from_ = "+447481345615",
    url = "http://jacobsenior.coventry.domains/textToSpeech.xml") 
    print("Phone call made.")
    return ""