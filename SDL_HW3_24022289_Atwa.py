import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget

#This will create the central widget
application = QApplication(sys.argv)
arrwidget = QWidget()

#This will create the 6 by 6 grid 
Layoutforgrid = QGridLayout()
Layoutforgrid.setSpacing(10) 

#This will create a place above the grid for the max sum to be displayed
maxLabel = QLabel()
maxLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
Layoutforgrid.addWidget(maxLabel, 0, 0, 1, 6)

#This will create a 6 by 6 boxes to hold the numbers
arr2D = [[QLabel() for j in range(6)] for i in range(6)]
for q in range(6):
    for r in range(6):
        Layoutforgrid.addWidget(arr2D[q][r], q+1, r)
        arr2D[q][r].setAlignment(Qt.AlignmentFlag.AlignCenter)

#This will take in a file name as a command line arguemnt and use the data inside the file to fill up the grid
if len(sys.argv) != 2:
    sys.exit(1)
filetitle = sys.argv[1]
with open(filetitle) as file:
    arrValues = [[int(num) for num in row.strip().split()] for row in file]
def grid_filler():
    for t in range(6):
        for f in range(6):
            arr2D[t][f].setText(str(arrValues[t][f]))

grid_filler()

#This will create the solve button and place it directly under the grid
ButtonSol = QPushButton("Solve")
Layoutforgrid.addWidget(ButtonSol, 7, 0, 1, 6) 

#This will give the widget a grid layout
arrwidget.setLayout(Layoutforgrid)

# function to calculate the hourglass with the greatest sum and highlight it on the grid.
def greatest_sum_highlighter():
    hourglasssumlist = []
    hourglasssumindex = []
    for i in range(4):
        for j in range(4):
        # calculates the hourglass sum and appends it to a list of the hourglass sums
            hourglasssumlist.append(int(arr2D[i][j].text()) + int(arr2D[i][j+1].text()) + int(arr2D[i][j+2].text()) + int(arr2D[i+1][j+1].text()) + int(arr2D[i+2][j].text()) + int(arr2D[i+2][j+1].text()) + int(arr2D[i+2][j+2].text()))
            hourglasssumindex.append((i,j))
    maxsum = hourglasssumlist[0]
    maxsumindex = hourglasssumindex[0] 
    for h in range(len(hourglasssumlist)):
        if hourglasssumlist[h] > maxsum:
            maxsum = hourglasssumlist[h]
            maxsumindex = hourglasssumindex[h]
    highlighted_elements = []  # This chunk will store the boxes that should be highlighted into a list
    for w in range(maxsumindex[0], maxsumindex[0]+3):
        for z in range(maxsumindex[1], maxsumindex[1]+3):
            if w == maxsumindex[0]:
                highlighted_elements.append(arr2D[w][z])
            elif w == maxsumindex[0]+2:
                highlighted_elements.append(arr2D[w][z])
            elif w == maxsumindex[0]+1 and z == maxsumindex[1]+1:
                highlighted_elements.append(arr2D[w][z])
    for maximum in highlighted_elements:  #This will go through the list and highlight the boxes that were stored in the list
        maximum.setStyleSheet("background-color: yellow")
    maxLabel.setText(f"The max Hourglass Sum is {maxsum}")

#This will connect the button and the function, so when the button is clicked it will run the highlighting function
ButtonSol.clicked.connect(greatest_sum_highlighter)
arrwidget.show()
sys.exit(application.exec())
