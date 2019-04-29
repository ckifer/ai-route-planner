"""
DOCSTRING
this file does image processing
"""

import time
import cv2
import numpy as np
from skimage.measure import compare_ssim as ssim
import traversal
import astarsearch
import random

def main(image_filename):
    """Do some image processing, iterate through images, determine best path through obstacles"""
    # 2 arrays
    occupied_grids = []  # List to store coordinates of occupied grid
    planned_path = {}   # Dictionary to store information regarding path planning

    # load image
    image = cv2.imread(image_filename)
    (win_w, win_h) = (60, 60)

    obstacles = []
    index = [1, 1]

    # create blank image, a matrix of 0's
    blank_image = np.zeros((60, 60, 3), np.uint8)
    # create array of 100 blank images
    list_images = [[blank_image for i in range(10)] for i in range(10)]
    maze = [[0 for i in range(10)] for i in range(10)]

    # image traversal; detect non empty squares
    for(x, y, window) in traversal.sliding_window(image, step_size=60, window_size=(win_w, win_h)):
        # ignore window if it doesn't meet our size requirements
        if(window.shape[0]) != win_h or window.shape[1] != win_w:
            continue
        # print index, img is our iterator
        clone = image.copy()
        # format the square for open cv
        cv2.rectangle(clone, (x, y), (x + win_w, y + win_h), (0, 255, 0), 2)
        crop_img = image[x:x + win_w, y:y + win_h]
        list_images[index[0]-1][index[1]-1] = crop_img.copy()
        # print occupied grid
        average_color_per_row = np.average(crop_img, axis=0)
        average_color = np.average(average_color_per_row, axis=0)
        average_color = np.uint8(average_color)

        # iterate through color matrix
        if any(i <= 240 for i in average_color):
            maze[index[1]-1][index[0]-1] = 1  # if not majority white
            occupied_grids.append(tuple(index))

        # add black squares
        if any(i <= 20 for i in average_color):
            obstacles.append(tuple(index))

        cv2.imshow("window", clone)
        cv2.waitKey(1)
        time.sleep(0.05)

        # Iterate
        index[1] = index[1] + 1
        if index[1] > 10:
            index[0] = index[0] + 1
            index[1] = 1

    # perform shortest path search
    list_colored_grids = [n for n in occupied_grids if n not in obstacles]

    for startimage in list_colored_grids:
        # start image
        img1 = list_images[startimage[0]-1][startimage[1]-1]
        for grid in [n for n in list_colored_grids if n != startimage]:
            # next image
            img = list_images[grid[0]-1][grid[1]-1]
            # convert to grayscale
            image = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            image2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # compare structural similarities
            s = ssim(image, image2)

            # if similar, perform a star search
            if s > 0.9:
                result = astarsearch.astar(
                    maze, (startimage[0]-1, startimage[1]-1), (grid[0]-1, grid[1]-1))
                # print result
                list2 = []
                for t in result:
                    x, y = t[0], t[1]
                    # Contains min path + startimage + endimage
                    list2.append(tuple((x + 1, y + 1)))
                    # Result contains the minimum path required
                    result = list(list2[1:-1])
                if not result:  # If no path is found;
                    planned_path[startimage] = list(["NO PATH", [], 0])
                planned_path[startimage] = list(
                    [str(grid), result, len(result)+1])

    for obj in list_colored_grids:
        if not obj in planned_path:  # If no matched object is found;
            planned_path[obj] = list(["NO MATCH", [], 0])
    
    image = cv2.imread(image_filename)
    clone = image.copy()

    drawn = list()

    for obj in planned_path:
      color = list(np.random.choice(range(256), size=3))
      if(planned_path[obj][0] == 'NO MATCH'):
        cv2.putText(clone,"NO MATCH", ((((obj[0] - 1) * 60)), (((obj[1] - 1) * 60) + 30)), cv2.FONT_HERSHEY_SIMPLEX, .35, 0)
        cv2.imshow("window", clone)
        cv2.waitKey()
        continue
      end_str = planned_path[obj][0].strip('(').strip(')').strip()
      end = tuple((int(end_str.split(',')[0]), int(end_str.split(',')[1])))

      # do this so we don't draw duplicate paths the opposite direction
      if(drawn.__contains__(end)):
        continue

      traversal.path_line(clone, start=obj, end=end, path=planned_path[obj][1], color=(int(color[0]), int(color[1]), int(color[2])))
      drawn.append(obj)
      cv2.imshow("window", clone)
      cv2.waitKey()

    cv2.imshow("window", clone)
    cv2.waitKey()

    return occupied_grids, planned_path

if __name__ == '__main__':

        # change filename to check for other images
    FILENAME = "Test_Images/test_image1.jpg"

    main(FILENAME)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
