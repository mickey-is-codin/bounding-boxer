import os
import sys
import cv2

from pathlib import Path

cropping = False
bbox = []
bbox_exists = False

num_labeled = 0

def main():
    print("\n\nWelcome to Bounding Boxer\n\n")

    name = input("Please enter your first name: ")

    data_path   = Path("data/sacral-labeling-template/avg-heatmaps")
    output_path = Path(f"results/box-results/{name.lower()}_bounding_boxes.csv")

    results_exist = touch_results_file(output_path)
    labeled_paths = read_results_file(output_path, data_path) if results_exist else None
    all_paths     = read_image_directory(data_path)
    todo_paths    = compare_paths(all_paths, labeled_paths) if results_exist else all_paths

    # print(f"Total images: {len(all_paths)}")
    # print(f"Prelabeled images: {len(labeled_paths) if labeled_paths else 0}")
    # print(f"To be labelled: {len(todo_paths)}")

    scroll_images(todo_paths, output_path)

def touch_results_file(output_path):
    if not os.path.exists(output_path):
        header_string = f"filename,bbox_upper_left_x,bbox_upper_left_y,bbox_lower_right_x,bbox_lower_right_y\n"
        with open(output_path, 'w') as output_file:
            output_file.write(header_string)
        return False
    else:
        print("Welcome back!")
        return True

def read_results_file(output_path, data_path):
    paths = []
    with open(output_path, 'r') as existing_results_file:
        next(existing_results_file)
        for line in existing_results_file.readlines():
            paths.append(data_path/line.split(",")[0].split("/")[-1])

    return paths

def read_image_directory(data_path):
    paths = []
    for path in os.listdir(data_path):
        if path[-4:] == ".png":
            paths.append(data_path/path)

    return paths

def compare_paths(full_path, subset_path):
    return list(set(full_path) - set(subset_path))

def scroll_images(img_paths, output_path):
    global cropping, bbox, bbox_exists, num_labeled

    num_images = len(img_paths)
    img_paths = iter(img_paths)
    img_path = str(next(img_paths))
    unlabeled_img = cv2.imread(img_path, 1)

    cv2.namedWindow("Current Frame")
    cv2.setMouseCallback("Current Frame", mouse_boxing)

    while True:

        if bbox_exists:
            display_image(unlabeled_img, show_bbox=True)
        else:
            display_image(unlabeled_img)

        user_key = cv2.waitKey(33)
        if user_key == 27 or user_key == 113 or (num_images - num_labeled) == 0:
            print("Thank you for taking the time to contribute to this study!")
            sys.exit(0)
        elif user_key == 13 and bbox_exists:
            save_bbox_to_csv(output_path, img_path, num_images)
            num_labeled += 1

            bbox = []
            bbox_exists = []

            img_path = str(next(img_paths))
            unlabeled_img = cv2.imread(img_path)

def display_image(unlabeled_img, show_bbox=False):
    if show_bbox:
        labeled_img = cv2.rectangle(
            unlabeled_img,
            bbox[0],
            bbox[1],
            (0,255,0),
            2
        )
        cv2.imshow("Current Frame", labeled_img)
    else:
        cv2.imshow("Current Frame", unlabeled_img)

def mouse_boxing(event, x, y, flags, params):
    global cropping, bbox, bbox_exists

    if event == cv2.EVENT_LBUTTONDOWN:
        bbox = []
        cropping = True
        bbox.append((x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        bbox_exists = True
        cropping = False
        bbox.append((x,y))

def save_bbox_to_csv(csv_path, img_path, num_images):
    global bbox, num_labeled
    print(f"\nSaved {img_path.split('/')[-1]} bounding box")
    print(f"{num_images - num_labeled - 1} images left to label")
    write_string = f"{img_path},{bbox[0][0]},{bbox[0][1]},{bbox[1][0]},{bbox[1][1]}\n"
    with open(csv_path, "a") as bbox_file:
        bbox_file.write(write_string)

if __name__ == "__main__":
    main()
tp11_supine_0_none.png
