from PIL import Image, ImageChops
import sys

def generateNewImage(imprintImage, tintList, rows, cols ,bW, bH, w, h):
    master = Image.new('RGB',(w,h))
    for y in range(rows):
        for x in range(cols):
            toPaste = tint_image(imprintImage, tintList[y*cols+x])
            offset = (x*bW, y*bH)
            master.paste(toPaste, offset)
    master.save('out.png')

def tint_image(image, tint_color):
    return ImageChops.multiply(image, Image.new('RGB', image.size, tint_color))


def generateTintBlockList(templateImage, rows, cols, bW, bH):
    tintList = []
    templatePX = templateImage.load()
    for row in range(rows):
        for col in range(cols):
            tintList.append(getAveragePXOfBlock(templatePX, col,row,bW,bH))
    templateImage.close()
    return tintList

def getAveragePXOfBlock(tempPX,x,y,bW, bH):
    pxSum = (0,0,0)
    offsetX = x*bW
    offsetY = y*bH
    for px in range(bW):
        for py in range(bH):
            pxSum = addColors(pxSum, tempPX[offsetX+px,offsetY+py])
    return divColors(pxSum, bH*bW)

def divColors(colA, denom):
    colC = []
    for i in range(len(colA)):
        colC.append(colA[i]//denom)
    return tuple(colC)

def addColors(colA, colB):
    colC = []
    for i in range(len(colA)):
        colC.append(colA[i]+colB[i])
    return tuple(colC)

def loadImges(templateFileName, imprintFileName):
    template = Image.open(templateFileName)
    imprint = Image.open(imprintFileName)
    return template, imprint

def scaleImage(imageToScale, w, h):
    imageToScale = imageToScale.resize((w,h))
    return imageToScale

def init():
    #Change image paths
    template, imprint = loadImges("mona-lisa.jpg","dan.jpg")
    imgWidth, imgHeight = template.size 
    #change rows and cols to adjust resolution
    rows = 40
    cols = 80
    blockWidth = imgWidth // cols
    blockHeight = imgHeight // rows
    print(blockWidth, blockHeight)
    cols -= 1 
    rows -= 1
    imprint = scaleImage(imprint, blockWidth, blockHeight)
    tintList = generateTintBlockList(template,rows,cols,blockWidth,blockHeight)
    generateNewImage(imprint,tintList,rows,cols,blockWidth,blockHeight,imgWidth,imgHeight)

init()