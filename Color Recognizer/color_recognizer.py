import pandas as pd
import cv2

img = cv2.imread('img/cyberpunk.jpeg')
headers = ['color', 'color_name', 'hex', 'R', 'G', 'B']
csv = pd.read_csv('dataset/colors.csv', names=headers, header=None)

# To find out if the image was clicked
clicked = False

# RGB values
r = g = b = 0

# cursor position on the Cartesian plane
xpos = ypos = 0


def identify_color(red, green, blue):
    minimum = 10000
    color_name = ''
    for i in range(len(csv)):
        # loc = retrieves the values in data frame cells. loc [row, column]
        absolute_value = abs(red - int(csv.loc[i, 'R'])) + abs(green - int(csv.loc[i, 'G'])) + abs(blue - int(csv.loc[i, 'B']))
        if absolute_value <= minimum:
            minimum = absolute_value
            color_name = csv.loc[i, 'color_name']
    return color_name


def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # taking the global variables we defined earlier
        global b, g, r, xpos, ypos, clicked

        clicked = True
        xpos = x
        ypos = y

        # tacking de RGB values
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('Color Recognizer')
cv2.setMouseCallback('Color Recognizer', mouse_click)

while 1:
    cv2.imshow('Color Recognizer', img)
    if clicked:
        # image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # displaying the color name and RGB values
        text = identify_color(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # imgage, text, start, font(0-7), fontScale, color, thickness, lineType
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # for very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        cv2.destroyAllWindows()

