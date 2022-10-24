#!/bin/bash

# Cria screen "LarTelegramBot"
screen -dmS LarTelegramBot
screen -dmS LarTelegramBotRESPOSTAS

#Executa o script do loop dentro da screen
screen -S LarTelegramBot -X stuff 'bash /diretorio/do/BOT/loopLAR.sh\n'
screen -S LarTelegramBotRESPOSTAS -X stuff 'python3 /diretorio/do/BOT/Bot_Telegram.py\n'
