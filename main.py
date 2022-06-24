from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np
from functools import partial
import itertools
import sys
import os
import random
import cv2
import csv
from datetime import datetime
class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.errorData = []
		self.mainframe = QtWidgets.QFrame()
		self.setCentralWidget(self.mainframe)
		self.grid = QtWidgets.QGridLayout()
		self.mainframe.setLayout(self.grid)
		x=Content().frame(self)
		for i in x:
			self.grid.addWidget(i[0],i[1],i[2])
		self.resize(800,550)				
		self.show()
	def Question(self,data):
		self.correctAnswer = QtWidgets.QLabel()
		self.userScore = 0
		self.num = 1
		self.mistakes = 0
		self.total = len(data)
		self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
		self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
		self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
		random.shuffle(data)
		self.data = (x for x in data)
		type_,question,answer =next(self.data)
		self.q = '#'.join([type_,question,answer])
		
		if type_.lower() == "text":
			self.textQuestion(type_,question,answer)
		elif type_.lower() == "pictext":
			print(question)
			self.picText(type_,question,answer)
		elif type_.lower() == "pic":
			print(question)
			self.picQuestion(type_,question,answer)
	def textQuestion(self,type_,question,answer):
		self.resize(800,520)	
		self.clear()
		self.correctAnswer.clear()
		self.next=False
		label=QtWidgets.QLabel(question)
		label.setWordWrap(0)
		label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		label.setFont(QtGui.QFont('Ubuntu',12,QtGui.QFont.Bold))
		userInput = QtWidgets.QLineEdit()
		userInput.setFocus(1)
		userInput.returnPressed.connect(
		lambda:self.checkAnswer(question,answer,userInput.text()))
		button = QtWidgets.QPushButton("Check answer",
		clicked=lambda:self.checkAnswer(question,answer,userInput.text()))
		self.grid.addWidget(self.score,0,0)
		self.grid.addWidget(self.correct,0,1)
		self.grid.addWidget(self.incorrect,0,2)
		self.grid.addWidget(label,1,0)
		self.grid.addWidget(userInput,2,0,1,2)
		
		self.grid.addWidget(button,3,3)
			
	def checkAnswer(self,question,answer,userInput):
		self.correctAnswer = QtWidgets.QLabel()
		self.grid.addWidget(self.correctAnswer,3,0,1,2)
		if all(i.lower() in userInput.lower() for i in answer.split(',')):
			self.userScore+=1
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
			self.nextQuestion()
		else:
			self.mistakes+=1
			self.errorData.append(self.q)
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
			self.correctAnswer.setText(f"Answer: {answer}")
			
			nextButton=QtWidgets.QPushButton("Continue")
			nextButton.clicked.connect(self.nextQuestion)
			nextButton.setAutoDefault(True)
			nextButton.setFocus(1)
			self.grid.addWidget(nextButton,3,3)
	def checkAnswerPicText(self,question,answer,userInput):
		self.correctAnswer = QtWidgets.QLabel()
		self.grid.addWidget(self.correctAnswer,4,0,1,2)
		if all(i.lower() in userInput.lower() for i in answer.split(',')):
			self.userScore+=1
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
			self.nextQuestion()
		else:
			self.mistakes+=1
			self.errorData.append(self.q)
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
			self.correctAnswer.setText(f"Answer: {answer}")
			nextButton=QtWidgets.QPushButton("Continue")
			nextButton.setAutoDefault(True)
			nextButton.setFocus(True)
			nextButton.clicked.connect(self.nextQuestion)
			self.grid.addWidget(nextButton,4,3)
	def clear(self):
		while self.grid.count():
			self.grid.takeAt(0).widget().deleteLater()		
	def nextQuestion(self):
		try:
			type_,question,answer =next(self.data)
			self.q = '#'.join([type_,question,answer])
			if type_.lower() == "text":
				self.textQuestion(type_,question,answer)
			elif type_.lower() == "pictext":
				print(question)
				self.picText(type_,question,answer)
			elif type_.lower() == "pic":
				print(question)
				self.picQuestion(type_,question,answer)
		except StopIteration:
			self.clear()
			percent=round(int(self.correct.text().split(' ')[0])/(int(self.correct.text().split(' ')[0])+int(self.incorrect.text().split(' ')[0]))*100,2)
			
			self.score = QtWidgets.QLabel(f'{self.num-1} of {self.total}')
			label = QtWidgets.QLabel(f'{self.correct.text()} {self.incorrect.text()} and scored {percent}')
			self.grid.addWidget(self.score,0,0)
			self.grid.addWidget(self.correct,0,1)
			self.grid.addWidget(self.incorrect,0,2)
			self.grid.addWidget(label,1,0)
			
			log = "Files/stats.csv"
			if not os.path.exists(log) and self.filename!='Errors':
				os.mknod(log)
				
				with open(log,mode='a+') as f:
					reader = csv.DictReader(f,delimiter="#",quotechar="'")
					for row in reader:
						if row['file'] == self.filename:
							print(row)
					writer = csv.DictWriter(f,
					["date","file","correct","incorrect","percent"],
					delimiter="#",quotechar="'")
					writer.writeheader()
					writer.writerow({
					"date":datetime.now().strftime('%d/%m/%y %H:%M'),
					"file":self.filename,
					"correct":self.correct.text().split(' ')[0],
					"incorrect":self.incorrect.text().split(' ')[0],
					"percent":percent
					})
			elif self.filename!="Errors":
				with open(log,mode='a+') as f:
					reader = csv.DictReader(f,delimiter="#",quotechar="'")
					for row in reader:
						print(self.filename)
						if row['file'] == self.filename:
							print(row)
					writer = csv.DictWriter(f,
					["date","file","correct","incorrect","percent"],
					delimiter="#",quotechar="'")
					
					writer.writerow({
					"date":datetime.now().strftime('%d/%m/%y %H:%M'),
					"file":self.filename,
					"correct":self.correct.text().split(' ')[0],
					"incorrect":self.incorrect.text().split(' ')[0],
					"percent":percent
					})
			errorfile = 'Files/Errors'
			if not os.path.exists(errorfile):
				os.mknod(errorfile)
			
			if len(errorfile) != 0 and self.filename != 'Errors':
				errors = [x.rstrip() for x in open(errorfile,'r')]
				errors = errors+self.errorData
				f=open(errorfile,'w')
				for q in set(errors):
					f.write(f'{q}\n')
			elif len(errorfile) != 0 and self.filename == 'Errors':
				errors = self.errorData
				f=open(errorfile,'w')
				for q in set(errors):
					f.write(f'{q}\n')
	def picText(self,type_,question,answer):
		self.resize(800,550)	
		self.clear()
		self.correctAnswer.clear()
		self.next=False
		question,pic = question.split('|')
		
		label=QtWidgets.QLabel(question)
		#label.setWordWrap(True)
		picture = QtWidgets.QLabel()
		picture.setPixmap(QtGui.QPixmap.fromImage(self.image(pic)))
		
		label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
		#label.setFont(QtGui.QFont('Ubuntu',20,QtGui.QFont.Bold))
		userInput = QtWidgets.QLineEdit()
		
		userInput.setFocus(1)
		userInput.returnPressed.connect(
		lambda:self.checkAnswerPicText(question,answer,userInput.text()))
		button = QtWidgets.QPushButton("Check answer",
		clicked=lambda:self.checkAnswerPicText(question,answer,userInput.text()))
		button.setFocus(True)
		showButton = QtWidgets.QPushButton("Open Pic")
		showButton.clicked.connect(lambda:os.system(f'shotwell {pic}'))
		self.grid.addWidget(self.score,0,0)
		self.grid.addWidget(self.correct,0,1)
		self.grid.addWidget(self.incorrect,0,2)
		self.grid.addWidget(showButton,0,3)
		self.grid.addWidget(label,1,0)
		self.grid.addWidget(picture,2,0)
		self.grid.addWidget(userInput,3,0,1,2)
		self.grid.addWidget(self.correctAnswer,4,0,1,2)
		self.grid.addWidget(button,4,3)
	def picQuestion(self,type_,question,answer):
		#mark files with * at end to specify to get pictures only from that folder
		self.resize(800,550)	
		pics=[]
		if answer.endswith("*g"):
			answer = answer.replace("*","")
			dir = answer.rsplit("/",1)[0]
			Files=Content().getPictures(dir)
			
		else:
			Files=Content().getPictures()
		#pics = random.choices(Files,k=8)
		pics = []
		while True:
			pic=random.choice(Files)
			if all(not x.rsplit('/',1)[1].endswith(pic.rsplit('/',1)[1])
			 for x in pics) and pic != answer:
				pics.append(pic)
			if len(pics) == 8:
				break;
		pics.append(answer)
		random.shuffle(pics)
		self.clear()
		self.correctAnswer.clear()
		self.next=False
		label=QtWidgets.QLabel(question)
		#label.setWordWrap(True)
		label.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)		
		#label.setFont(QtGui.QFont('Ubuntu',20,QtGui.QFont.Bold))
		button = QtWidgets.QPushButton("Check answer")
		label.setFocus(1)
		#,
		#clicked=lambda:self.checkAnswerPicText(question,answer,userInput.text()))
		
		self.grid.addWidget(self.score,0,0)
		self.grid.addWidget(self.correct,0,1)
		self.grid.addWidget(self.incorrect,0,2)
		self.grid.addWidget(label,1,0)
		
		
		col=2
		row=0
		frame = QtWidgets.QFrame()
		grid = QtWidgets.QGridLayout()
		frame.setLayout(grid)
		for i in range(0,9):
			if pics[i] == answer:
				pic=ClickablePic()
				pic.setFocus(1)
				pic.setPixmap(QtGui.QPixmap.fromImage(self.image(pics[i],100,100)))
				self.border = FrameBorder(pics[i])
				pic.clicked.connect(partial(self.clickme,answer,
				pics[i],self.border))
				grid.addWidget(self.border.setPic(pic),col,row)
			else:
				pic=ClickablePic()
				pic.setFocus(1)
				pic.setPixmap(QtGui.QPixmap.fromImage(
				self.image(pics[i],100,100)))
				border = FrameBorder(pics[i])
				pic.clicked.connect(partial(self.clickme,answer,pics[i],border))
				grid.addWidget(border.setPic(pic),col,row)
			
			if i in [2,5,8]:
				col+=1
				row=0	
			else:
				row+=1
				
		self.grid.addWidget(frame,2,0,3,3)
		self.grid.addWidget(button,5,3)
	def clickme(self,answer,name,border):
		self.correctAnswer = QtWidgets.QLabel()
		self.grid.addWidget(self.correctAnswer,4,0,1,2)
		if name == answer:
			border.stylesheet('green')
			self.userScore+=1
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')
			self.nextQuestion()
		else:
			self.border.stylesheet('green')
			border.stylesheet('red')
			self.mistakes+=1
			self.errorData.append(self.q)
			self.num+=1
			self.score = QtWidgets.QLabel(f'{self.num} of {self.total}')
			self.correct = QtWidgets.QLabel(f'{self.userScore} Correct')
			self.incorrect = QtWidgets.QLabel(f'{self.mistakes} Incorrect')

			nextButton=QtWidgets.QPushButton("Continue")
			nextButton.setAutoDefault(True)
			nextButton.setFocus(1)
			nextButton.clicked.connect(self.nextQuestion)
			self.grid.addWidget(nextButton,5,3)
	def image(self,pic,x=300,y=300):
		if pic.startswith('question'):
			print(pic)
			
		pic=cv2.cvtColor(cv2.resize(cv2.imread(pic),(x,y)),cv2.COLOR_BGR2RGB)
		w,h,c=pic.shape
		img=QtGui.QImage(pic.data,w,h,w*c,QtGui.QImage.Format_RGB888)
		return(img)
