import cv2
import mediapipe as mp

import customtkinter
import tkinter
import threading
import time
from djitellopy import Tello
import random
import pygame
from PIL import ImageTk, Image









global game_mode

global set_time_reaction
global set_game_score
global set_time_between_arrow

global app5
global app4
global save_photo

####################################### Variables information about drone #############################################
"""

'command_ended' is used to know when the command that was sent to the drone has finished. For example,
if the action is 'TAKE OFF', you won't be able to send another action until 'TAKE OFF' is finished.
"""
command_ended = True
global assign_first_time
drone_connected = False
arrow_confirmed = False
process_finished = True

global up_arrow
global down_arrow
global left_arrow
global right_arrow
global flip_left_arrow
global flip_right_arrow

global score
global wrong_pose
global time_exceeded
global winner
global timer_finished


music_on = True


easy_difficulty = False
hard_difficulty = False
impossible_difficulty = False


"""
'Frame' is used for the video of the computer camera.
'telloFrame' is used for the video of the drone camera.
"""
global frame




global takingVideo

taken_photo = False
taking_shot = False


# ####################################### Variables assign drone commands ##############################################
"""
Cuando se ponga en True la variable, significará que esa función ya
ha sido asignada y por tanto, no se podrá volver a asignar
"""
TAKE_OFF_assigned = False
LAND_assigned = False
MOVE_UP_assigned = False
MOVE_DOWN_assigned = False
MOVE_FORWARD_assigned = False
MOVE_BACK_assigned = False
MOVE_LEFT_assigned = False
MOVE_RIGHT_assigned = False
ROTATE_CLOCKWISE_assigned = False
ROTATE_COUNTER_CLOCKWISE_assigned = False
FLIP_FORWARD_assigned = False
FLIP_BACK_assigned = False
FLIP_LEFT_assigned = False
FLIP_RIGHT_assigned = False

TAKE_OFF_pose_number = 0
LAND_pose_number = 0
MOVE_UP_pose_number = 0
MOVE_DOWN_pose_number = 0
MOVE_FORWARD_pose_number = 0
MOVE_BACK_pose_number = 0
MOVE_LEFT_pose_number = 0
MOVE_RIGHT_pose_number = 0
ROTATE_CLOCKWISE_pose_number = 0
ROTATE_COUNTER_CLOCKWISE_pose_number = 0
FLIP_FORWARD_pose_number = 0
FLIP_BACK_pose_number = 0
FLIP_LEFT_pose_number = 0
FLIP_RIGHT_pose_number = 0


######################################## Variables assign drone commands ##############################################



####################################### Pose variables ##############################################################
"""
'counter_pose' is the counter of how many poses has been added.
'captured_pose_number' is the number of the pose that has been done when you are playing with the drone
'pose_number' is the number of a registered pose. It is only used when you want to MODIFY the pose of a command and it
changes constantly.
"""
counter_pose = 0
captured_pose_number = 0
pose_number = 0
####################################### Pose variables ##############################################################


diccionario_principal = {}


lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame



####################################################### LISTAS ####################################################
lista_LEFT_SHOULDER_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
lista_LEFT_SHOULDER_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame



#################################### Variables Mediapipe ##############################################################
mp_drawing = mp.solutions.drawing_utils  # nos ayudará a dibujar los resultados de las detecciones, los 33 puntos y
# conexiones

mp_hands = mp.solutions.hands

mp_pose = mp.solutions.pose
#################################### Variables Mediapipe ##############################################################






####################################################### DICCIONARIOS ##############################################
LEFTHAND_diccionario_principal = {}
RIGHTHAND_diccionario_principal = {}

LEFTHAND_diccionario_FRAME = {}
RIGHTHAND_diccionario_FRAME = {}
# Crearemos subdiccionarios

####################################################### LISTAS ####################################################
LEFTHAND_lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
LEFTHAND_lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
RIGHTHAND_lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
RIGHTHAND_lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame












global tello

global ErrorWindow
global Error_text
global OK_button

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def quit_ERROR_WINDOW():
    global ErrorWindow

    time.sleep(1)
    ErrorWindow.quit()


def destroy_ERROR_WINDOW():
    global ErrorWindow

    ErrorWindow.destroy()


def Error_Window():
    global ErrorWindow
    global Error_text
    global OK_button

    ErrorWindow = customtkinter.CTk()
    ErrorWindow.resizable(False, False)
    ErrorWindow.title("ERROR")
    Error_text = customtkinter.CTkLabel(ErrorWindow)
    Error_text.place(x=0, y=0)
    Error_text.configure(padx=20, pady=10)

    OK_button = customtkinter.CTkButton(ErrorWindow, text="OK", command=destroy_ERROR_WINDOW)
    OK_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5", font=("Arial black", 15),
                        border_color="#374BB5", border_width=4)



def connect_drone():
    global tello
    global drone_connected
    if drone_connected is False:
        drone_connected = True
        tello = Tello()
        tello.connect()

        print('BATTERY: ', tello.get_battery())

    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("200x80+587+505")
        Error_text.configure(text="Drone is already connected.",
                             font=("Helvetica", 15))

        OK_button.place(x=30, y=40)
        ErrorWindow.mainloop()





############################################ HELPFUL FUNCTIONS #######################################################
def show_photos():

    global counter_pose

    if counter_pose == 0:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("300x80+587+505")
        Error_text.configure(text="There are no poses registered.",
                             font=("Helvetica", 20))

        OK_button.place(x=75, y=40)
        ErrorWindow.mainloop()

    else:
        contador2 = 0
        contador3 = 0
        contador4 = 0

        for i in range(counter_pose):
            nombre_archivo = f"POSE_{i}.jpg"
            if i < 4:
                ####################### Mostrar fotos en ventanas de manera ordenada ##############################
                window_x_image = 1592
                window_y_image = 0 + contador2

                contador2 += 255
                # Define el ancho y alto de la ventana
                window_width_image = 322
                window_height_image = 244

            elif i >= 4 and i < 8:
                ####################### Mostrar fotos en ventanas de manera ordenada ##############################
                window_x_image = 1270
                window_y_image = 0 + contador3

                contador3 += 255
                # Define el ancho y alto de la ventana
                window_width_image = 322
                window_height_image = 244

            elif i >= 8:
                ####################### Mostrar fotos en ventanas de manera ordenada ##############################
                window_x_image = 948
                window_y_image = 0 + contador4

                contador4 += 255
                # Define el ancho y alto de la ventana
                window_width_image = 322
                window_height_image = 244

            # Define la posición de la ventana en la pantalla
            cv2.namedWindow(nombre_archivo, cv2.WINDOW_NORMAL)
            cv2.moveWindow(nombre_archivo, window_x_image, window_y_image)
            cv2.resizeWindow(nombre_archivo, window_width_image, window_height_image)
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            image = cv2.imread(nombre_archivo)
            cv2.imshow(nombre_archivo, image)

def close_photos():
    cv2.destroyAllWindows()
############################################ HELPFUL FUNCTIONS ########################################################

#######################################################################################################################
#######################################################################################################################

############################################ ASSIGN COMMANDS ##########################################################
def assign_commands():
    close_photos()
    global assign_first_time
    assign_first_time = True

    app2 = customtkinter.CTk()
    app2.title("Assign Commands")
    app2.geometry("200X200")


    app2.resizable(False, False)

    # Calcular las coordenadas para centrar la ventana
    x = 691
    y = 500

    # Establecer las coordenadas de la ventana
    app2.geometry(f"+{x}+{y}")

    customtkinter.set_appearance_mode("dark")



    if hard_difficulty is True or impossible_difficulty is True:
        Move_UP_button = customtkinter.CTkButton(app2, text="MOVE_UP", command=assign_MOVE_UP)
        Move_UP_button.grid(row=0, column=0, padx=20, pady=20)
        Move_UP_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3, font=("Arial black", 15))

        Move_DOWN_button = customtkinter.CTkButton(app2, text="MOVE_DOWN", command=assign_MOVE_DOWN)
        Move_DOWN_button.grid(row=0, column=1, padx=20, pady=20)
        Move_DOWN_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

        Move_LEFT_button = customtkinter.CTkButton(app2, text="MOVE_LEFT", command=assign_MOVE_LEFT)
        Move_LEFT_button.grid(row=1, column=0, padx=20, pady=20)
        Move_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

        Move_RIGHT_button = customtkinter.CTkButton(app2, text="MOVE_RIGHT", command=assign_MOVE_RIGHT)
        Move_RIGHT_button.grid(row=1, column=1, padx=20, pady=20)
        Move_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

        Flip_LEFT_button = customtkinter.CTkButton(app2, text="FLIP_LEFT", command=assign_FLIP_LEFT)
        Flip_LEFT_button.grid(row=2, column=0, padx=20, pady=20)
        Flip_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

        Flip_RIGHT_button = customtkinter.CTkButton(app2, text="FLIP_RIGHT", command=assign_FLIP_RIGHT)
        Flip_RIGHT_button.grid(row=2, column=1, padx=20, pady=20)
        Flip_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

    else:
        Move_UP_button = customtkinter.CTkButton(app2, text="MOVE_UP", command=assign_MOVE_UP)
        Move_UP_button.grid(row=0, column=0, padx=20, pady=20)
        Move_UP_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                 border_width=3, font=("Arial black", 15))

        Move_DOWN_button = customtkinter.CTkButton(app2, text="MOVE_DOWN", command=assign_MOVE_DOWN)
        Move_DOWN_button.grid(row=0, column=1, padx=20, pady=20)
        Move_DOWN_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                   border_width=3,
                                   font=("Arial black", 15))

        Move_LEFT_button = customtkinter.CTkButton(app2, text="MOVE_LEFT", command=assign_MOVE_LEFT)
        Move_LEFT_button.grid(row=1, column=0, padx=20, pady=20)
        Move_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                   border_width=3,
                                   font=("Arial black", 15))

        Move_RIGHT_button = customtkinter.CTkButton(app2, text="MOVE_RIGHT", command=assign_MOVE_RIGHT)
        Move_RIGHT_button.grid(row=1, column=1, padx=20, pady=20)
        Move_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                    border_width=3,
                                    font=("Arial black", 15))




    app2.mainloop()



def assign_MOVE_UP():
    close_photos()
    global MOVE_UP_assigned
    global diccionario_principal
    global counter_pose
    global MOVE_UP_pose_number


    if MOVE_UP_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()

            take_info_from_captures_ONE_HAND()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_UP"

            MOVE_UP_pose_number = counter_pose
            MOVE_UP_assigned = True
            counter_pose += 1

        elif game_mode == "TWO_HANDS":

            information_about_taking_a_shot()

            take_info_from_captures_TWO_HANDS()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_UP"

            MOVE_UP_pose_number = counter_pose
            MOVE_UP_assigned = True
            counter_pose += 1

        elif game_mode == "BODY_POSE":

            information_about_taking_a_shot()

            take_info_from_captures_BODY_POSE()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_UP"

            MOVE_UP_pose_number = counter_pose
            MOVE_UP_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("455x80+587+505")
        Error_text.configure(text="MOVE UP command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=150, y=40)
        ErrorWindow.mainloop()

def assign_MOVE_DOWN():
    close_photos()
    global MOVE_DOWN_assigned
    global diccionario_principal
    global counter_pose
    global MOVE_DOWN_pose_number


    if MOVE_DOWN_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_DOWN"

            MOVE_DOWN_pose_number = counter_pose
            MOVE_DOWN_assigned = True
            counter_pose += 1


        elif game_mode == "TWO_HANDS":
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_DOWN"

            MOVE_DOWN_pose_number = counter_pose
            MOVE_DOWN_assigned = True
            counter_pose += 1



        elif game_mode == "BODY_POSE":
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()

            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_DOWN"

            MOVE_DOWN_pose_number = counter_pose
            MOVE_DOWN_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("495x80+587+505")
        Error_text.configure(text="MOVE DOWN command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=170, y=40)
        ErrorWindow.mainloop()

def assign_MOVE_LEFT():
    close_photos()
    global MOVE_LEFT_assigned
    global diccionario_principal
    global counter_pose
    global MOVE_LEFT_pose_number


    if MOVE_LEFT_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)



            cv2.imwrite(nombre_archivo, frame)



            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_LEFT"

            MOVE_LEFT_pose_number = counter_pose
            MOVE_LEFT_assigned = True
            counter_pose += 1


        elif game_mode == "TWO_HANDS":
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_LEFT"

            MOVE_LEFT_pose_number = counter_pose
            MOVE_LEFT_assigned = True
            counter_pose += 1



        elif game_mode == "BODY_POSE":
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_LEFT"

            MOVE_LEFT_pose_number = counter_pose
            MOVE_LEFT_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("485x80+587+505")
        Error_text.configure(text="MOVE LEFT command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=164, y=40)
        ErrorWindow.mainloop()

def assign_MOVE_RIGHT():
    close_photos()
    global MOVE_RIGHT_assigned
    global diccionario_principal
    global counter_pose
    global MOVE_RIGHT_pose_number


    if MOVE_RIGHT_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)



            cv2.imwrite(nombre_archivo, frame)



            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_RIGHT"

            MOVE_RIGHT_pose_number = counter_pose
            MOVE_RIGHT_assigned = True
            counter_pose += 1



        elif game_mode == "TWO_HANDS":
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_RIGHT"

            MOVE_RIGHT_pose_number = counter_pose
            MOVE_RIGHT_assigned = True
            counter_pose += 1



        elif game_mode == "BODY_POSE":
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "MOVE_RIGHT"

            MOVE_RIGHT_pose_number = counter_pose
            MOVE_RIGHT_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("485x80+587+505")
        Error_text.configure(text="MOVE RIGHT command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=164, y=40)
        ErrorWindow.mainloop()

def assign_FLIP_LEFT():
    close_photos()
    global FLIP_LEFT_assigned
    global diccionario_principal
    global counter_pose
    global FLIP_LEFT_pose_number


    if FLIP_LEFT_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_LEFT"

            FLIP_LEFT_pose_number = counter_pose
            FLIP_LEFT_assigned = True
            counter_pose += 1



        elif game_mode == "TWO_HANDS":
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_LEFT"

            FLIP_LEFT_pose_number = counter_pose
            FLIP_LEFT_assigned = True
            counter_pose += 1



        elif game_mode == "BODY_POSE":
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_LEFT"

            FLIP_LEFT_pose_number = counter_pose
            FLIP_LEFT_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("475x80+587+505")
        Error_text.configure(text="FLIP LEFT command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=158, y=40)
        ErrorWindow.mainloop()

def assign_FLIP_RIGHT():
    close_photos()
    global FLIP_RIGHT_assigned
    global diccionario_principal
    global counter_pose
    global FLIP_RIGHT_pose_number

    if FLIP_RIGHT_assigned is False:
        if game_mode == "ONE_HAND":
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_RIGHT"

            FLIP_RIGHT_pose_number = counter_pose
            FLIP_RIGHT_assigned = True
            counter_pose += 1



        elif game_mode == "TWO_HANDS":
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_RIGHT"

            FLIP_RIGHT_pose_number = counter_pose
            FLIP_RIGHT_assigned = True
            counter_pose += 1



        elif game_mode == "BODY_POSE":
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{counter_pose}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)

            pose = "pose_" + str(counter_pose)
            diccionario_principal[pose] = "FLIP_RIGHT"

            FLIP_RIGHT_pose_number = counter_pose
            FLIP_RIGHT_assigned = True
            counter_pose += 1

    else:
        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
        close_window_thread.start()
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("475x80+587+505")
        Error_text.configure(text="FLIP RIGHT command has been already assigned.",
                             font=("Helvetica", 20))

        OK_button.place(x=158, y=40)
        ErrorWindow.mainloop()

############################################ ASSIGN COMMANDS ##########################################################

#######################################################################################################################
#######################################################################################################################

############################################ MODIFY COMMANDS ##########################################################
def modify_commands():
    close_photos()
    global assign_first_time
    assign_first_time = False

    app2 = customtkinter.CTk()
    app2.title("Modify Commands")
    app2.geometry("200X200")

    app2.resizable(False, False)
    # Calcular las coordenadas para centrar la ventana
    x = 675
    y = 500

    # Establecer las coordenadas de la ventana
    app2.geometry(f"+{x}+{y}")

    customtkinter.set_appearance_mode("dark")

    if hard_difficulty is True or impossible_difficulty is True:
        Move_UP_button = customtkinter.CTkButton(app2, text="MOVE_UP", command=modify_MOVE_UP)
        Move_UP_button.grid(row=0, column=0, padx=20, pady=20)
        Move_UP_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                 font=("Arial black", 15))

        Move_DOWN_button = customtkinter.CTkButton(app2, text="MOVE_DOWN", command=modify_MOVE_DOWN)
        Move_DOWN_button.grid(row=0, column=1, padx=20, pady=20)
        Move_DOWN_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                   font=("Arial black", 15))

        Move_LEFT_button = customtkinter.CTkButton(app2, text="MOVE_LEFT", command=modify_MOVE_LEFT)
        Move_LEFT_button.grid(row=1, column=0, padx=20, pady=20)
        Move_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                   font=("Arial black", 15))

        Move_RIGHT_button = customtkinter.CTkButton(app2, text="MOVE_RIGHT", command=modify_MOVE_RIGHT)
        Move_RIGHT_button.grid(row=1, column=1, padx=20, pady=20)
        Move_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white", border_width=3,
                                    font=("Arial black", 15))

        Flip_LEFT_button = customtkinter.CTkButton(app2, text="FLIP_LEFT", command=modify_FLIP_LEFT)
        Flip_LEFT_button.grid(row=2, column=0, padx=20, pady=20)
        Flip_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                   border_width=3,
                                   font=("Arial black", 15))

        Flip_RIGHT_button = customtkinter.CTkButton(app2, text="FLIP_RIGHT", command=modify_FLIP_RIGHT)
        Flip_RIGHT_button.grid(row=2, column=1, padx=20, pady=20)
        Flip_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                    border_width=3,
                                    font=("Arial black", 15))

    else:
        Move_UP_button = customtkinter.CTkButton(app2, text="MOVE_UP", command=modify_MOVE_UP)
        Move_UP_button.grid(row=0, column=0, padx=20, pady=20)
        Move_UP_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                 border_width=3,
                                 font=("Arial black", 15))

        Move_DOWN_button = customtkinter.CTkButton(app2, text="MOVE_DOWN", command=modify_MOVE_DOWN)
        Move_DOWN_button.grid(row=0, column=1, padx=20, pady=20)
        Move_DOWN_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                   border_width=3,
                                   font=("Arial black", 15))

        Move_LEFT_button = customtkinter.CTkButton(app2, text="MOVE_LEFT", command=modify_MOVE_LEFT)
        Move_LEFT_button.grid(row=1, column=0, padx=20, pady=20)
        Move_LEFT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                   border_width=3,
                                   font=("Arial black", 15))

        Move_RIGHT_button = customtkinter.CTkButton(app2, text="MOVE_RIGHT", command=modify_MOVE_RIGHT)
        Move_RIGHT_button.grid(row=1, column=1, padx=20, pady=20)
        Move_RIGHT_button.configure(text_color="white", fg_color="#B32028", hover_color="#75151A", border_color="white",
                                    border_width=3,
                                    font=("Arial black", 15))

    app2.mainloop()


