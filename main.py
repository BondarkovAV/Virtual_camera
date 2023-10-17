import PySimpleGUI as sg
from PySimpleGUI import VSeparator, VerticalSeparator
import socket
import time
import json

sg.theme('Dark')
green = "#99FF99"
red = "#FFB6C1"
old_path = ''

with open('settings.json', 'r') as settings:
    set = json.load(settings)

host = set['ip']
port = set['port']
delay = set['delay']
#--------------------FUN-------------------------

def connect_socket(host, port):
    window['-STATUS-'].update(f'Please, wait for the connection', text_color=red)
    s = socket.socket()
    #host = '192.168.20.225'
    #port = 9998
    try:
        s.bind((host, port))
        s.listen()
        c, addr = s.accept()
        print("Got connection ", addr)
        window['-STATUS-'].update(f'Connected to:{addr}', text_color=green)
        return c
    except:
        print('connected error')
        window['-STATUS-'].update(f'Connected error!', text_color=red)
        connect = False
        return connect


def read_file(path):
    codes_base = []
    with open(path, 'r') as f:
        codes = f.readlines()
        for code in codes:
            code_n = code.rstrip()
            code_r = "{" + code_n + "}"
            codes_base.append(code_r)
        window["-QUAN-"].update(len(codes_base))
    return codes_base



#---------------------GUI------------------------

open_file = [
    [sg.In(font=('Ubuntu', 32), size=(20, 1), k='-TEXT-PATH-', readonly=True, enable_events=True),
     sg.FileBrowse('DOWNLOAD', font=('Ubuntu', 32), button_color=("#FFFFFF", "#1F75FE"), k='-PATH-', enable_events=True)]
]

connect_button = [
    [sg.Button('Connect', k='-CONNECT-', font=('Ubuntu', 32), button_color=("#FFFFFF", "#006400"))]
]

start_button = [
    [sg.Button('Start', k='-START-', font=('Ubuntu', 32), button_color=("#FFFFFF", "#006400"))]
]

stop_button = [
    [sg.Button('Stop', k='-STOP-', font=('Ubuntu', 32), button_color=("#FFFFFF", "#FF033E"))]
]

status_text = [
    [sg.Text('No connected', font=('Ubuntu', 20), k='-STATUS-')]
]

log_text = [
    [sg.Text('Log', font=('Ubuntu', 10), k='-LOG-')]
]

quantity_input = [
    [sg.Text('Quantity codes:', font=('Ubuntu', 25)), sg.In(font=('Ubuntu', 25), enable_events=True, k='-QUAN-', size=(15, 1))]
]

layout = [
    [sg.Push(), sg.Column(open_file), sg.Push()],
    [sg.Column(quantity_input), sg.Push()],
    [sg.HorizontalSeparator()],
    [sg.Column(connect_button), sg.Push(), sg.Column(status_text)],
    [sg.HorizontalSeparator()],
    [sg.Column(start_button), sg.Push(), sg.Column(stop_button)],
    [sg.HorizontalSeparator()],
    [sg.Column(log_text), sg.Push()]
]

window = sg.Window('Virtual cam', layout)
connect = False
start = False
n = 0
while True:
    event, values = window.read(timeout=delay)
    if event == sg.WINDOW_CLOSED:
        break

    if event == '-CONNECT-':
        try:
            c = connect_socket(host, port)
            connect = True
            print('connected')
        except:
            print('connected error')
            window['-STATUS-'].update(f'Connected error!', text_color=red)
            connect = False

    if event == '-START-':
        if connect:
            if values['-TEXT-PATH-']:
                print('start')
                start = True

    if event == '-STOP-':
        start = False

    if values['-TEXT-PATH-']:
        path = values['-TEXT-PATH-']
        if old_path != path:
            old_path = path
            cd_bs = read_file(path)
        else:
            print('path not changed')


    if values['-QUAN-']:
        if values['-TEXT-PATH-']:
            try:
                quan = int(values['-QUAN-'])
                if quan > int(len(cd_bs)):
                    quan = int(len(cd_bs))
                print(quan)
            except:
                print('Values is not int')

    if event == sg.TIMEOUT_EVENT:
        #print('Timeout event')
        if start == True:
            print('start True')
            if n < quan:
                print(f'{n} < {quan}')
                code_b = cd_bs[n].encode()
                print(code_b)
                c.sendall(code_b)
                #time.sleep(0.1)
                print(f'code {code_b}')
                window['-LOG-'].update(cd_bs[n])
                n += 1
            else:
                print(f'{n} > {quan}')
                start = False
                n = 0







