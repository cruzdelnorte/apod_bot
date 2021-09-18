from telegram.ext import Updater
from telegram.ext import CommandHandler
from astropy.coordinates import SkyCoord
import urllib.request
from astromaterial import *
'''
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
'''
# Utilidades
def visual_fov_calc(entrada):
    '''
    Guarda imagen de un objeto conforme al campo abarcado combinación ocular y telescopio.
    '''
    # Datos imagen
    survey = 'CDS/P/DSS2/color'
    dict_survey = {'CDS/P/DSS2/color':'DSS2_color'}
    width = 400
    height = 400
    formato = 'jpg'
    # Datos Equipo

    # Telescopio
    telescopio_diametro = float(entrada[0])
    telescopio_focal = float(entrada[1])
    telescopio = Telescopio(telescopio_diametro, telescopio_focal)

    # Ocular
    ocular_focal = float(entrada[2])
    ocular_fov = float(entrada[3])
    ocular = Ocular(ocular_focal, ocular_fov)

    # Equipo
    equipo = EquipoVisual(telescopio, ocular)

    # Datos objeto
    objeto = entrada[4]
    
    # Calculamos coordenadas
    sc = SkyCoord.from_name(objeto)
    objeto_ra = sc.icrs.ra.deg
    objeto_dec = sc.icrs.dec.deg

    # Obtenemos la url de la imagen
    url_base = 'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?'
    url_params_imagen = 'hips={}&width={}&height={}&format={}'.format(survey,
                                                                      width,
                                                                      height,
                                                                      formato)
    url_params_fov = '&fov={}'.format(equipo.fov())
    url_params_objeto = '&projection=TAN&coordsys=icrs&ra={}&dec={}'.format(objeto_ra,
                                                                            objeto_dec)
    url = url_base + url_params_imagen + url_params_fov + url_params_objeto

    # Nombre fichero
    nombre_fichero = 'fov_output_images/' + objeto + '_' + dict_survey[survey] + '_' + str(equipo.fov()).replace('.', 'd') + '.jpg'

    # Guardamos imagen
    urllib.request.urlretrieve(url, nombre_fichero)
    return nombre_fichero
    
# Comportamiento del Bot
## CommandHandler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola")

def fov(update, context):
    '''
    Envía una imagen de un objeto al chat generada por visual_fov_calc.
    conforme campo abarcado combinación ocular y telescopio
    '''
    if context.args == []:
        texto_info_1 = 'El comando fov devuelve una imagen de un objeto del campo abarcado '
        texto_info_2 = 'por una combinación determinada de telescopio y ocular. \n'
        texto_info_3 = 'Sintaxis (todos los parámteros separados por espacio):\n /fov diametro focal_teles focal_ocular campo_aparente_ocular objeto \n'
        texto_info_4 = 'Dimensiones en mm y campo aparente del ocular en grados. El nombre del objeto no debe contener espacios'
        texto_info = texto_info_1 + texto_info_2 + texto_info_3 + texto_info_4
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=texto_info)
    else:
        fichero_imagen = visual_fov_calc(context.args)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(fichero_imagen, 'rb'))    

def info(update, context):
    '''
    manda un mensaje explicando las funcionalidades del bot
    '''
    pass

# Datos Bot
# Añadir el token del bot. eliminado por seguridad
bot_token =''
# Activación Bot
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

## Señales

## CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

fov_handler = CommandHandler('fov', fov)
dispatcher.add_handler(fov_handler)

updater.start_polling()
