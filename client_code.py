import socket

def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

def menu():
  print("**********************************************************")
  print("*                                                        *")
  print("*                        *********                       *")
  print("*                        *********                       *")
  print("*                        *********                       *")
  print("*                *************************               *")
  print("*                *************************               *")
  print("*                *************************               *")
  print("*                *************************               *")
  print("*                        *********                       *")
  print("*                        *********                       *")
  print("*                        *********                       *")
  print("*                                                        *")
  print("*                                                        *")
  print("*    Press C to Run Emergency Chatbot(open server first) *")
  print("*    Press E to exit                                     *")
  print("*                                                        *")
  print("**********************************************************")
  while True:
    ch=getchar()
    if(ch=="e"):
      quit()
    if(ch=="c"):
      break

menu()
#name=input("What is your full name?\n")
#problem=("Please describe your situation.")

#connection to ChatBot 
host = '127.0.0.1'
port = 5001	
count = 0
thisSocket = socket.socket()
thisSocket.connect((host,port))
#Reading first message to ChatBot
message = "client"
#Continue conversation with ChatBot until end is types

while message != "end":
	#send message to Chatbot
	thisSocket.send(message.encode())
	#Receive Message from ChatBot
	RMess = thisSocket.recv(1024).decode()
	#Print message from ChatBot
	print('Emergency Chatbot: '+RMess)
	#Get user message to ChatBot
	message = input("Message to  ChatBot: ")
#Close Socket
thisSocket.close()
#Display conversation is over
print("Conversation between user and ChatBot Ended")
#Check if running directly from this file


if __name__ == '__main__':
    Main()
