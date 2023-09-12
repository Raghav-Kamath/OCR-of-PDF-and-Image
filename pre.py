import numpy as np
import cv2

# simple image processing to start with
class preproc(object):

    def contrast(image_path):
        # Read the image
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to create a binary image
        _, thresholded_image = cv2.threshold(gray_image,128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        denoised_image = cv2.fastNlMeansDenoising(thresholded_image, None, h=48, templateWindowSize=7, searchWindowSize=21)

        # Perform erosion and dilation to reduce noise and enhance text
        kernel = np.ones((3, 3), np.uint8)
        processed_image = cv2.erode(denoised_image, kernel, iterations=1)
        processed_image = cv2.dilate(processed_image, kernel, iterations=1)

        # Invert the colors (optional, depending on your image)
        inverted_image = cv2.bitwise_not(processed_image)

        # Save the preprocessed image
        cv2.imwrite("preprocessed.png", inverted_image)

        # return inverted_image