import cv2 as open_cv
import numpy as np

from colors import COLOR_WHITE
from drawing_utils import draw_contours


class CoordinatesGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, output, color):
        self.output = output
        self.caption = image
        self.color = color

        self.image = open_cv.imread(image).copy()
        self.click_count = 0
        self.ids = 0
        self.coordinates = []

        open_cv.namedWindow(self.caption, open_cv.WINDOW_GUI_EXPANDED)  # method is used to create a window with a
        # suitable name and size to display images and videos on the screen

        open_cv.setMouseCallback(self.caption, self.__mouse_callback)  # method to listen to mouse events

    def generate(self):  # function for generation or rectangles around the parking area to accurately detect slots
        while True:
            open_cv.imshow(self.caption, self.image)  # this method is used to display an image in a window
            key = open_cv.waitKey(0)

            if key == CoordinatesGenerator.KEY_RESET:
                self.image = self.image.copy()
            elif key == CoordinatesGenerator.KEY_QUIT:
                break
        open_cv.destroyWindow(self.caption)

    def __mouse_callback(self, event, x, y, flags, params):

        if event == open_cv.EVENT_LBUTTONDOWN:  # indicates that the left mouse button is pressed.
            self.coordinates.append((x, y))
            self.click_count += 1  # increases the click count by 1

            if self.click_count >= 4:
                self.__handle_done()  # parking slot selection is done when click count reaches 4

            elif self.click_count > 1:
                self.__handle_click_progress()  # if click count is less than 1, parking slot selection continues

        open_cv.imshow(self.caption, self.image)

    def __handle_click_progress(self):
        open_cv.line(self.image, self.coordinates[-2], self.coordinates[-1], (255, 0, 0), 1)
        # method is used to draw a line on image.

    def __handle_done(self):  # if parking slot selection is done, the coordinates are connected to visualise the space
        open_cv.line(self.image,
                     self.coordinates[2],
                     self.coordinates[3],
                     self.color, 1)
        open_cv.line(self.image,
                     self.coordinates[3],
                     self.coordinates[0],
                     self.color, 1)

        self.click_count = 0  # after one successful selection of slot, return the click count to zero

        coordinates = np.array(self.coordinates) # saving the selected coordinates in numpy array

        self.output.write("-\n          id: " + str(self.ids) + "\n          coordinates: [" +
                          "[" + str(self.coordinates[0][0]) + "," + str(self.coordinates[0][1]) + "]," +
                          "[" + str(self.coordinates[1][0]) + "," + str(self.coordinates[1][1]) + "]," +
                          "[" + str(self.coordinates[2][0]) + "," + str(self.coordinates[2][1]) + "]," +
                          "[" + str(self.coordinates[3][0]) + "," + str(self.coordinates[3][1]) + "]]\n")

        draw_contours(self.image, coordinates, str(self.ids + 1), COLOR_WHITE)
        # used to draw any shape provided its boundary points are known

        for i in range(0, 4):
            self.coordinates.pop()

        self.ids += 1   # slot id increases by one everytime after handling
