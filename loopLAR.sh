#!/bin/sh
#Tempo para reiniciar o mqtt client
tempoReabrirMqtt=1

python3 /diretorio/do/BOT/Bot_MQTT.py
if [ "$?" -eq "1" ]; then
	clear
	contador=1
	while :
		do
			echo "erro na execucao, tentando executar novamente"
			if [ "$contador" -eq "$tempoReabrirMqtt" ]; then
				contador=0
				clear
				python3 /diretorio/do/BOT/Bot_MQTT.py
			else
				contador=$(($contador+1))
                        	sleep 1s
				clear
			fi
		done
fi
