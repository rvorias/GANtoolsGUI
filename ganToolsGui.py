import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QLabel, QSpinBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import subprocess

class App(QWidget):
    keys = []
    
    def __init__(self):
        super().__init__()
        self.title = 'ganBreeder - ganTool'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 200
        self.outputFolder = os.path.dirname(os.path.realpath(__file__))+'/output/'
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        hboxTotal = QHBoxLayout()
        vboxLeft = QVBoxLayout()
        vboxRight = QVBoxLayout()
        
        # LOGIN ###############################################################
        # Username
        usernameLabel = QLabel()
        usernameLabel.setText('username')
        self.usernameLE = QLineEdit(self)
        # Password
        passwordLabel = QLabel()
        passwordLabel.setText('password')
        self.passwordLE = QLineEdit(self)
                
        hboxLogin = QHBoxLayout()
        hboxLogin.addWidget(usernameLabel)
        hboxLogin.addWidget(self.usernameLE)
        hboxLogin.addWidget(passwordLabel)
        hboxLogin.addWidget(self.passwordLE)
        self.passwordLE.setEchoMode(QLineEdit.Password)
                
        vboxLeft.addLayout(hboxLogin)
        
        # FRAMES ##############################################################
        # Number of frames
        hboxNFrames = QHBoxLayout()      
        nFramesLabel = QLabel()
        nFramesLabel.setText('nFrames')
        self.nFramesSB = QSpinBox()
        self.nFramesSB.setMinimum(0)
        self.nFramesSB.setValue(10)
        
        hboxNFrames.addWidget(nFramesLabel)   
        hboxNFrames.addWidget(self.nFramesSB)  
        
        vboxLeft.addLayout(hboxNFrames)
        
        # OUTPUT FOLDER #######################################################
        hboxOutput = QHBoxLayout()      
        outputLabel = QLabel()
        outputLabel.setText('outputFolder')
        self.outputLE = QLineEdit(self)
        self.outputLE.setText(self.outputFolder)
        
        hboxOutput.addWidget(outputLabel)   
        hboxOutput.addWidget(self.outputLE)  
        
        vboxLeft.addLayout(hboxOutput)        
        
        # KEYS ################################################################
        self.addNewKey()
        self.addNewKey()
        self.addNewKey()
        self.addNewKey()
        self.addNewKey()
        vboxKeys = QVBoxLayout()
        for k in self.keys:
            vboxKeys.addWidget(k)
        vboxLeft.addLayout(vboxKeys)
        vboxLeft.addStretch(1)
        
        # RIGHT VBOX ##########################################################
        runButton = QPushButton('run', self)
        runButton.clicked.connect(self.run)
        vboxRight.addWidget(runButton)
        
        viewButton = QPushButton('view', self)
        viewButton.clicked.connect(self.view)
        vboxRight.addWidget(viewButton)
        
        # compiling total layout
        hboxTotal.addLayout(vboxLeft)
        hboxTotal.addLayout(vboxRight)
        self.setLayout(hboxTotal)
        
        self.setUserSettings()
        
        self.show()
        
    def setUserSettings(self):
        #Fill here for auto-fill
        self.usernameLE.setText('')
        self.passwordLE.setText('')
        self.keys[0].setText('7968340a72eabab735d04dba')
        self.keys[1].setText('0416461072e5e22fd6d1637c')
        self.keys[2].setText('c37d216dfd865aa7397db242')
        
    def addNewKey(self):
        keyVal = QLineEdit(self)
        keyVal.setText('')
        self.keys.append(keyVal)

    @pyqtSlot()
    def run(self):
        print('calling command inside conda environment')
        print('bash command:')
        cmd = ['gantools']
        cmd.append('--username')
        cmd.append(self.usernameLE.text())
        cmd.append('--password')
        cmd.append(self.passwordLE.text())
        cmd.append('--nframes')
        cmd.append(str(self.nFramesSB.value()))
        cmd.append('--output-dir')
        cmd.append(self.outputLE.text())
        cmd.append('--keys')
        for k in self.keys:
            if k.text() != '':
                cmd.append(k.text())
            
        print(cmd)

        MyOut = subprocess.Popen(cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        print(stdout)
        print(stderr)
        
    @pyqtSlot()
    def view(self):
        print('calling command inside conda environment')
        print('bash command:')
        cmd = ['ffmpeg']
        cmd.append('-f')
        cmd.append('image2')
        cmd.append('-i')
        cmd.append('output/%04d.jpeg')
        cmd.append('-crf')
        cmd.append('18')
        cmd.append('output/output.mp4')
        print(cmd)
        subprocess.run(cmd)
        
        #Play the file        
        cmd = ['mpv','output.mp4','--loop']
        print(cmd)
        subprocess.run(cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
