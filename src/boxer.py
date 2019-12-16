import os
import sys
import cv2

from pathlib import Path

cropping = False
bbox = []
bbox_exists = False

def main():
    print("\n\nWelcome to Bounding Boxer\n\n")

    data_path   = Path("data/sacral-labeling-template/avg-heatmaps")
    output_path = Path("results/box-results/bounding_boxes.csv")

    results_exist = touch_results_file(output_path)
    labeled_paths = read_results_file(output_path) if results_exist else None
    all_paths     = read_image_directory(data_path)
    todo_paths    = compare_paths(all_paths, labeled_paths)

    print(f"Total images: {len(all_paths)}")
    print(f"Prelabeled images: {len(labeled_paths)}")
    print(f"To be labelled: {len(todo_paths)}")

    scroll_images(todo_paths, output_path)

def touch_results_file(output_path):
    if not os.path.exists(output_path):
        with open(output_path, 'w'): pass
        return False
    else:
        return True

def read_results_file(output_path):
    paths = []
    with open(output_path, 'r') as existing_results_file:
        next(existing_results_file)
        for line in existing_results_file.readlines():
            paths.append(line.split(",")[0])

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
    global cropping, bbox, bbox_exists

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
        if user_key == 27 or user_key == 113:
            # save_bbox_to_csv(output_path)
            sys.exit(0)
        elif user_key == 13:
            print(bbox)
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
        print(f"Bounding box upper left: ({x}, {y})")
        bbox = []
        cropping = True
        bbox.append((x,y))
    elif event == cv2.EVENT_LBUTTONUP:
        print(f"Bounding box lower right: ({x}, {y})")
        bbox_exists = True
        cropping = False
        bbox.append((x,y))

if __name__ == "__main__":
    main()
tp11_supine_0_none.png
