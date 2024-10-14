import flet as ft
import pygame
import os
import asyncio
from mutagen.mp3 import MP3#se hace un from para poder importar los audios en mp3

class song:
    def __init__(self,filename):
        self.filename = filename
        self.title= os.path.splitext(filename)[0]#se hace un splitexy del texto del parametro filenme y va agarra el elemento 0 ose que cunado se reprodusca solo va salir el nombre de la cancion sin el .mp3
        self.duration= self.get_duration()#se hace otro para metro para llamado duracion donde nos va poder dar la duracion de la cancion

    def get_duration(self):# es un def para poder poner la duracion de la cancion 
        audio=MP3(os.path.join("canciones",self.filename))#se pone MP3 por que se va a llamar a la carpeta canciones donde estan los audios en mp3
        return audio.info.length # se hace un return de audio info y length para que nos de el return de la duracion de la cancion 

async def main(page: ft.page):#se hace un para metro para hacer el diseño de la pantalla 
#se usa async para que a la hora de que cargue el udio lo pueda hacer en segundo plano sin que se bloque el programa
    #titulo de la app
    page.title="Reproductor de musica"
    #color de fondo de la pantalla
    page.bgcolor=ft.colors.PURPLE_900
    page.padding=20 #esta el margen de donde se va empezar a escribir
    Img1=ft.Image(src="musica.jpg")
    #se usa pygame.mixer.init() para poder reproducir musica
    pygame.mixer.init()
    #se va crear una lista donde vamos a llamar a la carpeta donde tenga los archivos mp3
    playlist=[song(f) for f in os.listdir("canciones") if f.endswith(".mp3")]#f.endswith(".mp3") es para que de vulve la cancion si solo termina en mp3

    def abrir_musica():
        pygame.mixer.music.load(os.path.join("canciones",playlist[canciones_actuales].filename))#se usa poner la carpeta de las canciones y decir que empice desde el indice 0 de la lista

    def play_pause(e):#es un para metro para que el boton tenga un cambio cundo se este reproduciendo la cancion
        if pygame.mixer_music.get_busy():#esta comprobando si el mixer esta ocupado(si se esta reproduciendo algun tipo de cancion)
           pygame.mixer.music.pause()#va ser que se pause la cancion
           boton_play.icon=ft.icons.PLAY_ARROW # va ser que el icono de play
        else:
            if pygame.mixer.music.get_pos() == -1:#este hace que cuando la cancion este en su posicion inicial si es el caso que este inicia se va ejecutar correctamente ,el -1 dice que no haya ninguna cancio en reproduccion y que este en su inicial
                abrir_musica()
                pygame.mixer.music.play()#esto va hacer que la cancion que se este reprodusiendo este en play 
            else:
                pygame.mixer.music.unpause()#si el caso contrario con este lo va a poder pausar
                boton_play.icon=ft.icons.PAUSE # va canbiar al icono pause
        page.update()
    
    def change_song(delta):#esto es para cambiar la cancion y cuntas canciones me quiero saltar
        nonlocal canciones_actuales# se toma el indice actual de la cancion
        canciones_actuales=(canciones_actuales + delta) % len (playlist)#aqui se suma las canciones que se van a saltar y se usa el modulo para cundo termine en la ultima cancion se reinicie de nuevo y lo contrario si es que estamos en la primera que se pueda reproducir la anterior
        abrir_musica()# se va a cargar la cancion con el indice actualizado
        pygame.mixer.music.play()
        update_song_info()
        boton_play.icon=ft.icons.PAUSE
        page.update()

    def update_song_info():
        song=playlist[canciones_actuales]#se crear una variable llamada song donde se va tomar la cancion actual de pendiendo de las canciones actuales
        info_cancion.value= f"{song.title}"#este es para cambiar el titulo de la cancion ya que anteriormete estba solo vacia
        duracion.value = format_time(song.duration)#este es el valor de la cancion ya que tambien estba en 0 y con esto va tener la duracion de la cancion
        tiempo.value= 0.0
        hora_actual_text.value= "00:00"
        page.update()
    
    def format_time(seconds):# este def hace que la duracion que este a segundos la cambie a minutos y segundos
        minutes , seconds=divmod(int(seconds),60) # hace que los segundos los divida en 60 segundos
        return f"{minutes:02d}:{seconds:02d}"#esto hace que el formato de los minutos tengan dos digitos , despues dos puntos(:) y los dos digitos de los segundos (00:00)

    async def update_progress():#este def hace que mientras se este ejecutando la playliste  se va ir actualizando la cancion
        while True:#dice que si esta ocupado
            if pygame.mixer.music.get_busy():
                hora_actual=pygame.mixer.music.get_pos() / 1000#el tiempo actual va se la posicion de la cancion , se divide en 1000 por esta enla posicion actual no las da en milesegundo y entos se divide en mil para que no los de segundos
                tiempo.value= hora_actual / playlist[canciones_actuales].duration#el valor de la linea de tiempo se va a canbiar por la hora actual dividida en el tiempo actual de la cancion  
                hora_actual_text.value=format_time(hora_actual)#el valor de tiempo acrual se va a un formato de tiempo de la hora actual que esta en segundos
                page.update()
            await asyncio.sleep(1)#se hace una espero de un 1 segundo es decir que se actualiza cada segundo

    canciones_actuales= 0 #se hace una variabla par decir que va empezar dende el indice 0 de las canciones
    info_cancion=ft.Text(size=50,color=ft.colors.BLUE_500)#se hace una variable con la informacion de la cancion el texto tendra un tamaño de 50 y un color azul
    hora_actual_text= ft.Text("00:00",color=ft.colors.WHITE60)#se hace la variable para donde se va a gurardar el tiempo actual y se va iniciar en un timpo de 00:00
    duracion=ft.Text("00:00",color=ft.colors.WHITE60)#es para que se vaya actualizando la duracion de la cancion
    tiempo=ft.ProgressBar(value=0.0,width=300,color="green",bgcolor="black")#se hace una linea de duracion de la cancion tiene un tamaño de 300 el color green es cundo se esta llenado la line y el color negro es para distinguir la linea 
    boton_play=ft.IconButton(icon=ft.icons.PLAY_ARROW,on_click=play_pause,icon_color=ft.colors.WHITE)#se hace un boton de play para reproducir la musica
    boton_anterior=ft.IconButton(icon=ft.icons.SKIP_PREVIOUS,on_click=lambda _:change_song(-1),icon_color=ft.colors.WHITE)#se hace un boton para regresar una cancion
    boton_siguiente=ft.IconButton(icon=ft.icons.SKIP_NEXT,on_click=lambda _:change_song(1),icon_color=ft.colors.WHITE)#se hace un boton pra poner la proxima cancion

    controls=ft.Column(#se hizo una columna paraaliner la imagen en el centro
            [ft.Row([Img1],alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([boton_anterior,boton_play,boton_siguiente],#se alinearon los botones en el centro 
                       alignment=ft.MainAxisAlignment.CENTER
                        ),
            ],#se va hacer una fila para alinear los botones y no se vean uno bajo al otro 
        )

    fila_reproductor=ft.Row([hora_actual_text,tiempo,duracion],alignment=ft.MainAxisAlignment.CENTER)#el reproductor se alineo en el centro
    
    columna=ft.Column(
        [ info_cancion,fila_reproductor,controls],
        alignment=ft.MainAxisAlignment.CENTER)

    page.add(columna)
    
    if playlist:#si la playlist estabacia se va a cargar la cancion
        abrir_musica()
        update_song_info()
        page.update()
        await update_progress()#se llama a la funcion para que se pueda actualizar
    else:
        info_cancion.value="No se encontraron canciones en la carpeta 'canciones' "# si es el caso que no va madar un error
        page.update()
ft.app(main)