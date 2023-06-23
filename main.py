from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

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
        self.block1Button.clicked.connect(lambda: self.addBlock('maju.png'))
        self.buttonsLayout.addWidget(self.block1Button)

        self.block2Button = QtWidgets.QPushButton(self.centralwidget, text='Mundur')
        self.block2Button.clicked.connect(lambda: self.addBlock('mundur.png'))
        self.buttonsLayout.addWidget(self.block2Button)
        
        self.block3Button = QtWidgets.QPushButton(self.centralwidget, text='Kanan')
        self.block3Button.clicked.connect(lambda: self.addBlock('kanan.png'))
        self.buttonsLayout.addWidget(self.block3Button)
        
        self.block4Button = QtWidgets.QPushButton(self.centralwidget, text='Kiri')
        self.block4Button.clicked.connect(lambda: self.addBlock('kiri.png'))
        self.buttonsLayout.addWidget(self.block4Button)
        
        # Tombol Kirim dan Reset
        self.sendButton = QtWidgets.QPushButton(self.centralwidget, text='Kirim')
        self.sendButton.clicked.connect(self.sendBlocks)
        self.buttonsLayout.addWidget(self.sendButton)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget, text='Reset')
        self.resetButton.clicked.connect(self.resetBlocks)
        self.buttonsLayout.addWidget(self.resetButton)

        self.mainLayout.addLayout(self.blocksLayout)
        self.mainLayout.addLayout(self.buttonsLayout)

        MainWindow.setCentralWidget(self.centralwidget)

    def addBlock(self, blockName):
        block = QLabel(self.centralwidget)
        pixmap = QPixmap(blockName).scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        block.setPixmap(pixmap)
        self.blocksLayout.addWidget(block)

    def sendBlocks(self):
        # Implementasikan fungsi ini
        pass

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
