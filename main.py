from PIL import Image, ImageChops
import sys


def generate_new_image(imprintImage, tintList, rows, cols, bW, bH, w, h):
    master = Image.new('RGB', (bW * cols, bH * rows))
    for y in range(rows):
        for x in range(cols):
            toPaste = tint_image(imprintImage, tintList[y*cols+x])
            offset = (x*bW, y*bH)
            master.paste(toPaste, offset)
    master.save('out.png')


def tint_image(image, tint_color):
    return ImageChops.multiply(image, Image.new('RGBA', image.size, tint_color))


def generate_tint_blockList(templateImage, rows, cols, bW, bH):
    tintList = []
    templatePX = templateImage.load()
    for row in range(rows):
        for col in range(cols):
            tintList.append(get_average_px_of_blocks(templatePX, col, row, bW, bH))
    templateImage.close()
    return tintList


def get_average_px_of_blocks(tempPX, x, y, bW, bH):
    pxSum = (0, 0, 0)
    offsetX = x*bW
    offsetY = y*bH
    for px in range(bW):
        for py in range(bH):
            pxSum = add_colors(pxSum, tempPX[offsetX+px, offsetY+py])
    return divide_colors(pxSum, bH*bW)


def divide_colors(colA, denom):
    colC = []
    for i in range(len(colA)):
        colC.append(colA[i]//denom)
    return tuple(colC)


def add_colors(colA, colB):
    colC = []
    for i in range(len(colA)):
        colC.append(colA[i]+colB[i])
    return tuple(colC)


def load_images(templateFileName, imprintFileName):
    template = Image.open(templateFileName)
    imprint = Image.open(imprintFileName)
    return template, imprint


def scale_image(imageToScale, w, h):
    imageToScale = imageToScale.resize((w, h))
    return imageToScale


def init():
    # Change image paths
    template, imprint = load_images("mona-lisa.jpg", "matt.jpg")
    imgWidth, imgHeight = template.size
    # change rows and cols to adjust resolution
    rows = 30
    cols = 20
    blockWidth = imgWidth // cols
    blockHeight = imgHeight // rows
    cols -= 1
    rows -= 1
    imprint = scale_image(imprint, blockWidth, blockHeight)
    tintList = generate_tint_blockList(
        template, rows, cols, blockWidth, blockHeight)
    generate_new_image(imprint, tintList, rows, cols,
                       blockWidth, blockHeight, imgWidth, imgHeight)


init()
