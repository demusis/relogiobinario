from datetime import datetime   
from sense_hat import SenseHat  
from time import sleep
import socket
import fcntl
import struct
import os

# Inicializa Sense Hat.
sense=SenseHat()

# Define cores.
colors={"red":(255,0,0),
        "orange":(255,103,0),
        "yellow":(255,246,0),
        "green":(0,255,0),
        "turquoise":(8,232,222),
        "blue":(0,0,255),
        "pink":(255,0,127),
        "white":(255,255,255),
        "black":(0,0,0),
        }

sense.low_light=True

def get_pixellist(count, component, color):    
    # rownumbers and colors for date/time components
    row_num={"d":0,"m":1,"y":2,"h":5,"min":6,"s":7}
    global colors
    
    # convert num of seconds to binary (str)
    count_bin="{0:b}".format(count)
    
    # fill binary number with zeros to length of 8
    if len(count_bin)<8:
        count_bin="{0}".format((8-len(count_bin))*"0"+count_bin)

    #  build pixellist to represent seconds
    plist=[]
    index=0     # for x-position
    for i in count_bin:
        if i=="1":
            plist.append((index,row_num[component],colors[color]))
        else:
            plist.append((index, row_num[component],colors["black"]))
        index+=1
        
    return plist

def update_pixellist(pixellist):
    for pixel in pixellist:
        sense.set_pixel(pixel[0],pixel[1],pixel[2])

def obtemHost():
    return(socket.gethostname())

def mostraHost():
    sense.clear()
    sense.show_message(obtemHost(), text_colour=[255, 0, 0])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1)) 
    ip_local = s.getsockname()[0]
    sense.show_message(ip_local, text_colour=[120, 120, 120])

def ligaRelogio():
    while True:
        sleep(1)
        
        # assign current time to object
        now=datetime.now()
        #print(str(now.hour) +":"+str(now.minute)+":"+str(now.second))
        
        # process day
        update_pixellist(get_pixellist(now.day, "d", "red"))
        
        # ... month
        update_pixellist(get_pixellist(now.month, "m", "orange"))
        
        # ... year
        update_pixellist(get_pixellist(now.year-2000, "y", "yellow"))
        
        # ... hours
        update_pixellist(get_pixellist(now.hour, "h", "green"))
        
        # ... minutes
        update_pixellist(get_pixellist(now.minute, "min", "blue"))
        
        # ... seconds
        update_pixellist(get_pixellist(now.second, "s", "white"))
        
        for evento in sense.stick.get_events():
            if evento.direction == 'down':
                sense.clear()
                return

def mostraVC():
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    t_CPU = temp/1000
          
    t_SH = sense.get_temperature()
    t_SH_H = sense.get_temperature_from_humidity()
    t_SH_P = sense.get_temperature_from_pressure()
    P = sense.get_pressure()
    UR = sense.get_humidity()

    sense.show_message('T.CPU: %.1fC' % t_CPU, text_colour=[255, 0, 0]) # Temperaturada CPU
    sense.show_message('T.SH: %.1fC' % t_SH, text_colour=[0, 255, 0]) # Temperatura do Sense Hat
    sense.show_message('P:%.1fpa' % P, text_colour=[130, 130, 130]) # Pressão atmosférica
    sense.show_message('UR: %.1f%%' % UR, text_colour=[0, 0, 255]) # Umidade relativa

sense.stick.direction_up = ligaRelogio
sense.stick.direction_left = mostraHost
sense.stick.direction_right = mostraVC 
sense.clear()

while True:
    pass    
