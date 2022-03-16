import sys

from PyQt5.Qt import QWidget, QColor, QPixmap, QIcon, QSize, QCheckBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QSplitter, \
    QComboBox, QLabel, QSpinBox, QFileDialog, QApplication
from Paintboard import PaintBoard
import cv2
import tensorflow as tf
import numpy as np

try:
    import tensorflow.python.keras as keras
except:
    import tensorflow.keras as keras


class Interface(QWidget):

    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData()
        self.__InitView()
        self.__initmodel()

    def __initmodel(self):
        model = tf.keras.models.load_model('saved_model/my_model_28')
        self.__model = model

    def __InitData(self):
        '''
                  Initializing data
        '''
        self.__paintBoard = PaintBoard(self)
        # 获取颜色列表(字符串类型)
        self.__colorList = QColor.colorNames()

    def __InitView(self):
        '''
                  Initializing
        '''
        # set a new mainlayout
        main_layout = QHBoxLayout(self)
        # Set the distence between each components
        main_layout.setSpacing(40)

        # Put the paintboard in
        main_layout.addWidget(self.__paintBoard)

        # set subui for bottom
        sub_layout = QVBoxLayout()


        # Set size of the sublayout
        sub_layout.setContentsMargins(10, 10, 10, 10)

        # splitter = QSplitter(self)
        # sub_layout.addWidget(splitter)

        self.__btn_Recognize = QPushButton("Start recognition")
        self.__btn_Recognize.setParent(self)
        self.__btn_Recognize.clicked.connect(self.on_btn_Recognize_Clicked)
        sub_layout.addWidget(self.__btn_Recognize)

        self.__btn_Clear = QPushButton("Clear")
        self.__btn_Clear.setParent(self)

        # Connect Clear bottom to the function
        self.__btn_Clear.clicked.connect(self.__paintBoard.Clear)
        sub_layout.addWidget(self.__btn_Clear)

        self.__btn_Quit = QPushButton("Exit")
        self.__btn_Quit.setParent(self)  # Set parent as interface
        self.__btn_Quit.clicked.connect(self.Quit)
        sub_layout.addWidget(self.__btn_Quit)

        self.__btn_Save = QPushButton("Save")
        self.__btn_Save.setParent(self)
        self.__btn_Save.clicked.connect(self.on_btn_Save_Clicked)
        sub_layout.addWidget(self.__btn_Save)

        self.__cbtn_Eraser = QCheckBox("Eraser")
        self.__cbtn_Eraser.setParent(self)
        self.__cbtn_Eraser.clicked.connect(self.on_cbtn_Eraser_clicked)
        sub_layout.addWidget(self.__cbtn_Eraser)

        self.__label_penThickness = QLabel(self)
        self.__label_penThickness.setText("Size")
        self.__label_penThickness.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penThickness)

        self.__spinBox_penThickness = QSpinBox(self)
        self.__spinBox_penThickness.setMaximum(30)
        self.__spinBox_penThickness.setMinimum(1)
        self.__spinBox_penThickness.setValue(20)  # Default value of painter size
        self.__spinBox_penThickness.setSingleStep(1)  # min change value
        self.__spinBox_penThickness.valueChanged.connect(
            self.on_PenThicknessChange)  # Connect the change value with function(on_PenThicknessChange)
        sub_layout.addWidget(self.__spinBox_penThickness)

        self.__label_penColor = QLabel(self)
        self.__label_penColor.setText("Color")
        self.__label_penColor.setFixedHeight(20)
        sub_layout.addWidget(self.__label_penColor)

        self.__comboBox_penColor = QComboBox(self)
        self.__fillColorList(self.__comboBox_penColor)  # fill the list with colors
        self.__comboBox_penColor.currentIndexChanged.connect(
            self.on_PenColorChange)  # connect the color change with function(on_PenColorChange)
        sub_layout.addWidget(self.__comboBox_penColor)

        main_layout.addLayout(sub_layout)  #add the sublayout to main layout

    def __fillColorList(self, comboBox):

        index_black = 0
        index = 0
        for color in self.__colorList:
            if color == "black":
                index_black = index
            index += 1
            pix = QPixmap(20, 20)
            pix.fill(QColor(color))
            comboBox.addItem(QIcon(pix), None)
            comboBox.setIconSize(QSize(20, 20))
            comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        comboBox.setCurrentIndex(index_black)

    def on_PenColorChange(self):
        color_index = self.__comboBox_penColor.currentIndex()
        color_str = self.__colorList[color_index]
        self.__paintBoard.ChangePenColor(color_str)

    def on_PenThicknessChange(self):
        penThickness = self.__spinBox_penThickness.value()
        self.__paintBoard.ChangePenThickness(penThickness)

    def on_btn_Save_Clicked(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath[0])
        print(savePath[0])

    def on_cbtn_Eraser_clicked(self):
        if self.__cbtn_Eraser.isChecked():
            self.__paintBoard.EraserMode = True  # Enter eraser mode
        else:
            self.__paintBoard.EraserMode = False  # Exit eraser mode


    def on_btn_Recognize_Clicked(self):
        savePath = "test.png"
        image = self.__paintBoard.GetContentAsQImage()
        image.save(savePath)
        print(savePath)
        # Loading img
        img = cv2.imread(savePath, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (28, 28), )
        img = np.array(img)
        img = img/255.0
        x = []
        x.append(img)
        x = np.array(x)
        x = x.reshape((1, 28, 28, 1))
        prediction = self.__model.predict(x)
        y = np.argmax(prediction)
        if(int(y) < 26 ):
            letter = chr(int(y)+65)
        else :
            letter = chr(int(y)+71)
        print("letter is recognized as：" + letter)


    def Quit(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    interface = Interface()
    interface.show()
    exit(app.exec_())

