from email.charset import add_charset
from re import T
import paho.mqtt.client as mqtt
import time
import requests
import json

caminho = ''

def abreultima ():
    """Função que abre o JSON"""
    with open(f'{caminho}ultima.json') as file:    #Abre o arquivo
        ultima = json.load(file)
        
    return ultima

def escreveultima (ultima):
    """Função que escreve no JSON"""
    with open(f'{caminho}ultima.json', 'w') as file:   #Abre o arquivo no modo escrita "Write"#
        json.dump(ultima, file, indent=4)

def adiciona (ultima, int):
    """Função responsável por adicionar usuários ao JSON"""
    ultima["ultima"].pop()
    ultima["ultima"].append(int)
    escreveultima(ultima)

ultima = abreultima()

TOKEN = ""
chat_id = ""


broker=""
porta= 0
subscricao=[]


def on_connect(client, userdata, flags, rc):  # The callback for when 
	print("Connected with result code {0}".format(str(rc)))
	client.subscribe(subscricao)


def on_message(client, userdata, message):
    print("tópico: " + message.topic)
    print("mensagem: " +  message.payload.decode("utf-8"))
    print("retem: " + str(message.retain))
    print("qos: " + str(message.qos))
    

    if message.topic=='canal':
        message ="Cartão aceito --> " + str(message.payload.decode("utf-8")) + " entrou no laboratório!"
        ultima = abreultima()
        adiciona(ultima, message)
        escreveultima(ultima)

    elif  message.topic=='canal':
        message ="Cartão cadastrado --> " + str(message.payload.decode("utf-8"))

    else:
	    message ="Logs/Outros --> " + str(message.payload.decode("utf-8"))

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    print(requests.get(url).json())     #This sends the message
    


client = mqtt.Client("")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.connect(broker, porta)
client.loop_forever()  # Start networking daemon
