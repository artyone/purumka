import os
import sys
import time
from itertools import cycle, count
import ctypes
from msp_constants import *
from msp_types import *
from msp_fucntions import *
from msp_flags import *
from icecream import ic

from functools import partial
import numpy as np
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QUdpSocket
from PyQt5.QtWidgets import (QAction, QApplication, QComboBox, QHBoxLayout, QGridLayout,
                             QLabel, QMainWindow, QMenu, QCheckBox, QGroupBox,
                             QPushButton, QSlider, QStyle, QToolBar, QRadioButton,
                             QTreeWidget, QTreeWidgetItem, QVBoxLayout, QTextEdit,
                             QWidget, QLineEdit)


class ClassWrapper:
    def __init__(self, device_info: msp_DeviceInfo):
        self.fields = [name[0]
                       for name in getattr(type(device_info), '_fields_')]
        for field in self.fields:
            setattr(self, field, getattr(device_info, field))

    def __str__(self):
        res = [f'{field}: {getattr(self, field)}' for field in self.fields]
        return ' '.join(res)


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        msp_Startup()
        self.dev_handle = None
        self.log_counter = count(1)
        self.RT = 4
        self.SA = 1
        self.wcnt = 2
        self.cw = msp_BCCW_CHANNEL_A
        self.SU = 0b0000_0000_0000_0000
        self.activated = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Purumka MKIO")
        self.setGeometry(0, 0, 1350, 768)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        left_widget = QWidget()
        self.main_layout.addWidget(left_widget, 4)
        self.left_layout = QVBoxLayout(left_widget)

        self.init_device_block()
        
        self.init_bis_to_diss_block()
        send_bis_to_diss_btn = QPushButton('Отправить из БИС в ДИСС')
        send_bis_to_diss_btn.clicked.connect(self.send_command)
        self.left_layout.addWidget(send_bis_to_diss_btn)
        
        self.init_diss_to_bis01_block()
        send_diss_to_bis_btn01 = QPushButton('Отправить из ДИСС в БИС подадрес 01')
        send_diss_to_bis_btn01.clicked.connect(self.send_command)
        self.left_layout.addWidget(send_diss_to_bis_btn01)
        
        self.init_diss_to_bis02_block()
        send_diss_to_bis_btn02 = QPushButton('Отправить из ДИСС в БИС подадрес 02')
        send_diss_to_bis_btn02.clicked.connect(self.send_command)
        self.left_layout.addWidget(send_diss_to_bis_btn02)
        
        self.left_layout.addStretch(1)

        self.add_log_button = QPushButton('Отправить команду', self)
        self.add_log_button.clicked.connect(self.send_command)
        self.left_layout.addWidget(self.add_log_button)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.main_layout.addWidget(self.log_text, 1)

        self.showMaximized()

    def init_device_block(self):
        block_layout = QHBoxLayout()
        self.left_layout.addLayout(block_layout)

        self.device_combobox = QComboBox()
        self.udpate_combobox()
        
        block_layout.addWidget(self.device_combobox)
        block_button = QPushButton('Подключить')
        block_button.setFixedWidth(100)
        block_button.clicked.connect(self.activate_device)
        block_layout.addWidget(block_button)
        self.channel_combo_box = QComboBox()
        self.channel_combo_box.addItems(['Шина А', 'Шина Б'])
        self.channel_combo_box.setFixedWidth(100)
        block_layout.addWidget(self.channel_combo_box)
        
    
    def udpate_combobox(self):
        self.device_combobox.clear()
        for device in range(msp_GetNumberOfDevices()):
            raw_device_info = msp_DeviceInfo()
            msp_GetDeviceInfo(device, ctypes.byref(raw_device_info))
            device_info = ClassWrapper(raw_device_info)
            self.device_combobox.addItem(f'{device + 1}: {device_info}')


    def init_bis_to_diss_block(self):
        group_box = QGroupBox('Массив параметров из БИС в ДИСС')
        box_layout = QGridLayout(group_box)
        headers_su = [
            ('Достоверность крена, тангажа',     0b0000_0010_0000_0000),
            ('Достоверность введённых поправок', 0b0000_0100_0000_0000),
            ('Ввод поправок',                    0b0000_1000_0000_0000),
            ("Море",                             0b0001_0000_0000_0000),
            ("Контроль",                         0b0010_0000_0000_0000),
            ("Шасси обжато",                     0b0100_0000_0000_0000),
            ("Запрет излучения",                 0b1000_0000_0000_0000)
        ]
        positions = [(i, j) for i in range(2) for j in range(4)]
        for position, (header, val) in zip(positions, headers_su):
            chkbx = QCheckBox(header)
            box_layout.addWidget(chkbx, *position)
            chkbx.clicked.connect(partial(self.su_clicked_chkbox, val))

        headers_params = [
            ('Слово управления', 'su_bis_ledit'),
            ('Угол крена', 'angle_kren_bis_ledit'),
            ('Угол тангажа', 'angle_tang_bis_ledit'),
            ('Точность установки блока по крену', 'kren_accuracy_bis_ledit'),
            ('Точность установки блока по тангажу', 'tang_accuracy_bis_ledit'),
            ('Точность установки блока по курсу', 'kurs_accuracy_bis_ledit'),
            ('Абсолютная высота полёта', 'absolute_height_bis_ledit'),
        ]
        self.input_le = []
        positions = [(i, j) for i in range(2, 5) for j in range(4)]
        for position, (header, val) in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setFixedWidth(100)
            le.setToolTip(header)
            layout.addWidget(le)
            layout.addWidget(
                QLabel(header))
            box_layout.addLayout(layout, *position)
            self.input_le.append(le)

        self.left_layout.addWidget(group_box)

    def su_clicked_chkbox(self, val):
        self.SU ^= val
        self.input_le[0].setText(f'{self.SU}')
        
    def init_diss_to_bis01_block(self):
        group_box = QGroupBox('Массив параметров из ДИСС в БИС')
        box_layout = QGridLayout(group_box)
        headers_ss = [
            ('Отказ МП',         0b0000_0000_0100_0000, 'otkaz_mao_chkbox'),
            ('Отказ МЦО',        0b0000_0000_1000_0000, 'otkaz_mco_chkbox'),
            ('Отказ МАО',        0b0000_0001_0000_0000, 'otkaz_mao_chkbox'),
            ('Отказ УСК',        0b0000_0010_0000_0000, 'otkaz_usk_chkbox'),
            ('Отказ МПП',        0b0000_0100_0000_0000, 'otkaz_mpp_chkbox'),
            ('Отказ УС',         0b0000_1000_0000_0000, 'otkaz_us_chkbox'),
            ('Исправность',      0b0001_0000_0000_0000, 'isprav_chkbox'),
            ('Память',           0b0010_0000_0000_0000, 'pamyat_chkbox'),
            ('Контроль',         0b0100_0000_0000_0000, 'kontrol_chkbox'),
            ('Запрет излучения', 0b1000_0000_0000_0000, 'zapr_chkbox'),
        ]
        positions = [(i, j) for i in range(2) for j in range(4)]
        for position, (header, mask, name) in zip(positions, headers_ss):
            chkbx = QCheckBox(header)
            chkbx.setDisabled(True)
            box_layout.addWidget(chkbx, *position)
            self.output_chkbox = {}
            self.output_chkbox[chkbx] = mask

        headers_params = [
            'Идентификатор массива', 
            'Слово состояния',
            'Продольная составляющая вектора скорости',
            'Вертикальная составляющая вектора скорости',
            'Поперечная составляющая вектора скорости',
            'Путевая скорость',
            'Угол сноса',
            'Время наработки',
        ]
        self.output_le01 = []
        positions = [(i, j) for i in range(2, 5) for j in range(4)]
        for position, header in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(header)
            layout.addWidget(le)
            layout.addWidget(QLabel(header))
            box_layout.addLayout(layout, *position)
            self.output_le01.append(le)

        self.left_layout.addWidget(group_box)
        
        
    def init_diss_to_bis02_block(self):
        group_box = QGroupBox('Массив параметров из ДИСС в БИС')
        box_layout = QGridLayout(group_box)
        
        headers_params = [
            'Версия ПМО',
            'Дата ПМО',
            'Контрольная сумма ПМО1',
            'Контрольная сумма ПМО2',
            'Контрольная сумма ПМО3',
            'Контрольная сумма ПМО4',
            'Контрольная сумма ПМО5',
            'Контрольная сумма ПМО6',
            'Контрольная сумма ПМО7',
            'Контрольная сумма ПМО8',
            'Серий номер изделия'
        ]
        self.output_le02 = []
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, header in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(header)
            layout.addWidget(le)
            layout.addWidget(QLabel(header))
            box_layout.addLayout(layout, *position)
            self.output_le01.append(le)

        self.left_layout.addWidget(group_box)

    def activate_device(self):
        if self.dev_handle is not None:
            msp_Reset(self.dev_handle)
            msp_Close(self.dev_handle)
            
        raw_device_info = msp_DeviceInfo()
        msp_GetDeviceInfo(self.device_combobox.currentIndex(),
                          ctypes.byref(raw_device_info))
        
        if raw_device_info.Busy == 1:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Устройство id: {raw_device_info.DeviceId} <b>занято</b>'
            )
            self.udpate_combobox()
            return
        
        self.dev_handle = msp_Open(self.device_combobox.currentIndex())
        

        if self.dev_handle:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Устройство id: {raw_device_info.DeviceId} <b>подключено</b>')
        else:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка подключения устройства')
            self.udpate_combobox()
            return

        bcflags = (msp_FLAGID * 6)(
            mspF_ENHANCED_MODE,
            mspF_256WORD_BOUNDARY_DISABLE,
            mspF_MESSAGE_GAP_TIMER_ENABLED,
            mspF_INTERNAL_TRIGGER_ENABLED,
            mspF_EXPANDED_BC_CONTROL_WORD,
            0
        )
        try:
            msp_Configure(self.dev_handle, msp_MODE_BC + msp_MODE_ENHANCED, bcflags, None)
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Устройство id: {raw_device_info.DeviceId} <b>настроено</b> в режим КШ-ОУ')
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка: {e}')
            return
        self.activated = True

    def send_command(self):
        if self.dev_handle is None:
            self.activate_device()
            if not self.activated:
                self.log_text.append(
                    f'<b>{next(self.log_counter)}</b>. Ошибка подключения устройства'
                )
                return
        fr = msp_CreateFrame(self.dev_handle, 1000, 2)
        if not fr:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Не удалось создать фрейм'
            )
            return

        message = msp_Message()

        msp_AddMessage(
            fr,
            msp_CreateMessage(
                self.dev_handle,
                msp_RTtoBC(message, 4, 1, 2, msp_BCCW_CHANNEL_A)
            ),
            1000
        )

        msp_LoadFrame(fr, msp_AUTOREPEAT)

        msp_Start(self.dev_handle)

        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')

        msp_RetrieveMessage(fr, msp_NEXT_MESSAGE, message)
        recv_data = message.Data[:message.dataWordCount]

        recv_data = [f'<b>0x{data:04x}</b>' for data in recv_data]

        log_message = f'<b>{next(self.log_counter)}</b>. Полученные данные: {":".join(recv_data)}'
        self.log_text.append(log_message)
        
    def send_rt_to_bc(self,):
        ...

    def closeEvent(self, event):
        if self.dev_handle:
            msp_Reset(self.dev_handle)
            msp_Close(self.dev_handle)
            msp_Cleanup(self.dev_handle)
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
