""" main """
import process_image

OCCUPIED_GRIDS, PLANNED_PATH = process_image.main(
    "Test_Images/test_image1.jpg")
print("Occupied Grids : ")
print(OCCUPIED_GRIDS)
print("Planned Path :")
for obj in PLANNED_PATH:
    print('path from:', end=' ')
    print(obj, end=' ')
    print('path:', end=' ')
    print(PLANNED_PATH[obj])
