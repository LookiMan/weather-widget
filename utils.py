# -*- coding: UTF-8 -*-
import os
import re
import sys
import winreg
import ctypes
import pickle
import threading

from PyQt5 import QtCore

import ui

images_dirrectory = os.path.join(os.path.dirname(sys.argv[0]), 'Images')
data_dirrectory = os.path.join(os.path.dirname(sys.argv[0]), 'Data')

config_filename = 'config.bin'
swap_filename = 'swap.bin'

# Служит для сглаживания ступенек между показаниями температуры и значений цветовой схемы
steps = {
    -32: -32, -31: -32, -30: -32, -29: -32, -28: -28, -27: -28, -26: -28, -25: -28, -24: -24, -23: -24,
    -22: -24, -21: -24, -20: -20, -19: -20, -18: -20, -17: -20, -16: -16, -15: -16, -14: -16, -13: -16, 
    -12: -12, -11: -12, -10: -12, -9: -12, -8: -8, -7: -8, -6: -8, -5: -8, -4: -4, -3: -4, -2: -4, -1: -4, 
    0: 0, 1: 0, 2: 0, 3: 0, 4: 4, 5: 4, 6: 4, 7: 4, 8: 8, 9: 8, 10: 8, 11: 8, 12: 12, 13: 12, 14: 12, 15: 12, 
    16: 16, 17: 16, 18: 16, 19: 16, 20: 20, 21: 20, 22: 20, 23: 20, 24: 24, 25: 24, 26: 24, 27: 24, 28: 28, 
    29: 28, 30: 28, 31: 28, 32: 32, 33: 32, 34: 32, 35: 32, 36: 36, 37: 36, 38: 36, 39: 36, 40: 40, 41: 40,
    42: 40, 43: 40, 44: 44, 45: 44, 46: 44, 47: 44, 48: 48, 49: 48, 50: 48, 51: 48, 52: 52, 53: 52, 54: 52, 55: 52
    }

# Значения записан в следующем порядке (bottom, top, bottom_hover, top_hover)
colors = {
    -32: ('#571F85', '#802EC5', '#802EC5', '#9F3AF5'),  
    -28: ('#6A2586', '#9D37C5', '#9D37C5', '#B540E5'),  
    -24: ('#695CC6', '#7A6AE5', '#7A6AE5', '#8372F5'),  
    -20: ('#2F1784', '#443384', '#443384', '#423084'),  
    -16: ('#3628FF', '#4E41FF', '#4E41FF', '#5E53FF'),  
    -12: ('#003BFF', '#2C5DFF', '#2C5DFF', '#3E6BFF'),  
    -8: ('#0FA4BE', '#4BADBE', '#4BADBE', '#5BAFBE'),  
    -4: ('#18AF64', '#35AF72', '#35AF72', '#45AF7A'),  
    0: ('#00BE35', '#25BE51', '#25BE51', '#45BE67'),  
    4: ('#00CD63', '#00EA71', '#00EA71', '#44EA94'),  
    8: ('#00FF00', '#38FF38', '#38FF38', '#5FFF5F'),  
    12: ('#00BE00', '#33BE33', '#33BE33', '#52BE52'),  
    16: ('#41BE00', '#61BE2E', '#61BE2E', '#6FBE45'),  
    20: ('#85FF00', '#A0FF3B', '#A0FF3B', '#AFFF59'),  
    24: ('#D3FF00', '#DEFF3B', '#DEFF3B', '#E4FF5F'),  
    28: ('#F9F951', '#F6FF4D', '#EDED4D', '#FFFF00'),
    32: ('#FFA300', '#FFAE21', '#FFAE21', '#FFB941'),  
    36: ('#FF6E00', '#FF6E00', '#FF6E00', '#FF8121'),  
    40: ('#FF5000', '#FF6118', '#FF6118', '#FF712F'), 
    44: ('#FF4400', '#FF642C', '#FF642C', '#FF713E'), 
    48: ('#FF3E24', '#FF523B', '#FF523B', '#FF624D'), 
    52: ('#FF2121', '#FF3535', '#FF3535', '#FF4A4A'),
    56: ('#A3A3A3', '#808080', '#BEBEBE', '#949494'),
    60: ('#F9F951', '#008EFF', '#FFFF00', '#0081EA'),
}

# 
def get_path_to_images_dirrectory():
    return images_dirrectory

# 
def get_path_to_data_dirrectory():
    return data_dirrectory

# 
def get_path_to_config_file():
    return os.path.join(get_path_to_data_dirrectory(), config_filename)

# 
def get_path_to_swap_file():
    return os.path.join(get_path_to_data_dirrectory(), swap_filename)

# 
def base_position():
    user32 = ctypes.windll.user32
    screensize_x = user32.GetSystemMetrics(0)
    position = (screensize_x / 2 - 324 / 2, 0)
    return position

# 
def timer(target, timeout: int):
    timer_object = QtCore.QTimer()
    timeout_in_miliseconds = timeout * 1000 * 60
    timer_object.singleShot(timeout_in_miliseconds, target)

# 
def add_programm_to_register():
    REG_PATH = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, 'Weather_Widget', 0, winreg.REG_SZ, sys.argv[0])
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

# Загрузка данные с файла. Указывать только имя файла без пути к нему.
def load_data(filename: str):
    with open(filename, mode='rb') as file:
        return pickle.load(file)

# 
def save_data(filename, data):
    try:
        with open(filename, mode='wb') as file:
            pickle.dump(data, file)     
   
    except PermissionError:
        ui.show_error('Ошибка', 'Нет права на запись в данной папке ')
    
    except Exception as exc:
        ui.show_error('Ошибка', 'Возникла непредвиденая ошибка %s' % exc)

