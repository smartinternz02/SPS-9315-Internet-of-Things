import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json
from playsound import playsound
from pygame import mixer
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#Provide your IBM Watson Device Credentials
organization = "8s8b0k"
deviceType = "IOTDEVICE"
deviceId = "3007"
authMethod = "token"
authToken = "mission123"


# Initialize the device client.
T=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='CRYING':
                api=IAMAuthenticator("H52pfbRJJrWrU-82BPYb8oCMWVMJJL_0HK7QhC1QHXe7")
                text_2_speech= TextToSpeechV1(authenticator = api)
                text_2_speech.set_service_url("https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/b265e0ba-7854-44ba-8087-9ea63b2b6ce2")
                with open("welcome.mp3","wb") as audiofile:
                        audiofile.write(text_2_speech.synthesize("The Baby is Crying ,Play the song ,and Switch on the swing and set the speed of the swing",accept="audio/mp3").get_result().content)
                playsound("C:\\Users\\asus\\Downloads\\welcome.mp3")
                
                print("PLAY THE MUSIC")
                print("TURN ON THE SWING AND SET THE SPEED")
                mixer.init() #Initialzing pyamge mixer
                mixer.music.load('C:\\Users\\asus\\Downloads\\lullabygoodnight.mp3') #Loading Music File
                mixer.music.play()
                
        elif cmd.data['command']=='STOPPED':
                print("STOP THE MUSIC")
                mixer.music.stop()  #command to stop the music File.
                print("TURN OFF THE SWING")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        T=95
        
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'temperature' : T}}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % T, "to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
