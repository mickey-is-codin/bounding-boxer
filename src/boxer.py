import os
import cv2

from pathlib import Path

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

    scroll_images(todo_paths)

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

def scroll_images(image_paths):
    for image_path in image_paths:
        print(image_path)
        unlabeled_image = cv2.imread(image_path, 0)

        print(type(unlabeled_image))

        cv2.imshow(unlabeled_image, image_path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