def modify_MOVE_UP():
    close_photos()
    global MOVE_UP_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if MOVE_UP_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = MOVE_UP_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = MOVE_UP_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = MOVE_UP_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE UP"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:

        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("355x80+587+505")
        Error_text.configure(text="MOVE UP command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=98, y=40)
        ErrorWindow.mainloop()

def modify_MOVE_DOWN():
    close_photos()
    global MOVE_DOWN_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if MOVE_DOWN_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = MOVE_DOWN_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = MOVE_DOWN_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = MOVE_DOWN_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE DOWN"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("373x80+587+505")
        Error_text.configure(text="MOVE DOWN command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=105, y=40)
        ErrorWindow.mainloop()

def modify_MOVE_LEFT():
    close_photos()
    global MOVE_LEFT_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if MOVE_LEFT_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = MOVE_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = MOVE_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = MOVE_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("368x80+587+505")
        Error_text.configure(text="MOVE LEFT command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=100, y=40)
        ErrorWindow.mainloop()

def modify_MOVE_RIGHT():
    close_photos()
    global MOVE_RIGHT_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if MOVE_RIGHT_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = MOVE_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = MOVE_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = MOVE_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "MOVE RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("375x80+587+505")
        Error_text.configure(text="MOVE RIGHT command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=102, y=40)
        ErrorWindow.mainloop()

def modify_FLIP_LEFT():
    close_photos()
    global FLIP_LEFT_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if FLIP_LEFT_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = FLIP_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = FLIP_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = FLIP_LEFT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP LEFT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("357x80+587+505")
        Error_text.configure(text="FLIP LEFT command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=102, y=40)
        ErrorWindow.mainloop()

def modify_FLIP_RIGHT():
    close_photos()
    global FLIP_RIGHT_assigned
    global diccionario_principal
    global counter_pose
    global pose_number

    if FLIP_RIGHT_assigned is True:
        if game_mode == "ONE_HAND":
            pose_number = FLIP_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_ONE_HAND()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


        elif game_mode == "TWO_HANDS":
            pose_number = FLIP_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_TWO_HANDS()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)




        elif game_mode == "BODY_POSE":
            pose_number = FLIP_RIGHT_pose_number
            information_about_taking_a_shot()
            take_info_from_captures_BODY_POSE()
            # Guardar imagen
            nombre_archivo = f"POSE_{pose_number}.jpg"

            name = "FLIP RIGHT"
            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)

            # Calcular las coordenadas del rectángulo del fondo
            text_x = 10
            text_y = 50
            background_x = text_x - 17
            background_y = text_y - text_size[1] - 20
            background_width = text_size[0] + 20
            background_height = text_size[1] + 30

            # Dibujar el rectángulo de fondo
            cv2.rectangle(frame, (background_x, background_y),
                          (background_x + background_width, background_y + background_height), (0, 0, 0), -1)

            # Agregar el texto
            cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            cv2.imwrite(nombre_archivo, frame)


    else:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("360x80+587+505")
        Error_text.configure(text="FLIP RIGHT command hasn't been already assigned.",
                             font=("Helvetica", 15))

        OK_button.place(x=104, y=40)
        ErrorWindow.mainloop()
############################################ MODIFY COMMANDS ##########################################################

#######################################################################################################################
#######################################################################################################################

########################################### TAKE INFO #################################################################
def close_app4():
    global app4
    app4.destroy()
    app4.quit()

def information_about_taking_a_shot():
    global app4
    app4 = customtkinter.CTk()
    app4.title("Information")
    app4.geometry("394x80+690+300")

    customtkinter.set_appearance_mode("dark")


    app4.resizable(False, False)

    if game_mode == 'ONE_HAND':
        my_text = customtkinter.CTkLabel(app4, text="To take a shot, press the key 'Space'.",
                                         font=("Helvetica", 23))
        app4.geometry("394x80+690+300")
        my_text.place(x=0, y=0)
        my_text.configure(text_color='white', padx=20)

        Go_button = customtkinter.CTkButton(app4, text="GO", command=close_app4)
        Go_button.place(x=130, y=40)
        Go_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5", font=("Arial black", 15),
                            border_color="#374BB5", border_width=4)


    else:
        my_text = customtkinter.CTkLabel(app4, text="To take a shot, press the key 'Space' and wait 3 seconds.",
                                         font=("Helvetica", 23))
        app4.geometry("585x80+530+300")
        my_text.place(x=0, y=0)
        my_text.configure(text_color='white', padx=20)

        Go_button = customtkinter.CTkButton(app4, text="GO", command=close_app4)
        Go_button.place(x=210, y=40)
        Go_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5", font=("Arial black", 15),
                            border_color="#374BB5", border_width=4)


    app4.mainloop()

def yes_button():
    global save_photo
    save_photo = True

    global app5
    app5.destroy()
    app5.quit()

def no_button():
    global save_photo
    save_photo = False

    global app5
    app5.destroy()
    app5.quit()

def take_info_from_captures_ONE_HAND():
    close_photos()
    global counter_pose
    global lista_THUMB_TIP_x_BBDD
    global lista_THUMB_TIP_y_BBDD
    global diccionario_principal
    global frame
    global assign_first_time
    global pose_number
    global app5

    pose_captured = False

    # -----------------------------------------------------------------------------------------------------------#

    # Inicializar la cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Obtiene las dimensiones de la pantalla
    screen_width = 1920
    screen_height = 1080

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 900
    window_height_Video = 725

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Camera", window_x_Video, window_y_Video)
    cv2.resizeWindow("Camera", window_width_Video, window_height_Video)

    # Verificar que se haya abierto correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()


    # Leer imágenes de la cámara
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            frame_rgb = cv2.cvtColor(frame,
                                     cv2.COLOR_BGR2RGB)  # debemos pasar a RGB la imagen porque con BGR no puede

            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2,
                                                                     circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2))

        # Mostrar imagen en una ventana
        cv2.imshow("Camera", frame)

        # Esperar a que se presione la tecla 's' para guardar una imagen
        ######################## EN ESTE IF ES DONDE VAMOS A TRABAJAR ############################################

        if cv2.waitKey(1) == ord(" "):

            if assign_first_time is True:
                if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:


                        #################### Cogemos los puntos clave de la pose de la mano ################################
                        THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                        INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                        MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                        RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                        RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                        PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                        PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                        ######## IMPORTAAAAAAAAAAAAAAAAAAAAAAAAANTEEEEEEEEEEEEEEEEEE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
                        lista_THUMB_TIP_x_BBDD.append(THUMB_TIP_x_BBDD)
                        lista_THUMB_TIP_y_BBDD.append(THUMB_TIP_y_BBDD)
                        ######## IMPORTAAAAAAAAAAAAAAAAAAAAAAAAANTEEEEEEEEEEEEEEEEEE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #



                        #################### Cogemos los puntos clave de la pose de la mano ################################

                        ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                        lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,
                                   RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                        lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,
                                   RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                        sub_diccionario = "sub_diccionario_" + str(
                            counter_pose)  # Tendré un diccionario por cada HANDPOSE
                        sub_diccionario = {}

                        for i in range(5):
                            x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.05, lista_y[i] + 0.05
                            x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.05, lista_y[i] - 0.05

                            x1_rectangle = int(x1_rectangle_normalized * width)
                            x2_rectangle = int(x2_rectangle_normalized * width)

                            y1_rectangle = int(y1_rectangle_normalized * height)
                            y2_rectangle = int(y2_rectangle_normalized * height)

                            # Dibujamos el cuadrado en la imagen
                            #cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle), (0, 255, 0), 2)

                            lista_marginsRectangle_finger = "lista_marginsRectangle_finger_" + str(i)

                            sub_diccionario[lista_marginsRectangle_finger] = [x1_rectangle_normalized,
                                                                              x2_rectangle_normalized,
                                                                              y1_rectangle_normalized,
                                                                              y2_rectangle_normalized]

                        margins_each_HANDPOSE = "margins_each_HANDPOSE_" + str(counter_pose)
                        diccionario_principal[margins_each_HANDPOSE] = sub_diccionario
                        ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA CÁMARA
                        XMAX = max(lista_x)
                        XMIN = min(lista_x)
                        YMAX = max(lista_y)
                        YMIN = min(lista_y)

                        anchura_BBDD = XMAX - XMIN
                        altura_BBDD = YMAX - YMIN

                        rectangle_adapt_size_BBDD = "rectangle_adapt_size_BBDD_" + str(counter_pose)
                        diccionario_principal[rectangle_adapt_size_BBDD] = [anchura_BBDD, altura_BBDD]
                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        app5 = customtkinter.CTk()
                        app5.title("Save or repeat")
                        app5.geometry("360x90+200+630")

                        customtkinter.set_appearance_mode("dark")


                        app5.resizable(False, False)

                        my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                         font=("Helvetica", 23), text_color="white")
                        my_text.place(x=15, y=0)
                        my_text.configure(padx=20)

                        frame_ = customtkinter.CTkFrame(app5)
                        frame_.place(x=10, y=45)
                        frame_.configure(fg_color='transparent')

                        Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                        Yes_button.grid(row=0, column=0, padx=20)
                        Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                            font=("Arial black", 15), border_color="#374BB5", border_width=4)

                        No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                        No_button.grid(row=0, column=1)
                        No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                            font=("Arial black", 15), border_color="#374BB5", border_width=4)



                        app5.mainloop()



                        if save_photo is True:
                            close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                            close_window_thread.start()
                            Error_Window()
                            ErrorWindow.title("INFO")
                            ErrorWindow.geometry("242x80+587+505")
                            Error_text.configure(text="Pose saved succesfully.",
                                                 font=("Helvetica", 20))

                            OK_button.place(x=50, y=40)
                            ErrorWindow.mainloop()

                            pose_captured = True

                            break

                else:

                    print("No se ha detectado correctamente la pose.")

            else:
                if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:

                        #################### Cogemos los puntos clave de la pose de la mano ################################
                        THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                        INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                        MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                        RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                        RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                        PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                        PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y


                        ######## IMPORTAAAAAAAAAAAAAAAAAAAAAAAAANTEEEEEEEEEEEEEEEEEE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
                        lista_THUMB_TIP_x_BBDD[pose_number] = THUMB_TIP_x_BBDD
                        lista_THUMB_TIP_y_BBDD[pose_number] = THUMB_TIP_y_BBDD
                        ######## IMPORTAAAAAAAAAAAAAAAAAAAAAAAAANTEEEEEEEEEEEEEEEEEE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #




                        #################### Cogemos los puntos clave de la pose de la mano ################################

                        ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                        lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,
                                   RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                        lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,
                                   RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                        sub_diccionario = "sub_diccionario_" + str(
                            pose_number)  # Tendré un diccionario por cada HANDPOSE
                        sub_diccionario = {}

                        for i in range(5):
                            x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.05, lista_y[i] + 0.05
                            x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.05, lista_y[i] - 0.05

                            x1_rectangle = int(x1_rectangle_normalized * width)
                            x2_rectangle = int(x2_rectangle_normalized * width)

                            y1_rectangle = int(y1_rectangle_normalized * height)
                            y2_rectangle = int(y2_rectangle_normalized * height)

                            # Dibujamos el cuadrado en la imagen
                            # cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle), (0, 255, 0), 2)

                            lista_marginsRectangle_finger = "lista_marginsRectangle_finger_" + str(i)

                            sub_diccionario[lista_marginsRectangle_finger] = [x1_rectangle_normalized,
                                                                              x2_rectangle_normalized,
                                                                              y1_rectangle_normalized,
                                                                              y2_rectangle_normalized]

                        margins_each_HANDPOSE = "margins_each_HANDPOSE_" + str(pose_number)
                        diccionario_principal[margins_each_HANDPOSE] = sub_diccionario
                        ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                        XMAX = max(lista_x)
                        XMIN = min(lista_x)
                        YMAX = max(lista_y)
                        YMIN = min(lista_y)

                        anchura_BBDD = XMAX - XMIN
                        altura_BBDD = YMAX - YMIN

                        rectangle_adapt_size_BBDD = "rectangle_adapt_size_BBDD_" + str(pose_number)
                        diccionario_principal[rectangle_adapt_size_BBDD] = [anchura_BBDD, altura_BBDD]
                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                        app5 = customtkinter.CTk()
                        app5.title("Save or repeat")
                        app5.geometry("360x90+200+630")

                        customtkinter.set_appearance_mode("dark")

                        app5.resizable(False, False)

                        my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                         font=("Helvetica", 23), text_color="white")
                        my_text.place(x=15, y=0)
                        my_text.configure(padx=20)

                        frame_ = customtkinter.CTkFrame(app5)
                        frame_.place(x=10, y=45)
                        frame_.configure(fg_color='transparent')

                        Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                        Yes_button.grid(row=0, column=0, padx=20)
                        Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                             font=("Arial black", 15), border_color="#374BB5", border_width=4)

                        No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                        No_button.grid(row=0, column=1)
                        No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                            font=("Arial black", 15), border_color="#374BB5", border_width=4)

                        app5.mainloop()

                        if save_photo is True:
                            close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                            close_window_thread.start()
                            Error_Window()
                            ErrorWindow.title("INFO")
                            ErrorWindow.geometry("242x80+587+505")
                            Error_text.configure(text="Pose saved succesfully.",
                                                 font=("Helvetica", 20))

                            OK_button.place(x=50, y=40)
                            ErrorWindow.mainloop()

                            pose_captured = True

                            break

                else:

                    print("No se ha detectado correctamente la pose.")



        if pose_captured is True:
            break

    # Liberar recursos y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

    # ---------------------------------------------------------------------------------------------------------------------#

