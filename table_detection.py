import cv2
import numpy as np
import os


def has_table_boundaries(contour, vertical_lines_img, horizontal_lines_img, min_vertical_lines=3,
                         min_horizontal_lines=3):
    x, y, w, h = cv2.boundingRect(contour)
    roi_vertical = vertical_lines_img[y:y + h, x:x + w]
    roi_horizontal = horizontal_lines_img[y:y + h, x:x + w]

    vertical_lines = cv2.countNonZero(roi_vertical)
    horizontal_lines = cv2.countNonZero(roi_horizontal)

    return vertical_lines >= min_vertical_lines and horizontal_lines >= min_horizontal_lines


def table_detection(img_path):
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, img_bin) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = cv2.bitwise_not(img_bin)

    kernel_length_v = (np.array(img_gray).shape[1]) // 120
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length_v))
    im_temp1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(im_temp1, vertical_kernel, iterations=3)

    kernel_length_h = (np.array(img_gray).shape[1]) // 40
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length_h, 1))
    im_temp2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(im_temp2, horizontal_kernel, iterations=3)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    table_segment = cv2.addWeighted(vertical_lines_img, 0.5, horizontal_lines_img, 0.5, 0.0)
    table_segment = cv2.erode(cv2.bitwise_not(table_segment), kernel, iterations=2)
    thresh, table_segment = cv2.threshold(table_segment, 0, 255, cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(table_segment, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    img_width = img.shape[1]
    for c, hier in zip(contours, hierarchy[0]):
        x, y, w, h = cv2.boundingRect(c)

        # Filter out small bounding boxes
        if w < 70 or h < 120:
            continue

        # Filter out too rectangular bounding boxes
        if w > 10 * h or h > 10 * w:
            continue

        # Filter out bounding boxes on the right side of the page
        if x + w > 0.9 * img_width:
            continue

        # Filter out contours without table boundaries
        if not has_table_boundaries(c, vertical_lines_img, horizontal_lines_img):
            continue

        if hier[1] != -1:
            count += 1
            cropped = img[y:y + h, x:x + w]
            if True:
                cv2.imwrite("./results/cropped/crop_" + str(count) + "__" + img_path.split('/')[-1], cropped)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if True:
        cv2.imwrite("./results/table_detect/table_detect__" + img_path.split('/')[-1], table_segment)
        cv2.imwrite("./results/bb/bb__" + img_path.split('/')[-1], img)


{table_detection('./form/' + i) for i in os.listdir('./form/') if
 i.endswith('.png') or i.endswith('.PNG') or i.endswith('.jpg') or i.endswith('.JPG')}
