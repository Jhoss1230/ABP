import flet as ft
import pygame
import os
from mutagen.mp3 import MP3 #se hace un from para poder importar los audios en mp3

async def main(page: ft.page):#se hace un para metro para hacer el diseño de la pantalla #se usa async para que a la hora de que cargue el udio lo pueda hacer en segundo plano sin que se bloque el programa
    #titulo de la app
    page.title="Reproductor de musica"
    #color de fondo de la pantalla
    page.bgcolor=ft.colors.GREEN_200
    page.padding=20
    titulo=ft.Text("Musica")

ft.app(target=main)



