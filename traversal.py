""" Traversing through the image to perform image processing """
import cv2

def sliding_window(image, step_size, window_size):
    """ Traversing through the image """
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])

def path_line(image, start, end, path, color):
    """ following the path line """
    # draw a line through a path
    path.insert(0, start)
    path.append(end)
    i = 0
    for point in path:
        if(i < len(path) - 1):
            x1 = (((point[0] - 1) * 60) + 30)
            y1 = (((point[1] - 1) * 60) + 30)
            x2 = (((path[i + 1][0] - 1) * 60) + 30)
            y2 = (((path[i + 1][1] - 1) * 60) + 30)
            cv2.line(image, (x1, y1), (x2, y2), color, 2)
            i += 1