""" main """
import process_image

OCCUPIED_GRIDS, PLANNED_PATH = process_image.main(
    "Test_Images/test_image4.jpg")
print("Occupied Grids : ")
print(OCCUPIED_GRIDS)
print("Planned Path :")
print(PLANNED_PATH)
