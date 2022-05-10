from ast import While
import json
import os
import random
import ssl
import time
from tkinter import BOTH, TOP, Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import PySimpleGUI as sg
from paho.mqtt import client as mqtt_client

global liveObj 
liveObj = {
    "value":{
        "temperature": random.randint(0, 100),
    }
}
global updated
updated = False
broker = 'liveobjects.orange-business.com'
port = 8883
topic = "fifo/mqttfx"
client_id = f'python-mqtt'
username = 'application'
with open('api.key') as f:
    password = f'{f.read()}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.tls_set(os.path.expanduser('~') + "/.cert/liveobj.pem", tls_version=ssl.PROTOCOL_TLSv1_2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global liveObj, updated
        liveObj = json.loads(msg.payload.decode())
        updated = True

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)


def draw_chart(data):
    fig.clear()
    fig.add_subplot(111).plot(data)
    canvas.draw_idle()


if __name__ == '__main__':
    run()
    myData = []
    layout = [[sg.Canvas(key="-CANVAS-")], [sg.Button("Close")]]

    window = sg.Window(
        "Demo", layout,
        location=(0, 0),
        finalize=True,
        element_justification="center",
        font="Helvetica 18"
    )

    #root = Tk()

    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)

    canvas = FigureCanvasTkAgg(fig, master=window["-CANVAS-"].TKCanvas)
    canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

    while True:
        if updated:
            myData.append(liveObj["value"]["temperature"])
            updated = False
        fig.clear()
        fig.add_subplot(111).plot(myData)
        canvas.draw_idle()
        event, values = window.read(timeout = 10)
        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()