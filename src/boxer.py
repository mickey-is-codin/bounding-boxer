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

    setup_directories()

    name = input("Please enter your first name: ")

    img_dir     = Path("data/sacral-labeling-template/avg-heatmaps")
    output_path = Path(f"results/{name.lower()}_bounding_boxes.csv")

    results_exist = touch_results_file(output_path)
    all_paths     = read_image_directory(img_dir)
    labeled_paths = read_results_file(output_path, img_dir) if results_exist else None
    todo_paths    = compare_paths(all_paths, labeled_paths)
    system_paths  = convert_paths_to_unix(img_dir, todo_paths)
    scroll_images(system_paths, output_path)

def setup_directories():
    if not os.path.isdir("results"):
        os.mkdir("results")

def touch_results_file(output_path):
    if not os.path.exists(output_path):
        header_string = f"filename,bbox_upper_left_x,bbox_upper_left_y,bbox_lower_right_x,bbox_lower_right_y\n"
        with open(output_path, 'w') as output_file:
            output_file.write(header_string)
        return False
    else:
        print("Welcome back!")
        return True

def read_results_file(output_path, img_dir):
    paths = []
    with open(output_path, 'r') as existing_results_file:
        next(existing_results_file)
        for line in existing_results_file.readlines():
            paths.append(line.split(",")[0])

    return paths

def read_image_directory(img_dir):
    paths = []
    for path in os.listdir(img_dir):
        if path[-4:] == ".png":
            paths.append(path)

    return paths

def compare_paths(full_path, subset_path):
    if not subset_path:
        return list(set(full_path))
    else:
        return list(set(full_path) - set(subset_path))

def convert_paths_to_unix(img_dir, img_filenames):
    return [Path(img_dir, img_filename) for img_filename in img_filenames]

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
    write_string = f"{img_path.split('/')[-1]},{bbox[0][0]},{bbox[0][1]},{bbox[1][0]},{bbox[1][1]}\n"
    with open(csv_path, "a") as bbox_file:
        bbox_file.write(write_string)

if __name__ == "__main__":
    main()
tp11_supine_0_none.png
