""" Traversing through the image to perform image processing """


def sliding_window(image, step_size, window_size):
    """ Traversing through the image """
    # slide a window across the image
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            # yield the current window
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])
