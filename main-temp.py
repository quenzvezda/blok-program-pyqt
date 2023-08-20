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
        self.upperLayout = QHBoxLayout()  # mendefinisikan upperLayout

        # Dropdown untuk memilih Serial COM
        self.comDropdown = QComboBox(self.centralwidget)
        self.comDropdown.addItems(['COM3', 'COM4', 'COM9', 'COM11'])
        self.upperLayout.addWidget(self.comDropdown)

        # Button untuk mengecek koneksi ke Arduino
        self.checkButton = QtWidgets.QPushButton(self.centralwidget, text='Cek Koneksi')
        self.checkButton.clicked.connect(self.checkConnection)
        self.upperLayout.addWidget(self.checkButton)

        # Label untuk menampilkan status koneksi
        self.statusLabel = QLabel(self.centralwidget, text='Status: Tidak Terhubung')
        self.upperLayout.addWidget(self.statusLabel)

        # Menambahkan upperLayout ke mainLayout
        self.mainLayout.addLayout(self.upperLayout)

        # Tombol blok program
        self.block1Button = QtWidgets.QPushButton(self.centralwidget, text='Maju')
        self.block1Button.clicked.connect(lambda: self.addBlock('pic\maju.png', 'F'))
        self.buttonsLayout.addWidget(self.block1Button)

        self.block2Button = QtWidgets.QPushButton(self.centralwidget, text='Mundur')
        self.block2Button.clicked.connect(lambda: self.addBlock('pic\mundur.png', 'B'))
        self.buttonsLayout.addWidget(self.block2Button)
        
        self.block3Button = QtWidgets.QPushButton(self.centralwidget, text='Kanan')
        self.block3Button.clicked.connect(lambda: self.addBlock('pic\kanan.png', 'R'))
        self.buttonsLayout.addWidget(self.block3Button)
        
        self.block4Button = QtWidgets.QPushButton(self.centralwidget, text='Kiri')
        self.block4Button.clicked.connect(lambda: self.addBlock('pic\kiri.png', 'L'))
        self.buttonsLayout.addWidget(self.block4Button)
        
        #self.block5Button = QtWidgets.QPushButton(self.centralwidget, text='Stop')
        #self.block5Button.clicked.connect(lambda: self.addBlock('pic\kiri.png', 'S'))
        #self.buttonsLayout.addWidget(self.block5Button)

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
        dropdown.setFixedWidth(150)  # Set fixed width of the dropdown to match the block
        if blockCode in ['F', 'B']:
            dropdown.addItems(['10cm', '20cm', '30cm', '40cm', '50cm'])
        else:  # 'L' dan 'R'
            dropdown.addItems(['30°', '45°', '60°', '90°'])
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
                # Parse nilai dari dropdown, hanya mengambil angka
                value = ''.join(filter(str.isdigit, value))
                f.write(f'{blockCode}{value}\n')
            f.write(f'S0\n')
                
        selected_com = str(self.comDropdown.currentText())
        ser = serial.Serial(selected_com, 9600)  # ganti 'COM4' dengan port yang sesuai
        time.sleep(2)  # memberi waktu untuk koneksi serial untuk membuka

        with open('output.txt', 'r') as f:
            data = f.read().replace('\n', ',')  # baca file dan ganti newline dengan koma

        ser.write(data.encode())  # kirim data
        time.sleep(1)  # menunggu sedikit
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                
                # Jika pesan khusus diterima, keluar dari loop
                if line == "Semua Perintah Dijalankan":
                    break


        # Menampilkan serial monitor tapi gk akan pernah berhenti
        # while True:
        #     if ser.in_waiting > 0:
        #         line = ser.readline().decode('utf-8').rstrip()
        #         print(line)

        ser.close()  # tutup koneksi ketika selesai


    def resetBlocks(self):
        for i in reversed(range(self.blocksLayout.count())): 
            self.blocksLayout.itemAt(i).widget().setParent(None)
            
    def checkConnection(self):
        port = self.comDropdown.currentText()
        try:
            ser = serial.Serial(port, 9600)
            time.sleep(2)  # memberi waktu untuk koneksi serial untuk membuka
            ser.close()
            self.statusLabel.setText('Status: Terhubung')
        except:
            self.statusLabel.setText('Status: Tidak Terhubung')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
