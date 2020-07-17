#!/usr/bin/python

import json

add_library('controlP5')
templateImg = 'AccuracyTemplate.png'

drawRange = (30, 570)
drawCenter = 410
xOffsetBuffer = 105

sw = 50  # Threashold for displaying yellow to red
mapColors = ('#00FF00', '#ecca00', '#2f0000')

pathList = [['', 'save'], ['', 'import']]
textFieldList = ['moa', 'distances']

outputMessage = ''
outputMessagePos = (230, 570)


def setup():
	global cp5, templateImg
	size(600, 600)
	background(loadImage(templateImg))
	stroke('#555555')
	strokeWeight(2)

	textSize(12)
	textLeading(12)
	textAlign(LEFT)

	cp5 = ControlP5(this)
	cp5.enableShortcuts()

	cp5.addTextfield('moa').setPosition(20, 500).setSize(60, 25)

	cp5.addTextfield('distances').setPosition(100, 500).setSize(120, 25)

	(cp5.addButton('save image').setPosition(15, 550).setSize(100, 35)
		.onClick(lambda f: save('frame')))

	(cp5.addButton('import data').setPosition(120, 550).setSize(100, 35)
		.onClick(lambda f: save('import')))


# If tab pressed, set focus to opposite text field
def keyPressed():
	if keyCode == 9: # Tab
		for field in textFieldList:
			fieldObj = cp5.get(field)
			fieldObj.setFocus(not fieldObj.isFocus())


def draw(*args):
	global outputMessage
	background(loadImage(templateImg))

	text(str(outputMessage), *outputMessagePos)

	if args:
		moa = args[0]
		distances = args[1]
	else:
		moa = cp5.getController('moa').getText()
		distances = cp5.getController('distances').getText()

	# MOA in game, converted to centimeters
	try:
		accuracy = float(moa) * 2.54
		outputMessage = ''
	except ValueError:
		if moa != '':
			text('Bad MOA input', *outputMessagePos)
		return

	# List of distances to display accuracy for, defaults if bad input
	distanceList = []
	for i in distances.split(','):
		try:
			distanceList += [float(i)/100]
			outputMessage = ''
		except ValueError:
			distanceList = [0.5, 1, 2, 3, 4, 5]
			break

	yOffsetStep = (drawRange[1] - drawRange[0]) / (len(distanceList) + 1)

	# For each distance (reversed for readability)
	for j in range(len(distanceList), 0, -1):
		diameter = accuracy * distanceList[j - 1] * 2

		yOffset = yOffsetStep * j + drawRange[0]

		# Get color in spectrum between green and yellow
		# if diameter less than threashold, else yellow and red
		# map diameter to between 0 and 1 as lerpColor takes float input

		big = diameter > sw
		fill(lerpColor(mapColors[big], mapColors[big + 1],
			map(diameter, big * sw, big * sw + sw, 0, 1)))
		circle(drawCenter, yOffset, diameter * (464.0 / 170.0))

	# Although not ideal, the second loop will overlay the text
	# to avoid the following circle overwriting the previous text

	for k in range(len(distanceList), 0, -1):
		diameter = accuracy * distanceList[k - 1] * 2

		yOffset = yOffsetStep * k + drawRange[0]
		xOffset = drawCenter

		xOffsetModifier = diameter / 2 * (464.0 / 170.0) + 10

		if xOffsetModifier < xOffsetBuffer:
			xOffset += xOffsetModifier
		else:
			xOffset += xOffsetBuffer

		accuracyText = '{} CM\n@ {}m'.format(
			str(diameter)[:6], distanceList[k - 1] * 100)

		fill('#FFFFFF')
		text(accuracyText, xOffset, yOffset)

	text(str(outputMessage), *outputMessagePos)


# This function is awful. selectInput is threaded so I have to wait
# until the user finishes selecting before the program can continue

def save(mode):
	global pathList, outputMessage

	if mode == 'import':
		selectInput('Import data', 'globalImportPath')

		outputMessage = waitForPath(1)
		if outputMessage != '':
			return

	selectFolder('Select output folder', 'globalSavePath')

	outputMessage = waitForPath(0)
	if outputMessage != '':
		return

	if mode == 'frame':
		saveCurrentFrame(
			cp5.getController('moa').getText(),
			cp5.getController('distances').getText(),
			mode
		)
	elif mode == 'import':
		importData()

	pathList = [['', 'save'], ['', 'import']]


def waitForPath(index):
	global pathList
	# While user hasn't done anything
	while True:
		# If user has done something
		if pathList[index][0] != '':
			break
	# selectInput returns None if cancelled
	if pathList[index][0] == None:
		pathList = [['', 'save'], ['', 'import']]
		return 'Bad {} path'.format(pathList[index][1])

	return ''


# Hide UI, draw then save image, show ui
def saveCurrentFrame(moa, distances, mode):
	global outputMessage

	cp5.hide()
	oldOutputMessage = outputMessage
	outputMessage = ''

	if moa == '':
		oldOutputMessage = 'No MOA entered'
		return

	if distances == '':
		distances = '50, 100, 200, 300, 400, 500'

	draw(moa, distances)

	textSize(25)
	textAlign(CENTER)
	text('{} MOA'.format(moa), drawCenter, 70)

	saveName = '{}/{} MOA @ {}.png'.format(
		pathList[0][0], moa, distances)

	saveFrame(saveName)

	textSize(12)
	textAlign(LEFT)

	outputMessage = oldOutputMessage
	cp5.show()


def importData():
	global outputMessage

	# Load file and display error if there is one
	with open(str(pathList[1][0]), 'r') as file:
		try:
			data = json.load(file)
		except ValueError, e:
			outputMessage = e
			return

	outputMessage = ''

	for i in data:
		# If item is list, convert all values following the first into a string
		# separated by commas. Else send default distance list
		if type(i) == list:
			moa = i[0]
			distances = ', '.join([str(distance) for distance in i[1:]])
		else:
			moa = i
			distances = '50, 100, 200, 300, 400, 500'

		saveCurrentFrame(moa, distances, 'import')

		outputMessage = 'Finished rendering'


# Set global variables to given variables. Awful
def globalSavePath(newSavePath):
	global pathList
	pathList[0][0] = newSavePath

def globalImportPath(newImportPath):
	global pathList
	pathList[1][0] = newImportPath
