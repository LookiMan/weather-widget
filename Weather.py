# -*- coding: UTF-8 -*-

'''
pip install requests
pip install bs4
'''

import os
import sys

import ui
import utils
import weather_parser



# 
def update_weather(parser, widget, config):
    swap_file = utils.get_path_to_swap_file()
    # data = parser.get_weather()
    data = None
    if(not data):
        # Если возникла ошибка при получении данных с sinoptic.ua, загрузит сохраненные данные
        if(os.path.exists(swap_file)):
            data = utils.load_data(swap_file)
        # Если не удалось получить данные о погоде, спустя минуту попытается получить их вновь
        # Будет продолжаться до тех пока данные не будут получены, после чего программа выйдет на 
        # стандартный интервал обновления
        utils.timer(lambda: update_weather(parser, widget, config), 1)
    else:
        utils.save_data(swap_file, data)
        utils.timer(lambda: update_weather(parser, widget, config), config['timeout'])

    widget.update(data)

# 
def main():
    config_file = utils.get_path_to_config_file()
    
    app = ui.QApplication(sys.argv)
    Form = ui.QWidget()
    
    if(os.path.exists(config_file)):
        config = utils.load_data(config_file)
    else:
        # Базовые настройки
        config = {}
        config.update({
            'orientation': 'horizontal',
            'panel_width': 45,
            'panel_height': 45,
            'proportional_height_and_width': False,
            'font_size': 7,
            'position': utils.base_position(),
            'opacity': 0.8,
            'city': 'Черкаси',
            'timeout': 30, # Указывать у минутах
            'added_to_register': False,
            'amount_panels': 3,
            'panels_color_index': None,
            'show_day': False,
            'show_date': False,
            'show_max_temperature': True,
            'show_min_temperature': False,
            'show_settings_panel': True,
            })

        utils.save_data(config_file, config)

    parser = weather_parser.Parser(config['city'])

    widget = ui.Widget(config)
    widget.set_parser(parser)

    update_weather(parser, widget, config)

    if(not config['added_to_register']):
        if(ui.show_question('Внимание', 'Добавьте приложение в реестр, или создайте ярлык приложения в папке автозагрузки.\n'\
            'Добавить приложение в реестр?')):
            if(utils.add_programm_to_register()): # Вернет True если запись в реестр зделана успешно 
                config.update({'added_to_register': True})
                utils.save_data(config_file, config)
            else:
                ui.show_error('Ошибка записи в реестр', 'Не удалось зделать запись в реестр.\n'\
                                 'Запустите программу с правами администратора и попробуйте снова.')

    sys.exit(app.exec_())

# 
if(__name__ == '__main__'):
    main()

