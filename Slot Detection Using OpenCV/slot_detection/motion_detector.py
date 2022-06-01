import cv2 as open_cv
import numpy as np
import logging
from drawing_utils import draw_contours
from colors import COLOR_GREEN, COLOR_WHITE, COLOR_BLUE


class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self, video, coordinates, start_frame):
        self.video = video
        self.coordinates_data = coordinates
        self.start_frame = start_frame
        self.contours = []
        self.bounds = []
        self.mask = []

    def detect_motion(self):  # base function to detect motion in the generated parking slots

        # method for video capturing from video files, image sequences or cameras
        capture = open_cv.VideoCapture(self.video)
        # method to start the video from a particular position
        capture.set(open_cv.CAP_PROP_POS_FRAMES, self.start_frame)

        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        for p in coordinates_data:
            coordinates = self._coordinates(p)
            logging.debug("coordinates: %s", coordinates)

            # below function is used to draw an approximate rectangle around the binary image
            rect = open_cv.boundingRect(coordinates)
            logging.debug("rect: %s", rect)

            new_coordinates = coordinates.copy()  # create a copy of the coordinates generated
            new_coordinates[:, 0] = coordinates[:, 0] - rect[0]
            new_coordinates[:, 1] = coordinates[:, 1] - rect[1]
            logging.debug("new_coordinates: %s", new_coordinates)

            self.contours.append(coordinates)  # function to detect the contours in the image
            self.bounds.append(rect)   # function to append the previous bound

            mask = open_cv.drawContours(
                np.zeros((rect[3], rect[2]), dtype=np.uint8),
                [new_coordinates],
                contourIdx=-1,
                color=255,
                thickness=-1,
                lineType=open_cv.LINE_8)     # method to get an image mask from the contour

            mask = mask == 255
            self.mask.append(mask)
            logging.debug("mask: %s", self.mask)

        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        while capture.isOpened():   # read the data while capturing process is started
            result, frame = capture.read()
            if frame is None:
                break

            if not result:
                raise CaptureReadError("Error reading video capture on frame %s" % str(frame))  # error handling

            # using below method the image is convolved with a Gaussian filter instead of the box filter
            # Gaussian filter is a low-pass filter that removes the high-frequency components
            blurred = open_cv.GaussianBlur(frame.copy(), (5, 5), 3)

            # below method is used to convert an image from one color space to another
            grayed = open_cv.cvtColor(blurred, open_cv.COLOR_BGR2GRAY)

            new_frame = frame.copy()  # create a copy of the frame captured
            logging.debug("new_frame: %s", new_frame)

            position_in_seconds = capture.get(open_cv.CAP_PROP_POS_MSEC) / 1000.0

            for index, c in enumerate(coordinates_data):
                status = self.__apply(grayed, index, c)   # get the status of slot, weather changed or unchanged

                # if status is same, continue with detection
                if times[index] is not None and self.same_status(statuses, index, status):
                    times[index] = None
                    continue

                # if status is changed, detect the change and change color of slot
                if times[index] is not None and self.status_changed(statuses, index, status):
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                        statuses[index] = status
                        times[index] = None
                    continue

                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index] = position_in_seconds

            for index, p in enumerate(coordinates_data):
                coordinates = self._coordinates(p)

                color = COLOR_GREEN if statuses[index] else COLOR_BLUE
                draw_contours(new_frame, coordinates, str(p["id"] + 1), COLOR_WHITE, color)

            open_cv.imshow(str(self.video), new_frame)
            k = open_cv.waitKey(1)
            if k == ord("q"):
                break
        capture.release()
        open_cv.destroyAllWindows()  # close the openCV window after the end of video

    def __apply(self, grayed, index, p):
        coordinates = self._coordinates(p)
        logging.debug("points: %s", coordinates)

        rect = self.bounds[index]
        logging.debug("rect: %s", rect)

        # convert the captured frame to gray scale
        roi_gray = grayed[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])]

        # below method applies a Laplacian operator to the grayscale image and stores the output image
        laplacian = open_cv.Laplacian(roi_gray, open_cv.CV_64F)
        logging.debug("laplacian: %s", laplacian)

        coordinates[:, 0] = coordinates[:, 0] - rect[0]
        coordinates[:, 1] = coordinates[:, 1] - rect[1]

        status = np.mean(np.abs(laplacian * self.mask[index])) < MotionDetector.LAPLACIAN
        logging.debug("status: %s", status)

        return status   # returns the status of parking lot, occupied or empty

    @staticmethod
    def _coordinates(p):
        return np.array(p["coordinates"])  # returns numpy array of the generated coordinates

    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]


class CaptureReadError(Exception):
    pass
