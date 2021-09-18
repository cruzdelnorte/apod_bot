"""
Requiere ejecutarse a la hora deseada mediante una tarea cron.
"""

# Librerías
import telegram
import requests

# Inicializamos bot
# Añadir token. Eliminado por seguridad
bot = telegram.Bot(token='')
updates = bot.get_updates()

#hacemos algo
def fetchAPOD(date):
    URL_APOD = "https://api.nasa.gov/planetary/apod"
    params = {
        'api_key':'',
        'date':date,
        'hd':'True'
        }
    response = requests.get(URL_APOD,params=params).json()
    return(response)

#API NASA Token
api_nasa_token = "" 
fecha = ''
APOD_obtenido = fetchAPOD(fecha)

def makeintro(APOD):
    intro_1 = 'La Imagen Astronómica del Día (APOD) de {date} '.format(date=APOD['date'])
    #intro_2 = '{media_type} '.format(media_type=APOD['media_type'])
    if 'copyright' in APOD:
        intro_3 = 'de {autor} '.format(autor=APOD['copyright'])
    else:
        intro_3 = ''
    intro_4 = 'tiene por título "{title}"'.format(title=APOD['title'])
    return intro_1 + intro_3 + intro_4

intro = makeintro(APOD_obtenido)

if APOD_obtenido['media_type'] == 'video':
    imagen = APOD_obtenido['url']
else:
    imagen = APOD_obtenido['hdurl']
    
resumen = APOD_obtenido['explanation']
enlace = 'https://apod.nasa.gov/apod/ap' + APOD_obtenido['date'].replace('-','')[2:] + '.html'
#Enviamos mensajes en Telegram
chat_id=-582402090
bot.send_message(text=intro, chat_id=chat_id)
bot.send_message(text=imagen, chat_id=chat_id)
bot.send_message(text=resumen, chat_id=chat_id)
bot.send_message(text=enlace, chat_id=chat_id)