def take_info_from_captures_TWO_HANDS():
    close_photos()
    global counter_pose
    global taken_photo
    global lista_THUMB_TIP_x_BBDD
    global lista_THUMB_TIP_y_BBDD
    global diccionario_principal
    global frame
    global taking_shot
    global assign_first_time
    global pose_number
    global app5

    pose_captured = False

    # -----------------------------------------------------------------------------------------------------------#

    # Inicializar la cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Obtiene las dimensiones de la pantalla
    screen_width = 1920
    screen_height = 1080

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 700
    window_height_Video = 525

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Camera", window_x_Video, window_y_Video)
    cv2.resizeWindow("Camera", window_width_Video, window_height_Video)

    # Verificar que se haya abierto correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    # Leer imágenes de la cámara
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # debemos pasar a RGB la imagen porque con BGR no puede
        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            results = hands.process(frame_rgb)


        # print("Hand landmarks:", results.multi_hand_landmarks)
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar imagen en una ventana
        cv2.imshow("Camera", frame)

        if taken_photo is True:
            taken_photo = False
            if assign_first_time is True:
                if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks) == 2:


                    contador3 = 0
                    for hand_landmarks in results.multi_hand_landmarks:  # Realiza el for 2 veces, 1 por cada mano detectada.
                        ################################# MANO IZQUIERDA ##################################################
                        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                        # print(handIndex)
                        handLabel = results.multi_handedness[handIndex].classification[0].label

                        if handLabel == "Left":
                            #################### Cogemos los puntos clave de la pose de la mano ################################
                            THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                            THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                            INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                            INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                            MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                            MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                            RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                            RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                            PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                            PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                            LEFTHAND_lista_THUMB_TIP_x_BBDD.append(THUMB_TIP_x_BBDD)
                            LEFTHAND_lista_THUMB_TIP_y_BBDD.append(THUMB_TIP_y_BBDD)
                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                            lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,
                                       RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                            lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,
                                       RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                            LEFTHAND_sub_diccionario = "LEFTHAND_sub_diccionario_" + str(
                                counter_pose)  # Tendré un diccionario por cada HANDPOSE y por cada mano
                            LEFTHAND_sub_diccionario = {}

                            for i in range(5):
                                x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.04, lista_y[i] + 0.04
                                x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.04, lista_y[i] - 0.04

                                x1_rectangle = int(x1_rectangle_normalized * width)
                                x2_rectangle = int(x2_rectangle_normalized * width)

                                y1_rectangle = int(y1_rectangle_normalized * height)
                                y2_rectangle = int(y2_rectangle_normalized * height)

                                # Dibujamos el cuadrado en la imagen
                                # cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle), (0, 255, 0), 2)

                                LEFTHAND_lista_marginsRectangle_finger = "LEFTHAND_lista_marginsRectangle_finger_" + str(i)

                                LEFTHAND_sub_diccionario[LEFTHAND_lista_marginsRectangle_finger] = [x1_rectangle_normalized,
                                                                                                    x2_rectangle_normalized,
                                                                                                    y1_rectangle_normalized,
                                                                                                    y2_rectangle_normalized]

                            LEFTHAND_margins_each_HANDPOSE = "LEFTHAND_margins_each_HANDPOSE_" + str(counter_pose)
                            LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE] = LEFTHAND_sub_diccionario
                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                            XMAX = max(lista_x)
                            XMIN = min(lista_x)
                            YMAX = max(lista_y)
                            YMIN = min(lista_y)

                            anchura_BBDD = XMAX - XMIN
                            altura_BBDD = YMAX - YMIN

                            LEFTHAND_rectangle_adapt_size_BBDD = "LEFTHAND_rectangle_adapt_size_BBDD_" + str(counter_pose)
                            LEFTHAND_diccionario_principal[LEFTHAND_rectangle_adapt_size_BBDD] = [anchura_BBDD, altura_BBDD]
                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        if handLabel == "Right":
                            #################### Cogemos los puntos clave de la pose de la mano ################################
                            THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                            THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                            INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                            INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                            MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                            MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                            RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                            RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                            PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                            PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                            RIGHTHAND_lista_THUMB_TIP_x_BBDD.append(THUMB_TIP_x_BBDD)
                            RIGHTHAND_lista_THUMB_TIP_y_BBDD.append(THUMB_TIP_y_BBDD)
                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                            lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,
                                       RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                            lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,
                                       RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                            RIGHTHAND_sub_diccionario = "RIGHTHAND_sub_diccionario_" + str(
                                counter_pose)  # Tendré un diccionario por cada HANDPOSE y por cada mano
                            RIGHTHAND_sub_diccionario = {}

                            for i in range(5):
                                x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.05, lista_y[i] + 0.05
                                x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.05, lista_y[i] - 0.05

                                x1_rectangle = int(x1_rectangle_normalized * width)
                                x2_rectangle = int(x2_rectangle_normalized * width)

                                y1_rectangle = int(y1_rectangle_normalized * height)
                                y2_rectangle = int(y2_rectangle_normalized * height)

                                # Dibujamos el cuadrado en la imagen
                                """cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle),
                                              (0, 255, 0), 2)"""

                                RIGHTHAND_lista_marginsRectangle_finger = "RIGHTHAND_lista_marginsRectangle_finger_" + str(
                                    i)

                                RIGHTHAND_sub_diccionario[RIGHTHAND_lista_marginsRectangle_finger] = [
                                    x1_rectangle_normalized,
                                    x2_rectangle_normalized,
                                    y1_rectangle_normalized,
                                    y2_rectangle_normalized]

                            RIGHTHAND_margins_each_HANDPOSE = "RIGHTHAND_margins_each_HANDPOSE_" + str(counter_pose)
                            RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE] = RIGHTHAND_sub_diccionario
                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                            XMAX = max(lista_x)
                            XMIN = min(lista_x)
                            YMAX = max(lista_y)
                            YMIN = min(lista_y)

                            anchura_BBDD = XMAX - XMIN
                            altura_BBDD = YMAX - YMIN

                            RIGHTHAND_rectangle_adapt_size_BBDD = "RIGHTHAND_rectangle_adapt_size_BBDD_" + str(counter_pose)
                            RIGHTHAND_diccionario_principal[RIGHTHAND_rectangle_adapt_size_BBDD] = [anchura_BBDD,
                                                                                                    altura_BBDD]
                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        contador3 += 1
                        if contador3 == 2:
                            app5 = customtkinter.CTk()
                            app5.title("Save or repeat")
                            app5.geometry("360x90+200+630")

                            customtkinter.set_appearance_mode("dark")

                            app5.resizable(False, False)

                            my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                             font=("Helvetica", 23), text_color="white")
                            my_text.place(x=15, y=0)
                            my_text.configure(padx=20)

                            frame_ = customtkinter.CTkFrame(app5)
                            frame_.place(x=10, y=45)
                            frame_.configure(fg_color='transparent')

                            Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                            Yes_button.grid(row=0, column=0, padx=20)
                            Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                                 font=("Arial black", 15), border_color="#374BB5", border_width=4)

                            No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                            No_button.grid(row=0, column=1)
                            No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                                font=("Arial black", 15), border_color="#374BB5", border_width=4)

                            app5.mainloop()

                            if save_photo is True:
                                close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                                close_window_thread.start()
                                Error_Window()
                                ErrorWindow.title("INFO")
                                ErrorWindow.geometry("242x80+587+505")
                                Error_text.configure(text="Pose saved succesfully.",
                                                     font=("Helvetica", 20))

                                OK_button.place(x=50, y=40)
                                ErrorWindow.mainloop()

                                pose_captured = True

                                break


                else:
                    print("No se han detectado dos manos.")

            else:
                if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks) == 2:

                    contador3 = 0

                    for hand_landmarks in results.multi_hand_landmarks:  # Realiza el for 2 veces, 1 por cada mano detectada.

                        ################################# MANO IZQUIERDA ##################################################

                        handIndex = results.multi_hand_landmarks.index(hand_landmarks)

                        # print(handIndex)

                        handLabel = results.multi_handedness[handIndex].classification[0].label

                        if handLabel == "Left":

                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x

                            THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                            INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x

                            INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                            MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[
                                mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x

                            MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[
                                mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                            RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x

                            RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                            PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x

                            PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                            LEFTHAND_lista_THUMB_TIP_x_BBDD[pose_number] = THUMB_TIP_x_BBDD

                            LEFTHAND_lista_THUMB_TIP_y_BBDD[pose_number] = THUMB_TIP_y_BBDD

                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,

                                       RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                            lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,

                                       RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                            LEFTHAND_sub_diccionario = "LEFTHAND_sub_diccionario_" + str(

                                counter_pose)  # Tendré un diccionario por cada HANDPOSE y por cada mano

                            LEFTHAND_sub_diccionario = {}

                            for i in range(5):
                                x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.04, lista_y[i] + 0.04

                                x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.04, lista_y[i] - 0.04

                                x1_rectangle = int(x1_rectangle_normalized * width)

                                x2_rectangle = int(x2_rectangle_normalized * width)

                                y1_rectangle = int(y1_rectangle_normalized * height)

                                y2_rectangle = int(y2_rectangle_normalized * height)

                                # Dibujamos el cuadrado en la imagen

                                # cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle), (0, 255, 0), 2)

                                LEFTHAND_lista_marginsRectangle_finger = "LEFTHAND_lista_marginsRectangle_finger_" + str(
                                    i)

                                LEFTHAND_sub_diccionario[LEFTHAND_lista_marginsRectangle_finger] = [
                                    x1_rectangle_normalized,

                                    x2_rectangle_normalized,

                                    y1_rectangle_normalized,

                                    y2_rectangle_normalized]

                            LEFTHAND_margins_each_HANDPOSE = "LEFTHAND_margins_each_HANDPOSE_" + str(counter_pose)

                            LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE] = LEFTHAND_sub_diccionario

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                            XMAX = max(lista_x)

                            XMIN = min(lista_x)

                            YMAX = max(lista_y)

                            YMIN = min(lista_y)

                            anchura_BBDD = XMAX - XMIN

                            altura_BBDD = YMAX - YMIN

                            LEFTHAND_rectangle_adapt_size_BBDD = "LEFTHAND_rectangle_adapt_size_BBDD_" + str(
                                counter_pose)

                            LEFTHAND_diccionario_principal[LEFTHAND_rectangle_adapt_size_BBDD] = [anchura_BBDD,
                                                                                                  altura_BBDD]

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        if handLabel == "Right":

                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            THUMB_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x

                            THUMB_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                            INDEX_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x

                            INDEX_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                            MIDDLE_FINGER_TIP_x_BBDD = hand_landmarks.landmark[
                                mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x

                            MIDDLE_FINGER_TIP_y_BBDD = hand_landmarks.landmark[
                                mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                            RING_FINGER_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x

                            RING_FINGER_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                            PINKY_TIP_x_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x

                            PINKY_TIP_y_BBDD = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                            RIGHTHAND_lista_THUMB_TIP_x_BBDD[pose_number] = THUMB_TIP_x_BBDD

                            RIGHTHAND_lista_THUMB_TIP_y_BBDD[pose_number] = THUMB_TIP_y_BBDD

                            #################### Cogemos los puntos clave de la pose de la mano ################################

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            lista_x = [THUMB_TIP_x_BBDD, INDEX_FINGER_TIP_x_BBDD, MIDDLE_FINGER_TIP_x_BBDD,

                                       RING_FINGER_TIP_x_BBDD, PINKY_TIP_x_BBDD]

                            lista_y = [THUMB_TIP_y_BBDD, INDEX_FINGER_TIP_y_BBDD, MIDDLE_FINGER_TIP_y_BBDD,

                                       RING_FINGER_TIP_y_BBDD, PINKY_TIP_y_BBDD]

                            RIGHTHAND_sub_diccionario = "RIGHTHAND_sub_diccionario_" + str(

                                counter_pose)  # Tendré un diccionario por cada HANDPOSE y por cada mano

                            RIGHTHAND_sub_diccionario = {}

                            for i in range(5):
                                x1_rectangle_normalized, y1_rectangle_normalized = lista_x[i] + 0.05, lista_y[i] + 0.05

                                x2_rectangle_normalized, y2_rectangle_normalized = lista_x[i] - 0.05, lista_y[i] - 0.05

                                x1_rectangle = int(x1_rectangle_normalized * width)

                                x2_rectangle = int(x2_rectangle_normalized * width)

                                y1_rectangle = int(y1_rectangle_normalized * height)

                                y2_rectangle = int(y2_rectangle_normalized * height)

                                # Dibujamos el cuadrado en la imagen

                                """cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle),

                                              (0, 255, 0), 2)"""

                                RIGHTHAND_lista_marginsRectangle_finger = "RIGHTHAND_lista_marginsRectangle_finger_" + str(

                                    i)

                                RIGHTHAND_sub_diccionario[RIGHTHAND_lista_marginsRectangle_finger] = [

                                    x1_rectangle_normalized,

                                    x2_rectangle_normalized,

                                    y1_rectangle_normalized,

                                    y2_rectangle_normalized]

                            RIGHTHAND_margins_each_HANDPOSE = "RIGHTHAND_margins_each_HANDPOSE_" + str(counter_pose)

                            RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE] = RIGHTHAND_sub_diccionario

                            ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                            XMAX = max(lista_x)

                            XMIN = min(lista_x)

                            YMAX = max(lista_y)

                            YMIN = min(lista_y)

                            anchura_BBDD = XMAX - XMIN

                            altura_BBDD = YMAX - YMIN

                            RIGHTHAND_rectangle_adapt_size_BBDD = "RIGHTHAND_rectangle_adapt_size_BBDD_" + str(
                                counter_pose)

                            RIGHTHAND_diccionario_principal[RIGHTHAND_rectangle_adapt_size_BBDD] = [anchura_BBDD,

                                                                                                    altura_BBDD]

                            # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        contador3 += 1

                        if contador3 == 2:

                            app5 = customtkinter.CTk()
                            app5.title("Save or repeat")
                            app5.geometry("360x90+200+630")

                            customtkinter.set_appearance_mode("dark")

                            app5.resizable(False, False)

                            my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                             font=("Helvetica", 23), text_color="white")
                            my_text.place(x=15, y=0)
                            my_text.configure(padx=20)

                            frame_ = customtkinter.CTkFrame(app5)
                            frame_.place(x=10, y=45)
                            frame_.configure(fg_color='transparent')

                            Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                            Yes_button.grid(row=0, column=0, padx=20)
                            Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                                 font=("Arial black", 15), border_color="#374BB5", border_width=4)

                            No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                            No_button.grid(row=0, column=1)
                            No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                                font=("Arial black", 15), border_color="#374BB5", border_width=4)

                            app5.mainloop()

                            if save_photo is True:
                                close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                                close_window_thread.start()
                                Error_Window()
                                ErrorWindow.title("INFO")
                                ErrorWindow.geometry("242x80+587+505")
                                Error_text.configure(text="Pose saved succesfully.",
                                                     font=("Helvetica", 20))

                                OK_button.place(x=50, y=40)
                                ErrorWindow.mainloop()

                                pose_captured = True

                                break


                else:

                    print("No se han detectado dos manos.")

        if cv2.waitKey(1) == ord(" ") and taking_shot is False:
            taking_shot = True
            temporizador_thread = threading.Thread(target=temporizador)
            temporizador_thread.start()

        if pose_captured is True:
            break

    # Liberar recursos y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()

def take_info_from_captures_BODY_POSE():
    close_photos()
    global taking_shot
    global taken_photo
    global counter_pose
    global lista_LEFT_SHOULDER_x_BBDD
    global lista_LEFT_SHOULDER_y_BBDD
    global diccionario_principal
    global frame
    global assign_first_time
    global pose_number
    global app5


    pose_captured = False

    # -----------------------------------------------------------------------------------------------------------#

    # Inicializar la cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Obtiene las dimensiones de la pantalla
    screen_width = 1920
    screen_height = 1080

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 700
    window_height_Video = 525

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Camera", window_x_Video, window_y_Video)
    cv2.resizeWindow("Camera", window_width_Video, window_height_Video)

    # Verificar que se haya abierto correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()

    while True:
        ################################# Inicio #####################################

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # debemos pasar a RGB la imagen porque con BGR no puede
        with mp_pose.Pose(
                static_image_mode=True) as pose:
            results = pose.process(frame_rgb)



        if results.pose_landmarks is not None:
            LEFT_SHOULDER_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)
            LEFT_SHOULDER_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)

            LEFT_ELBOW_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * width)
            LEFT_ELBOW_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * height)

            LEFT_WRIST_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width)
            LEFT_WRIST_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

            RIGHT_SHOULDER_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)
            RIGHT_SHOULDER_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)

            RIGHT_ELBOW_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * width)
            RIGHT_ELBOW_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * height)

            RIGHT_WRIST_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width)
            RIGHT_WRIST_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)

            cv2.circle(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD), 6, (128, 0, 255), -1)
            cv2.circle(frame, (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD), 6, (128, 0, 255), -1)
            cv2.circle(frame, (LEFT_WRIST_x_BBDD, LEFT_WRIST_y_BBDD), 6, (128, 0, 255), -1)
            cv2.circle(frame, (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD), 6, (128, 0, 255), -1)
            cv2.circle(frame, (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD), 6, (128, 0, 255), -1)
            cv2.circle(frame, (RIGHT_WRIST_x_BBDD, RIGHT_WRIST_y_BBDD), 6, (128, 0, 255), -1)

            cv2.line(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD), (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD),
                     (255, 255, 255), 3)
            cv2.line(frame, (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD), (LEFT_WRIST_x_BBDD, LEFT_WRIST_y_BBDD),
                     (255, 255, 255), 3)
            cv2.line(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD),
                     (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD),
                     (255, 255, 255), 3)
            cv2.line(frame, (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD), (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD),
                     (255, 255, 255), 3)
            cv2.line(frame, (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD), (RIGHT_WRIST_x_BBDD, RIGHT_WRIST_y_BBDD),
                     (255, 255, 255), 3)

        # Mostrar imagen en una ventana
        cv2.imshow("Camera", frame)
        ################################# Inicio #####################################

        if taken_photo is True:
            taken_photo = False
            if assign_first_time is True:
                if results.pose_landmarks is not None:
                    #################### Cogemos los puntos clave de la pose del cuerpo ################################
                    # Los puntos clave serán en total 6 puntos: hombros, codos y muñecas.
                    LEFT_SHOULDER_x_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER].x
                    LEFT_SHOULDER_y_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER].y

                    LEFT_ELBOW_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x
                    LEFT_ELBOW_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y

                    LEFT_WRIST_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
                    LEFT_WRIST_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y

                    RIGHT_SHOULDER_x_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_SHOULDER].x
                    RIGHT_SHOULDER_y_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_SHOULDER].y

                    RIGHT_ELBOW_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x
                    RIGHT_ELBOW_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y

                    RIGHT_WRIST_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
                    RIGHT_WRIST_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y

                    lista_x_BBDD = [LEFT_SHOULDER_x_BBDD, LEFT_ELBOW_x_BBDD, LEFT_WRIST_x_BBDD,
                                    RIGHT_SHOULDER_x_BBDD, RIGHT_ELBOW_x_BBDD, RIGHT_WRIST_x_BBDD]

                    lista_y_BBDD = [LEFT_SHOULDER_y_BBDD, LEFT_ELBOW_y_BBDD, LEFT_WRIST_y_BBDD,
                                    RIGHT_SHOULDER_y_BBDD, RIGHT_ELBOW_y_BBDD, RIGHT_WRIST_y_BBDD]

                    ###### Listas para luego desplazar el frame ##########
                    lista_LEFT_SHOULDER_x_BBDD.append(LEFT_SHOULDER_x_BBDD)
                    lista_LEFT_SHOULDER_y_BBDD.append(LEFT_SHOULDER_y_BBDD)
                    ###### Listas para luego desplazar el frame ##########
                    #################### Cogemos los puntos clave de la pose del cuerpo ################################

                    ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                    sub_diccionario = "sub_diccionario_" + str(counter_pose)  # Tendré un diccionario por cada BODYPOSE
                    sub_diccionario = {}

                    for i in range(6):
                        x1_rectangle_normalized, y1_rectangle_normalized = lista_x_BBDD[i] + 0.11, lista_y_BBDD[
                            i] + 0.11
                        x2_rectangle_normalized, y2_rectangle_normalized = lista_x_BBDD[i] - 0.11, lista_y_BBDD[
                            i] - 0.11

                        x1_rectangle = int(x1_rectangle_normalized * width)
                        x2_rectangle = int(x2_rectangle_normalized * width)

                        y1_rectangle = int(y1_rectangle_normalized * height)
                        y2_rectangle = int(y2_rectangle_normalized * height)

                        # Dibujamos el cuadrado en la imagen
                        """cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle),
                                      (0, 255, 0), 2)"""

                        lista_marginsRectangle_shoulders_elbows_wrists = "lista_marginsRectangle_shoulders_elbows_wrists_" + str(
                            i)

                        sub_diccionario[lista_marginsRectangle_shoulders_elbows_wrists] = [x1_rectangle_normalized,
                                                                                           x2_rectangle_normalized,
                                                                                           y1_rectangle_normalized,
                                                                                           y2_rectangle_normalized]

                    margins_each_BODYPOSE = "margins_each_BODYPOSE_" + str(counter_pose)
                    diccionario_principal[margins_each_BODYPOSE] = sub_diccionario
                    ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                    # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                    XMAX = max(lista_x_BBDD)
                    XMIN = min(lista_x_BBDD)
                    YMAX = max(lista_y_BBDD)
                    YMIN = min(lista_y_BBDD)

                    anchura_BBDD = XMAX - XMIN
                    altura_BBDD = YMAX - YMIN

                    rectangle_adapt_size_BBDD = "rectangle_adapt_size_BBDD_" + str(counter_pose)
                    diccionario_principal[rectangle_adapt_size_BBDD] = [anchura_BBDD, altura_BBDD]
                    # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                    app5 = customtkinter.CTk()
                    app5.title("Save or repeat")
                    app5.geometry("360x90+200+630")

                    customtkinter.set_appearance_mode("dark")

                    app5.resizable(False, False)

                    my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                     font=("Helvetica", 23), text_color="white")
                    my_text.place(x=15, y=0)
                    my_text.configure(padx=20)

                    frame_ = customtkinter.CTkFrame(app5)
                    frame_.place(x=10, y=45)
                    frame_.configure(fg_color='transparent')

                    Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                    Yes_button.grid(row=0, column=0, padx=20)
                    Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                         font=("Arial black", 15), border_color="#374BB5", border_width=4)

                    No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                    No_button.grid(row=0, column=1)
                    No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                        font=("Arial black", 15), border_color="#374BB5", border_width=4)

                    app5.mainloop()

                    if save_photo is True:
                        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                        close_window_thread.start()
                        Error_Window()
                        ErrorWindow.title("INFO")
                        ErrorWindow.geometry("242x80+587+505")
                        Error_text.configure(text="Pose saved succesfully.",
                                             font=("Helvetica", 20))

                        OK_button.place(x=50, y=40)
                        ErrorWindow.mainloop()

                        pose_captured = True

                        break



                else:
                    print("No se ha detectado ninguna pose.")

            else:
                if results.pose_landmarks is not None:
                    #################### Cogemos los puntos clave de la pose del cuerpo ################################
                    # Los puntos clave serán en total 6 puntos: hombros, codos y muñecas.
                    LEFT_SHOULDER_x_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER].x
                    LEFT_SHOULDER_y_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.LEFT_SHOULDER].y

                    LEFT_ELBOW_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x
                    LEFT_ELBOW_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y

                    LEFT_WRIST_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
                    LEFT_WRIST_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y

                    RIGHT_SHOULDER_x_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_SHOULDER].x
                    RIGHT_SHOULDER_y_BBDD = results.pose_landmarks.landmark[
                        mp_pose.PoseLandmark.RIGHT_SHOULDER].y

                    RIGHT_ELBOW_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x
                    RIGHT_ELBOW_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y

                    RIGHT_WRIST_x_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
                    RIGHT_WRIST_y_BBDD = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y

                    lista_x_BBDD = [LEFT_SHOULDER_x_BBDD, LEFT_ELBOW_x_BBDD, LEFT_WRIST_x_BBDD,
                                    RIGHT_SHOULDER_x_BBDD, RIGHT_ELBOW_x_BBDD, RIGHT_WRIST_x_BBDD]

                    lista_y_BBDD = [LEFT_SHOULDER_y_BBDD, LEFT_ELBOW_y_BBDD, LEFT_WRIST_y_BBDD,
                                    RIGHT_SHOULDER_y_BBDD, RIGHT_ELBOW_y_BBDD, RIGHT_WRIST_y_BBDD]

                    ###### Listas para luego desplazar el frame ##########
                    lista_LEFT_SHOULDER_x_BBDD[pose_number] = LEFT_SHOULDER_x_BBDD
                    lista_LEFT_SHOULDER_y_BBDD[pose_number] = LEFT_SHOULDER_x_BBDD
                    ###### Listas para luego desplazar el frame ##########
                    #################### Cogemos los puntos clave de la pose del cuerpo ################################

                    ################################### RECTÁNGULO PARA CADA PUNTO #####################################
                    sub_diccionario = "sub_diccionario_" + str(counter_pose)  # Tendré un diccionario por cada BODYPOSE
                    sub_diccionario = {}

                    for i in range(6):
                        x1_rectangle_normalized, y1_rectangle_normalized = lista_x_BBDD[i] + 0.11, lista_y_BBDD[
                            i] + 0.11
                        x2_rectangle_normalized, y2_rectangle_normalized = lista_x_BBDD[i] - 0.11, lista_y_BBDD[
                            i] - 0.11

                        x1_rectangle = int(x1_rectangle_normalized * width)
                        x2_rectangle = int(x2_rectangle_normalized * width)

                        y1_rectangle = int(y1_rectangle_normalized * height)
                        y2_rectangle = int(y2_rectangle_normalized * height)

                        # Dibujamos el cuadrado en la imagen
                        cv2.rectangle(frame, (x1_rectangle, y1_rectangle), (x2_rectangle, y2_rectangle),
                                      (0, 255, 0), 2)

                        lista_marginsRectangle_shoulders_elbows_wrists = "lista_marginsRectangle_shoulders_elbows_wrists_" + str(
                            i)

                        sub_diccionario[lista_marginsRectangle_shoulders_elbows_wrists] = [x1_rectangle_normalized,
                                                                                           x2_rectangle_normalized,
                                                                                           y1_rectangle_normalized,
                                                                                           y2_rectangle_normalized]

                    margins_each_BODYPOSE = "margins_each_BODYPOSE_" + str(counter_pose)
                    diccionario_principal[margins_each_BODYPOSE] = sub_diccionario
                    ################################### RECTÁNGULO PARA CADA PUNTO #####################################

                    # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                    XMAX = max(lista_x_BBDD)
                    XMIN = min(lista_x_BBDD)
                    YMAX = max(lista_y_BBDD)
                    YMIN = min(lista_y_BBDD)

                    anchura_BBDD = XMAX - XMIN
                    altura_BBDD = YMAX - YMIN

                    rectangle_adapt_size_BBDD = "rectangle_adapt_size_BBDD_" + str(counter_pose)
                    diccionario_principal[rectangle_adapt_size_BBDD] = [anchura_BBDD, altura_BBDD]
                    # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                    app5 = customtkinter.CTk()
                    app5.title("Save or repeat")
                    app5.geometry("360x90+200+630")

                    customtkinter.set_appearance_mode("dark")

                    app5.resizable(False, False)

                    my_text = customtkinter.CTkLabel(app5, text="Do you want to save this pose?",
                                                     font=("Helvetica", 23), text_color="white")
                    my_text.place(x=15, y=0)
                    my_text.configure(padx=20)

                    frame_ = customtkinter.CTkFrame(app5)
                    frame_.place(x=10, y=45)
                    frame_.configure(fg_color='transparent')

                    Yes_button = customtkinter.CTkButton(frame_, text="YES", command=yes_button)
                    Yes_button.grid(row=0, column=0, padx=20)
                    Yes_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                         font=("Arial black", 15), border_color="#374BB5", border_width=4)

                    No_button = customtkinter.CTkButton(frame_, text="NO, REPEAT", command=no_button)
                    No_button.grid(row=0, column=1)
                    No_button.configure(fg_color="white", hover_color="#C4C4C4", text_color="#374BB5",
                                        font=("Arial black", 15), border_color="#374BB5", border_width=4)

                    app5.mainloop()

                    if save_photo is True:
                        close_window_thread = threading.Thread(target=quit_ERROR_WINDOW)
                        close_window_thread.start()
                        Error_Window()
                        ErrorWindow.title("INFO")
                        ErrorWindow.geometry("242x80+587+505")
                        Error_text.configure(text="Pose saved succesfully.",
                                             font=("Helvetica", 20))

                        OK_button.place(x=50, y=40)
                        ErrorWindow.mainloop()

                        pose_captured = True

                        break



                else:
                    print("No se ha detectado ninguna pose.")

        if cv2.waitKey(1) == ord(" ") and taking_shot is False:
            taking_shot = True
            temporizador_thread = threading.Thread(target=temporizador)
            temporizador_thread.start()

        if pose_captured is True:
            break


    # Liberar recursos y cerrar la ventana
    cap.release()
    cv2.destroyAllWindows()


