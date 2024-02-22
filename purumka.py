import ctypes
import os
import sys
import time
from functools import partial
from itertools import count, cycle

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
import numpy as np
import binascii


class MainData:
    headers = [
        'identificator',
        'ss',
        'wx',
        'wy',
        'wz',
        'wp',
        'us',
        'time'
    ]

    def __init__(self):
        self.data = []

    def get_obj(self, name):
        return self.data[self.headers.index(name)::8]

    def add_data(self, data):
        if len(self.data) > len(self.headers) * 200_000_000:
            self.data = self.data[len(self.headers) * 100_000_000:]
        self.data.extend(data)

    def get_last(self):
        return self.data[-8:]


class ClassWrapper:
    def __init__(self, device_info):
        self.fields = [name[0]
                       for name in getattr(type(device_info), '_fields_')]
        for field in self.fields:
            setattr(self, field, getattr(device_info, field))

    def __str__(self):
        res = [f'{field}: {getattr(self, field)}' for field in self.fields]
        return ' '.join(res)


class GraphWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.data = MainData()

        self.dev_handle = None
        self.log_counter = count(1)
        self.SU = 0b0000_0000_0000_0000

        try:
            self.lib = RTL('./drtl3.dll')
            self.lib.startUp()
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
        to_diss_btn = QPushButton('Отправить в ДИСС')
        to_diss_btn.clicked.connect(self.send_to_diss)
        self.main_layout.addWidget(to_diss_btn)

        self.init_to_bis01_block()
        to_bis01_btn = QPushButton(
            'Получить из ДИСС подадрес 01')
        to_bis01_btn.clicked.connect(self.send_to_bis01)
        self.main_layout.addWidget(to_bis01_btn)

        self.init_to_bis02_block()
        to_bis02_btn = QPushButton(
            'Получить из ДИСС подадрес 02')
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
        blk_layout.addWidget(self.dev_cmbbox)

        self.chl_cmbbox = QComboBox()
        self.chl_cmbbox.addItems(['Шина А', 'Шина Б'])
        self.chl_cmbbox.setFixedWidth(100)
        blk_layout.addWidget(self.chl_cmbbox)

        self.power_cmbbox = QComboBox()
        self.power_cmbbox.addItems(['Питание Внутренее', 'Питание Внешнее'])
        self.power_cmbbox.setFixedWidth(150)
        self.power_cmbbox.activated.connect(self.deactivate_dev)
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
        self.to_diss_chkbox = {}
        for position, (header, val) in zip(positions, headers_su):
            chkbx = QCheckBox(header)
            chkbx.setFixedWidth(250)
            box_layout.addWidget(chkbx, *position)
            chkbx.clicked.connect(partial(self.su_clicked_chkbox, val))
            self.to_diss_chkbox[chkbx] = val

        self.to_diss_elems = [
            {'name': 'Слово управления', 'coef': 1, 'signed': False, 'func': self.change_su_widgets},
            {'name': 'Угол крена', 'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Угол тангажа', 'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Точность установки блока по крену',
                'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Точность установки блока по тангажу',
                'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Точность установки блока по курсу',
                'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Абсолютная высота полёта', 'coef': 1, 'signed': True},
        ]
        positions = [(j, i) for i in range(2, 4) for j in range(4)]
        for position, elem in zip(positions, self.to_diss_elems):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setFixedWidth(100)
            le.setToolTip(elem['name'])
            label = QLabel(elem['name'])
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            elem['widget'] = le
            if 'func' in elem:
                le.textChanged.connect(partial(elem['func'], le))

        box_layout.setColumnStretch(5, 1)
        self.to_diss_hex_chkbox = QCheckBox('значение в HEX')
        self.to_diss_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_diss_hex_chkbox, self.to_diss_elems))
        box_layout.addWidget(self.to_diss_hex_chkbox, 0, 6)
        # self.to_diss_elems[0]['widget'].textChanged.connect(
        #     self.change_su_widgets)

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
            ('Исправность (0 - исправность, 1 - отказ)',      0b0000_0000_0000_1000),
            ('Память',           0b0000_0000_0000_0100),
            ('Контроль',         0b0000_0000_0000_0010),
            ('Запрет излучения', 0b0000_0000_0000_0001)
        ]
        positions = [(j, i) for i in range(2) for j in range(5)]
        self.to_biss_chkbox = {}
        for position, (header, mask) in zip(positions, headers_ss):
            chkbx = QCheckBox(header)
            chkbx.setDisabled(True)
            chkbx.setFixedWidth(250)
            box_layout.addWidget(chkbx, *position)
            self.to_biss_chkbox[chkbx] = mask

        self.to_bis01_elems = [
            {'name': 'Идентификатор массива', 'coef': 1, 'signed': False},
            {'name': 'Слово состояния', 'coef': 1, 'signed': False, 'func': self.send_to_bis01_checkboxes},
            {'name': 'Продольная составляющая вектора скорости',
                'coef': 4096 / 2 ** 16, 'signed': False},
            {'name': 'Вертикальная составляющая вектора скорости',
                'coef': 256 / 2 ** 15, 'signed': True},
            {'name': 'Поперечная составляющая вектора скорости',
                'coef': 256 / 2 ** 15, 'signed': True},
            {'name': 'Путевая скорость', 'coef': 4096 / 2 ** 16, 'signed': False},
            {'name': 'Угол сноса', 'coef': 360 / (2 ** 16), 'signed': True},
            {'name': 'Время наработки', 'coef': 1, 'signed': False}
        ]

        positions = [(j, i) for i in range(2, 4) for j in range(5)]
        for position, elem in zip(positions, self.to_bis01_elems):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(elem['name'])
            label = QLabel(elem['name'])
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            elem['widget'] = le
            if 'func' in elem:
                le.textChanged.connect(partial(elem['func'], le))

        box_layout.setColumnStretch(5, 1)

        self.to_bis01_hex_chkbox = QCheckBox('значение в HEX')
        self.to_bis01_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_bis01_hex_chkbox, self.to_bis01_elems))
        box_layout.addWidget(self.to_bis01_hex_chkbox, 0, 6)

        self.main_layout.addWidget(group_box)

    def init_to_bis02_block(self):
        group_box = QGroupBox('Массив параметров из ДИСС в БИС подадрес 2')
        box_layout = QGridLayout(group_box)

        self.to_bis02_elems = [
            {'name': 'Версия ПМО', 'coef': 1, 'signed': False},
            {'name': 'Дата ПМО', 'coef': 1, 'signed': False, 'func': self.int_to_date},
            {'name': 'Контрольная сумма ПМО1', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО2', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО3', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО4', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО5', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО6', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО7', 'coef': 1, 'signed': False},
            {'name': 'Контрольная сумма ПМО8', 'coef': 1, 'signed': False},
            {'name': 'Серий номер изделия', 'coef': 1, 'signed': False}
        ]

        self.to_bis02_input = []
        positions = [(j, i) for i in range(4) for j in range(4)]
        for position, elem in zip(positions, self.to_bis02_elems):
            layout = QHBoxLayout()
            le = QLineEdit()
            le.setDisabled(True)
            le.setFixedWidth(100)
            le.setToolTip(elem['name'])
            label = QLabel(elem['name'])
            label.setFixedWidth(250)
            layout.addWidget(le)
            layout.addWidget(label)
            box_layout.addLayout(layout, *position)
            elem['widget'] = le
            if 'func' in elem:
                le.textChanged.connect(partial(elem['func'], le))

        box_layout.setColumnStretch(4, 1)

        self.to_bis02_hex_chkbox = QCheckBox('значение в HEX')
        self.to_bis02_hex_chkbox.clicked.connect(
            partial(self.convert_to_hex, self.to_bis02_hex_chkbox, self.to_bis02_elems))
        box_layout.addWidget(self.to_bis02_hex_chkbox, 0, 6)

        self.main_layout.addWidget(group_box)

    def change_su_widgets(self, data_widget):
        widget_text = data_widget.text() 
        if not widget_text:
            widget_text = 0
            self.to_diss_elems[0]['widget'].setText('0')
        if self.to_diss_hex_chkbox.isChecked():
            self.SU = int(widget_text, 16)
        else:
            self.SU = int(widget_text)
        for widget, mask in self.to_diss_chkbox.items():
            if self.SU & mask:
                widget.setChecked(True)
            else:
                widget.setChecked(False)

    def su_clicked_chkbox(self, val):
        self.SU ^= val
        if self.to_diss_hex_chkbox.isChecked():
            text = f'{self.SU:04X}'
        else:
            text = f'{self.SU}'
        self.to_diss_elems[0]['widget'].setText(text)

    def convert_to_hex(self, chkbox, elems):
        for elem in elems:
            elem['widget'].blockSignals(True)
            widget_text = elem['widget'].text()
            if not widget_text:
                continue
            try:
                if chkbox.isChecked():
                    val = round(float(widget_text) / elem['coef'])
                    val = val.to_bytes(length=2, signed=elem['signed'])
                    text = f'{val.hex().upper()}'
                else:
                    byte_value = binascii.unhexlify(widget_text)
                    val = int.from_bytes(
                        byte_value, byteorder="big", signed=elem['signed'])
                    text = f'{round(val * elem["coef"], 2)}'
            except:
                if '.' in widget_text:
                    text = widget_text
                else:
                    text = '0'

            elem['widget'].setText(text)
            elem['widget'].blockSignals(False)

    def int_to_date(self, data_widget: QLineEdit):
        data_widget.blockSignals(True)
        try:
            num = int(data_widget.text(), 16)
            year = str(num >> 9).zfill(4)
            month = str((num >> 5) & 0x0F).zfill(2)
            day = str(num & 0x1F).zfill(2)
            data_widget.setText(f'{day}.{month}.{year}')
        except:
            day, month, year = [int(x) for x in data_widget.text().split('.')]
            num = (year << 9) + (month << 5) + day
            data_widget.setText(f'{num:04X}')
        data_widget.blockSignals(False)

        

    def activate_dev(self):
        if self.dev_handle is not None:
            try:
                self.lib.reset(self.dev_handle)
                self.lib.close(self.dev_handle)
            except:
                pass
            finally:
                self.dev_handle = None

        self.dev_handle = self.lib.open(self.dev_cmbbox.currentIndex())
        power = self.power_cmbbox.currentIndex()
        self.lib.writeReg(self.dev_handle, mspRR_EXTERNAL_USB_POWER, power)
        bcflags = [
            mspF_ENHANCED_MODE,
            mspF_256WORD_BOUNDARY_DISABLE,
            mspF_MESSAGE_GAP_TIMER_ENABLED,
            mspF_INTERNAL_TRIGGER_ENABLED,
            mspF_EXPANDED_BC_CONTROL_WORD,
        ]
        self.lib.configure(
            self.dev_handle,
            msp_MODE_BC + msp_MODE_ENHANCED,
            bcflags,
            None
        )

    def deactivate_dev(self):
        try:
            self.lib.reset(self.dev_handle)
            self.lib.close(self.dev_handle)
        except:
            pass
        finally:
            self.dev_handle = None

    def send_to_diss(self):
        try:
            self.activate_dev()
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Произошла ошибка подключения к устройству: {e}. Попробуйте выбрать другое или выключить другие программы по работе с ним.')
            self.deactivate_dev()
            return

        try:
            fr = self.lib.createFrame(self.dev_handle, 1000, 1)
            channel = msp_BCCW_CHANNEL_B if self.chl_cmbbox.currentIndex() else msp_BCCW_CHANNEL_A
            data = []
            for elem in self.to_diss_elems:
                if not elem['widget'].text():
                    data.append(0)
                    continue
                if self.to_diss_hex_chkbox.isChecked():
                    data.append(int(elem['widget'].text(), base=16))
                else:
                    data.append(
                        round(float(elem['widget'].text()) / elem['coef']))

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
            self.lib.loadFrame(fr, msp_AUTOREPEAT)
            self.lib.start(self.dev_handle)
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')
            self.lib.retrieveMessage(fr, msp_NEXT_MESSAGE, message)

            recv_data = message.Data[:message.dataWordCount]
            recv_data = [f'<b>0x{data:04x}</b>' for data in recv_data]

            log_message = f'<b>{next(self.log_counter)}</b>. Отправленные данные: {":".join(recv_data)}'
            self.log_text.append(log_message)
            if not message.StatusWord1:
                raise ValueError('Ответ не получен')
            else:
                log_message = f'<b>{next(self.log_counter)}</b>. Получен ответ: 0x{message.StatusWord1:04x}'
                self.log_text.append(log_message)
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка отправки: {e}'
            )
        finally:
            self.deactivate_dev()

    def send_to_bis01(self):
        try:
            self.activate_dev()
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Произошла ошибка подключения к устройству: {e}. Попробуйте выбрать другое или выключить другие программы по работе с ним.')
            self.deactivate_dev()
            return

        try:
            recv_data = self.recieve_data(1, 8, 1)
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка получения сообщения: {e}'
            )
            return
        finally:
            self.deactivate_dev()

        # recv_data = [0, 257,2,3,4,5,6,7]

        for elem, val in zip(self.to_bis01_elems, recv_data):
            string = f'{val:04X}' if self.to_bis01_hex_chkbox.isChecked(
            ) else f'{round(val * elem["coef"], 2)}'
            elem['widget'].setText(string)


    def send_to_bis01_checkboxes(self, data_widget):
        data_widget_value = int(data_widget.text())
        for widget, mask in self.to_biss_chkbox.items():
            if int(data_widget_value) & mask != 0:
                widget.setDisabled(False)
                widget.setChecked(True)
                widget.setDisabled(True)
            else:
                widget.setDisabled(False)
                widget.setChecked(False)
                widget.setDisabled(True)

    def send_to_bis02(self):
        try:
            self.activate_dev()
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Произошла ошибка подключения к устройству: {e}. Попробуйте выбрать другое или выключить другие программы по работе с ним.')
            self.deactivate_dev()
            return
        try:
            recv_data = self.recieve_data(2, 11, 1)
        except Exception as e:
            self.log_text.append(
                f'<b>{next(self.log_counter)}</b>. Ошибка получения сообщения: {e}'
            )
            return
        finally:
            self.deactivate_dev()

        # recv_data = [0, 257,2,3,4,5,6,7]
        for elem, val in zip(self.to_bis02_elems, recv_data):
            string = f'{val:04X}' if self.to_bis02_hex_chkbox.isChecked(
            ) else f'{round(val * elem["coef"], 2)}'
            elem['widget'].setText(string)

    def recieve_data(self, address, words, count):
        fr = self.lib.createFrame(self.dev_handle, 1000, 1)
        channel = msp_BCCW_CHANNEL_B if self.chl_cmbbox.currentIndex() else msp_BCCW_CHANNEL_A

        message = msp_Message()
        self.lib.addMessage(
            fr,
            self.lib.createMessage(
                self.dev_handle,
                self.lib.RTtoBC(message, 4, address, words, channel)
            ),
            1000
        )
        self.lib.loadFrame(fr, msp_AUTOREPEAT)

        self.lib.start(self.dev_handle)

        self.log_text.append(
            f'<b>{next(self.log_counter)}</b>. Отправлена команда: 0x{message.CmdWord1:04x}')
        while count != 0:
            self.lib.retrieveMessage(fr, msp_NEXT_MESSAGE, message)
            if not message.StatusWord1:
                raise RuntimeError('Данные не получены')
            recv_data = message.Data[:message.dataWordCount]
            if not recv_data:
                continue
            log_data = [f'<b>0x{data:04x}</b>' for data in recv_data]
            log_message = f'<b>{next(self.log_counter)}</b>. Полученные данные: {":".join(log_data)}'
            self.log_text.append(log_message)
            time.sleep(0.008)
            count -= 1
        return recv_data

    def make_graph(self):
        ...

    def closeEvent(self, event):
        self.deactivate_dev()
        self.lib.cleanup()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())
