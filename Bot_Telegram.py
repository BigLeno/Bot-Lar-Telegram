from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
import requests
import os
import json

#Se for usar uma VM, tenha certeza que ela aceita o Switch case
#Para ter certeza, ten que usar if, elif e else

#Caminho do diretório que estão os arquivos
caminho = '/diretorio/do/BOT/'
nomeBOT = '@nomeBOT'

def abredicesar ():
    """Função que abre o configuracoes.json"""
    with open(f'{caminho}configuracoes.json') as file:    #Abre o arquivo
        data = json.load(file)
        
    return data

def Token ():
	"""Função que abre o token.json"""
	tk_config = open(f'{caminho}token.json')

	tk_cf = json.load(tk_config)

	tk_config.close()

	token = tk_cf["token"]

	return token

def escrevejson (data):
    """Função que escreve no configuracoes.json"""
    with open(f'{caminho}configuracoes.json', 'w', encoding='utf-8') as file:   #Abre o arquivo no modo escrita "Write"#
     json.dump(data, file, indent=4)

def carachacha ():
    """Função que cria um vetor com os nomes dos usuários"""
    perfil = []
    with open(f'{caminho}configuracoes.json', 'r', encoding='utf-8') as arquivo:  #Abre o arquivo em modo leitura "Read"#
        data = json.load(arquivo)
        for i in data['Administradores']:
            perfil.append(i['usuario'])
    return perfil


def abreultima ():
    """Função que abre o ultima.json"""
    with open(f'{caminho}ultima.json', 'r', encoding='utf-8') as file:    #Abre o arquivo
        ultima = json.load(file)
    return ultima

def adiciona (data, name):
    """Função responsável por adicionar usuários ao JSON"""

    new_user = {"usuario": name}
    data['Integrantes'].append(new_user)
    escrevejson(data)  

def remove (data, name):
    """Função responsável por adicionar usuários ao JSON"""
    
    for k in data['Integrantes']:
        if k["usuario"] == name:
            old_user = {"usuario": k["usuario"]}
                    
    for j, l in enumerate(data["Integrantes"]):

        if old_user['usuario'] == l['usuario']:
            data['Integrantes'].pop(j)
            escrevejson(data)

def achaeshow (nome):
    """Função que cria um vetor com os nomes dos usuários"""
    show = []
    with open(f'{caminho}configuracoes.json', 'r', encoding='utf-8') as arquivo:  #Abre o arquivo em modo leitura "Read"#
        data = json.load(arquivo)

        if nome == "admin":
            for i in data["Administradores"]:
                show.append(i['usuario'])
        elif nome == "prof":
            for i in data["Profs"]:
                show.append(i['usuario'])
        elif nome == "bolsistas":
            for i in data["Bolsistas"]:
                show.append(i['usuario'])
        elif nome == "integrantes":
            for i in data["Integrantes"]:
                show.append(i['usuario'])
        else:
            print("Não existe isso para ser mostrado!")
            
        return show

data = abredicesar()

ultima = abreultima()

perfil = carachacha()

token = Token()

bot = Bot(token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "inicio", "começo", "começar", "ajuda"])
async def mensagem(message: types.Message):
    mensagem = text(bold('Selecione o que deseja:'),
               '/horarios', '/bolsistas', '/ultima', '/pessoas', sep='\n')
    await message.reply(mensagem, parse_mode=ParseMode.MARKDOWN)

#funções secretas do bot

@dp.message_handler(commands=["ovo"])
async def mensagem(message: types.Message):
		await message.reply('te reiar COVIDado!')

@dp.message_handler(commands=["livia"])
async def mensagem(message: types.Message):
		await message.reply('Expulso do laboratório!')

# até agora, são estas

@dp.message_handler(commands=["pessoas", "criadores", "professores", "integrantes", "bolsistas"])
async def mensagem(message: types.Message):
    comando = (message.text).strip()

    if comando == "/pessoas" or comando == "/pessoas@LAR_UFRN_bot":
        await message.reply(f"Escolha o que deseja listar:\n/criadores\n/professores\n/bolsistas\n/integrantes")
    else:   
        comandoFormatado = (comando.replace("/", " ")).strip()
        comandoFormatado = (comandoFormatado.replace(nomeBOT, " ")).strip()
        lista = '' 
        listar = []
        if comandoFormatado == "criadores":
            comandoFormatado = "administradores"
            listar = perfil[:]
        elif comandoFormatado == "professores":
            comandoFormatado = "prof"
            listar = achaeshow(comandoFormatado)
        elif  comandoFormatado == "bolsistas":
            comandoFormatado = "bolsistas"
            listar = achaeshow(comandoFormatado)
            chatIDpessoa=message.chat.id
            msg = "Horário dos bolsistas"
            img = open(f"{caminho}horarioBolsista.png", 'rb')
            telegram_msg = requests.get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
        elif comandoFormatado == "integrantes":
            comandoFormatado = "integrantes"
            listar = achaeshow(comandoFormatado)
        else:
            await message.reply("Não existe esta categoria para ser mostrado!")

            
        for i in listar:
            lista = (lista + "@" + i +"\n")
        await message.reply(f'{lista.strip()}')


@dp.message_handler(commands=["horarios"])
async def mensagem(message: types.Message):
    chatIDpessoa=message.chat.id
    msg = "Horário dos bolsistas"
    img = open(f"{caminho}horarioBolsista.png", 'rb')
    telegram_msg = requests.get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})

@dp.message_handler(lambda message: message.from_user.username not in perfil)
async def mensagem(message: types.Message):
	await message.reply('Sem permissão')
	await message.answer('Este é um bot em desenvolvimento do Laboratório de Automação e robótica. Se tiver interesse de interagir comigo, entre em contato com o laboratório!')


@dp.message_handler(lambda message: message.from_user.username in perfil, commands=["ultima"])
async def mensagem(message: types.Message):
	ultima = abreultima()
	for i in ultima["ultima"]:
		await message.reply(i)

@dp.message_handler(lambda message: message.from_user.username in perfil, commands=["foto"])
async def mensagem(message: types.Message):
	chatIDpessoa=message.chat.id
	msg = "Sharkboy e Lavagirl"
	img_uri = "https://br.web.img3.acsta.net/r_654_368/newsv7/20/11/18/19/09/4479152.jpg"
	telegram_msg = requests.get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}&photo={img_uri}')


@dp.message_handler(lambda message: message.from_user.username in perfil, commands=["add"])
async def mensagem(message: types.Message):
    comando = (message.text).strip()
    
    if comando == "/add" or comando == "/add@LAR_UFRN_bot":
        await message.reply(f"Escreva após /add o nome do usuário do telegram que deseja adicionar.")
    else:
        data = abredicesar()
        comandoFormatado = (comando.replace("/add", " ")).strip()
        adiciona(data, comandoFormatado)
        await message.reply(f"O usuario @'{comandoFormatado}' foi adicionado com sucesso!")

@dp.message_handler(lambda message: message.from_user.username in perfil, commands=["remove"])
async def mensagem(message: types.Message):
    comando = (message.text).strip()
    
    if comando == "/remove" or comando == "/remove@LAR_UFRN_bot":
        await message.reply(f"Escreva após /remove o nome do usuário do telegram que deseja remover.")
    else:
        data = abredicesar()
        comandoFormatado = (comando.replace("/remove", " ")).strip()
        remove(data, comandoFormatado)
        await message.reply(f"O usuario @'{comandoFormatado}' foi removido com sucesso!")

executor.start_polling(dp)
