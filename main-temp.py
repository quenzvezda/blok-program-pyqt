from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QScrollArea, QWidget, QComboBox
from PyQt5.QtGui import QPixmap

import serial
import time
import re

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.blocksLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()

        # Tombol blok program
        self.block1Button = QtWidgets.QPushButton(self.centralwidget, text='Maju')
        self.block1Button.clicked.connect(lambda: self.addBlock('maju.png', 'F'))
        self.buttonsLayout.addWidget(self.block1Button)

        self.block2Button = QtWidgets.QPushButton(self.centralwidget, text='Mundur')
        self.block2Button.clicked.connect(lambda: self.addBlock('mundur.png', 'B'))
        self.buttonsLayout.addWidget(self.block2Button)
        
        self.block3Button = QtWidgets.QPushButton(self.centralwidget, text='Kanan')
        self.block3Button.clicked.connect(lambda: self.addBlock('kanan.png', 'R'))
        self.buttonsLayout.addWidget(self.block3Button)
        
        self.block4Button = QtWidgets.QPushButton(self.centralwidget, text='Kiri')
        self.block4Button.clicked.connect(lambda: self.addBlock('kiri.png', 'L'))
        self.buttonsLayout.addWidget(self.block4Button)


        # Tombol Kirim dan Reset
        self.sendButton = QtWidgets.QPushButton(self.centralwidget, text='Kirim')
        self.sendButton.clicked.connect(self.sendBlocks)
        self.buttonsLayout.addWidget(self.sendButton)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget, text='Reset')
        self.resetButton.clicked.connect(self.resetBlocks)
        self.buttonsLayout.addWidget(self.resetButton)

        # Area Scroll untuk blocksLayout
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setLayout(self.blocksLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addLayout(self.buttonsLayout)

        MainWindow.setCentralWidget(self.centralwidget)

    def addBlock(self, blockName, blockCode):
        # Widget yang berisi gambar dan dropdown
        widget = QtWidgets.QWidget(self.centralwidget)
        layout = QVBoxLayout(widget)
        block = QLabel(self.centralwidget)
        pixmap = QPixmap(blockName).scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        block.setPixmap(pixmap)
        layout.addWidget(block)

        # Dropdown dengan pilihan pengguna
        dropdown = QComboBox(self.centralwidget)
        dropdown.setFixedWidth(150) # Set fixed width of the dropdown to match the block
        dropdown.addItems(['10', '20', '30', '40', '45', '50', '60', '90'])
        layout.addWidget(dropdown)

        # Menambah widget ke blocksLayout
        self.blocksLayout.addWidget(widget)

        # Menyimpan kode blok dan dropdown untuk nanti
        widget.setProperty('blockCode', blockCode)
        widget.setProperty('dropdown', dropdown)

    def sendBlocks(self):
        with open('output.txt', 'w') as f:
            for i in range(self.blocksLayout.count()):
                widget = self.blocksLayout.itemAt(i).widget()
                blockCode = widget.property('blockCode')
                dropdown = widget.property('dropdown')
                value = dropdown.currentText()
                f.write(f'{blockCode}{value}\n')
                
        ser = serial.Serial('COM4', 9600)  # ganti 'COM4' dengan port yang sesuai
        time.sleep(2)  # memberi waktu untuk koneksi serial untuk membuka

        with open('output.txt', 'r') as f:
            lines = f.read().splitlines()  # baca file dan hapus newline di akhir setiap baris
            data = [[re.findall("[a-zA-Z]+", line)[0], re.findall("\d+", line)[0]] for line in lines]  # pisahkan huruf dan angka

        ser.write(str(len(data)).encode())  # kirim ukuran array
        time.sleep(1)  # menunggu sedikit

        for pair in data:
            ser.write(pair[0].encode())  # kirim huruf
            time.sleep(1)
            ser.write(pair[1].encode())  # kirim angka
            time.sleep(1)

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)

        ser.close()  # tutup koneksi ketika selesai


    def resetBlocks(self):
        for i in reversed(range(self.blocksLayout.count())): 
            self.blocksLayout.itemAt(i).widget().setParent(None)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