class FrameBorder():
	def __init__(self,name):
		self.name = name
		self.frame = QtWidgets.QFrame()
	def setPic(self,pic):
		setWidget=QtWidgets.QHBoxLayout()
		self.frame.setLayout(setWidget)
		setWidget.addWidget(pic)
		self.frame.setStyleSheet('border:2px solid black;background-color:black')
		return(self.frame)
	def stylesheet(self,color):
		self.frame.setStyleSheet(f'border:2px solid {color};background-color:{color}')
		
class ClickablePic(QtWidgets.QLabel):
	clicked = QtCore.pyqtSignal()
	def mousePressEvent(self,event):
		if event.button() == QtCore.Qt.LeftButton:
			self.clicked.emit()
		else:
			super().mousePressEvent(event)
class Content:
	@staticmethod
	def frame(parent):
		Content.create_random([x for x in os.listdir('Files') if not os.path.isdir(f'Files/{x}') 
		and not any(x.endswith(i) for i in ['.png','.jpg','.jpeg','.swp','.csv','zip'])])
		
		files =[x for x in os.listdir('Files') if not os.path.isdir(f'Files/{x}') 
		and not any(x.endswith(i) for i in ['.png','.jpg','.jpeg','.swp','.csv','zip'])]
		data = []
		row=0
		col=0
		files = sorted(files)
		for n,i in enumerate(files):
			n=n+1
			button=QtWidgets.QPushButton(i,clicked=partial(Content().getData,i,parent))
			button.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
			data.append([button,row,col])
			if n%5==0 and n >3:
				row+=1
				col=-1	
			elif n < 3:
				row=0
			col+=1	
		return(data)
	@staticmethod
	def create_random(files):
		data = [[x for x in open(f'Files/{data}')] for data in files]
		data=list(itertools.chain.from_iterable(data))
		if os.path.exists('Files/Random'):
			os.remove('Files/Random')
		os.mknod('Files/Random')
		f = open('Files/Random','a')
		for x in range(20):
			line = random.choice(data)
			data.remove(line)
			f.write(line)
		f.close()
		
	@staticmethod	
	def getData(text,parent):
		parent.filename = text
		data = [x.rstrip().split("#") for x in open(f'Files/{text}')]
		parent.Question(data)
		
	@staticmethod
	def getPictures(dir='Files'):
		files=[]
		for r,d,f in os.walk(dir):
			for file in f:
				if any(file.endswith(i) for i in ['.png','.jpg','.jpeg']):
					files.append(os.path.join(r,file))
		return(files)
					
app = QtWidgets.QApplication(sys.argv)
ui = Main()
sys.exit(app.exec_())
