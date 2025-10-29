try:
	from PySide6 import QtCore, QtGui, QtWidgets
	from shiboken6 import wrapInstance
except:
	from PySide2 import QtCore, QtGui, QtWidgets
	from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import random

IMAGE_DIR = 'C:/Users/Acer/OneDrive/เอกสาร/maya/2024/scripts/fp/picture'

class SlotmacDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)


		self.setWindowTitle('🍒⭐Slot machine🍉🔔')
		self.resize(500,300)

		self.mainLayout = QtWidgets.QVBoxLayout(self)
		self.setStyleSheet(
			'''
				font-family: Times New Roman;
				background-color: #b33737;
			'''
		)
		self.headerLayout = QtWidgets.QHBoxLayout()
		self.titleLabel = QtWidgets.QLabel("⭐🍒🔔🍉🍋SLOT MACHINE")
		self.titleLabel.setStyleSheet(
			'''
				font-size: 40px;
				font-family: Times New Roman;
				font-weight: bold;
				background-color: black;
				color: white;
				padding: 10px;
			'''
		)
		self.headerLayout.addWidget(self.titleLabel, alignment=QtCore.Qt.AlignCenter)
		self.mainLayout.addLayout(self.headerLayout)


		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/header.png')
		scaledPixmap = self.imagePixmap.scaled(
			QtCore.QSize(500,300),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation
		)

		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.mainLayout.addWidget(self.imageLabel)
		self.mainLayout.addStretch()

		self.slotRow = QtWidgets.QLabel("🍒 | 🍋 | 🔔")
		self.slotRow.setAlignment(QtCore.Qt.AlignCenter)
		self.slotRow.setStyleSheet("font-size: 50px; color: white;")
		self.mainLayout.addWidget(self.slotRow)

		self.resultLabel = QtWidgets.QLabel("")
		self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.resultLabel.setStyleSheet(
			'''
				font-size: 20px;
				color: yellow;
			'''

		)

		self.imageLabel = QtWidgets.QLabel()
		self.imagePixmap = QtGui.QPixmap(f'{IMAGE_DIR}/header.png')
		scaledPixmap = self.imagePixmap.scaled(
			QtCore.QSize(500,300),
			QtCore.Qt.KeepAspectRatio,
			QtCore.Qt.SmoothTransformation
		)

		self.imageLabel.setPixmap(scaledPixmap)
		self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)

		self.mainLayout.addWidget(self.imageLabel)

		self.mainLayout.addWidget(self.resultLabel)

		self.balance = 1000
		self.balanceLabel = QtWidgets.QLabel(f"Balance: ${self.balance}")
		self.balanceLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.balanceLabel.setStyleSheet(
			'''
				font-size: 20px;
				color: white;
			'''
		)
		self.mainLayout.addWidget(self.balanceLabel)

		self.bet_amount = 10  
		self.inputLayout = QtWidgets.QHBoxLayout()

		self.betLabel = QtWidgets.QLabel('Bet Amount:')
		self.betLabel.setStyleSheet("color: white; font-size: 18px;")
		self.inputLayout.addWidget(self.betLabel)

		self.betInput = QtWidgets.QLineEdit(str(self.bet_amount))
		self.betInput.setFixedWidth(100)
		self.betInput.setStyleSheet(
			'''
				background-color: white;
				color: black;
				border-radius: 8px;
				font-weight: bold;
				font-family: Times New Roman;
			'''
		)
		self.inputLayout.addWidget(self.betInput)
 
		self.decreaseButton = QtWidgets.QPushButton("-")
		self.decreaseButton.setFixedWidth(40)
		self.decreaseButton.clicked.connect(self.decrease_bet)
		self.inputLayout.addWidget(self.decreaseButton)

		self.increaseButton = QtWidgets.QPushButton("+")
		self.increaseButton.setFixedWidth(40)
		self.increaseButton.clicked.connect(self.increase_bet)
		self.inputLayout.addWidget(self.increaseButton)

		self.mainLayout.addLayout(self.inputLayout)

		self.buttonLayout = QtWidgets.QHBoxLayout()
		self.spinButton = QtWidgets.QPushButton("Spin!")
		self.spinButton.setStyleSheet(
			'''
				QPushButton {
					background-color: black;
					border-radius: 12px;
					font-size: 25px;
					font-weight: bold;
					padding: 12px;
					color: white;
				}
				QPushButton:hover {
					background-color: yellow;
					color: red;
				}
				QPushButton:pressed {
					background-color: red;
					color: yellow;
				}
			'''
		)
		self.spinButton.clicked.connect(self.spin)
		self.buttonLayout.addWidget(self.spinButton)

		self.resetButton = QtWidgets.QPushButton("Reset Balance")
		self.resetButton.setStyleSheet(
			'''
				QPushButton {
					background-color: black;
					border-radius: 12px;
					font-size: 25px;
					font-weight: bold;
					padding: 12px;
					color: white;
				}
				QPushButton:hover {
					background-color: yellow;
					color: red;
				}
				QPushButton:pressed {
					background-color: red;
					color: yellow;
				}
			'''
		)
		self.resetButton.clicked.connect(self.reset_balance)
		self.buttonLayout.addWidget(self.resetButton)
		self.mainLayout.addLayout(self.buttonLayout)

		
	def increase_bet(self):
		self.bet_amount += 10
		self.betInput.setText(str(self.bet_amount))

	def decrease_bet(self):
		if self.bet_amount > 10:
			self.bet_amount -= 10
			self.betInput.setText(str(self.bet_amount))

	def spin(self):
		symbols = ['🍒', '🍉', '🍋', '🔔', '⭐','🪙']


		bet_text = self.betInput.text()
		if not bet_text.isdigit():
			self.resultLabel.setText("Enter a valid bet amount.")
			return
		bet = int(bet_text)
		if bet <= 0:
			self.resultLabel.setText("Bet must be greater than 0.")
			return
		if bet > self.balance:
			self.resultLabel.setText("Insufficient balance.")
			return

		self.balance -= bet

		row = [random.choice(symbols) for _ in range(3)]
		self.slotRow.setText(" | ".join(row))

		payout = self.get_payout(row, bet)
		if payout:
			self.balance += payout
			self.resultLabel.setText(f"You won ${payout}!")
		else:
			self.resultLabel.setText("No match, try again!")

		self.balanceLabel.setText(f"Balance: ${self.balance}")
		if self.balance <= 0:
				self.resultLabel.setText("You ran out of money! Press Reset to play again.")

	def reset_balance(self):
		self.balance = 1000
		self.balanceLabel.setText(f"Balance: ${self.balance}")
		self.resultLabel.setText("Balance reset. Ready to play!")

	def get_payout(self, row, bet):
		if row[0] == row[1] == row[2]:
			payouts = {
				'🍒': 3,
				'🍉': 4,
				'🍋': 5,
				'🔔': 10,
				'⭐': 20,
				'🪙': 50
			}
			return bet * payouts.get(row[0], 0)
		return 0

def run():
	global ui
	try:
		ui.close()
	except:
		pass
	ptr = wrapInstance(int(omui.MQtUtil.mainWindow()),QtWidgets.QWidget)
	ui = SlotmacDialog(parent=ptr)
	ui.show()