def temporizador():
    global taken_photo
    global taking_shot
    print("TOMANDO FOTO EN 3 SEGUNDOS...")
    time.sleep(3)

    taking_shot = False
    taken_photo = True
    # cv2.imshow("Foto_3_segundos", frame)

########################################### TAKE INFO #################################################################

#######################################################################################################################
#######################################################################################################################

############################################### COMMANDS ##############################################################
def all_drone_commands():
    global captured_pose_number
    global command_ended
    global process_finished
    global up_arrow
    global down_arrow
    global left_arrow
    global right_arrow
    global flip_left_arrow
    global flip_right_arrow
    global time_exceeded
    global score
    global takingVideo
    global wrong_pose




    pose = "pose_" + str(captured_pose_number)
    command_drone = diccionario_principal[pose]

    if command_drone == "MOVE_UP" and up_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        MOVE_UP()

        print("MOVE_UP")
        command_ended = True
        time_exceeded = False
        score += 1

    elif command_drone == "MOVE_DOWN" and down_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        MOVE_DOWN()

        print("MOVE_DOWN")

        time_exceeded = False
        command_ended = True
        score += 1

    elif command_drone == "MOVE_LEFT" and left_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        MOVE_RIGHT()

        print("MOVE_LEFT")
        time_exceeded = False
        command_ended = True
        score += 1

    elif command_drone == "MOVE_RIGHT" and right_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        MOVE_LEFT()


        print("MOVE_RIGHT")

        time_exceeded = False
        command_ended = True
        score += 1

    elif command_drone == "FLIP_LEFT" and flip_left_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        FLIP_LEFT()


        print("FLIP_LEFT")

        time_exceeded = False
        command_ended = True
        score += 1

    elif command_drone == "FLIP_RIGHT" and flip_right_arrow is True:
        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz
        FLIP_RIGHT()


        print("FLIP_RIGHT")

        time_exceeded = False
        command_ended = True
        score += 1

    else:
        tello.send_control_command("EXT mled g 00bbbb000b0000b0b0b00b0bb000000bb00bb00bb0b00b0b0b0000b000bbbb00")  # Cara triste
        time.sleep(1.5)

        print("WRONG POSE")
        wrong_pose = True
        takingVideo = False
        command_ended = True

    time.sleep(set_time_between_arrow)
    process_finished = True
    reset_arrows()



def MOVE_UP():
    tello.move_up(20)


def MOVE_DOWN():
    tello.move_down(20)


def MOVE_LEFT():
    tello.move_left(20)


def MOVE_RIGHT():
    tello.move_right(20)


def FLIP_LEFT():
    tello.flip_left()


def FLIP_RIGHT():
    tello.flip_right()

############################################### COMMANDS ##############################################################

#######################################################################################################################
#######################################################################################################################

