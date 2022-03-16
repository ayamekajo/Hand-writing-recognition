
from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen, \
    QColor, QSize
from PyQt5.QtCore import Qt


class PaintBoard(QWidget):

    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData()
        self.__InitView()

    def __InitData(self):

        self.__size = QSize(480, 460)

        # Set a paintboard with size
        self.__board = QPixmap(self.__size)
        self.__board.fill(Qt.white)  # fill with white

        self.__IsEmpty = True  # Default as empty
        self.EraserMode = False  # Default as not erasermode

        self.__lastPos = QPoint(0, 0)  # last position of mouse
        self.__currentPos = QPoint(0, 0)  # current position of mouse

        self.__painter = QPainter()

        self.__thickness = 20  # Default size as 20
        self.__penColor = QColor("black")  # Default color as black
        self.__colorList = QColor.colorNames()  # get color list

    def __InitView(self):
        # set size
        self.setFixedSize(self.__size)

    def Clear(self):
        # Clear
        self.__board.fill(Qt.white)
        self.update()
        self.__IsEmpty = True

    def ChangePenColor(self, color="black"):
        # Change pencolor
        self.__penColor = QColor(color)

    def ChangePenThickness(self, thickness=10):
        # change pen size
        self.__thickness = thickness

    def IsEmpty(self):
        # return if the paintboard is empty
        return self.__IsEmpty

    def GetContentAsQImage(self):
        # 获取画板内容（返回QImage）
        image = self.__board.toImage()
        return image

    def paintEvent(self, paintEvent):
        # 绘图事件
        # 绘图时必须使用QPainter的实例，此处为__painter
        # 绘图在begin()函数与end()函数间进行
        # begin(param)的参数要指定绘图设备，即把图画在哪里
        # drawPixmap用于绘制QPixmap类型的对象
        self.__painter.begin(self)
        # 0,0为绘图的左上角起点的坐标，__board即要绘制的图
        self.__painter.drawPixmap(0, 0, self.__board)
        self.__painter.end()

    def mousePressEvent(self, mouseEvent):
        # save current position as last postion when click mouse
        self.__currentPos = mouseEvent.pos()
        self.__lastPos = self.__currentPos

    def mouseMoveEvent(self, mouseEvent):
        # update position and paint line when mouse removing
        self.__currentPos = mouseEvent.pos()
        self.__painter.begin(self.__board)

        if self.EraserMode == False:
            # not ereasermode
            self.__painter.setPen(QPen(self.__penColor, self.__thickness))  # 设置画笔颜色，粗细
        else:
            # set pen to white when is ereasermode
            self.__painter.setPen(QPen(Qt.white, 10))


        self.__painter.drawLine(self.__lastPos, self.__currentPos)
        self.__painter.end()
        self.__lastPos = self.__currentPos

        self.update()

    def mouseReleaseEvent(self, mouseEvent):
        self.__IsEmpty = False  # board is not empty after paint

