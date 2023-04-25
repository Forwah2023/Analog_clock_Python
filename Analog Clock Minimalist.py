import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import copy
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRAME_WIDTH=0.7*SCREEN_WIDTH
FRAME_HEIGHT=0.7*SCREEN_WIDTH 

class MainWindow(qtw.QMainWindow):
	def __init__(self):
		"""MainWindow constructor"""
		super().__init__()
		self.resize(qtc.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))
		self.scene = Scene()
		view = qtw.QGraphicsView(self.scene)
		self.setCentralWidget(view)
		self.setWindowTitle('Nice clock')
		self.show()
class Scene(qtw.QGraphicsScene):
	def __init__(self):
		super().__init__()
		clock_center=qtc.QPointF(0.5*FRAME_WIDTH,0.5*FRAME_HEIGHT)
		self.setBackgroundBrush(qtg.QBrush(qtg.QColor('white')))
		self.setSceneRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
		wall_brush =qtg.QBrush(qtg.QColor('white'))
		frame_pen=qtg.QPen(qtg.QColor('black'),16)
		self.setBackgroundBrush(qtg.QBrush(qtg.QColor('grey')))

		clock_frame=self.addEllipse(qtc.QRectF(0,0,FRAME_WIDTH,FRAME_HEIGHT),pen=frame_pen,brush=wall_brush)
		self.digit3=self.addText('3',qtg.QFont('Arial',40))
		self.digit3.setPos(FRAME_WIDTH-70,0.5*FRAME_HEIGHT-50)
		self.digit9=self.addText('9',qtg.QFont('Arial',40))
		self.digit9.setPos(20,0.5*FRAME_HEIGHT-50)
		self.digit6=self.addText('6',qtg.QFont('Arial',40))
		self.digit6.setPos(0.35*SCREEN_WIDTH-25,FRAME_HEIGHT-100)
		self.digit12=self.addText('12',qtg.QFont('Arial',40))
		self.digit12.setPos(0.35*SCREEN_WIDTH-50,15)
		#ticks at 30 degrees interval
		for i in list(range(0,331,30)):
			newtick=self.addLine(0.35*SCREEN_WIDTH,0,0.35*SCREEN_WIDTH,10,frame_pen)
			newtick.setTransformOriginPoint(clock_center)
			newtick.setRotation(i)
			
		
		self.curr_time=qtc.QTime.currentTime()
		
		secondHand_pen=qtg.QPen(qtg.QColor('black'),3)
		secondHand_pen.setCapStyle(qtc.Qt.RoundCap)
		self.secondHand=self.addLine(0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.05*SCREEN_WIDTH,secondHand_pen)
		self.secondHand.setTransformOriginPoint(clock_center)
		self.secondHand.setRotation(self.curr_time.second()/60*360)
		#minute hand
		longHand_pen=qtg.QPen(qtg.QColor('black'),10)
		longHand_pen.setCapStyle(qtc.Qt.RoundCap)
		self.longHand=self.addLine(0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.05*SCREEN_WIDTH,longHand_pen)
		self.longHand.setTransformOriginPoint(clock_center)
		self.longHand.setRotation((self.curr_time.minute()+self.curr_time.second()/60)/60*360)
		#hour hand
		shortHand_pen=qtg.QPen(qtg.QColor('black'),10)
		shortHand_pen.setCapStyle(qtc.Qt.RoundCap)
		self.shortHand=self.addLine(0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.35*SCREEN_WIDTH,0.15*SCREEN_WIDTH,shortHand_pen)
		self.shortHand.setTransformOriginPoint(clock_center)
		self.shortHand.setRotation(((self.curr_time.hour()+self.curr_time.minute()/60)%12)/12*360)
		
		self.timer=qtc.QTimer()
		self.timer.timeout.connect(self.Update_time)
		self.timer.start(1000)
	def Update_time(self):
		self.curr_time=qtc.QTime.currentTime()
		self.secondHand.setRotation(self.secondHand.rotation()+360/60)
		self.longHand.setRotation(self.longHand.rotation()+360/3600)
		self.shortHand.setRotation(self.shortHand.rotation()+360/43200)
			
		
if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	mw = MainWindow()
	sys.exit(app.exec_())