################################################## PLAY ###############################################################
def play():
    global takingVideo
    global score
    global wrong_pose
    global winner
    global arrow_confirmed
    global process_finished
    global tello
    global time_exceeded
    global app
    global image_label
    global my_image
    global ErrorWindow
    global Error_text

    my_image = customtkinter.CTkImage(light_image=Image.open("last.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    """if game_mode == "ONE_HAND":
        total_poses = 4

    else:
        total_poses = 6"""

    if drone_connected is True and counter_pose > 0:
        """tello.send_control_command(
            "EXT mled g 0000000000000000000000000000000000000000000000000000000000000000")"""

        score = 0
        wrong_pose = False
        takingVideo = True
        winner = False
        arrow_confirmed = False
        process_finished = True
        time_exceeded = False

        close_photos()
        tello.takeoff()





        play_song("playing_song.mp3")
        arrows_thread = threading.Thread(target=random_arrow)
        arrows_thread.start()

        if game_mode == "ONE_HAND":
            computer_camera_thread = threading.Thread(target=computer_camera_ON_ONE_HAND)
            computer_camera_thread.start()

        elif game_mode == "TWO_HANDS":
            computer_camera_thread = threading.Thread(target=computer_camera_ON_TWO_HANDS)
            computer_camera_thread.start()

        elif game_mode == "BODY_POSE":
            computer_camera_thread = threading.Thread(target=computer_camera_ON_BODY_POSE)
            computer_camera_thread.start()






    elif drone_connected is False and counter_pose < total_poses:
        if total_poses == 4:
            Error_Window()
            ErrorWindow.title("ERROR")
            ErrorWindow.geometry("575x80+587+505")
            Error_text.configure(text="ACTION REFUSED: you MUST assign all the four poses and then connect the drone.",
                                 font=("Helvetica", 15))

            OK_button.place(x=210, y=40)
            ErrorWindow.mainloop()

        else:
            Error_Window()
            ErrorWindow.title("ERROR")
            ErrorWindow.geometry("570x80+587+505")
            Error_text.configure(text="ACTION REFUSED: you MUST assign all the six poses and then connect the drone.",
                                 font=("Helvetica", 15))

            OK_button.place(x=210, y=40)
            ErrorWindow.mainloop()

    elif drone_connected is False:
        Error_Window()
        ErrorWindow.title("ERROR")
        ErrorWindow.geometry("385x80+587+505")
        Error_text.configure(text="ACTION REFUSED: first, you MUST connect the drone.",
                             font=("Helvetica", 15))

        OK_button.place(x=115, y=40)
        ErrorWindow.mainloop()

    elif counter_pose < 4:
        if total_poses == 4:
            Error_Window()
            ErrorWindow.title("ERROR")
            ErrorWindow.geometry("398x80+587+505")
            Error_text.configure(text="ACTION REFUSED: you have to assign all the four poses.",
                                 font=("Helvetica", 15))

            OK_button.place(x=121, y=40)
            ErrorWindow.mainloop()

        else:
            Error_Window()
            ErrorWindow.title("ERROR")
            ErrorWindow.geometry("394x80+587+505")
            Error_text.configure(text="ACTION REFUSED: you have to assign all the six poses.",
                                 font=("Helvetica", 15))

            OK_button.place(x=118, y=40)
            ErrorWindow.mainloop()

def play_song(song_name):
    if music_on == True:
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play()

def stop_music():
    global music_on

    if music_on == True:
        pygame.mixer.music.stop()
        music_on = False

def start_music():
    global music_on

    if music_on == False:
        music_on = True
        play_song("main_song_extended.mp3")

    else:
        Error_Window()

        Error_text.configure(text="Music is already turned on.",
                             font=("Helvetica", 20))

        ErrorWindow.mainloop()

def game_over():
    global tello
    if time_exceeded is True:
        play_song("ring.mp3")
        time.sleep(4)
        play_song("loser_song.mp3")
        tello.send_control_command("EXT mled g 0000000000000000000000000000000000000000000000000000000000000000")
        time.sleep(1)
        tello.send_control_command("EXT mled l r 2.5 TIMEOUT!")
        time.sleep(5.5)
        tello.send_control_command("EXT mled g 0000000000000000000000000000000000000000000000000000000000000000")
        time.sleep(1)
        tello.send_control_command("EXT mled l r 2.5 YOULOSE!!")
        time.sleep(5.5)

        tello.send_control_command("EXT mled g 00bbbb000b0000b0b0b00b0bb000000bb00bb00bb0b00b0b0b0000b000bbbb00")  # Cara triste
        time.sleep(2)



    elif wrong_pose is True:
        play_song("loser_song.mp3")
        tello.send_control_command("EXT mled g 0000000000000000000000000000000000000000000000000000000000000000")
        time.sleep(1)
        tello.send_control_command("EXT mled l r 2.5 WRONGPOSE!")
        time.sleep(6)
        tello.send_control_command("EXT mled g 0000000000000000000000000000000000000000000000000000000000000000")
        time.sleep(1)
        tello.send_control_command("EXT mled l r 2.5 YOULOSE!!")
        time.sleep(5.5)

        tello.send_control_command("EXT mled g 00bbbb000b0000b0b0b00b0bb000000bb00bb00bb0b00b0b0b0000b000bbbb00")  #
        # Cara triste

        time.sleep(2)



    elif winner is True:
        play_song("winner_song.mp3")
        tello.send_control_command("EXT mled l r 2.5 WINNER!!")
        time.sleep(5.5)
        play_song("aplausos.mp3")


        tello.send_control_command(
            "EXT mled g 00pppp000p0000p0p0p00p0pp000000pp0p00p0pp00pp00p0p0000p000pppp00")  # Cara feliz

        time.sleep(2)




    tello.send_control_command("EXT mled l r 2.5 GAME OVER")
    tello.land()

def random_number():
    if hard_difficulty is True or impossible_difficulty is True:
        numero = random.randint(1, 6)  # Genera un número aleatorio entre 1 y 6
        return numero

    else:
        numero = random.randint(1, 4)  # Genera un número aleatorio entre 1 y 4
        return numero

def reset_arrows():
    global up_arrow
    global down_arrow
    global left_arrow
    global right_arrow
    global flip_left_arrow
    global flip_right_arrow

    up_arrow = False
    down_arrow = False
    left_arrow = False
    right_arrow = False
    flip_left_arrow = False
    flip_right_arrow = False

def random_arrow():
    global up_arrow
    global down_arrow
    global left_arrow
    global right_arrow
    global flip_left_arrow
    global flip_right_arrow

    global arrow_confirmed
    global process_finished
    global winner
    global takingVideo
    global tello
    global time_exceeded
    global timer
    global timer_finished

    timer = set_time_reaction

    play_song("playing_song_extended.mp3")

    tello.send_control_command('EXT led 0 0 255')


    tello.send_control_command(
        "EXT mled g 0bbbbbbb0000000b000000b000000b000000b000000b000000b0000000b00000")  # número 7
    time.sleep(1)

    tello.send_control_command('EXT led 255 0 255')
    tello.send_control_command(
        "EXT mled g 00000p000000p000000p000000p0000000pppp0000p00p0000p00p0000pppp00")  # número 6
    time.sleep(1)

    tello.send_control_command(
        "EXT mled g 0ppppp000p0000000p0000000pppp00000000p0000000p0000000p000pppp000")  # número 5
    time.sleep(1)

    tello.send_control_command(
        "EXT mled g 00000000000pp00000p0p0000p00p000p000p000ppppppp00000p0000000p000")  # número 4
    time.sleep(1)

    tello.send_control_command('EXT led 255 0 0')
    tello.send_control_command(
        "EXT mled g 0000000000rrr00000000r0000000r0000rrr00000000r0000000r0000rrr000")  # Número 3

    time.sleep(1)

    tello.send_control_command(
        "EXT mled g 00000000000rr00000r00r0000000r000000r000000r000000r0000000rrrr00")  # Número 2

    time.sleep(1)

    tello.send_control_command(
        "EXT mled g 0000r000000rr00000r0r0000000r0000000r0000000r0000000r00000rrrrr0")  # Número 1

    time.sleep(1)

    tello.send_control_command('EXT led 0 0 0')



    counter_x = 0
    counter_y = 0

    while takingVideo:
        if arrow_confirmed is False and process_finished is True:
            arrow_number = random_number()
            timer_finished = False

            if score == set_game_score:
                takingVideo = False
                winner = True

            if winner is False:
                if arrow_number == 1 and counter_y < 3:
                    tello.send_control_command(
                        "EXT mled g 000bb00000bbbb000bbbbbb0bb0bb0bbb00bb00b000bb000000bb000000bb000")  # Flecha arriba
                    up_arrow = True
                    arrow_confirmed = True
                    counter_y += 1

                elif arrow_number == 2 and counter_y > -3:
                    tello.send_control_command(
                        "EXT mled g 000bb000000bb000000bb000b00bb00bbb0bb0bb0bbbbbb000bbbb00000bb000")  # Flecha abajo
                    down_arrow = True
                    arrow_confirmed = True
                    counter_y -= 1

                elif arrow_number == 3 and counter_x > -3:
                    tello.send_control_command(
                        "EXT mled g 000bb00000bb00000bb00000bbbbbbbbbbbbbbbb0bb0000000bb0000000bb000")  # Flecha izquierda
                    left_arrow = True
                    arrow_confirmed = True
                    counter_x -= 1

                elif arrow_number == 4 and counter_x < 3:
                    tello.send_control_command(
                        "EXT mled g 000bb0000000bb0000000bb0bbbbbbbbbbbbbbbb00000bb00000bb00000bb000")  # Flecha derecha
                    right_arrow = True
                    arrow_confirmed = True
                    counter_x += 1

                elif arrow_number == 5 and counter_x < 3:
                    tello.send_control_command(
                        "EXT mled g 0000bbbb0b00bb00b000b0b0b000b00bb000000bb000000b0b0000b000bbbb00")  # Flip_left_arrow
                    flip_left_arrow = True
                    arrow_confirmed = True
                    counter_x -= 1

                elif arrow_number == 6 and counter_x < 3:
                    tello.send_control_command(
                        "EXT mled g bbbb000000bb00b00b0b000bb00b000bb000000bb000000b0b0000b000bbbb00")  # Flip_right_arrow
                    flip_right_arrow = True
                    arrow_confirmed = True
                    counter_x += 1




                if arrow_confirmed:
                    process_finished = False

                    initial_time = time.time()

                    while True:
                        time_elapsed = time.time() - initial_time
                        #print(time_elapsed)
                        if time_elapsed >= timer:
                            time_exceeded = True
                            takingVideo = False
                            break

                        if timer_finished is True:
                            break




    game_over()

def apagarluces():
    global tello

    tello.send_control_command(
        "EXT mled g 00000000000000000000000000000000000000000000000000000000000000000")  # Flecha abajo


def computer_camera_ON_ONE_HAND():
    close_photos()
    global captured_pose_number
    global counter_pose
    global diccionario_principal
    global lista_THUMB_TIP_x_BBDD
    global lista_THUMB_TIP_y_BBDD
    global tello
    global command_ended
    global frame
    global arrow_confirmed
    global takingVideo
    global timer_finished

    # ABRIMOS VÍDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

    # ABRIMOS VÍDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 900
    window_height_Video = 725

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Frame", window_x_Video, window_y_Video)
    cv2.resizeWindow("Frame", window_width_Video, window_height_Video)

    contador2 = 0
    contador3 = 0
    contador4 = 0

    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################
    for i in range(counter_pose):
        nombre_archivo = f"POSE_{i}.jpg"
        if i < 4:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1592
            window_y_image = 0 + contador2

            contador2 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 4 and i < 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1270
            window_y_image = 0 + contador3

            contador3 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 948
            window_y_image = 0 + contador4

            contador4 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        # Define la posición de la ventana en la pantalla
        cv2.namedWindow(nombre_archivo, cv2.WINDOW_NORMAL)
        cv2.moveWindow(nombre_archivo, window_x_image, window_y_image)
        cv2.resizeWindow(nombre_archivo, window_width_image, window_height_image)
        ####################### Mostrar fotos en ventanas de manera ordenada ##############################
        image = cv2.imread(nombre_archivo)
        cv2.imshow(nombre_archivo, image)
    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################

    while takingVideo:
        ret, frame = cap.read()
        if ret is not True:
            break

        frame = cv2.flip(frame, 1)

        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:

            frame_rgb = cv2.cvtColor(frame,
                                     cv2.COLOR_BGR2RGB)  # debemos pasar a RGB la imagen porque con BGR no puede

            results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2,
                                                                 circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2))

        if arrow_confirmed is True:
            if results.multi_hand_landmarks is not None:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    if command_ended is True:
                        #################### Cogemos los puntos clave de la pose del frame #################################
                        THUMB_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        THUMB_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                        INDEX_FINGER_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        INDEX_FINGER_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        MIDDLE_FINGER_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                        MIDDLE_FINGER_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                        RING_FINGER_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                        RING_FINGER_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                        PINKY_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                        PINKY_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                        #################### Cogemos los puntos clave de la pose del frame #################################

                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                        lista_x_frame = [THUMB_TIP_x_FRAME, INDEX_FINGER_TIP_x_FRAME, MIDDLE_FINGER_TIP_x_FRAME,
                                         RING_FINGER_TIP_x_FRAME, PINKY_TIP_x_FRAME]

                        lista_y_frame = [THUMB_TIP_y_FRAME, INDEX_FINGER_TIP_y_FRAME, MIDDLE_FINGER_TIP_y_FRAME,
                                         RING_FINGER_TIP_y_FRAME, PINKY_TIP_y_FRAME]

                        XMAX = max(lista_x_frame)
                        XMIN = min(lista_x_frame)
                        YMAX = max(lista_y_frame)
                        YMIN = min(lista_y_frame)

                        anchura_FRAME = XMAX - XMIN
                        altura_FRAME = YMAX - YMIN
                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        # Además, pasaba que en algún momento, no aparecía la mano y
                        # entonces se quedaba con los datos de la anterior pose, entonces aunque no saliera ninguna pose en
                        # pantalla, seguía diciendo que había una pose porque se le quedaban los datos guardados. Para
                        # resolver esto, lo que se ha hecho es que cada vez que vaya a comparar poses, que antes compruebe
                        # que haya una mano. Si no hay ninguna mano a detectar, los valores a comparar se irán a 0 y por
                        # tanto, saldrá que no hay ninguna pose hecha.
                        ManoDetectada = True
                        if results.multi_handedness is None:
                            ManoDetectada = False
                            anchura_FRAME = 1
                            altura_FRAME = 1
                            THUMB_TIP_x_FRAME_modified_and_shifted = 0
                            THUMB_TIP_y_FRAME_modified_and_shifted = 0
                            INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                            INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                            MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                            MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                            RING_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                            RING_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                            PINKY_TIP_x_FRAME_modified_and_shifted = 0
                            PINKY_TIP_y_FRAME_modified_and_shifted = 0

                        decision_tomada = False

                        if decision_tomada is not True and ManoDetectada is True:
                            for j in range(counter_pose):
                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################
                                rectangle_adapt_size_BBDD_in_video = "rectangle_adapt_size_BBDD_" + str(j)

                                anchura_pose_BBDD = diccionario_principal[rectangle_adapt_size_BBDD_in_video][0]
                                altura_pose_BBDD = diccionario_principal[rectangle_adapt_size_BBDD_in_video][1]

                                factor_x = anchura_pose_BBDD / anchura_FRAME
                                factor_y = altura_pose_BBDD / altura_FRAME

                                THUMB_TIP_x_FRAME_modified = THUMB_TIP_x_FRAME * factor_x
                                THUMB_TIP_y_FRAME_modified = THUMB_TIP_y_FRAME * factor_y

                                INDEX_FINGER_TIP_x_FRAME_modified = INDEX_FINGER_TIP_x_FRAME * factor_x
                                INDEX_FINGER_TIP_y_FRAME_modified = INDEX_FINGER_TIP_y_FRAME * factor_y

                                MIDDLE_FINGER_TIP_x_FRAME_modified = MIDDLE_FINGER_TIP_x_FRAME * factor_x
                                MIDDLE_FINGER_TIP_y_FRAME_modified = MIDDLE_FINGER_TIP_y_FRAME * factor_y

                                RING_FINGER_TIP_x_FRAME_modified = RING_FINGER_TIP_x_FRAME * factor_x
                                RING_FINGER_TIP_y_FRAME_modified = RING_FINGER_TIP_y_FRAME * factor_y

                                PINKY_TIP_x_FRAME_modified = PINKY_TIP_x_FRAME * factor_x
                                PINKY_TIP_y_FRAME_modified = PINKY_TIP_y_FRAME * factor_y

                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################

                                # ###------------------ Ahora ambas capturas tienen la misma profundidad, la profundidad de
                                # la captura de la BBDD. Hemos adaptado la NewPose a la BBDD.

                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################
                                diferencia_THUMB_INDEX_x = lista_THUMB_TIP_x_BBDD[j] - THUMB_TIP_x_FRAME_modified
                                diferencia_THUMB_INDEX_y = lista_THUMB_TIP_y_BBDD[j] - THUMB_TIP_y_FRAME_modified
                                # Solo hay que mirar la diferencia de un dedo de la BBDD con un dedo del FRAME porque toda la
                                # mano es un bloque, entonces si la diferencia de distancia entre un dedo y otro es,
                                # por ejemplo, 0.2, significa que todos los dedos tienen esa misma distancia con sus
                                # respectivos dedos si es la misma pose.

                                THUMB_TIP_x_FRAME_modified_and_shifted = THUMB_TIP_x_FRAME_modified + diferencia_THUMB_INDEX_x
                                THUMB_TIP_y_FRAME_modified_and_shifted = THUMB_TIP_y_FRAME_modified + diferencia_THUMB_INDEX_y

                                INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = INDEX_FINGER_TIP_x_FRAME_modified + diferencia_THUMB_INDEX_x
                                INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = INDEX_FINGER_TIP_y_FRAME_modified + diferencia_THUMB_INDEX_y

                                MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = MIDDLE_FINGER_TIP_x_FRAME_modified + diferencia_THUMB_INDEX_x
                                MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = MIDDLE_FINGER_TIP_y_FRAME_modified + diferencia_THUMB_INDEX_y

                                RING_FINGER_TIP_x_FRAME_modified_and_shifted = RING_FINGER_TIP_x_FRAME_modified + diferencia_THUMB_INDEX_x
                                RING_FINGER_TIP_y_FRAME_modified_and_shifted = RING_FINGER_TIP_y_FRAME_modified + diferencia_THUMB_INDEX_y

                                PINKY_TIP_x_FRAME_modified_and_shifted = PINKY_TIP_x_FRAME_modified + diferencia_THUMB_INDEX_x
                                PINKY_TIP_y_FRAME_modified_and_shifted = PINKY_TIP_y_FRAME_modified + diferencia_THUMB_INDEX_y

                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################

                                # Ahora, todas las coordenadas están situadas en el mismo sitio que en la BBDD, por tanto, si son la misma
                                # pose, los rectángulos de cada punto coindirán con los de las capturas.

                                ############################    CONDICIONES     ############################
                                # Márgenes
                                # if(margen1 > punto x ó y > -margen1)
                                margins_each_HANDPOSE_in_video = "margins_each_HANDPOSE_" + str(j)
                                for i in range(5):
                                    lista_marginsRectangle_finger_in_video = "lista_marginsRectangle_finger_" + str(i)
                                    # Coordenada1 = x + 0.05
                                    # Coordenada2 = x - 0.05
                                    # Coordenada3 = y + 0.05
                                    # Coordenada4 = y - 0.05

                                    if i == 0:
                                        coordenada1 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][0]
                                        coordenada2 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][1]
                                        coordenada3 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][2]
                                        coordenada4 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][3]

                                    if i == 1:
                                        coordenada5 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][0]
                                        coordenada6 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][1]
                                        coordenada7 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][2]
                                        coordenada8 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][3]

                                    if i == 2:
                                        coordenada9 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][0]
                                        coordenada10 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][1]
                                        coordenada11 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][2]
                                        coordenada12 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][3]

                                    if i == 3:
                                        coordenada13 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][0]
                                        coordenada14 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][1]
                                        coordenada15 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][2]
                                        coordenada16 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][3]

                                    if i == 4:
                                        coordenada17 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][0]
                                        coordenada18 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][1]
                                        coordenada19 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][2]
                                        coordenada20 = \
                                            diccionario_principal[margins_each_HANDPOSE_in_video][
                                                lista_marginsRectangle_finger_in_video][3]

                                coordenadas_THUMB = [coordenada1, coordenada2, coordenada3, coordenada4]
                                coordenadas_INDEX = [coordenada5, coordenada6, coordenada7, coordenada8]
                                coordenadas_MIDDLE = [coordenada9, coordenada10, coordenada11, coordenada12]
                                coordenadas_RING = [coordenada13, coordenada14, coordenada15, coordenada16]
                                coordenadas_PINKY = [coordenada17, coordenada18, coordenada19, coordenada20]



                                if (coordenadas_THUMB[0] > THUMB_TIP_x_FRAME_modified_and_shifted > coordenadas_THUMB[
                                    1]) \
                                        and (coordenadas_THUMB[2] > THUMB_TIP_y_FRAME_modified_and_shifted >
                                             coordenadas_THUMB[3]) \
                                        and (coordenadas_INDEX[0] > INDEX_FINGER_TIP_x_FRAME_modified_and_shifted >
                                             coordenadas_INDEX[1]) \
                                        and (coordenadas_INDEX[2] > INDEX_FINGER_TIP_y_FRAME_modified_and_shifted >
                                             coordenadas_INDEX[3]) \
                                        and (coordenadas_MIDDLE[0] > MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted >
                                             coordenadas_MIDDLE[1]) \
                                        and (coordenadas_MIDDLE[2] > MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted >
                                             coordenadas_MIDDLE[3]) \
                                        and (coordenadas_RING[0] > RING_FINGER_TIP_x_FRAME_modified_and_shifted >
                                             coordenadas_RING[1]) \
                                        and (coordenadas_RING[2] > RING_FINGER_TIP_y_FRAME_modified_and_shifted >
                                             coordenadas_RING[3]) \
                                        and (coordenadas_PINKY[0] > PINKY_TIP_x_FRAME_modified_and_shifted >
                                             coordenadas_PINKY[1]) \
                                        and (coordenadas_PINKY[2] > PINKY_TIP_y_FRAME_modified_and_shifted >
                                             coordenadas_PINKY[3]):


                                    timer_finished = True
                                    command_ended = False
                                    arrow_confirmed = False
                                    captured_pose_number = j
                                    drone_thread = threading.Thread(target=all_drone_commands)
                                    drone_thread.start()

                                    decision_tomada = True

                        if (decision_tomada is not True):
                            # print("No ha detectado ninguna pose.")
                            decision_tomada = True

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()


def computer_camera_ON_TWO_HANDS():
    close_photos()
    global captured_pose_number
    global counter_pose
    global diccionario_principal
    global lista_THUMB_TIP_x_BBDD
    global lista_THUMB_TIP_y_BBDD
    global tello
    global command_ended
    global frame
    global arrow_confirmed
    global takingVideo
    global timer_finished

    # ABRIMOS VÍDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 900
    window_height_Video = 725

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Camera", window_x_Video, window_y_Video)
    cv2.resizeWindow("Camera", window_width_Video, window_height_Video)

    contador2 = 0
    contador3 = 0
    contador4 = 0

    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################
    for i in range(counter_pose):
        nombre_archivo = f"POSE_{i}.jpg"
        if i < 4:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1592
            window_y_image = 0 + contador2

            contador2 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 4 and i < 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1270
            window_y_image = 0 + contador3

            contador3 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 948
            window_y_image = 0 + contador4

            contador4 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        # Define la posición de la ventana en la pantalla
        cv2.namedWindow(nombre_archivo, cv2.WINDOW_NORMAL)
        cv2.moveWindow(nombre_archivo, window_x_image, window_y_image)
        cv2.resizeWindow(nombre_archivo, window_width_image, window_height_image)
        ####################### Mostrar fotos en ventanas de manera ordenada ##############################
        image = cv2.imread(nombre_archivo)
        cv2.imshow(nombre_archivo, image)
    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################

    while takingVideo:
        ret, frame = cap.read()
        if ret is not True:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            results = hands.process(frame_rgb)

        if arrow_confirmed is True:
            if results.multi_hand_landmarks is not None and len(results.multi_hand_landmarks) == 2:
                ################################ INICIALIZACIÓN ###########################################
                RIGHTHAND_anchura_FRAME = 1
                RIGHTHAND_altura_FRAME = 1
                RIGHTHAND_THUMB_TIP_x_FRAME_modified_and_shifted = 0
                RIGHTHAND_THUMB_TIP_y_FRAME_modified_and_shifted = 0
                RIGHTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                RIGHTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                RIGHTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                RIGHTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                RIGHTHAND_PINKY_TIP_x_FRAME_modified_and_shifted = 0
                RIGHTHAND_PINKY_TIP_y_FRAME_modified_and_shifted = 0

                LEFTHAND_anchura_FRAME = 1
                LEFTHAND_altura_FRAME = 1
                LEFTHAND_THUMB_TIP_x_FRAME_modified_and_shifted = 0
                LEFTHAND_THUMB_TIP_y_FRAME_modified_and_shifted = 0
                LEFTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                LEFTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                LEFTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted = 0
                LEFTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted = 0
                LEFTHAND_PINKY_TIP_x_FRAME_modified_and_shifted = 0
                LEFTHAND_PINKY_TIP_y_FRAME_modified_and_shifted = 0
                ################################ INICIALIZACIÓN ###########################################

                ################################# COGER COORDENADAS DEL FRAME ##################################
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                    # print(handIndex)
                    handLabel = results.multi_handedness[handIndex].classification[0].label
                    if handLabel == "Left":
                        #################### Cogemos los puntos clave de la pose del frame #################################
                        LEFTHAND_THUMB_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        LEFTHAND_THUMB_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                        LEFTHAND_INDEX_FINGER_TIP_x_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        LEFTHAND_INDEX_FINGER_TIP_y_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                        LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                        LEFTHAND_RING_FINGER_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                        LEFTHAND_RING_FINGER_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                        LEFTHAND_PINKY_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                        LEFTHAND_PINKY_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                        #################### Cogemos los puntos clave de la pose del frame #################################

                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                        LEFTHAND_lista_x_frame = [LEFTHAND_THUMB_TIP_x_FRAME, LEFTHAND_INDEX_FINGER_TIP_x_FRAME,
                                                  LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME,
                                                  LEFTHAND_RING_FINGER_TIP_x_FRAME,
                                                  LEFTHAND_PINKY_TIP_x_FRAME]

                        LEFTHAND_lista_y_frame = [LEFTHAND_THUMB_TIP_y_FRAME, LEFTHAND_INDEX_FINGER_TIP_y_FRAME,
                                                  LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME,
                                                  LEFTHAND_RING_FINGER_TIP_y_FRAME,
                                                  LEFTHAND_PINKY_TIP_y_FRAME]

                        XMAX = max(LEFTHAND_lista_x_frame)
                        XMIN = min(LEFTHAND_lista_x_frame)
                        YMAX = max(LEFTHAND_lista_y_frame)
                        YMIN = min(LEFTHAND_lista_y_frame)

                        LEFTHAND_anchura_FRAME = XMAX - XMIN
                        LEFTHAND_altura_FRAME = YMAX - YMIN
                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        # Además, me pasaba que en algún momento, no aparecía la mano y
                        # entonces se quedaba con los datos de la anterior pose, entonces aunque no saliera ninguna pose en
                        # pantalla, seguía diciendo que había una pose porque se le quedaban los datos guardados. Para
                        # resolver esto, lo que se ha hecho es que cada vez que vaya a comparar poses, que antes compruebe
                        # que haya una mano. Si no hay ninguna mano a detectar, los valores a comparar se irán a 0 y por
                        # tanto, saldrá que no hay ninguna pose hecha.

                    if handLabel == "Right":
                        #################### Cogemos los puntos clave de la pose del frame #################################
                        RIGHTHAND_THUMB_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                        RIGHTHAND_THUMB_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                        RIGHTHAND_INDEX_FINGER_TIP_x_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        RIGHTHAND_INDEX_FINGER_TIP_y_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                        RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                        RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME = hand_landmarks.landmark[
                            mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                        RIGHTHAND_RING_FINGER_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
                        RIGHTHAND_RING_FINGER_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

                        RIGHTHAND_PINKY_TIP_x_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
                        RIGHTHAND_PINKY_TIP_y_FRAME = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                        #################### Cogemos los puntos clave de la pose del frame #################################

                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                        RIGHTHAND_lista_x_frame = [RIGHTHAND_THUMB_TIP_x_FRAME, RIGHTHAND_INDEX_FINGER_TIP_x_FRAME,
                                                   RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME,
                                                   RIGHTHAND_RING_FINGER_TIP_x_FRAME,
                                                   RIGHTHAND_PINKY_TIP_x_FRAME]

                        RIGHTHAND_lista_y_frame = [RIGHTHAND_THUMB_TIP_y_FRAME, RIGHTHAND_INDEX_FINGER_TIP_y_FRAME,
                                                   RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME,
                                                   RIGHTHAND_RING_FINGER_TIP_y_FRAME,
                                                   RIGHTHAND_PINKY_TIP_y_FRAME]

                        XMAX = max(RIGHTHAND_lista_x_frame)
                        XMIN = min(RIGHTHAND_lista_x_frame)
                        YMAX = max(RIGHTHAND_lista_y_frame)
                        YMIN = min(RIGHTHAND_lista_y_frame)

                        RIGHTHAND_anchura_FRAME = XMAX - XMIN
                        RIGHTHAND_altura_FRAME = YMAX - YMIN
                        # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                        # Además, me pasaba que en algún momento, no aparecía la mano y
                        # entonces se quedaba con los datos de la anterior pose, entonces aunque no saliera ninguna pose en
                        # pantalla, seguía diciendo que había una pose porque se le quedaban los datos guardados. Para
                        # resolver esto, lo que se ha hecho es que cada vez que vaya a comparar poses, que antes compruebe
                        # que haya una mano. Si no hay ninguna mano a detectar, los valores a comparar se irán a 0 y por
                        # tanto, saldrá que no hay ninguna pose hecha.
                ################################# COGER COORDENADAS DEL FRAME ##################################

                decision_tomada = False
                if decision_tomada is not True:
                    contador4 = 0
                    ########################## COORDENADAS DEL FRAME MODIFIED & SHIFTED ###############################
                    for hand_landmarks in results.multi_hand_landmarks:  # Recordemos: este for lo hace 2 veces, 1 por mano
                        contador4 += 1  # Este contador lo ponemos para que no haga el "for" 2 veces en la parte que no nos interesa.
                        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                        # print(handIndex)
                        handLabel = results.multi_handedness[handIndex].classification[0].label
                        for j in range(4):
                            if handLabel == "Left":
                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################
                                LEFTHAND_rectangle_adapt_size_BBDD_in_video = "LEFTHAND_rectangle_adapt_size_BBDD_" + str(j)

                                LEFTHAND_anchura_pose_BBDD = \
                                LEFTHAND_diccionario_principal[LEFTHAND_rectangle_adapt_size_BBDD_in_video][0]
                                LEFTHAND_altura_pose_BBDD = \
                                LEFTHAND_diccionario_principal[LEFTHAND_rectangle_adapt_size_BBDD_in_video][1]

                                LEFTHAND_factor_x = LEFTHAND_anchura_pose_BBDD / LEFTHAND_anchura_FRAME
                                LEFTHAND_factor_y = LEFTHAND_altura_pose_BBDD / LEFTHAND_altura_FRAME

                                LEFTHAND_THUMB_TIP_x_FRAME_modified = LEFTHAND_THUMB_TIP_x_FRAME * LEFTHAND_factor_x
                                LEFTHAND_THUMB_TIP_y_FRAME_modified = LEFTHAND_THUMB_TIP_y_FRAME * LEFTHAND_factor_y

                                LEFTHAND_INDEX_FINGER_TIP_x_FRAME_modified = LEFTHAND_INDEX_FINGER_TIP_x_FRAME * LEFTHAND_factor_x
                                LEFTHAND_INDEX_FINGER_TIP_y_FRAME_modified = LEFTHAND_INDEX_FINGER_TIP_y_FRAME * LEFTHAND_factor_y

                                LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified = LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME * LEFTHAND_factor_x
                                LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified = LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME * LEFTHAND_factor_y

                                LEFTHAND_RING_FINGER_TIP_x_FRAME_modified = LEFTHAND_RING_FINGER_TIP_x_FRAME * LEFTHAND_factor_x
                                LEFTHAND_RING_FINGER_TIP_y_FRAME_modified = LEFTHAND_RING_FINGER_TIP_y_FRAME * LEFTHAND_factor_y

                                LEFTHAND_PINKY_TIP_x_FRAME_modified = LEFTHAND_PINKY_TIP_x_FRAME * LEFTHAND_factor_x
                                LEFTHAND_PINKY_TIP_y_FRAME_modified = LEFTHAND_PINKY_TIP_y_FRAME * LEFTHAND_factor_y
                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################

                                # ###------------------ Ahora ambas capturas tienen la misma profundidad, la profundidad de
                                # la captura de la BBDD. Hemos adaptado la NewPose a la BBDD.

                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################
                                LEFTHAND_diferencia_THUMB_INDEX_x = LEFTHAND_lista_THUMB_TIP_x_BBDD[
                                                                        j] - LEFTHAND_THUMB_TIP_x_FRAME_modified
                                LEFTHAND_diferencia_THUMB_INDEX_y = LEFTHAND_lista_THUMB_TIP_y_BBDD[
                                                                        j] - LEFTHAND_THUMB_TIP_y_FRAME_modified
                                # Solo hay que mirar la diferencia de un dedo de la BBDD con un dedo del FRAME porque toda la
                                # mano es un bloque, entonces si la diferencia de distancia entre un dedo y otro es,
                                # por ejemplo, 0.2, significa que todos los dedos tienen esa misma distancia con sus
                                # respectivos dedos si es la misma pose.

                                LEFTHAND_THUMB_TIP_x_FRAME_modified_and_shifted = LEFTHAND_THUMB_TIP_x_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_x
                                LEFTHAND_THUMB_TIP_y_FRAME_modified_and_shifted = LEFTHAND_THUMB_TIP_y_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_y

                                LEFTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = LEFTHAND_INDEX_FINGER_TIP_x_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_x
                                LEFTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = LEFTHAND_INDEX_FINGER_TIP_y_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_y

                                LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_x
                                LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_y

                                LEFTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted = LEFTHAND_RING_FINGER_TIP_x_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_x
                                LEFTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted = LEFTHAND_RING_FINGER_TIP_y_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_y

                                LEFTHAND_PINKY_TIP_x_FRAME_modified_and_shifted = LEFTHAND_PINKY_TIP_x_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_x
                                LEFTHAND_PINKY_TIP_y_FRAME_modified_and_shifted = LEFTHAND_PINKY_TIP_y_FRAME_modified + LEFTHAND_diferencia_THUMB_INDEX_y
                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################

                                # Ahora, todas las coordenadas están situadas en el mismo sitio que en la BBDD, por tanto, si son la misma
                                # pose, los rectángulos de cada punto coindirán con los de las capturas.
                                lista_LEFTHAND_x = "lista_LEFTHAND_x_" + str(j)
                                lista_LEFTHAND_y = "lista_LEFTHAND_y_" + str(j)
                                LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x] = [
                                    LEFTHAND_THUMB_TIP_x_FRAME_modified_and_shifted,
                                    LEFTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    LEFTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    LEFTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    LEFTHAND_PINKY_TIP_x_FRAME_modified_and_shifted]

                                LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y] = [
                                    LEFTHAND_THUMB_TIP_y_FRAME_modified_and_shifted,
                                    LEFTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    LEFTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    LEFTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    LEFTHAND_PINKY_TIP_y_FRAME_modified_and_shifted]

                            if handLabel == "Right":
                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################
                                RIGHTHAND_rectangle_adapt_size_BBDD_in_video = "RIGHTHAND_rectangle_adapt_size_BBDD_" + str(
                                    j)

                                RIGHTHAND_anchura_pose_BBDD = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_rectangle_adapt_size_BBDD_in_video][0]
                                RIGHTHAND_altura_pose_BBDD = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_rectangle_adapt_size_BBDD_in_video][1]

                                RIGHTHAND_factor_x = RIGHTHAND_anchura_pose_BBDD / RIGHTHAND_anchura_FRAME
                                RIGHTHAND_factor_y = RIGHTHAND_altura_pose_BBDD / RIGHTHAND_altura_FRAME

                                RIGHTHAND_THUMB_TIP_x_FRAME_modified = RIGHTHAND_THUMB_TIP_x_FRAME * RIGHTHAND_factor_x
                                RIGHTHAND_THUMB_TIP_y_FRAME_modified = RIGHTHAND_THUMB_TIP_y_FRAME * RIGHTHAND_factor_y

                                RIGHTHAND_INDEX_FINGER_TIP_x_FRAME_modified = RIGHTHAND_INDEX_FINGER_TIP_x_FRAME * RIGHTHAND_factor_x
                                RIGHTHAND_INDEX_FINGER_TIP_y_FRAME_modified = RIGHTHAND_INDEX_FINGER_TIP_y_FRAME * RIGHTHAND_factor_y

                                RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified = RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME * RIGHTHAND_factor_x
                                RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified = RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME * RIGHTHAND_factor_y

                                RIGHTHAND_RING_FINGER_TIP_x_FRAME_modified = RIGHTHAND_RING_FINGER_TIP_x_FRAME * RIGHTHAND_factor_x
                                RIGHTHAND_RING_FINGER_TIP_y_FRAME_modified = RIGHTHAND_RING_FINGER_TIP_y_FRAME * RIGHTHAND_factor_y

                                RIGHTHAND_PINKY_TIP_x_FRAME_modified = RIGHTHAND_PINKY_TIP_x_FRAME * RIGHTHAND_factor_x
                                RIGHTHAND_PINKY_TIP_y_FRAME_modified = RIGHTHAND_PINKY_TIP_y_FRAME * RIGHTHAND_factor_y
                                ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################

                                # ###------------------ Ahora ambas capturas tienen la misma profundidad, la profundidad de
                                # la captura de la BBDD. Hemos adaptado la NewPose a la BBDD.

                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################
                                RIGHTHAND_diferencia_THUMB_INDEX_x = RIGHTHAND_lista_THUMB_TIP_x_BBDD[
                                                                         j] - RIGHTHAND_THUMB_TIP_x_FRAME_modified
                                RIGHTHAND_diferencia_THUMB_INDEX_y = RIGHTHAND_lista_THUMB_TIP_y_BBDD[
                                                                         j] - RIGHTHAND_THUMB_TIP_y_FRAME_modified
                                # Solo hay que mirar la diferencia de un dedo de la BBDD con un dedo del FRAME porque toda la
                                # mano es un bloque, entonces si la diferencia de distancia entre un dedo y otro es,
                                # por ejemplo, 0.2, significa que todos los dedos tienen esa misma distancia con sus
                                # respectivos dedos si es la misma pose.

                                RIGHTHAND_THUMB_TIP_x_FRAME_modified_and_shifted = RIGHTHAND_THUMB_TIP_x_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_x
                                RIGHTHAND_THUMB_TIP_y_FRAME_modified_and_shifted = RIGHTHAND_THUMB_TIP_y_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_y

                                RIGHTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted = RIGHTHAND_INDEX_FINGER_TIP_x_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_x
                                RIGHTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted = RIGHTHAND_INDEX_FINGER_TIP_y_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_y

                                RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted = RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_x
                                RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted = RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_y

                                RIGHTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted = RIGHTHAND_RING_FINGER_TIP_x_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_x
                                RIGHTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted = RIGHTHAND_RING_FINGER_TIP_y_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_y

                                RIGHTHAND_PINKY_TIP_x_FRAME_modified_and_shifted = RIGHTHAND_PINKY_TIP_x_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_x
                                RIGHTHAND_PINKY_TIP_y_FRAME_modified_and_shifted = RIGHTHAND_PINKY_TIP_y_FRAME_modified + RIGHTHAND_diferencia_THUMB_INDEX_y
                                ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################

                                # Ahora, todas las coordenadas están situadas en el mismo sitio que en la BBDD, por tanto, si son la misma
                                # pose, los rectángulos de cada punto coindirán con los de las capturas.

                                lista_RIGHTHAND_x = "lista_RIGHTHAND_x_" + str(j)
                                lista_RIGHTHAND_y = "lista_RIGHTHAND_y_" + str(j)
                                RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x] = [
                                    RIGHTHAND_THUMB_TIP_x_FRAME_modified_and_shifted,
                                    RIGHTHAND_INDEX_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    RIGHTHAND_MIDDLE_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    RIGHTHAND_RING_FINGER_TIP_x_FRAME_modified_and_shifted,
                                    RIGHTHAND_PINKY_TIP_x_FRAME_modified_and_shifted]

                                RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y] = [
                                    RIGHTHAND_THUMB_TIP_y_FRAME_modified_and_shifted,
                                    RIGHTHAND_INDEX_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    RIGHTHAND_MIDDLE_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    RIGHTHAND_RING_FINGER_TIP_y_FRAME_modified_and_shifted,
                                    RIGHTHAND_PINKY_TIP_y_FRAME_modified_and_shifted]
                    ########################## COORDENADAS DEL FRAME MODIFIED & SHIFTED ###############################

                    for j in range(4):
                        ############################    CONDICIONES     ############################
                        # Márgenes
                        # if(margen1 > punto x ó y > -margen1)

                        LEFTHAND_margins_each_HANDPOSE_in_video = "LEFTHAND_margins_each_HANDPOSE_" + str(j)
                        RIGHTHAND_margins_each_HANDPOSE_in_video = "RIGHTHAND_margins_each_HANDPOSE_" + str(j)
                        for i in range(5):
                            LEFTHAND_lista_marginsRectangle_finger_in_video = "LEFTHAND_lista_marginsRectangle_finger_" + str(
                                i)
                            RIGHTHAND_lista_marginsRectangle_finger_in_video = "RIGHTHAND_lista_marginsRectangle_finger_" + str(
                                i)
                            # Coordenada1 = x + 0.05
                            # Coordenada2 = x - 0.05
                            # Coordenada3 = y + 0.05
                            # Coordenada4 = y - 0.05

                            if i == 0:
                                LEFTHAND_coordenada1 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][0]
                                LEFTHAND_coordenada2 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][1]
                                LEFTHAND_coordenada3 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][2]
                                LEFTHAND_coordenada4 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][3]

                                RIGHTHAND_coordenada1 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][0]
                                RIGHTHAND_coordenada2 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][1]
                                RIGHTHAND_coordenada3 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][2]
                                RIGHTHAND_coordenada4 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][3]

                            if i == 1:
                                LEFTHAND_coordenada5 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][0]
                                LEFTHAND_coordenada6 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][1]
                                LEFTHAND_coordenada7 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][2]
                                LEFTHAND_coordenada8 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][3]

                                RIGHTHAND_coordenada5 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][0]
                                RIGHTHAND_coordenada6 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][1]
                                RIGHTHAND_coordenada7 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][2]
                                RIGHTHAND_coordenada8 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][3]

                            if i == 2:
                                LEFTHAND_coordenada9 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][0]
                                LEFTHAND_coordenada10 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][1]
                                LEFTHAND_coordenada11 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][2]
                                LEFTHAND_coordenada12 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][3]

                                RIGHTHAND_coordenada9 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][0]
                                RIGHTHAND_coordenada10 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][1]
                                RIGHTHAND_coordenada11 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][2]
                                RIGHTHAND_coordenada12 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][3]

                            if i == 3:
                                LEFTHAND_coordenada13 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][0]
                                LEFTHAND_coordenada14 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][1]
                                LEFTHAND_coordenada15 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][2]
                                LEFTHAND_coordenada16 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][3]

                                RIGHTHAND_coordenada13 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][0]
                                RIGHTHAND_coordenada14 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][1]
                                RIGHTHAND_coordenada15 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][2]
                                RIGHTHAND_coordenada16 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][3]

                            if i == 4:
                                LEFTHAND_coordenada17 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][0]
                                LEFTHAND_coordenada18 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][1]
                                LEFTHAND_coordenada19 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][2]
                                LEFTHAND_coordenada20 = \
                                    LEFTHAND_diccionario_principal[LEFTHAND_margins_each_HANDPOSE_in_video][
                                        LEFTHAND_lista_marginsRectangle_finger_in_video][3]

                                RIGHTHAND_coordenada17 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][0]
                                RIGHTHAND_coordenada18 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][1]
                                RIGHTHAND_coordenada19 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][2]
                                RIGHTHAND_coordenada20 = \
                                    RIGHTHAND_diccionario_principal[RIGHTHAND_margins_each_HANDPOSE_in_video][
                                        RIGHTHAND_lista_marginsRectangle_finger_in_video][3]

                        LEFTHAND_coordenadas_THUMB = [LEFTHAND_coordenada1, LEFTHAND_coordenada2,
                                                      LEFTHAND_coordenada3, LEFTHAND_coordenada4]
                        LEFTHAND_coordenadas_INDEX = [LEFTHAND_coordenada5, LEFTHAND_coordenada6,
                                                      LEFTHAND_coordenada7, LEFTHAND_coordenada8]
                        LEFTHAND_coordenadas_MIDDLE = [LEFTHAND_coordenada9, LEFTHAND_coordenada10,
                                                       LEFTHAND_coordenada11, LEFTHAND_coordenada12]
                        LEFTHAND_coordenadas_RING = [LEFTHAND_coordenada13, LEFTHAND_coordenada14,
                                                     LEFTHAND_coordenada15, LEFTHAND_coordenada16]
                        LEFTHAND_coordenadas_PINKY = [LEFTHAND_coordenada17, LEFTHAND_coordenada18,
                                                      LEFTHAND_coordenada19, LEFTHAND_coordenada20]

                        RIGHTHAND_coordenadas_THUMB = [RIGHTHAND_coordenada1, RIGHTHAND_coordenada2,
                                                       RIGHTHAND_coordenada3, RIGHTHAND_coordenada4]
                        RIGHTHAND_coordenadas_INDEX = [RIGHTHAND_coordenada5, RIGHTHAND_coordenada6,
                                                       RIGHTHAND_coordenada7, RIGHTHAND_coordenada8]
                        RIGHTHAND_coordenadas_MIDDLE = [RIGHTHAND_coordenada9, RIGHTHAND_coordenada10,
                                                        RIGHTHAND_coordenada11, RIGHTHAND_coordenada12]
                        RIGHTHAND_coordenadas_RING = [RIGHTHAND_coordenada13, RIGHTHAND_coordenada14,
                                                      RIGHTHAND_coordenada15, RIGHTHAND_coordenada16]
                        RIGHTHAND_coordenadas_PINKY = [RIGHTHAND_coordenada17, RIGHTHAND_coordenada18,
                                                       RIGHTHAND_coordenada19, RIGHTHAND_coordenada20]

                        lista_LEFTHAND_x = "lista_LEFTHAND_x_" + str(j)
                        lista_LEFTHAND_y = "lista_LEFTHAND_y_" + str(j)
                        lista_RIGHTHAND_x = "lista_RIGHTHAND_x_" + str(j)
                        lista_RIGHTHAND_y = "lista_RIGHTHAND_y_" + str(j)

                        if (LEFTHAND_coordenadas_THUMB[0] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x][0] >
                            LEFTHAND_coordenadas_THUMB[1]) \
                                and (LEFTHAND_coordenadas_THUMB[2] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y][0] >
                                     LEFTHAND_coordenadas_THUMB[3]) \
                                and (LEFTHAND_coordenadas_INDEX[0] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x][1] >
                                     LEFTHAND_coordenadas_INDEX[1]) \
                                and (LEFTHAND_coordenadas_INDEX[2] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y][1] >
                                     LEFTHAND_coordenadas_INDEX[3]) \
                                and (LEFTHAND_coordenadas_MIDDLE[0] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x][2] >
                                     LEFTHAND_coordenadas_MIDDLE[1]) \
                                and (LEFTHAND_coordenadas_MIDDLE[2] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y][2] >
                                     LEFTHAND_coordenadas_MIDDLE[3]) \
                                and (LEFTHAND_coordenadas_RING[0] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x][3] >
                                     LEFTHAND_coordenadas_RING[1]) \
                                and (LEFTHAND_coordenadas_RING[2] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y][3] >
                                     LEFTHAND_coordenadas_RING[3]) \
                                and (LEFTHAND_coordenadas_PINKY[0] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_x][4] >
                                     LEFTHAND_coordenadas_PINKY[1]) \
                                and (LEFTHAND_coordenadas_PINKY[2] > LEFTHAND_diccionario_FRAME[lista_LEFTHAND_y][4] >
                                     LEFTHAND_coordenadas_PINKY[3]) \
                                and (RIGHTHAND_coordenadas_THUMB[0] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x][0] >
                                     RIGHTHAND_coordenadas_THUMB[1]) \
                                and (RIGHTHAND_coordenadas_THUMB[2] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y][0] >
                                     RIGHTHAND_coordenadas_THUMB[3]) \
                                and (RIGHTHAND_coordenadas_INDEX[0] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x][1] >
                                     RIGHTHAND_coordenadas_INDEX[1]) \
                                and (RIGHTHAND_coordenadas_INDEX[2] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y][1] >
                                     RIGHTHAND_coordenadas_INDEX[3]) \
                                and (RIGHTHAND_coordenadas_MIDDLE[0] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x][2] >
                                     RIGHTHAND_coordenadas_MIDDLE[1]) \
                                and (RIGHTHAND_coordenadas_MIDDLE[2] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y][2] >
                                     RIGHTHAND_coordenadas_MIDDLE[3]) \
                                and (RIGHTHAND_coordenadas_RING[0] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x][3] >
                                     RIGHTHAND_coordenadas_RING[1]) \
                                and (RIGHTHAND_coordenadas_RING[2] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y][3] >
                                     RIGHTHAND_coordenadas_RING[3]) \
                                and (RIGHTHAND_coordenadas_PINKY[0] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_x][4] >
                                     RIGHTHAND_coordenadas_PINKY[1]) \
                                and (RIGHTHAND_coordenadas_PINKY[2] > RIGHTHAND_diccionario_FRAME[lista_RIGHTHAND_y][4] >
                                     RIGHTHAND_coordenadas_PINKY[3]):
                            timer_finished = True
                            command_ended = False
                            arrow_confirmed = False
                            captured_pose_number = j
                            drone_thread = threading.Thread(target=all_drone_commands)
                            drone_thread.start()

                            decision_tomada = True

                if (decision_tomada is not True):
                    # print("No ha detectado ninguna pose.")
                    decision_tomada = True


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break


def computer_camera_ON_BODY_POSE():
    close_photos()
    global captured_pose_number
    global counter_pose
    global diccionario_principal
    global lista_LEFT_SHOULDER_x_BBDD
    global lista_LEFT_SHOULDER_y_BBDD
    global tello
    global command_ended
    global frame
    global arrow_confirmed
    global takingVideo
    global timer_finished

    # ABRIMOS VÍDEOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Define las coordenadas del punto superior izquierdo de la ventana
    window_x_Video = 0
    window_y_Video = 0

    # Define el ancho y alto de la ventana
    window_width_Video = 900
    window_height_Video = 725

    # Define la posición de la ventana en la pantalla
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Frame", window_x_Video, window_y_Video)
    cv2.resizeWindow("Frame", window_width_Video, window_height_Video)

    contador2 = 0
    contador3 = 0
    contador4 = 0

    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################
    for i in range(counter_pose):
        nombre_archivo = f"POSE_{i}.jpg"
        if i < 4:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1592
            window_y_image = 0 + contador2

            contador2 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 4 and i < 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 1270
            window_y_image = 0 + contador3

            contador3 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        elif i >= 8:
            ####################### Mostrar fotos en ventanas de manera ordenada ##############################
            window_x_image = 948
            window_y_image = 0 + contador4

            contador4 += 255
            # Define el ancho y alto de la ventana
            window_width_image = 322
            window_height_image = 244

        # Define la posición de la ventana en la pantalla
        cv2.namedWindow(nombre_archivo, cv2.WINDOW_NORMAL)
        cv2.moveWindow(nombre_archivo, window_x_image, window_y_image)
        cv2.resizeWindow(nombre_archivo, window_width_image, window_height_image)
        ####################### Mostrar fotos en ventanas de manera ordenada ##############################
        image = cv2.imread(nombre_archivo)
        cv2.imshow(nombre_archivo, image)
    ############################################ MOSTRAMOS LAS POSES EN VENTANAS ###################################

    while takingVideo:
        ret, frame = cap.read()
        if ret is not True:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        with mp_pose.Pose(
                static_image_mode=True) as pose:
            results = pose.process(frame_rgb)
        ################################# Inicio #####################################

        if arrow_confirmed is True:
            if results.pose_landmarks is not None:
                LEFT_SHOULDER_x_BBDD = int(
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)
                LEFT_SHOULDER_y_BBDD = int(
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)

                LEFT_ELBOW_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * width)
                LEFT_ELBOW_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * height)

                LEFT_WRIST_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * width)
                LEFT_WRIST_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * height)

                RIGHT_SHOULDER_x_BBDD = int(
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)
                RIGHT_SHOULDER_y_BBDD = int(
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)

                RIGHT_ELBOW_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * width)
                RIGHT_ELBOW_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * height)

                RIGHT_WRIST_x_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * width)
                RIGHT_WRIST_y_BBDD = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * height)

                cv2.circle(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD), 6, (128, 0, 255), -1)
                cv2.circle(frame, (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD), 6, (128, 0, 255), -1)
                cv2.circle(frame, (LEFT_WRIST_x_BBDD, LEFT_WRIST_y_BBDD), 6, (128, 0, 255), -1)
                cv2.circle(frame, (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD), 6, (128, 0, 255), -1)
                cv2.circle(frame, (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD), 6, (128, 0, 255), -1)
                cv2.circle(frame, (RIGHT_WRIST_x_BBDD, RIGHT_WRIST_y_BBDD), 6, (128, 0, 255), -1)

                cv2.line(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD), (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD),
                         (255, 255, 255), 3)
                cv2.line(frame, (LEFT_ELBOW_x_BBDD, LEFT_ELBOW_y_BBDD), (LEFT_WRIST_x_BBDD, LEFT_WRIST_y_BBDD),
                         (255, 255, 255), 3)
                cv2.line(frame, (LEFT_SHOULDER_x_BBDD, LEFT_SHOULDER_y_BBDD),
                         (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD),
                         (255, 255, 255), 3)
                cv2.line(frame, (RIGHT_SHOULDER_x_BBDD, RIGHT_SHOULDER_y_BBDD),
                         (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD),
                         (255, 255, 255), 3)
                cv2.line(frame, (RIGHT_ELBOW_x_BBDD, RIGHT_ELBOW_y_BBDD), (RIGHT_WRIST_x_BBDD, RIGHT_WRIST_y_BBDD),
                         (255, 255, 255), 3)

                #################### Cogemos los puntos clave de la pose del cuerpo ################################
                # Los puntos clave serán en total 6 puntos: hombros, codos y muñecas.
                LEFT_SHOULDER_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x
                LEFT_SHOULDER_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y

                LEFT_ELBOW_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x
                LEFT_ELBOW_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y

                LEFT_WRIST_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
                LEFT_WRIST_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y

                RIGHT_SHOULDER_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x
                RIGHT_SHOULDER_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y

                RIGHT_ELBOW_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x
                RIGHT_ELBOW_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y

                RIGHT_WRIST_x_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
                RIGHT_WRIST_y_FRAME = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y

                lista_x_FRAME = [LEFT_SHOULDER_x_FRAME, LEFT_ELBOW_x_FRAME, LEFT_WRIST_x_FRAME,
                                 RIGHT_SHOULDER_x_FRAME, RIGHT_ELBOW_x_FRAME, RIGHT_WRIST_x_FRAME]

                lista_y_FRAME = [LEFT_SHOULDER_y_FRAME, LEFT_ELBOW_y_FRAME, LEFT_WRIST_y_FRAME,
                                 RIGHT_SHOULDER_y_FRAME, RIGHT_ELBOW_y_FRAME, RIGHT_WRIST_y_FRAME]

                # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO
                XMAX = max(lista_x_FRAME)
                XMIN = min(lista_x_FRAME)
                YMAX = max(lista_y_FRAME)
                YMIN = min(lista_y_FRAME)

                anchura_FRAME = XMAX - XMIN
                altura_FRAME = YMAX - YMIN
                # RECTÁNGULO PARA ADAPTAR EL TAMAÑO DE LA MANO DEPENDIENDO SI ESTÁ MÁS LEJOS O MÁS CERCA DE LA MANO

                # Además, me pasaba que en algún momento, no aparecía la mano y
                # entonces se quedaba con los datos de la anterior pose, entonces aunque no saliera ninguna pose en
                # pantalla, seguía diciendo que había una pose porque se le quedaban los datos guardados. Para
                # resolver esto, lo que se ha hecho es que cada vez que vaya a comparar poses, que antes compruebe
                # que haya una mano. Si no hay ninguna mano a detectar, los valores a comparar se irán a 0 y por
                # tanto, saldrá que no hay ninguna pose hecha.
                ManoDetectada = True
                if results.pose_landmarks is None:
                    ManoDetectada = False
                    anchura_FRAME = 1
                    altura_FRAME = 1
                    LEFT_SHOULDER_x_FRAME_modified_and_shifted = 0
                    LEFT_SHOULDER_y_FRAME_modified_and_shifted = 0
                    LEFT_ELBOW_x_FRAME_modified_and_shifted = 0
                    LEFT_ELBOW_y_FRAME_modified_and_shifted = 0
                    LEFT_WRIST_x_FRAME_modified_and_shifted = 0
                    LEFT_WRIST_y_FRAME_modified_and_shifted = 0
                    RIGHT_SHOULDER_x_FRAME_modified_and_shifted = 0
                    RIGHT_SHOULDER_y_FRAME_modified_and_shifted = 0
                    RIGHT_ELBOW_x_FRAME_modified_and_shifted = 0
                    RIGHT_ELBOW_y_FRAME_modified_and_shifted = 0
                    RIGHT_WRIST_x_FRAME_modified_and_shifted = 0
                    RIGHT_WRIST_y_FRAME_modified_and_shifted = 0

                decision_tomada = False

                if decision_tomada is not True and ManoDetectada is True:
                    for j in range(4):
                        ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################
                        rectangle_adapt_size_BBDD_in_video = "rectangle_adapt_size_BBDD_" + str(j)

                        anchura_pose_BBDD = diccionario_principal[rectangle_adapt_size_BBDD_in_video][0]
                        altura_pose_BBDD = diccionario_principal[rectangle_adapt_size_BBDD_in_video][1]

                        factor_x = anchura_pose_BBDD / anchura_FRAME
                        factor_y = altura_pose_BBDD / altura_FRAME

                        LEFT_SHOULDER_x_FRAME_modified = LEFT_SHOULDER_x_FRAME * factor_x
                        LEFT_SHOULDER_y_FRAME_modified = LEFT_SHOULDER_y_FRAME * factor_y

                        LEFT_ELBOW_x_FRAME_modified = LEFT_ELBOW_x_FRAME * factor_x
                        LEFT_ELBOW_y_FRAME_modified = LEFT_ELBOW_y_FRAME * factor_y

                        LEFT_WRIST_x_FRAME_modified = LEFT_WRIST_x_FRAME * factor_x
                        LEFT_WRIST_y_FRAME_modified = LEFT_WRIST_y_FRAME * factor_y

                        RIGHT_SHOULDER_x_FRAME_modified = RIGHT_SHOULDER_x_FRAME * factor_x
                        RIGHT_SHOULDER_y_FRAME_modified = RIGHT_SHOULDER_y_FRAME * factor_y

                        RIGHT_ELBOW_x_FRAME_modified = RIGHT_ELBOW_x_FRAME * factor_x
                        RIGHT_ELBOW_y_FRAME_modified = RIGHT_ELBOW_y_FRAME * factor_y

                        RIGHT_WRIST_x_FRAME_modified = RIGHT_WRIST_x_FRAME * factor_x
                        RIGHT_WRIST_y_FRAME_modified = RIGHT_WRIST_y_FRAME * factor_y

                        ###################### COORDENADAS DEL FRAME AMPLIADAS/REDUCIDAS ##############################

                        # ###------------------ Ahora ambas capturas tienen la misma profundidad, la profundidad de
                        # la captura de la BBDD. Hemos adaptado la NewPose a la BBDD.

                        ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################
                        diferencia_LEFT_SHOULDER_x = lista_LEFT_SHOULDER_x_BBDD[j] - LEFT_SHOULDER_x_FRAME_modified
                        diferencia_LEFT_SHOULDER_y = lista_LEFT_SHOULDER_y_BBDD[j] - LEFT_SHOULDER_y_FRAME_modified
                        # Solo hay que mirar la diferencia de un dedo de la BBDD con un dedo del FRAME porque toda la
                        # mano es un bloque, entonces si la diferencia de distancia entre un dedo y otro es,
                        # por ejemplo, 0.2, significa que todos los dedos tienen esa misma distancia con sus
                        # respectivos dedos si es la misma pose.

                        LEFT_SHOULDER_x_FRAME_modified_and_shifted = LEFT_SHOULDER_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        LEFT_SHOULDER_y_FRAME_modified_and_shifted = LEFT_SHOULDER_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        LEFT_ELBOW_x_FRAME_modified_and_shifted = LEFT_ELBOW_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        LEFT_ELBOW_y_FRAME_modified_and_shifted = LEFT_ELBOW_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        LEFT_WRIST_x_FRAME_modified_and_shifted = LEFT_WRIST_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        LEFT_WRIST_y_FRAME_modified_and_shifted = LEFT_WRIST_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        RIGHT_SHOULDER_x_FRAME_modified_and_shifted = RIGHT_SHOULDER_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        RIGHT_SHOULDER_y_FRAME_modified_and_shifted = RIGHT_SHOULDER_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        RIGHT_ELBOW_x_FRAME_modified_and_shifted = RIGHT_ELBOW_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        RIGHT_ELBOW_y_FRAME_modified_and_shifted = RIGHT_ELBOW_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        RIGHT_WRIST_x_FRAME_modified_and_shifted = RIGHT_WRIST_x_FRAME_modified + diferencia_LEFT_SHOULDER_x
                        RIGHT_WRIST_y_FRAME_modified_and_shifted = RIGHT_WRIST_y_FRAME_modified + diferencia_LEFT_SHOULDER_y

                        ############################# COORDENADAS DEL FRAME DESPLAZADAS ###############################

                        # Ahora, todas las coordenadas están situadas en el mismo sitio que en la BBDD, por tanto, si son la misma
                        # pose, los rectángulos de cada punto coindirán con los de las capturas.

                        ############################    CONDICIONES     ############################
                        # Márgenes
                        # if(margen1 > punto x ó y > -margen1)
                        margins_each_BODYPOSE_in_video = "margins_each_BODYPOSE_" + str(j)
                        for i in range(6):
                            lista_marginsRectangle_shoulders_elbows_wrists_in_video = "lista_marginsRectangle_shoulders_elbows_wrists_" + str(
                                i)
                            # Coordenada1 = x + 0.05
                            # Coordenada2 = x - 0.05
                            # Coordenada3 = y + 0.05
                            # Coordenada4 = y - 0.05

                            if i == 0:
                                coordenada1 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada2 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada3 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada4 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                            if i == 1:
                                coordenada5 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada6 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada7 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada8 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                            if i == 2:
                                coordenada9 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada10 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada11 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada12 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                            if i == 3:
                                coordenada13 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada14 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada15 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada16 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                            if i == 4:
                                coordenada17 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada18 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada19 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada20 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                            if i == 5:
                                coordenada21 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][0]
                                coordenada22 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][1]
                                coordenada23 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][2]
                                coordenada24 = \
                                    diccionario_principal[margins_each_BODYPOSE_in_video][
                                        lista_marginsRectangle_shoulders_elbows_wrists_in_video][3]

                        coordenadas_LEFT_SHOULDER = [coordenada1, coordenada2, coordenada3, coordenada4]
                        coordenadas_LEFT_ELBOW = [coordenada5, coordenada6, coordenada7, coordenada8]
                        coordenadas_LEFT_WRIST = [coordenada9, coordenada10, coordenada11, coordenada12]
                        coordenadas_RIGHT_SHOULDER = [coordenada13, coordenada14, coordenada15, coordenada16]
                        coordenadas_RIGHT_ELBOW = [coordenada17, coordenada18, coordenada19, coordenada20]
                        coordenadas_RIGHT_WRIST = [coordenada21, coordenada22, coordenada23, coordenada24]

                        if (coordenadas_LEFT_SHOULDER[0] > LEFT_SHOULDER_x_FRAME_modified_and_shifted >
                            coordenadas_LEFT_SHOULDER[1]) \
                                and (coordenadas_LEFT_SHOULDER[2] > LEFT_SHOULDER_y_FRAME_modified_and_shifted >
                                     coordenadas_LEFT_SHOULDER[3]) \
                                and (coordenadas_LEFT_ELBOW[0] > LEFT_ELBOW_x_FRAME_modified_and_shifted >
                                     coordenadas_LEFT_ELBOW[1]) \
                                and (coordenadas_LEFT_ELBOW[2] > LEFT_ELBOW_y_FRAME_modified_and_shifted >
                                     coordenadas_LEFT_ELBOW[3]) \
                                and (coordenadas_LEFT_WRIST[0] > LEFT_WRIST_x_FRAME_modified_and_shifted >
                                     coordenadas_LEFT_WRIST[1]) \
                                and (coordenadas_LEFT_WRIST[2] > LEFT_WRIST_y_FRAME_modified_and_shifted >
                                     coordenadas_LEFT_WRIST[3]) \
                                and (coordenadas_RIGHT_SHOULDER[0] > RIGHT_SHOULDER_x_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_SHOULDER[1]) \
                                and (coordenadas_RIGHT_SHOULDER[2] > RIGHT_SHOULDER_y_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_SHOULDER[3]) \
                                and (coordenadas_RIGHT_ELBOW[0] > RIGHT_ELBOW_x_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_ELBOW[1]) \
                                and (coordenadas_RIGHT_ELBOW[2] > RIGHT_ELBOW_y_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_ELBOW[3]) \
                                and (coordenadas_RIGHT_WRIST[0] > RIGHT_WRIST_x_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_WRIST[1]) \
                                and (coordenadas_RIGHT_WRIST[2] > RIGHT_WRIST_y_FRAME_modified_and_shifted >
                                     coordenadas_RIGHT_WRIST[3]):
                            timer_finished = True
                            command_ended = False
                            arrow_confirmed = False
                            captured_pose_number = j
                            drone_thread = threading.Thread(target=all_drone_commands)
                            drone_thread.start()

                            decision_tomada = True

                if (decision_tomada is not True):
                    # print("No ha detectado ninguna pose.")
                    decision_tomada = True
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
################################################## PLAY ###############################################################

#######################################################################################################################
#######################################################################################################################

################################################## DIFFICULTY ########################################################
def easy_difficulty_button():
    global set_time_reaction
    global set_game_score
    global set_time_between_arrow
    global easy_difficulty

    easy_difficulty = True

    set_time_reaction = 8
    set_game_score = 3
    set_time_between_arrow = 3

    main_menu()

def hard_difficulty_button():
    global set_time_reaction
    global set_game_score
    global set_time_between_arrow
    global hard_difficulty

    hard_difficulty = True

    set_time_reaction = 5
    set_game_score = 5
    set_time_between_arrow = 0.5

    main_menu()

def impossible_difficulty_button():
    global set_time_reaction
    global set_game_score
    global set_time_between_arrow
    global impossible_difficulty

    impossible_difficulty = True

    set_time_reaction = 3
    set_game_score = 10
    set_time_between_arrow = 0.5

    main_menu()


def reset_difficulty():
    global easy_difficulty
    global hard_difficulty
    global impossible_difficulty

    easy_difficulty = False
    hard_difficulty = False
    impossible_difficulty = False

def game_difficulty():
    global app
    global image_label
    global my_image
    global check_var

    my_image = customtkinter.CTkImage(light_image=Image.open("circo.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    EasyButton = customtkinter.CTkButton(app, text="EASY", command=easy_difficulty_button)
    EasyButton.place(x=400, y=475)
    EasyButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    HardButton = customtkinter.CTkButton(app, text="HARD", command=hard_difficulty_button)
    HardButton.place(x=575, y=475)
    HardButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    ImpossibleButton = customtkinter.CTkButton(app, text="IMPOSSIBLE", command=impossible_difficulty_button)
    ImpossibleButton.place(x=750, y=475)
    ImpossibleButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    text = customtkinter.CTkLabel(app, text="DIFFICULTY", font=("Times New Roman", 80))
    text.place(x=415, y=340)
    text.configure(fg_color="#1E2768", text_color="white")

    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=850, y=610)
    checkbox.configure(bg_color="black", hover_color="#1E2768", fg_color="#1E2768")

    BackButton2 = customtkinter.CTkButton(app, text="BACK", command=backbutton2)
    BackButton2.place(x=850, y=570)
    BackButton2.configure(fg_color="black", text_color="white", font=("Times New Roman", 20), border_color="#B32028",
                         bg_color="#6C1211", hover_color="#474747", width=15)
################################################## DIFFICULTY ########################################################

#######################################################################################################################
#######################################################################################################################


def main_menu():
    global app
    global image_label
    global my_image
    global check_var


    my_image = customtkinter.CTkImage(light_image=Image.open("circo.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    PlayButton = customtkinter.CTkButton(app, text="PLAY", command=play)
    PlayButton.place(x=575, y=320)
    PlayButton.configure(fg_color="#FFC502", text_color="#BB1215", font=("TIMES NEW ROMAN", 50), border_color="white",
                         bg_color="#B32028", hover_color="#BFB208", border_width=3)


    ConnectDroneButton = customtkinter.CTkButton(app, text="CONNECT DRONE", command=connect_drone)
    ConnectDroneButton.place(x=435, y=470)
    ConnectDroneButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    how_to_play_button = customtkinter.CTkButton(app, text="HOW TO PLAY", command=how_to_play)
    how_to_play_button.place(x=685, y=470)
    how_to_play_button.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    AssignCommandsButton = customtkinter.CTkButton(app, text="ASSIGN COMMANDS", command=assign_commands)
    AssignCommandsButton.place(x=423, y=420)
    AssignCommandsButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    ModifyCommandsButton = customtkinter.CTkButton(app, text="MODIFY COMMANDS", command=modify_commands)
    ModifyCommandsButton.place(x=656, y=420)
    ModifyCommandsButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    ShowPoses = customtkinter.CTkButton(app, text="ShowPoses", command=show_photos)
    ShowPoses.place(x=455, y=520)
    ShowPoses.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    ClosePoses = customtkinter.CTkButton(app, text="ClosePoses", command=close_photos)
    ClosePoses.place(x=690, y=520)
    ClosePoses.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 17), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")



    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=850, y=610)
    checkbox.configure(bg_color="black", hover_color="#1E2768", fg_color= "#1E2768")

    BackButton3= customtkinter.CTkButton(app, text="BACK", command=backbutton3)
    BackButton3.place(x=850, y=570)
    BackButton3.configure(fg_color="black", text_color="white", font=("Times New Roman", 20), border_color="#B32028",
                         bg_color="#6C1211", hover_color="#474747", width=15)


def ONE_HAND():
    global game_mode

    reset_all_variables()
    game_mode = "ONE_HAND"

    game_difficulty()

def TWO_HANDS():
    global game_mode

    reset_all_variables()
    game_mode = "TWO_HANDS"
    game_difficulty()

def BODY_POSE():
    global game_mode

    reset_all_variables()
    game_mode = "BODY_POSE"
    game_difficulty()






def go_back_to_the_start():
    global root
    close_menu()
    root = CTk()
    root.geometry("1200x100")
    root.title("¿Qué quieres hacer?")

    menu_frame = CTkFrame(root, bg_color="#F0E68C")
    menu_frame.pack(fill=BOTH, expand=1)

    OneHandButton = CTkButton(menu_frame, text="ONE HAND", command=ONE_HAND, bg_color="#87CEEB")
    OneHandButton.pack(side=LEFT)

    TwoHandsButton = CTkButton(menu_frame, text="TWO HANDS", command=TWO_HANDS, bg_color="#87CEEB")
    TwoHandsButton.pack(side=LEFT)

    BodyPoseButton = CTkButton(menu_frame, text="BODY POSE", command=BODY_POSE, bg_color="#87CEEB")
    BodyPoseButton.pack(side=LEFT)

    close_button = CTkButton(menu_frame, text="Cerrar", command=close_menu)
    close_button.pack(side=LEFT)

    root.mainloop()

def reset_all_variables():
    global command_ended
    command_ended = True

    global arrow_confirmed
    arrow_confirmed = False

    global process_finished
    process_finished = True

    global score
    score = 0

    global wrong_pose
    wrong_pose = False

    global time_exceeded
    time_exceeded = False

    global winner
    winner = False

    global timer_finished
    timer_finished = False

    global easy_difficulty
    global hard_difficulty
    global impossible_difficulty
    easy_difficulty = False
    hard_difficulty = False
    impossible_difficulty = False

    global takingVideo
    takingVideo = True


    global taken_photo
    taken_photo = False

    global taking_shot
    taking_shot = False


    global MOVE_UP_assigned
    global MOVE_DOWN_assigned
    global MOVE_LEFT_assigned
    global MOVE_RIGHT_assigned
    global FLIP_LEFT_assigned
    global FLIP_RIGHT_assigned
    MOVE_UP_assigned = False
    MOVE_DOWN_assigned = False
    MOVE_LEFT_assigned = False
    MOVE_RIGHT_assigned = False
    FLIP_LEFT_assigned = False
    FLIP_RIGHT_assigned = False


    global MOVE_UP_pose_number
    global MOVE_DOWN_pose_number
    global MOVE_LEFT_pose_number
    global MOVE_RIGHT_pose_number
    global FLIP_LEFT_pose_number
    global FLIP_RIGHT_pose_number
    MOVE_UP_pose_number = 0
    MOVE_DOWN_pose_number = 0
    MOVE_LEFT_pose_number = 0
    MOVE_RIGHT_pose_number = 0
    FLIP_LEFT_pose_number = 0
    FLIP_RIGHT_pose_number = 0


    global counter_pose
    global captured_pose_number
    global pose_number
    counter_pose = 0
    captured_pose_number = 0
    pose_number = 0

    #One Hand
    global diccionario_principal
    global lista_THUMB_TIP_x_BBDD
    global lista_THUMB_TIP_y_BBDD
    diccionario_principal = {}
    lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
    lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame

    #Body Pose
    global lista_LEFT_SHOULDER_x_BBDD
    global lista_LEFT_SHOULDER_y_BBDD
    lista_LEFT_SHOULDER_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
    lista_LEFT_SHOULDER_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame



    #TWO HANDS
    global LEFTHAND_diccionario_principal
    global RIGHTHAND_diccionario_principal
    global LEFTHAND_diccionario_FRAME
    global RIGHTHAND_diccionario_FRAME
    LEFTHAND_diccionario_principal = {}
    RIGHTHAND_diccionario_principal = {}
    LEFTHAND_diccionario_FRAME = {}
    RIGHTHAND_diccionario_FRAME = {}

    global LEFTHAND_lista_THUMB_TIP_x_BBDD
    global LEFTHAND_lista_THUMB_TIP_y_BBDD
    global RIGHTHAND_lista_THUMB_TIP_x_BBDD
    global RIGHTHAND_lista_THUMB_TIP_y_BBDD

    LEFTHAND_lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
    LEFTHAND_lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
    RIGHTHAND_lista_THUMB_TIP_x_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame
    RIGHTHAND_lista_THUMB_TIP_y_BBDD = []  # esta lista se utilizará luego para desplazar la pose del frame

def how_to_play():
    # Crear una ventana
    ventana = tkinter.Toplevel()
    ventana.geometry("1500x1050")
    ventana.title("HOW TO PLAY")

    # Cargar la imagen
    imagen = Image.open("pergamino_english.png")

    # Redimensionar la imagen si es necesario
    # imagen = imagen.resize((ancho, alto))

    # Convertir la imagen a un formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Crear un widget de etiqueta (Label) para mostrar la imagen
    etiqueta = tkinter.Label(ventana, image=imagen_tk)
    etiqueta.pack()

    # Ejecutar el bucle principal de la ventana
    ventana.mainloop()




def START_BUTTON():
    global app
    global image_label
    global my_image
    global check_var

    my_image = customtkinter.CTkImage(light_image=Image.open("circo.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)



    my_button1 = customtkinter.CTkButton(app, text="ONE_HAND", command=ONE_HAND)
    my_button1.place(x=405, y=475)
    my_button1.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    my_button2 = customtkinter.CTkButton(app, text="TWO_HANDS", command=TWO_HANDS)
    my_button2.place(x=567, y=475)
    my_button2.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028", bg_color="#B32028", hover_color="#DBDBDB")

    my_button3 = customtkinter.CTkButton(app, text="BODY_POSE", command=BODY_POSE)
    my_button3.place(x=742, y=475)
    my_button3.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028", bg_color="#B32028", hover_color="#DBDBDB")

    text = customtkinter.CTkLabel(app, text="GAME MODE", font=("Times New Roman", 80))
    text.place(x=405, y=340)

    text.configure(fg_color="#1E2768", text_color="white")

    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=850, y=610)
    checkbox.configure(bg_color="black", hover_color="#1E2768", fg_color= "#1E2768")

    BackButton1 = customtkinter.CTkButton(app, text="BACK", command=backbutton1)
    BackButton1.place(x=850, y=570)
    BackButton1.configure(fg_color="black", text_color="white", font=("Times New Roman", 20), border_color="#B32028",
                         bg_color="#6C1211", hover_color="#474747", width=15)

def backbutton1():
    global app
    global image_label
    global my_image
    global check_var

    close_photos()

    my_image = customtkinter.CTkImage(light_image=Image.open("rx00_jxbx_160116.jpg"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    customtkinter.set_appearance_mode("dark")

    start_button = customtkinter.CTkButton(app, text="START", command=START_BUTTON)
    start_button.place(x=885, y=480)
    start_button.configure(text_color="#FFC502", fg_color="#AB1113", hover_color="#75151A", border_color="#FFC502",
                           border_width=3, font=("Arial black", 15))

    how_to_play_button = customtkinter.CTkButton(app, text="HOW TO PLAY", command=how_to_play)
    how_to_play_button.place(x=885, y=520)
    how_to_play_button.configure(text_color="#FFC502", fg_color="#AB1113", hover_color="#75151A",
                                 border_color="#FFC502", border_width=3, font=("Arial black", 15))

    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=970, y=650)
    checkbox.configure(bg_color="black", fg_color="#CC9E02", hover_color="#9C7801")

def backbutton2():
    global app
    global image_label
    global my_image
    global check_var

    close_photos()

    my_image = customtkinter.CTkImage(light_image=Image.open("circo.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    my_button1 = customtkinter.CTkButton(app, text="ONE_HAND", command=ONE_HAND)
    my_button1.place(x=405, y=475)
    my_button1.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    my_button2 = customtkinter.CTkButton(app, text="TWO_HANDS", command=TWO_HANDS)
    my_button2.place(x=567, y=475)
    my_button2.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    my_button3 = customtkinter.CTkButton(app, text="BODY_POSE", command=BODY_POSE)
    my_button3.place(x=742, y=475)
    my_button3.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    text = customtkinter.CTkLabel(app, text="GAME MODE", font=("Times New Roman", 80))
    text.place(x=405, y=340)

    text.configure(fg_color="#1E2768", text_color="white")

    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=850, y=610)
    checkbox.configure(bg_color="black", hover_color="#1E2768", fg_color="#1E2768")

    BackButton1 = customtkinter.CTkButton(app, text="BACK", command=backbutton1)
    BackButton1.place(x=850, y=570)
    BackButton1.configure(fg_color="black", text_color="white", font=("Times New Roman", 20), border_color="#B32028",
                          bg_color="#6C1211", hover_color="#474747", width=15)

def backbutton3():
    global app
    global image_label
    global my_image
    global check_var

    reset_difficulty()

    close_photos()

    my_image = customtkinter.CTkImage(light_image=Image.open("circo.png"),
                                      size=(1300, 700))

    image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
    image_label.place(x=0, y=0)

    EasyButton = customtkinter.CTkButton(app, text="EASY", command=easy_difficulty_button)
    EasyButton.place(x=400, y=475)
    EasyButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    HardButton = customtkinter.CTkButton(app, text="HARD", command=hard_difficulty_button)
    HardButton.place(x=575, y=475)
    HardButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                         bg_color="#B32028", hover_color="#DBDBDB")

    ImpossibleButton = customtkinter.CTkButton(app, text="IMPOSSIBLE", command=impossible_difficulty_button)
    ImpossibleButton.place(x=750, y=475)
    ImpossibleButton.configure(fg_color="white", text_color="#B32028", font=("Arial Black", 20), border_color="#B32028",
                               bg_color="#B32028", hover_color="#DBDBDB")


    text = customtkinter.CTkLabel(app, text="DIFFICULTY", font=("Times New Roman", 80))
    text.place(x=415, y=340)
    text.configure(fg_color="#1E2768", text_color="white")

    check_var = customtkinter.StringVar(value="on")
    checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                         variable=check_var, onvalue="on", offvalue="off")

    checkbox.place(x=850, y=610)
    checkbox.configure(bg_color="black", hover_color="#1E2768", fg_color="#1E2768")

    BackButton2 = customtkinter.CTkButton(app, text="BACK", command=backbutton2)
    BackButton2.place(x=850, y=570)
    BackButton2.configure(fg_color="black", text_color="white", font=("Times New Roman", 20), border_color="#B32028",
                          bg_color="#6C1211", hover_color="#474747", width=15)

def CHECKBOX_MUSIC():
    if check_var.get() == "on":
        start_music()

    else:
        stop_music()






play_song("main_song_extended.mp3")


app = customtkinter.CTk()
app.title("ArrowPose")
app.geometry("1920x1080-10-10")




my_image = customtkinter.CTkImage(light_image=Image.open("rx00_jxbx_160116.jpg"),
                                  size=(1300, 700))

image_label = customtkinter.CTkLabel(app, image=my_image, text="")  # display image with a CTkLabel
image_label.place(x=0, y=0)

customtkinter.set_appearance_mode("dark")

start_button = customtkinter.CTkButton(app, text="START", command=START_BUTTON)
start_button.place(x=885, y=480)
start_button.configure(text_color="#FFC502", fg_color="#AB1113", hover_color="#75151A", border_color="#FFC502", border_width=3, font=("Arial black", 15))


how_to_play_button = customtkinter.CTkButton(app, text="HOW TO PLAY", command= how_to_play)
how_to_play_button.place(x=885, y= 520)
how_to_play_button.configure(text_color="#FFC502", fg_color="#AB1113", hover_color="#75151A", border_color="#FFC502", border_width=3, font=("Arial black", 15))

check_var = customtkinter.StringVar(value="on")
checkbox = customtkinter.CTkCheckBox(app, text="MUSIC ON", command=CHECKBOX_MUSIC,
                                     variable=check_var, onvalue="on", offvalue="off")

checkbox.place(x=970, y=650)
checkbox.configure(bg_color="black", fg_color="#CC9E02", hover_color="#9C7801")







app.mainloop()








