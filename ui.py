import os
import re
import sys
import ctypes
import datetime

import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, 
                                QLabel, QSlider, QCheckBox, QLineEdit, QMessageBox)
from PyQt5 import (QtCore, QtGui)

import utils



# 
def show_info(title: str, message_text: str):
    QMessageBox.information(None, title, message_text, QMessageBox.Ok)

# 
def show_warning(title: str, message_text: str):
    QMessageBox.warning(None, title, message_text, QMessageBox.Ok)

# 
def show_error(title: str, message_text: str):
    QMessageBox.critical(None, title, message_text, QMessageBox.Ok)

# 
def show_question(title: str, message_text: str):
    result = QMessageBox.question(None, title, message_text, QMessageBox.Yes, QMessageBox.No)
    if(result == 16384):
        return True
    elif(result == 65536):
        return False

# 
class Widget:
    def __init__(self, config):
        self.Form = QWidget()
        self._config = config
        self._weather = None
        self.is_open_setting_window = False
        self.Form.setObjectName('Weather 2.0')
        self.Form.setEnabled(True)
        self.Form.move(*self._config['position'])
        self.Form.setMouseTracking(False)
        self.Form.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
        self.Form.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.Form.setWindowOpacity(0.8)
        self.Form.setAutoFillBackground(False)
        self.Form.setStyleSheet('background-color: transparent;')
        
        self.base_css = 'QPushButton{\nbackground-color: qlineargradient(x0:1 y0:1, x0:0 y1:1,   stop:0 #BEBEBE, stop:1   #BEBEBE);\n'\
                        'border: 0;\n'\
                        'border-radius: 5px;\n'\
                        '}\n\n'\
                        ':hover{\n background-color: qlineargradient(x0:1 y0:1, x0:0 y1:1,   stop:0 #949494, stop:1 #BEBEBE);\n'\
                        '}\n'

        self.tooltip = 'Показание погоды для города %s.\nОткрыть настройки можно двойным кликом по плитке' % self._config['city'].capitalize()

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8) # 
        self.font.setWeight(75)
        self.font.setBold(True)
        
        self.pushButton_0 = QPushButton(self.Form)
        self.pushButton_0.setFont(self.font)
        self.pushButton_0.setStyleSheet(self.base_css)
        self.pushButton_0.setObjectName('pushButton_0')
        self.pushButton_0.setToolTip(self.tooltip)
        
        self.pushButton_1 = QPushButton(self.Form)
        self.pushButton_1.setFont(self.font)
        self.pushButton_1.setStyleSheet(self.base_css)
        self.pushButton_1.setObjectName('pushButton_1')
        self.pushButton_1.setToolTip(self.tooltip)

        self.pushButton_2 = QPushButton(self.Form)
        self.pushButton_2.setFont(self.font)
        self.pushButton_2.setStyleSheet(self.base_css)
        self.pushButton_2.setObjectName('pushButton_2')
        self.pushButton_2.setToolTip(self.tooltip)

        self.pushButton_3 = QPushButton(self.Form)
        self.pushButton_3.setFont(self.font)
        self.pushButton_3.setStyleSheet(self.base_css )
        self.pushButton_3.setObjectName('pushButton_3')
        self.pushButton_3.setToolTip(self.tooltip)

        self.pushButton_4 = QPushButton(self.Form)
        self.pushButton_4.setFont(self.font)
        self.pushButton_4.setStyleSheet(self.base_css)
        self.pushButton_4.setObjectName('pushButton_4')
        self.pushButton_4.setToolTip(self.tooltip)

        self.pushButton_5 = QPushButton(self.Form)
        self.pushButton_5.setFont(self.font)
        self.pushButton_5.setStyleSheet(self.base_css)
        self.pushButton_5.setObjectName('pushButton_5')
        self.pushButton_5.setToolTip(self.tooltip)

        self.pushButton_6 = QPushButton(self.Form)
        self.pushButton_6.setFont(self.font)
        self.pushButton_6.setStyleSheet(self.base_css)
        self.pushButton_6.setObjectName('pushButton_6')
        self.pushButton_6.setToolTip(self.tooltip)

        self.pushButton_7 = QPushButton(self.Form)
        self.pushButton_7.setFont(self.font)
        self.pushButton_7.setStyleSheet(self.base_css)
        self.pushButton_7.setText('')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.join(utils.get_path_to_images_dirrectory(), 'settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon1)
        self.pushButton_7.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_7.setCheckable(False)
        self.pushButton_7.setObjectName('pushButton_7')

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

        self.set_move_window(self.pushButton_0)
        self.set_move_window(self.pushButton_1)
        self.set_move_window(self.pushButton_2)
        self.set_move_window(self.pushButton_3)
        self.set_move_window(self.pushButton_4)
        self.set_move_window(self.pushButton_5)
        self.set_move_window(self.pushButton_6)
        self.pushButton_7.clicked.connect(lambda : self.open_settings())
        self.draw(self._config)
        self.Form.show()

    #  
    def draw(self, config: dict):
        self.font.setPointSize(config['font_size'])
        self.Form.setWindowOpacity(config['opacity'])
        max_amount_panels = config['amount_panels']
        pw = config['panel_width']
        ph = config['panel_height']

        # Учет плитки настроек 
        k = 1 if(config['show_settings_panel']) else 0

        if(config['orientation'] == 'horizontal'):
            self.Form.setFixedSize((pw+1)*(max_amount_panels+k), ph) 
        else:
            self.Form.setFixedSize(pw, (ph+1)*(max_amount_panels+k))

        for i in range(8):
            pushButton = getattr(self, 'pushButton_%i' % i, None)

            if(config['orientation'] == 'horizontal'):
                pushButton.setGeometry(QtCore.QRect((pw+1)*i, 0, pw, ph))
            else:
                pushButton.setGeometry(QtCore.QRect(0, (ph+1)*i, pw, ph))
            
            pushButton.setFont(self.font)

        if(config['show_settings_panel']):
            if(config['orientation'] == 'horizontal'):
                self.pushButton_7.setGeometry(QtCore.QRect((pw+1)*max_amount_panels, 0, pw, ph))
            else:
                self.pushButton_7.setGeometry(QtCore.QRect(0, (ph+1)*max_amount_panels, pw, ph))

            if(pw < ph):
                size = pw / 2
            else:
                size = ph / 2
            self.pushButton_7.setIconSize(QtCore.QSize(size, size))

    # Используется для перерисовки окна виджета с новыми настройками
    def redraw(self, config: dict):
        self.draw(config)
        self.prewiev_text(config)
        self.prewiev_css(config)

    # 
    def retranslateUi(self):
        self.Form.setWindowTitle(QApplication.translate('Form', 'Wather', None))
        self.pushButton_0.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_1.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_2.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_3.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_4.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_5.setText(QApplication.translate('Form', 'Загрузка...', None))
        self.pushButton_6.setText(QApplication.translate('Form', 'Загрузка...', None))

    # Установливает новый конфиг для виджета
    def set_config(self, config: dict):
        self._config = config

    # Сохраняет объект парсера для дальнейшего его вызова с окна настроек при 
    def set_parser(self, parser):
        self.parser = parser

    # 
    def set_move_window(self, widget):
        win = widget.parentWidget().window()
        cursorShape = widget.cursor().shape()
        user32 = ctypes.windll.user32
        screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        moveSource = getattr(widget, 'mouseMoveEvent')
        pressSource = getattr(widget, 'mousePressEvent')
        releaseSource = getattr(widget, 'mouseReleaseEvent')
        doubleClickSource = getattr(widget, 'mouseDoubleClickEvent')
        
        # 
        def move(event):
            if(move.b_move):
                x = event.globalX() + move.x_korr - move.lastPoint.x()
                y = event.globalY() + move.y_korr - move.lastPoint.y()
                if x >= screensize[0] - win.geometry().width():
                    x = screensize[0] - win.geometry().width()
                if x <= 0:
                    x = 0
                if y >= screensize[1] - win.geometry().height():
                    y = screensize[1] - win.geometry().height()
                if y <= 0:
                    y = 0
                win.move(x, y)
                widget.setCursor(QtCore.Qt.SizeAllCursor)
            return moveSource(event)
        
        # 
        def press(event):
            if(event.button() == QtCore.Qt.LeftButton):
                x_korr = win.frameGeometry().x() - win.geometry().x()
                y_korr = win.frameGeometry().y() - win.geometry().y()
                parent = widget
                while not parent == win:
                    x_korr -= parent.x()
                    y_korr -= parent.y()
                    parent = parent.parent()

                move.__dict__.update({'lastPoint': event.pos(),  'b_move': True,  'x_korr': x_korr,  'y_korr': y_korr})
            else:
                move.__dict__.update({'b_move': False})
                widget.setCursor(cursorShape)
            return pressSource(event)

        # 
        def release(event):
            if(hasattr(move, 'x_korr') and hasattr(move, 'y_korr')):
                move.__dict__.update({'b_move': False})
                widget.setCursor(cursorShape)
                x = event.globalX() + move.x_korr - move.lastPoint.x()
                y = event.globalY() + move.y_korr - move.lastPoint.y()
                if((x, y) != self._config['position']):
                    self._config.update({'position': (x, y)})
                    utils.save_data(utils.get_path_to_config_file(), self._config)

                return releaseSource(event)

        #
        def double_click(event):
            self.open_settings()
            return doubleClickSource(event)               


        setattr(widget, 'mouseMoveEvent', move)
        setattr(widget, 'mousePressEvent', press)
        setattr(widget, 'mouseReleaseEvent', release)
        setattr(widget, 'mouseDoubleClickEvent', double_click)
        move.__dict__.update({'b_move': False})
        return widget

    # Формирует текст для плитки
    def _create_text(self, data: dict, config: dict):
        strings = []
        
        if(config['show_day']):
            strings.append(data['day'])

        if(config['show_date']):
            strings.append(data['date'])

        if(config['show_max_temperature']):
            strings.append(data['max_temperature'])

        if(config['show_min_temperature']):
            strings.append(data['min_temperature'])

        return '\n'.join(strings)

    # Используется при изменении настроек для предусмотрю отформатированного текста
    def prewiev_text(self, config: dict):
        day = datetime.datetime.now().day

        for index in range(7):
            panel = getattr(self, 'pushButton_%i' % index, None)
            dt = self._weather.get(day+index)
            if(not dt):
                panel.setText(QApplication.translate('Form', 'Загрузка\nпогоды...', None))
            else:
                panel.setText(QApplication.translate('Form', self._create_text(dt, config), None))

    # Формирует css стиль для плиток
    def _create_css(self, data: dict, config: dict):
        if(config['panels_color_index']):
            color = utils.colors.get(config['panels_color_index'])
        else:
            temperature = int(re.findall('\d+', data['min_temperature'])[0])
            # Если полученное значение меньше чем минимальное предусмотренное значение
            if temperature < -32:
                color = utils.colors[-32]
            # Если полученное значение больше чем максимальное предусмотренное значение
            elif temperature > 52:
                color = utils.colors[52]
            else:
                color = utils.colors.get(utils.steps.get(temperature))

        css = 'QPushButton{\n'\
                'background-color: qlineargradient(x0:1 y0:1, x0:0 y1:1, stop:0 %s, stop:1 %s);'\
                '\n'\
                'border: 0;\n'\
                'border-radius: 5px;'\
                '\n}\n'\
                ':hover{\n'\
                'background-color: qlineargradient(x0:1 y0:1, x0:0 y1:1, stop:0 %s, stop:1 %s);'\
                '\n}' % (color[0], color[1], color[2], color[3])

        return css

    # Используется при изменении настроек для предусмотра css стиля плиток
    def prewiev_css(self, config: dict):
        day = datetime.datetime.now().day

        for index in range(7):
            dt = self._weather.get(day+index)
            if(not dt):
                pass
            else:
                panel = getattr(self, 'pushButton_%i' % index, None)
                panel.setStyleSheet(QApplication.translate('Form', self._create_css(dt, config), None))

    # Обновление виджета 
    def update(self, data: dict):
        self._weather = data 
        day = datetime.datetime.now().day

        for index in range(7):
            dt = self._weather.get(day+index)
            if(not dt):
                panel.setText(QApplication.translate('Form', 'Загрузка\nпогоды...', None))
            else:
                panel = getattr(self, 'pushButton_%i' % index, None)
                panel.setText(QApplication.translate('Form', self._create_text(dt, self._config), None))
                panel.setStyleSheet(QApplication.translate('Form', self._create_css(dt, self._config), None))

    # 
    def open_settings(self):
        if(not self.is_open_setting_window):
            self.is_open_setting_window = True
            self.w = Settings(self, self._config)


# 
class Settings:
    # 
    def __init__(self, parent, config):
        self.form = QWidget()
        self.parent = parent
        self.config = config.copy()
        self.parser = None
        self.form.setObjectName('Form')
        self.form.setAcceptDrops(False)
        self.form.setFixedSize(400, 435)
        self.form.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(utils.get_path_to_images_dirrectory(), 'settings_icon.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.form.setWindowIcon(icon)

        self.label = QLabel(self.form)
        self.label.setGeometry(QtCore.QRect(10, 10, 381, 21))
        self.label.setObjectName('label')

        self.lineEdit = QLineEdit(self.form)
        self.lineEdit.setGeometry(QtCore.QRect(10, 35, 300, 20))
        self.lineEdit.setText(self.config['city'].capitalize())
        self.lineEdit.setObjectName('lineEdit')

        self.pushButton = QPushButton(self.form)
        self.pushButton.setGeometry(QtCore.QRect(310, 34, 80, 20))
        self.pushButton.setObjectName('pushButton')

        self.label_1 = QLabel(self.form)
        self.label_1.setGeometry(QtCore.QRect(10, 80, 180, 16))
        self.label_1.setObjectName('label_1')

        self.horizontalSlider = QSlider(self.form)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 100, 180, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setProperty('value', self.config['opacity'] * 10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName('horizontalSlider')

        self.label_2 = QLabel(self.form)
        self.label_2.setGeometry(QtCore.QRect(200, 80, 180, 16))
        self.label_2.setObjectName('label_2')

        self.horizontalSlider_1 = QSlider(self.form)
        self.horizontalSlider_1.setGeometry(QtCore.QRect(200, 100, 180, 22))
        self.horizontalSlider_1.setMinimum(7)
        self.horizontalSlider_1.setMaximum(12)
        self.horizontalSlider_1.setProperty('value', self.config['font_size'])
        self.horizontalSlider_1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_1.setObjectName('horizontalSlider_1')

        self.horizontalSlider_2 = QSlider(self.form)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(10, 160, 180, 22))
        self.horizontalSlider_2.setMinimum(45)
        self.horizontalSlider_2.setMaximum(97)
        self.horizontalSlider_2.setProperty('value', self.config['panel_width'])
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName('horizontalSlider_2')

        self.horizontalSlider_3 = QSlider(self.form)
        self.horizontalSlider_3.setGeometry(QtCore.QRect(200, 160, 180, 22))
        self.horizontalSlider_3.setMinimum(45)
        self.horizontalSlider_3.setMaximum(97)
        self.horizontalSlider_3.setProperty('value', self.config['panel_height'])
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName('horizontalSlider_3')

        self.checkBox = QCheckBox(self.form)
        self.checkBox.setGeometry(QtCore.QRect(10, 185, 300, 17))
        if(self.config['proportional_height_and_width']):
            self.checkBox.setChecked(True)
        self.checkBox.setObjectName('checkBox')

        self.label_3 = QLabel(self.form)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 100, 16))
        self.label_3.setObjectName('label_3')
        self.label_4 = QLabel(self.form)
        self.label_4.setGeometry(QtCore.QRect(200, 140, 100, 16))
        self.label_4.setObjectName('label_4')
        
        self.label_5 = QLabel(self.form)
        self.label_5.setGeometry(QtCore.QRect(10, 215, 381, 16))
        self.label_5.setObjectName('label_5')

        self.checkBox_1 = QCheckBox(self.form)
        self.checkBox_1.setGeometry(QtCore.QRect(10, 235, 161, 17))
        if(self.config['orientation'] == 'horizontal'):
            self.checkBox_1.setChecked(True)
        self.checkBox_1.setObjectName('checkBox')
  
        self.checkBox_2 = QCheckBox(self.form)
        self.checkBox_2.setGeometry(QtCore.QRect(200, 235, 151, 17))
        if(self.config['orientation'] == 'vertical'):
            self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName('checkBox_2')

        self.label_6 = QLabel(self.form)
        self.label_6.setGeometry(QtCore.QRect(10, 265, 381, 16))
        self.label_6.setObjectName('label_6')

        self.horizontalSlider_5 = QSlider(self.form)
        self.horizontalSlider_5.setGeometry(QtCore.QRect(10, 285, 180, 22))
        self.horizontalSlider_5.setMinimum(1)
        self.horizontalSlider_5.setMaximum(7)
        self.horizontalSlider_5.setProperty('value', self.config['amount_panels'])
        self.horizontalSlider_5.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_5.setObjectName('horizontalSlider_5')

        self.label_7 = QLabel(self.form)
        self.label_7.setGeometry(QtCore.QRect(200, 265, 200, 16))
        self.label_7.setObjectName('label_7')
        self.horizontalSlider_6 = QSlider(self.form)
        self.horizontalSlider_6.setGeometry(QtCore.QRect(200, 285, 180, 22))
        self.horizontalSlider_6.setMinimum(-9)
        self.horizontalSlider_6.setMaximum(15)
        if(self.config['panels_color_index']):
            self.horizontalSlider_6.setProperty('value', self.config['panels_color_index'] / 4)
        else:
            self.horizontalSlider_6.setProperty('value', -36)
        self.horizontalSlider_6.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_6.setObjectName('horizontalSlider_6')

        self.label_8 = QLabel(self.form)
        self.label_8.setGeometry(QtCore.QRect(10, 310, 200, 16))
        self.label_8.setObjectName('label_8')

        self.checkBox_3 = QCheckBox(self.form)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 335, 170, 17))
        if(self.config['show_day']):
            self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName('checkBox_3')

        self.checkBox_4 = QCheckBox(self.form)
        self.checkBox_4.setGeometry(QtCore.QRect(200, 335, 230, 17))
        if(self.config['show_max_temperature']):
            self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName('checkBox_5')

        self.checkBox_5 = QCheckBox(self.form)
        self.checkBox_5.setGeometry(QtCore.QRect(10, 360, 170, 17))
        if(self.config['show_date']):
            self.checkBox_5.setChecked(True)
        self.checkBox_5.setObjectName('checkBox_4')

        self.checkBox_6 = QCheckBox(self.form)
        self.checkBox_6.setGeometry(QtCore.QRect(200, 360, 230, 17))
        if(self.config['show_min_temperature']):
            self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName('checkBox_6')

        self.checkBox_7 = QCheckBox(self.form)
        self.checkBox_7.setGeometry(QtCore.QRect(10, 385, 230, 17))
        if(self.config['show_settings_panel']):
            self.checkBox_7.setChecked(True)
        self.checkBox_7.setObjectName('checkBox_7')

        self.pushButton_1 = QPushButton(self.form)
        self.pushButton_1.setGeometry(QtCore.QRect(295, 408, 100, 22))
        self.pushButton_1.setObjectName('pushButton')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.join(utils.get_path_to_images_dirrectory(), 'confirm.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon2)

        self.pushButton_2 = QPushButton(self.form)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 408, 100, 22))
        self.pushButton_2.setObjectName('pushButton_2')
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.join(utils.get_path_to_images_dirrectory(), 'cancel.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon3)

        self.pushButton_3 = QPushButton(self.form)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 408, 160, 22))
        self.pushButton_3.setObjectName('pushButton_2')
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.join(utils.get_path_to_images_dirrectory(), 'exit.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon4)
        self.pushButton_3.setIconSize(QtCore.QSize(16, 16))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)
        
        self.pushButton.clicked.connect(self.test_city)
        self.pushButton_1.clicked.connect(self.confirm)
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.exit)
        self.checkBox.clicked.connect(self.change_proportional_checkbox)
        self.checkBox_1.clicked.connect(self.change_horizontal_orietntation)
        self.checkBox_2.clicked.connect(self.change_vertical_orietntation)
        self.horizontalSlider.valueChanged.connect(self.change_opacity)
        self.horizontalSlider_1.valueChanged.connect(self.change_font_size)
        self.horizontalSlider_2.valueChanged.connect(self.change_panel_width)
        self.horizontalSlider_3.valueChanged.connect(self.change_panel_height)
        self.horizontalSlider_5.valueChanged.connect(self.change_amount_panels)
        self.horizontalSlider_6.valueChanged.connect(self.change_panels_color)

        self.checkBox_3.clicked.connect(self.change_panel_items)
        self.checkBox_4.clicked.connect(self.change_panel_items)
        self.checkBox_5.clicked.connect(self.change_panel_items)
        self.checkBox_6.clicked.connect(self.change_panel_items)
        self.checkBox_7.clicked.connect(self.change_panel_items)
        self.form.show()

    # 
    def retranslateUi(self):
        self.form.setWindowTitle(QApplication.translate('Form', 'Настройки', None))
        self.pushButton.setText(QApplication.translate('Form', 'Ок', None))
        self.pushButton_1.setText(QApplication.translate('Form', 'Применить', None))
        self.pushButton_2.setText(QApplication.translate('Form', 'Отмена', None))
        self.pushButton_3.setText(QApplication.translate('Form', 'Отключить виджет', None))
        self.label.setText(QApplication.translate('Form', 'Введите ваш город', None))
        self.label_1.setText(QApplication.translate('Form', 'Непрозрачность виджета: %s' % self.config['opacity'], None))
        self.label_2.setText(QApplication.translate('Form', 'Размер шрифта: %i' % self.config['font_size'], None))
        self.label_3.setText(QApplication.translate('Form', 'Ширина плитки: %i' % self.config['panel_width'], None))
        self.label_4.setText(QApplication.translate('Form', 'Высота плитки: %i' % self.config['panel_height'], None))
        self.checkBox.setText(QApplication.translate('Form', 'Пропорциональные высота и ширина', None))
        self.checkBox_1.setText(QApplication.translate('Form', 'Горизонтальная', None))
        self.label_5.setText(QApplication.translate('Form', 'Ориентация виджета', None))
        self.label_6.setText(QApplication.translate('Form', 'Количество плиток с погодой: %i' % self.config['amount_panels'], None))
        self.checkBox_2.setText(QApplication.translate('Form', 'Вертикальная', None))
        self.label_7.setText(QApplication.translate('Form', 'Цветовая схема: %s' % ('собственная' if(self.config['panels_color_index']) else 'адаптивная'), None))
        self.label_8.setText(QApplication.translate('Form', 'Отображать на пластине:', None))
        self.checkBox_3.setText(QApplication.translate('Form', 'День недели', None))
        self.checkBox_4.setText(QApplication.translate('Form', 'Максимальную температуру', None))
        self.checkBox_5.setText(QApplication.translate('Form', 'Число', None))
        self.checkBox_6.setText(QApplication.translate('Form', 'Минимальную температуру', None))
        self.checkBox_7.setText(QApplication.translate('Form', 'Плитку настроек', None))

    # 
    def change_horizontal_orietntation(self):
        self.config['orientation'] = 'horizontal'
        self.checkBox_1.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.parent.redraw(self.config)
 
    # 
    def change_vertical_orietntation(self):
        self.config['orientation'] = 'vertical'
        self.checkBox_1.setChecked(False)
        self.checkBox_2.setChecked(True)
        self.parent.redraw(self.config)

    # 
    def change_opacity(self):
        self.config['opacity'] = self.horizontalSlider.value() / 10
        self.label_1.setText('Непрозрачность виджета: %s' % self.config['opacity'])
        self.parent.redraw(self.config)

    # 
    def change_font_size(self):
        self.config['font_size'] = self.horizontalSlider_1.value()
        self.label_2.setText('Размер шрифта: %i' % self.config['font_size'])
        self.parent.redraw(self.config)

    # 
    def change_panel_width(self):
        value = self.horizontalSlider_2.value() 
        self.config['panel_width'] = value
        self.label_3.setText(QApplication.translate('Form', 'Ширина плитки: %i' % value, None))

        if(self.checkBox.isChecked()):
            self.config['panel_height'] = value
            self.horizontalSlider_3.setProperty('value', value)

        self.parent.redraw(self.config)

    # 
    def change_panel_height(self):
        value = self.horizontalSlider_3.value() 
        self.config['panel_height'] = value
        self.label_4.setText(QApplication.translate('Form', 'Высота плитки: %i' % value, None))

        if(self.checkBox.isChecked()):
            self.config['panel_width'] = value
            self.horizontalSlider_2.setProperty('value', value)

        self.parent.redraw(self.config)

    #
    def change_proportional_checkbox(self):
        if(self.checkBox.isChecked()):
            self.config['proportional_height_and_width'] = True
        else:
            self.config['proportional_height_and_width'] = False   

    # 
    def change_amount_panels(self):
        self.config['amount_panels'] = self.horizontalSlider_5.value()
        self.label_6.setText(QApplication.translate('Form', 'Количество плиток с погодой: %i' % self.config['amount_panels'], None))
        self.parent.redraw(self.config)

    # 
    def change_panel_items(self):
        if(self.checkBox_3.isChecked()):
            self.config['show_day'] = True
        else:
            self.config['show_day'] = False

        if(self.checkBox_4.isChecked()):
            self.config['show_max_temperature'] = True
        else:
            self.config['show_max_temperature'] = False

        if(self.checkBox_5.isChecked()):
            self.config['show_date'] = True
        else:
            self.config['show_date'] = False

        if(self.checkBox_6.isChecked()):
            self.config['show_min_temperature'] = True
        else:
            self.config['show_min_temperature'] = False

        if(self.checkBox_7.isChecked()):
            self.config['show_settings_panel'] = True
        else:
            self.config['show_settings_panel'] = False

        self.parent.redraw(self.config)

    # 
    def change_panels_color(self):
        index = self.horizontalSlider_6.value() * 4

        if(index == -36):
            self.label_7.setText(QApplication.translate('Form', 'Цветовая схема: адаптивная', None))
            index = None
        else:
            self.label_7.setText(QApplication.translate('Form', 'Цветовая схема: собственная', None))
        
        self.config['panels_color_index'] = index
        self.parent.redraw(self.config)

    # 
    def test_city(self):
        city = self.lineEdit.text().lower()
        if(self.is_valid_city(city)):   
            show_info('Успех!', 'Город указан корректно')
        else:
            show_warning('Ошибка!', 'Неверно указаный город')

    #
    def is_valid_city(self, city):
        try:
            page = requests.get('https://sinoptik.ua/погода-%s' % city)
        except ConnectionError:
            return False
        else:
            if(page.status_code == 200):
                return True
            return False

    # 
    def exit(self):
        sys.exit()

    # 
    def close(self):
        self.parent.redraw(self.parent._config)
        self.parent.is_open_setting_window = False
        self.form.destroy()

    # 
    def confirm(self):
        city = self.lineEdit.text().lower()
        if(city != self.config['city'].lower()):
            if(self.is_valid_city(city)):
                self.config.update({'city': city})
                self.parent.parser.set_city(city)
                self.parent.set_config(self.config)
                data = self.parent.parser.get_weather()
                self.parent.update(data)
                utils.save_data(utils.get_path_to_config_file(), self.config)
                self.close()
            else:
                show_warning('Ошибка!', 'Неверно указаный город')
        else:
            self.parent.set_config(self.config)
            utils.save_data(utils.get_path_to_config_file(), self.config)
            self.close()
