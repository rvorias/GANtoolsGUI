#Author: Raphael Vorias


import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QLabel, QSpinBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
import subprocess
import random

class App(QWidget):
    keys = []
    
    def __init__(self):
        super().__init__()
        self.title = 'ganBreeder - ganTool'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 400
        self.outputFolder = os.path.dirname(os.path.realpath(__file__))+'/output/'
        self.initUI()
        
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.hboxTotal = QHBoxLayout()
        self.vboxLeft = QVBoxLayout()
        self.vboxRight = QVBoxLayout()

        # LOGGING #############################################################
        self.logLabel = QLabel()
        self.logLabel.setAlignment(Qt.AlignCenter)
        self.logLabel.setStyleSheet('color: green')
        self.pushLog('__ ready for input __')
        self.vboxLeft.addWidget(self.logLabel)

        # LOGIN ###############################################################
        # Username
        usernameLabel = QLabel()
        usernameLabel.setText('username')
        self.usernameLE = QLineEdit(self)
        # Password
        passwordLabel = QLabel()
        passwordLabel.setText('password')
        self.passwordLE = QLineEdit(self)
        self.passwordLE.setEchoMode(QLineEdit.Password)
                
        hboxLogin = QHBoxLayout()
        hboxLogin.addWidget(usernameLabel)
        hboxLogin.addWidget(self.usernameLE)
        hboxLogin.addWidget(passwordLabel)
        hboxLogin.addWidget(self.passwordLE)
        self.passwordLE.setEchoMode(QLineEdit.Password)
                
        self.vboxLeft.addLayout(hboxLogin)
        
        # FRAMES ##############################################################
        # Number of frames
        hboxNFrames = QHBoxLayout()      
        nFramesLabel = QLabel()
        nFramesLabel.setText('nFrames')
        self.nFramesSB = QSpinBox()
        self.nFramesSB.setMinimum(0)
        self.nFramesSB.setMaximum(999)
        self.nFramesSB.setValue(10)
        
        hboxNFrames.addWidget(nFramesLabel)   
        hboxNFrames.addWidget(self.nFramesSB)  
        
        self.vboxLeft.addLayout(hboxNFrames)
        
        # OUTPUT FOLDER #######################################################
        hboxOutput = QHBoxLayout()      
        outputLabel = QLabel()
        outputLabel.setText('outputFolder')
        self.outputLE = QLineEdit(self)
        self.outputLE.setText(self.outputFolder)
        
        hboxOutput.addWidget(outputLabel)   
        hboxOutput.addWidget(self.outputLE)  
        
        self.vboxLeft.addLayout(hboxOutput)        
        
        # KEYS ################################################################
        hboxNKeys = QHBoxLayout()      
        nKeysLabel = QLabel()
        nKeysLabel.setText('nKeys')
        self.nKeysSB = QSpinBox()
        self.nKeysSB.setMinimum(3)
        self.nKeysSB.setMaximum(10)
        self.nKeysSB.setValue(3)
        self.nKeysSB.valueChanged.connect(self.keyValueChange)
        
        hboxNKeys.addWidget(nKeysLabel)   
        hboxNKeys.addWidget(self.nKeysSB)
        self.vboxLeft.addLayout(hboxNKeys)

        self.initKeys()
        self.vboxKeys = QVBoxLayout()
        self.setKeysWidgets() #puts keys in self.vboxKeys
        self.vboxLeft.addLayout(self.vboxKeys)
        self.vboxLeft.addStretch(1)
        
        # RIGHT VBOX ##########################################################
        runButton = QPushButton('run', self)
        runButton.clicked.connect(self.run)
        self.vboxRight.addWidget(runButton)
        
        viewButton = QPushButton('view', self)
        viewButton.clicked.connect(self.view)
        self.vboxRight.addWidget(viewButton)
        self.vboxRight.addStretch(1)
        
        # compiling total layout
        self.hboxTotal.addLayout(self.vboxLeft)
        self.hboxTotal.addLayout(self.vboxRight)
        self.setLayout(self.hboxTotal)
        
        self.setUserSettings()
        
        self.show()

    def pushLog(self,msg):
        self.logLabel.setText(msg)
        self.logLabel.update()
        
    def setUserSettings(self):
        #Fill here for auto-fill
        self.usernameLE.setText('') #<--- username
        self.passwordLE.setText('') #<--- passw
        self.keys[0].setText('b7be350699c9eef42f5e4c6a')
        self.keys[1].setText('b5c06f29c1b15039812bf45a')
        self.keys[2].setText('54fc255ae27d61ad87f34687')

    def initKeys(self):
        for i in range(self.nKeysSB.value()):
            self.addNewKey()

    def setKeysWidgets(self):
        for i in reversed(range(self.vboxKeys.count())): 
            self.vboxKeys.itemAt(i).widget().setParent(None)
        for k in self.keys:
            self.vboxKeys.addWidget(k)
        self.vboxKeys.update()

    def addNewKey(self):
        keyVal = QLineEdit(self)
        keyVal.setText('')
        self.keys.append(keyVal)

    @pyqtSlot()
    def keyValueChange(self):
        newVal = self.nKeysSB.value()
        oldVal = len(self.keys)
        delta = newVal-oldVal

        if delta > 0:
            for i in range(delta):
                self.addNewKey()
                self.pushLog('__ added key __')
        elif delta < 0:
            for i in range(-delta):
                self.keys.pop()
                self.pushLog('__ removed key __')
        self.setKeysWidgets()
        print('change')

    @pyqtSlot()
    def run(self):
        self.pushLog('__ running : might take a while to load bigGAN __')
        self.logLabel.update()
        self.randHex = '%06x' % random.randint(0, 0xFFFFFF)
        outputDir = self.outputLE.text()+self.randHex
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
        cmd.append(outputDir)
        cmd.append('--keys')
        for k in self.keys:
            if k.text() != '':
                cmd.append(k.text())

        # create output folder if it doesn't exist
        try:
            os.mkdir(outputDir)
        except OSError:
            print ("%s Already exists" % outputDir)
        else:
            print ("Successfully created the directory %s " % outputDir)
        
        # run ganTools
        print(cmd)
        MyOut = subprocess.Popen(cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
        stdout,stderr = MyOut.communicate()
        print(stdout)
        print(stderr)
        self.pushLog('__ running : complete __')
        
    @pyqtSlot()
    def view(self):
        self.pushLog('__ viewing : %s.mp4 __' % self.randHex)
        print('calling command inside conda environment')
        print('bash command:')
        
        cmd = ['ffmpeg']
        cmd.append('-f')
        cmd.append('image2')
        cmd.append('-i')
        cmd.append('output/'+self.randHex+'/%04d.jpeg')
        cmd.append('-crf')
        cmd.append('18')
        cmd.append('output/'+self.randHex+'.mp4')
        print(cmd)
        subprocess.run(cmd)
        
        #Play the file        
        cmd = ['mpv','output/'+self.randHex+'.mp4','--loop']
        print(cmd)
        subprocess.run(cmd)
        self.pushLog('__ viewing : done __')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
