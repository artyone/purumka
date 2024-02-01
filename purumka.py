import ctypes
import os
import sys
import time
from functools import partial
from itertools import count, cycle

import numpy as np
from icecream import ic
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QUdpSocket
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QLineEdit, QMainWindow, QMenu, QMessageBox,
                             QPushButton, QRadioButton, QSlider, QStyle,
                             QTextEdit, QToolBar, QTreeWidget, QTreeWidgetItem,
                             QVBoxLayout, QWidget)

from msp_constants import *
from msp_flags import *
from msp_fucntions import *
from msp_types import *
from rtl import RTL


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.dev_handle = None
        self.log_counter = count(1)
        self.SU = 0b0000_0000_0000_0000

        try:
            self.lib = RTL('./drtl3.dll')
        except Exception as e:
            QMessageBox.warning(
                self, 'Ошибка', 'Не обнаружено устройство. ' + str(e))
            sys.exit()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Purumka MKIO")
        self.setGeometry(0, 0, 1350, 768)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.main_layout = QVBoxLayout(main_widget)

        self.init_device_block()

        self.init_to_diss_block()
        to_diss_btn = QPushButton('Отправить из БИС в ДИСС')
        to_diss_btn.clicked.connect(self.send_to_diss)
        self.main_layout.addWidget(to_diss_btn)

        self.init_to_bis01_block()
        to_bis01_btn = QPushButton(
            'Получить из БИС подадрес 01')
        to_bis01_btn.clicked.connect(self.send_to_bis01)
        self.main_layout.addWidget(to_bis01_btn)

        self.init_to_bis02_block()
        to_bis02_btn = QPushButton(
            'Получить из БИС подадрес 02')
        to_bis02_btn.clicked.connect(self.send_to_bis02)
        self.main_layout.addWidget(to_bis02_btn)

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.main_layout.addWidget(self.log_text)

        self.showMaximized()

    def init_device_block(self):
        blk_layout = QHBoxLayout()
        self.main_layout.addLayout(blk_layout)

        self.dev_cmbbox = QComboBox()
        self.upd_dev_cmbbox()
        self.dev_cmbbox.activated.connect(self.deactivate_dev)
        blk_layout.addWidget(self.dev_cmbbox)

        activate_btn = QPushButton('Подключить')
        activate_btn.setFixedWidth(100)
        activate_btn.clicked.connect(self.activate_dev)
        blk_layout.addWidget(activate_btn)

        deactivate_btn = QPushButton('Отключить')
        deactivate_btn.setFixedWidth(100)
        deactivate_btn.clicked.connect(self.deactivate_dev)
        blk_layout.addWidget(deactivate_btn)

        self.chl_cmbbox = QComboBox()
        self.chl_cmbbox.addItems(['Шина А', 'Шина Б'])
        self.chl_cmbbox.setFixedWidth(100)
        blk_layout.addWidget(self.chl_cmbbox)

        self.power_cmbbox = QComboBox()
        self.power_cmbbox.addItems(['Питание Внешнее', 'Питание Внутренее'])
        self.power_cmbbox.setFixedWidth(150)
        self.power_cmbbox.activated.connect(self.activate_dev)
        blk_layout.addWidget(self.power_cmbbox)

    def upd_dev_cmbbox(self):
        self.dev_cmbbox.clear()
        for dev_num in range(self.lib.getNumberOfDevices()):
            dev_info = msp_DeviceInfo()
            self.lib.getDeviceInfo(dev_num, dev_info)
            dev_id = dev_info.DeviceId
            ser_number = dev_info.SerialNumber
            busy = dev_info.Busy
            self.dev_cmbbox.addItem(
                f'{dev_num + 1}: DEVICE ID : {dev_id}, Serial number: {ser_number}, busy: {busy}'
            )

    def init_to_diss_block(self):
        group_box = QGroupBox('Массив параметров из БИС в ДИСС')
        box_layout = QGridLayout(group_box)
        headers_su = [
            ('Достоверность крена, тангажа',     0b0000_0000_0100_0000),
            ('Достоверность введённых поправок', 0b0000_0000_0010_0000),
            ('Ввод поправок',                    0b0000_0000_0001_0000),
            ("Море",                             0b0000_0000_0000_1000),
            ("Контроль",                         0b0000_0000_0000_0100),
            ("Шасси обжато",                     0b0000_0000_0000_0010),
            ("Запрет излучения",                 0b0000_0000_0000_0001)
        ]
        positions = [(j, i) for i in range(2) for j in range(4)]
        for position, (header, val) in zip(positions, headers_su):
            chkbx = QCheckBox(header)
            chkbx.setFixedWidth(250)
            box_layout.addWidget(chkbx, *position)
            chkbx.clicked.connect(partial(self.su_clicked_chkbox, val))

        headers_params = [
            'Слово управления',
            'Угол крена',
            'Угол тангажа',
            'Точность установки блока по крену',
            'Точность установки блока по тангажу',
            'Точность установки блока по курсу',
            'Абсолютная высота полёта',
        ]
        self.to_diss_input = []
        positions = [(j, i) for i in range(2, 4) for j in range(4)]
        for position, header in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setFixedWidth(100)
            le.setToolTip(header)
            label = QLabel(header)
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            self.to_diss_input.append(le)

        box_layout.setColumnStretch(5, 1)
        self.to_diss_hex_chkbox = QCheckBox('значение в HEX')
        self.to_diss_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_diss_hex_chkbox, self.to_diss_input))
        box_layout.addWidget(self.to_diss_hex_chkbox, 0, 6)
        self.main_layout.addWidget(group_box)

    def init_to_bis01_block(self):
        group_box = QGroupBox('Массив параметров из ДИСС в БИС подадрес 1')
        box_layout = QGridLayout(group_box)
        headers_ss = [
            ('Отказ МП',         0b0000_0010_0000_0000),
            ('Отказ МЦО',        0b0000_0001_0000_0000),
            ('Отказ МАО',        0b0000_0000_1000_0000),
            ('Отказ УСК',        0b0000_0000_0100_0000),
            ('Отказ МПП',        0b0000_0000_0010_0000),
            ('Отказ УС',         0b0000_0000_0001_0000),
            ('Исправность',      0b0000_0000_0000_1000),
            ('Память',           0b0000_0000_0000_0100),
            ('Контроль',         0b0000_0000_0000_0010),
            ('Запрет излучения', 0b0000_0000_0000_0001)
        ]
        positions = [(j, i) for i in range(2) for j in range(4)]
        self.to_biss_chkbox = {}
        for position, (header, mask) in zip(positions, headers_ss):
            chkbx = QCheckBox(header)
            chkbx.setDisabled(True)
            chkbx.setFixedWidth(250)
            box_layout.addWidget(chkbx, *position)
            self.to_biss_chkbox[chkbx] = mask

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
        self.to_bis01_input = []
        positions = [(j, i) for i in range(2, 4) for j in range(4)]
        for position, header in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(header)
            label = QLabel(header)
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            self.to_bis01_input.append(le)

        box_layout.setColumnStretch(5, 1)

        self.to_bis01_hex_chkbox = QCheckBox('значение в HEX')
        self.to_bis01_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_bis01_hex_chkbox, self.to_bis01_input))
        box_layout.addWidget(self.to_bis01_hex_chkbox, 0, 6)

        self.main_layout.addWidget(group_box)

    def init_to_bis02_block(self):
        group_box = QGroupBox('Массив параметров из ДИСС в БИС подадрес 2')
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
        self.to_bis02_input = []
        positions = [(j, i) for i in range(4) for j in range(4)]
        for position, header in zip(positions, headers_params):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(header)
            label = QLabel(header)
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            self.to_bis02_input.append(le)

        box_layout.setColumnStretch(4, 1)

        self.to_bis02_hex_chkbox = QCheckBox('значение в HEX')
        self.to_bis02_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_bis02_hex_chkbox, self.to_bis02_input))
        box_layout.addWidget(self.to_bis02_hex_chkbox, 0, 6)

        self.main_layout.addWidget(group_box)

    def su_clicked_chkbox(self, val):
        self.SU ^= val
        if self.to_diss_hex_chkbox.isChecked():
            text = f'{self.SU:04X}'
        else:
            text = f'{self.SU}'
        self.to_diss_input[0].setText(text)

    def convert_to_hex(self, chkbox, widgets):
        for widget in widgets:
            if widget.text() == '':
                continue
            if chkbox.isChecked():
                try:
                    widget.setText(f'{int(widget.text()):04X}')
                except ValueError:
                    pass
            else:
                widget.setText(str(int(widget.text(), base=16)))

    def activate_dev(self):
        if self.dev_handle is not None:
            try:
                self.lib.reset(self.dev_handle)
                self.lib.close(self.dev_handle)
            except:
                pass
            finally:
                self.dev_handle = None

        try:
            self.dev_handle = self.lib.open(self.dev_cmbbox.currentIndex())
            if self.dev_handle:
                self.log_text.append(
                    f'<b>{next(self.log_counter)}</b>. Устройство подключено</b>'
                )
            else:
                self.log_text.append(
                    f'<b>{next(self.log_counter)}</b>. Ошибка подключения устройства')
                self.upd_dev_cmbbox()
                self.dev_handle = None
                return
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Произошла ошибка подключения: {e}')
            return

        try:
            power = 0 if self.power_cmbbox.currentIndex() else 1
            self.lib.writeReg(self.dev_handle, mspRR_EXTERNAL_USB_POWER, power)
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Произошла ошибка установки питания: {e}'
            )
            self.dev_handle = None
            self.upd_dev_cmbbox()
            return

        bcflags = [
            mspF_ENHANCED_MODE,
            mspF_256WORD_BOUNDARY_DISABLE,
            mspF_MESSAGE_GAP_TIMER_ENABLED,
            mspF_INTERNAL_TRIGGER_ENABLED,
            mspF_EXPANDED_BC_CONTROL_WORD,
        ]
        try:
            self.lib.configure(
                self.dev_handle,
                msp_MODE_BC + msp_MODE_ENHANCED,
                bcflags,
                None
            )
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Устройство настроено в режим КШ-ОУ')
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка настройки режима: {e}')
            self.dev_handle = None
            self.upd_dev_cmbbox()
            return

    def deactivate_dev(self):
        if self.dev_handle is not None:
            try:
                self.lib.reset(self.dev_handle)
                self.lib.close(self.dev_handle)
            except:
                pass
            finally:
                self.dev_handle = None
        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Устройство отключено.'
        )

    def send_to_diss(self):
        fr = self.get_frame()
        if not fr:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Не удалось создать фрейм'
            )
            return

        channel = msp_BCCW_CHANNEL_B if self.power_cmbbox.currentIndex() else msp_BCCW_CHANNEL_A
        data = [int(widget.text()) if widget.text()
                else 0 for widget in self.to_diss_input]
        try:
            message = msp_Message()
            self.lib.BCtoRT(message, 4, 1, 7, data, channel)
            self.lib.addMessage(
                fr,
                self.lib.createMessage(
                    self.dev_handle,
                    message
                ),
                1000
            )
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка создания сообщения: {e}'
            )
            return

        self.lib.loadFrame(fr, msp_AUTOREPEAT)
        self.lib.start(self.dev_handle)
        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')
        recv_data = message.Data[:message.dataWordCount]
        if not recv_data:
            log_message = f'<b>{next(self.log_counter)}</b>. Данные не доставлены.'
            self.log_text.append(log_message)
            return
        recv_data = [f'<b>0x{data:04x}</b>' for data in recv_data]

        log_message = f'<b>{next(self.log_counter)}</b>. Отправленные данные: {":".join(recv_data)}'
        self.log_text.append(log_message)

    def send_to_bis01(self):
        fr = self.get_frame()
        if not fr:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Не удалось создать фрейм'
            )
            return

        channel = msp_BCCW_CHANNEL_B if self.power_cmbbox.currentIndex() else msp_BCCW_CHANNEL_A
        try:
            message = msp_Message()
            self.lib.RTtoBC(message, 4, 1, 8, channel)
            self.lib.addMessage(
                fr,
                self.lib.createMessage(
                    self.dev_handle,
                    message
                ),
                1000
            )
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка создания сообщения: {e}'
            )
            return

        self.lib.loadFrame(fr, msp_AUTOREPEAT)

        self.lib.start(self.dev_handle)

        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')

        self.lib.retrieveMessage(fr, msp_NEXT_MESSAGE, message)

        recv_data = message.Data[:message.dataWordCount]

        recv_data = [
            22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34
        ]

        if not recv_data:
            log_message = f'<b>{next(self.log_counter)}</b>. Данные не получены'
            self.log_text.append(log_message)
            return

        for widget, val in zip(self.to_bis01_input, recv_data):
            widget.setText(f'{val}')

        for widget, mask in self.to_biss_chkbox.items():
            if recv_data[1] & mask != 0:
                widget.setDisabled(False)
                widget.setChecked(True)
                widget.setDisabled(True)
            else:
                widget.setDisabled(False)
                widget.setChecked(False)
                widget.setDisabled(True)

        recv_data = [f'<b>0x{data:04x}</b>' for data in recv_data]

        log_message = f'<b>{next(self.log_counter)}</b>. Полученные данные: {":".join(recv_data)}'
        self.log_text.append(log_message)

    def send_to_bis02(self):
        fr = self.get_frame()
        if not fr:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Не удалось создать фрейм'
            )
            return

        channel = msp_BCCW_CHANNEL_B if self.power_cmbbox.currentIndex() else msp_BCCW_CHANNEL_A
        try:
            message = msp_Message()
            self.lib.RTtoBC(message, 4, 2, 11, channel)
            self.lib.addMessage(
                fr,
                self.lib.createMessage(
                    self.dev_handle,
                    message
                ),
                1000
            )
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка создания сообщения: {e}'
            )
            return

        self.lib.loadFrame(fr, msp_AUTOREPEAT)

        self.lib.start(self.dev_handle)

        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')

        self.lib.retrieveMessage(fr, msp_NEXT_MESSAGE, message)

        recv_data = message.Data[:message.dataWordCount]

        if not recv_data:
            log_message = f'<b>{next(self.log_counter)}</b>. Данные не получены'
            self.log_text.append(log_message)
            return

        for widget, val in zip(self.to_bis02_input, recv_data):
            widget.setText(f'{val}')

        recv_data = [f'<b>0x{data:04x}</b>' for data in recv_data]

        log_message = f'<b>{next(self.log_counter)}</b>. Полученные данные: {":".join(recv_data)}'
        self.log_text.append(log_message)

    def get_frame(self):
        if self.dev_handle is None:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Устройство не подключено'
            )
            return
        try:
            fr = self.lib.createFrame(self.dev_handle, 1000, 1)
            return fr
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка создания фрейма: {e}'
            )
            return None

    def closeEvent(self, event):
        self.deactivate_dev()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
