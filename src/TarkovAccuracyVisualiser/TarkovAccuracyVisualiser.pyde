#!/usr/bin/python

import json

add_library('controlP5')
templateImg = 'AccuracyTemplate.png'
imageScale = (464.0/170.0)

mapColors = ('#00FF00', '#ecca00', '#2f0000')

pathList = [['', 'save'], ['', 'import']]
textFieldList = ['tarkov moa', 'distances']

outputMessage = ''
outputMessagePos = (20, 495)

zoomLevel = 1.0
imageSize = 600
backgroundColor = '#0b0b0b'

xOffsetBuffer = 105


def setup():
	global basicControls, templateImg
	templateImg = loadImage(templateImg)
	size(imageSize, imageSize)

	background(backgroundColor)
	image(templateImg, 0, 0)

	stroke('#555555')
	strokeWeight(2)

	textSize(12)
	textLeading(12)
	textAlign(CENTER)

	basicControls = ControlP5(this)
	basicControls.enableShortcuts()

	(basicControls.addTextfield('tarkov moa')
		.setPosition(20, 500)
		.setSize(50, 25)
	)

	(basicControls.addTextfield('distances')
		.setPosition(80, 500)
		.setSize(100, 25)
	)

	(basicControls.addButton('save image')
		.setPosition(20, 550)
		.setSize(60, 35)
		.onClick(lambda f: save('frame'))
	)

	(basicControls.addButton('import data')
		.setPosition(85, 550)
		.setSize(60, 35)
		.onClick(lambda f: save('import'))
	)

	(basicControls.addButton('reset zoom')
		.setPosition(150, 550)
		.setSize(60, 35)
		.onClick(lambda f: resetZoom())
	)

	(basicControls.addToggle('toggle inches')
		.setPosition(220, 550)
		.setSize(20, 20)
	)


def draw(*args):
	global outputMessage, zoomLevel, drawRange
	imageSizeScaled = imageSize * zoomLevel
	drawRange = imageSizeScaled * 0.9

	background(backgroundColor)

	if args:
		moa = args[0]
		distances = args[1]
	else:
		moa = basicControls.getController('tarkov moa').getText()
		distances = basicControls.getController('distances').getText()

	# MOA in game, converted to unit
	try:
		accuracy = float(moa) * 2.54
		outputMessage = ''
	except ValueError:
		if moa != '':
			outputMessage = 'Bad MOA input'

		image(
			templateImg,
			(imageSize - imageSizeScaled) / 2, 
			(imageSize - imageSizeScaled) / 2,
			imageSizeScaled,
			imageSizeScaled
		)

		drawOutputMessage()
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

	yOffsetStep = drawRange / (len(distanceList) + 1)
	xOffsetStart = (imageSize/2) + (imageSizeScaled/5)

	getYOffset = lambda count: (imageSize - drawRange) / 2 + (yOffsetStep * count)
	getDiameter = lambda count: accuracy * distanceList[count - 1] * 2 * zoomLevel

	diameterSum = sum(distanceList) * accuracy * 2 * zoomLevel

	sortedDistances = sorted(distanceList, reverse=True)


	offset = (drawRange - diameterSum) / (len(distanceList) + 1)

	print("Offset", offset)

	something = (imageSize - drawRange) / 2
	print("Sum", diameterSum)
	print("Something", something)
	#somethingList = [None] * (len(distanceList)-1)
	somethingList = []
	for x in range(0, len(distanceList)):
		diameter = getDiameter(x)
		something += diameter + (offset/distanceList[x])
		print("Distance", diameter/2)
		somethingList += [something - (diameter/2)]

	print("List", somethingList)

	# For each distance in order of largest to smallest
	for j in sortedDistances:
		index = distanceList.index(j)+1

		sw = 50 * zoomLevel	# Threashold for displaying yellow to red

		diameter = getDiameter(index)
		yOffset = getYOffset(index)

		yOffset = somethingList[distanceList.index(j)]

		# Get color in spectrum between green and yellow
		# if diameter less than threashold, else yellow and red
		# map diameter to between 0 and 1 as lerpColor takes float input

		big = diameter > sw
		fill(lerpColor(mapColors[big], mapColors[big + 1],
			map(diameter, big * sw, big * sw + sw, 0, 1)))
		circle(xOffsetStart, yOffset - (diameter/2), diameter * imageScale)

	image(
		templateImg,
		(imageSize - imageSizeScaled) / 2, 
		(imageSize - imageSizeScaled) / 2,
		imageSizeScaled,
		imageSizeScaled
	)

	# Although not ideal, the second loop will overlay the text
	# to avoid the circle overwriting the text
	for k in range(len(distanceList), 0, -1):
		diameter = getDiameter(k)
		yOffset = getYOffset(k)

		xOffsetModifier = diameter * 1.5 + 40
		if xOffsetStart + xOffsetModifier > imageSize * 0.95:
			xOffsetModifier = -xOffsetModifier
		xOffset = xOffsetStart + xOffsetModifier

		if basicControls.getController('toggle inches').getValue():
			accuracyTextOutput = (
				str(diameter/2.54/zoomLevel)[:6], 'IN', distanceList[k-1] * 100)
		else:
			accuracyTextOutput = (
				str(diameter/zoomLevel)[:6], 'CM', distanceList[k-1] * 100)

		accuracyText = '{} {}\n@ {}m'.format(*accuracyTextOutput)

		fill('#FFFFFF')
		text(accuracyText, xOffset, yOffset)

	drawOutputMessage()


def drawOutputMessage():
	global outputMessage, outputMessagePos

	textAlign(LEFT)
	text(str(outputMessage), *outputMessagePos)
	textAlign(CENTER)


# If tab pressed, set focus to opposite text field

def keyPressed():
	if keyCode == 9: # Tab
		for field in textFieldList:
			fieldObj = basicControls.get(field)
			fieldObj.setFocus(not fieldObj.isFocus())


def mouseWheel(event):
	global zoomLevel
	zoomRange = (0.3, 3)
	e = event.getCount()
	modifier = zoomLevel + float(e)/20

	if 0.3 <= modifier <= 3:
		zoomLevel = modifier


def resetZoom():
	global zoomLevel
	zoomLevel = 1


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
			basicControls.getController('tarkov moa').getText(),
			basicControls.getController('distances').getText(),
			mode
		)
	elif mode == 'import':
		importData()

	pathList = [['', 'save'], ['', 'import']]


# Hold program until user has selected path

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

	basicControls.hide()
	oldOutputMessage = outputMessage
	outputMessage = ''

	if moa == '':
		oldOutputMessage = 'No MOA entered'
		return
	if distances == '':
		distances = '50, 100, 200, 300, 400, 500'

	scalePosition = lambda positionBuffer: (
		(imageSize - drawRange) / 2 + (positionBuffer * zoomLevel))

	moaTextPosition = [140, 530]

	if zoomLevel < 1:
		moaTextPosition[1] = scalePosition(moaTextPosition[1])
	if zoomLevel < 1.5:
		moaTextPosition[0] = scalePosition(moaTextPosition[0])

	draw(moa, distances)

	textSize(25)
	text('{} MOA'.format(moa), moaTextPosition[0], moaTextPosition[1])
	textSize(12)
	textLeading(12)

	saveFrame('{}/{} MOA @ {}.png'.format(pathList[0][0], moa, distances))

	outputMessage = oldOutputMessage
	basicControls.show()


# Load and process json file, render each item in json

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