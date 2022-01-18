import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json

class MainMenu():

    def __init__(self):

        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.subjects = list(json.load(fileVals).keys())
        fileVals.close()

        self.app = QApplication(sys.argv)

        self.grid = QGridLayout()
        self.window = QDialog()
        self.window.setLayout(self.grid)

        ## Кнопка старта

        self.startButton = QPushButton(self.window)
        self.startButton.setText("Начать")
        #self.startButton.move(25, 25)
        self.startButton.clicked.connect(self.bootstrap)

        ## Меню

        self.menu = QComboBox()
        for i in self.subjects:
            self.menu.addItem(i)
            
        ## Название

        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setText("GradeMapper")

        self.grid.addWidget(self.startButton, 1, 0, 1, 2)
        self.grid.addWidget(self.menu, 2, 0, 1, 2)
        self.grid.addWidget(self.nameLabel, 0, 0, 1, 2)
        #self.grid.addWidget(self.out, 2, 0, 1, 2)
        
        self.window.setWindowTitle("GradeMapper PyQt")
        self.window.setGeometry(100, 100, 0, 0)
        self.window.show()

    def bootstrap(self):

        self.calc = GradeCalculator(self.menu.currentText())
        self.calc.window.show()
        
class GradeCalculator():

    def __init__(self, subject):

        #self.app = QApplication(sys.argv)

        self.grid = QGridLayout()
        self.window = QDialog()
        self.window.setLayout(self.grid)
        
        self.gradesWeighted = 0
        self.weightsSum = 0
        
        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.types = json.load(fileVals)[subject]
        fileVals.close()

        keys = list(self.types.keys())

        ## Текст ввода-вывода

        self.gradeIn = QLineEdit(self.window)
        self.gradeOut = QLabel(self.window)
        self.gradeOut.setAlignment(Qt.AlignCenter)
        self.gradeOut.setText("Оценка: -")

        ## Кнопки "Загрузить" и "Вычислить"

        self.loadGradeButton = QPushButton(self.window)
        self.clearButton = QPushButton(self.window)

        self.loadGradeButton.clicked.connect(self.loadGrade)
        self.clearButton.clicked.connect(self.clearGrade)

        self.loadGradeButton.setText("Загрузить и вычислить")
        self.clearButton.setText("Очистить")

        ## Меню с видами работ
        
        self.workMenu = QComboBox()
        for i in self.types.keys():
            self.workMenu.addItem(i)

        ## Сетка

        self.grid.addWidget(self.workMenu, 0, 0, 1, 1)
        self.grid.addWidget(self.gradeIn, 1, 0, 1, 1)
        self.grid.addWidget(self.gradeOut, 2, 0, 1, 1)
        self.grid.addWidget(self.loadGradeButton, 1, 1, 1, 1)
        self.grid.addWidget(self.clearButton, 2, 1, 1, 1)

        self.window.setWindowTitle("GradeMapper " + subject)
        self.window.setGeometry(100, 100, 0, 0)
        #self.window.show()

    def loadGrade(self):
        
        try:
            gr = int(self.gradeIn.text())
        except Exception:
            self.gradeOut.setText("Не является числом")
            return -1

        if gr < 1 or gr > 5:
            self.gradeOut.setText("Не является оценкой")
            return -1

        currentWorkWeight = self.types[self.workMenu.currentText()]
                    
        self.weightsSum += currentWorkWeight
        self.gradesWeighted += gr * currentWorkWeight
        
        self.gradeOut.setText("Оценка: " + str(round(self.gradesWeighted / self.weightsSum, 2)))

        #print(self.weightsSum, self.gradesWeighted)

        self.gradeIn.clear()

    def clearGrade(self):
        
        self.gradeIn.clear()
        self.gradeOut.clear()
        
        self.weightsSum = 0
        self.gradesWeighted = 0
        
        self.gradeOut.setText("Оценка: -")

if __name__ == "__main__":
    menu = MainMenu()
    sys.exit(menu.app.exec_())
