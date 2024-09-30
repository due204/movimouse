#!/usr/bin/env python3.11

"""
Movimouse - Mueve el mouse para evitar el apagado de los monitores, proyectores y demás.
Copyright (C) 2024 due204 <due204@gmail.com>

Este programa es software libre; puedes redistribuirlo y/o modificarlo bajo los términos de la
Licencia Pública General de GNU publicada por la Free Software Foundation, ya sea la versión 3
de la Licencia, o (a tu elección) cualquier versión posterior.

Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; incluso
sin la garantía implícita de COMERCIABILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. 
Para más detalles, consulta la Licencia Pública General de GNU.

Deberías haber recibido una copia de la Licencia Pública General de GNU junto con este programa.
Si no es así, consulta <http://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk
from pynput import Controller
from pynput.mouse import Listener
from threading import Thread
from time import sleep
from sys import platform
from random import randint

# Controlador del mouse
mouse = Controller()

sistema = platform

# Variables globales
mouse_posicion = (0, 0)            # Posición del mouse
mouse_movimiento = True            # Movimiento del mouse
detener_programa = False           # Detener ejecución
tiempo_inactivo = 10               # Tiempo por defecto en segundos
movimiento_rango = 1               # Rango de movimiento aleatorio por defecto
mouse_hilo = None                  # Hilo para iniciar la deteccion de mouse
listener = None
label_tiempo_inactivo_val = None   # Variable label del tiempo
label_rango_movimiento_val = None  # Variable label del rango

def movimiento_mouse(x, y):
    """Se activa cuando el mouse se mueve."""
    global mouse_posicion, mouse_movimiento
    mouse_posicion = (x, y)
    mouse_movimiento = True

def verificar_actividad_mouse():
    """Hilo que controla si el mouse está quieto."""
    global mouse_movimiento, detener_programa, tiempo_inactivo
    posicion_inicial = mouse_posicion
    while not detener_programa:
        if mouse_posicion == posicion_inicial:
            mouse_movimiento = False
        else:
            posicion_inicial = mouse_posicion
            mouse_movimiento = True
        
        # Si el mouse está quieto por más tiempo del configurado
        if not mouse_movimiento:
            sleep(tiempo_inactivo)
            if not mouse_movimiento:
                mover_mouse()
        sleep(1)

def mover_mouse():
    """Mueve el mouse de manera aleatoria dentro del rango configurado."""
    global movimiento_rango
    mover_x, mover_y = mouse.position
    mover_random_x = randint(-movimiento_rango, movimiento_rango)
    mover_random_y = randint(-movimiento_rango, movimiento_rango)
    mouse.position = (mover_x + mover_random_x, mover_y + mover_random_y)

def actu_tiempo_slider(value):
    """Tomar el valor del tiempo de inactividad desde el slider."""
    global tiempo_inactivo, label_tiempo_inactivo_val  # Asegura que la variable global sea accesible
    tiempo_inactivo = round(float(value))
    if label_tiempo_inactivo_val:
        label_tiempo_inactivo_val.config(text=f"{tiempo_inactivo} seg")  # Actualiza el valor en el label

def actu_movimiento_slider(value):
    """Actualiza el rango de movimiento aleatorio."""
    global movimiento_rango, label_rango_movimiento_val  # Asegura que la variable global sea accesible
    movimiento_rango = round(float(value))
    if label_rango_movimiento_val:
        label_rango_movimiento_val.config(text=f"{movimiento_rango} píxeles")  # Actualiza el valor en el label

def iniciar_():
    """Inicia o detiene el programa según el estado del botón."""
    global detener_programa, mouse_hilo
    if boton_inicio['text'] == "Iniciar":
        # Iniciar el programa
        detener_programa = False
        boton_inicio.config(text="Detener")  # Cambia el nombre al boton
        slider_tiempo_inactivo.config(state='disabled')  # Desabilita el slider
        slider_rango_movimiento.config(state='disabled')  # Desabilita el slider
        
        # Iniciar el hilo que detecta la actividad del mouse
        mouse_hilo = Thread(target=verificar_actividad_mouse)
        mouse_hilo.start()
    else:
        # Detener el programa
        detener_programa = True
        boton_inicio.config(text="Iniciar")  # Cambia el nombre al boton
        slider_tiempo_inactivo.config(state='normal')  # Habilita el slider 
        slider_rango_movimiento.config(state='normal')  # Habilita el slider


def salir_():
    """Salir sin detener el hilo programa"""
    global listener, detener_programa
    detener_programa = True  # Detener el hilo que verifica la actividad del mouse
    if listener is not None:
        listener.stop()  # Detener el listener de pynput
    root.quit()
    root.destroy()
    print("Saliendo")



# Interfaz gráfica (Tkinter)
root = tk.Tk()
root.title("Movimouse")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", salir_)

if sistema == "linux":
        logo = tk.PhotoImage(file="movimouse.gif")
        root.call("wm", "iconphoto", root._w, logo)
else:
    root.iconbitmap("movimouse.ico")

# Configurar el layout
frame_sliders = tk.Frame(root)
frame_sliders.pack(pady=10)

# Slider para el tiempo de inactividad
label_tiempo_incativo = ttk.Label(frame_sliders, text="Tiempo de inactividad:")
label_tiempo_incativo.grid(row=0, column=0, padx=5, pady=5, sticky="w")
slider_tiempo_inactivo = ttk.Scale(frame_sliders, from_=1, to=180, orient="horizontal", command=actu_tiempo_slider)
slider_tiempo_inactivo.set(tiempo_inactivo)
slider_tiempo_inactivo.grid(row=0, column=1, padx=5, pady=5)

# Label del tiempo ingresado con el slider
label_tiempo_inactivo_val = ttk.Label(frame_sliders, text=f"{tiempo_inactivo} seg")
label_tiempo_inactivo_val.grid(row=0, column=2, padx=5, pady=5)

# Slider para el rango de movimiento aleatorio
label_rango_movimiento = ttk.Label(frame_sliders, text="Rango de movimiento:")
label_rango_movimiento.grid(row=1, column=0, padx=5, pady=5, sticky="w")
slider_rango_movimiento = ttk.Scale(frame_sliders, from_=1, to=100, orient="horizontal", command=actu_movimiento_slider)
slider_rango_movimiento.set(movimiento_rango)
slider_rango_movimiento.grid(row=1, column=1, padx=5, pady=5)

# Label del tiempo ingresado con el slider
label_rango_movimiento_val = ttk.Label(frame_sliders, text=f"{movimiento_rango} píxeles")
label_rango_movimiento_val.grid(row=1, column=2, padx=5, pady=5)

# Botón de iniciar/detener el programa
boton_inicio = ttk.Button(root, text="Iniciar", command=iniciar_)
boton_inicio.pack(pady=10)

# Iniciar listener de pynput en un hilo separado
def inicio_listener():
    with Listener(on_move=movimiento_mouse) as listener:
        listener.join()

# Hilo para escuchar el movimiento del mouse
listener_thread = Thread(target=inicio_listener)
listener_thread.daemon = True
listener_thread.start()

# Ejecutar la interfaz gráfica
root.mainloop()
