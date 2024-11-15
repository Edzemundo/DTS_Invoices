import os
import cv2
import argparse
import numpy as np
from PIL import Image
import file_handling as fh
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

# to prevent "decompression bomb DOS attack"
Image.MAX_IMAGE_PIXELS = 933120000

def parse_arguments():
    parser = argparse.ArgumentParser(description="Watch directory for new files and process them.")
    parser.add_argument("-p", "--parent", type=bool, default=True, required=False,
                        help="Determine if the script should check cwd (parent direcrory is checked by default).")
    return parser.parse_args()


def scan_image(file):
    print(f"Scanning image: {file}...")
    # Check if the file exists
    if not os.path.isfile(file):
        print(f"File '{file}' does not exist.")
        exit()

    # Load the image using Pillow
    img = cv2.imread(file)

    # processed_image = process(img, 'save')
    processed_image = process(img)
    reference_num, date = ocr(processed_image)
    fh.rename_scans(file, f"{reference_num}_{date}.jpeg")


def scan_pdf(file, working_path):
    print(f"Scanning pdf: {file}...")
    # Check if the file exists
    if not os.path.isfile(file):
        print(f"File '{file}' does not exist.")
        exit()

    # Load the image using pdf2image
    print("Converting PDF page to image...")
    images = convert_from_path(file)
    images[0].save("temp_image.png")

    img = cv2.imread("temp_image.png")
    # processed_image = process(img, 'save')
    processed_image = process(img)
    reference_num, date = ocr(processed_image)

    print("Removing temporary images...")
    for possible_temp in os.listdir("."):
        if possible_temp.startswith("temp_"):
            os.remove(possible_temp)
    print("Temporary images removed.")

    fh.rename_scans(file, f"{reference_num}_{date}.pdf")
    fh.move_pdfs_to_folder(os.getcwd(), working_path, "cwd")


def process(img, *args):
    print(f"Processing image to improve readability: {file}...")
    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Apply Gaussian Blur (optional, for noise reduction)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # 3. Thresholding to convert image to binary (black and white)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY_INV)

    # 4. Dilation (to thicken characters)
    kernel = np.ones((2, 2), np.uint8)
    # dilated = cv2.dilate(thresh, kernel, iterations=1)
    dilated = cv2.erode(thresh, kernel, iterations=1)
    print("Image processed successfully.")

    if "save" in args:
        save_image(dilated)

    return dilated


def save_image(image):
    global file
    print(f"Saving processed image: {file}...")
    cv2.imwrite(f"{file}_processed.png", image)
    print(f"Processed image saved as processed_{file}.png")
    processed_image = Image.open(f"processed_{file}.png")
    processed_image.show()


def ocr(image):
    print(f"Reading text from processed image: {file}...")

    dates = ""
    reference_num = None
    best_fit = None

    # Initialize the reader. You can specify the languages here (e.g., ['en'] for English).
    reader = PaddleOCR(use_angle_cls=False, use_gpu=False, lang="en", det=True)

    # Extract the text
    result = reader.ocr(image, cls=False)
    print(result)

    # Print the result
    for detection in result:
        for detection_info in detection:
            word = detection_info[1][0]
            # print(word)  # Output the detected text
            if "OD" in word and len(word) == 10 and word[-4:].isdigit():
                reference_num = word

            if "/" in word:
                date_candidate = word.split(" ")[0]
                if date_candidate.count("/") > 1 and date_candidate[0] == "2":
                    best_fit = date_candidate

                dates += date_candidate + " "

    if reference_num is None:
        print("Reference number not found.")
        fh.folderize_no_reference(file)
        exit()
    if best_fit is None:
        print("Date not found.")
        fh.folderize_no_date(file)
        exit()

    # best_fit = re.search("^[0-9]{4}\/[0-9]{2}\/[0-9]{2}", dates)
    date = best_fit.replace("/", "-")
    print(f"Reference Number: {reference_num}")
    print(f"Date: {date}")

    return reference_num, date


if __name__ == "__main__":

    args = parse_arguments()
    if args.parent:
        working_path = os.path.dirname(os.getcwd())
        files = fh.listscans(working_path)
    else:
        working_path = os.getcwd()
        files = fh.listscans(working_path)

    if len(files) == 0:
        print("No scan files found in the current directory.")
        exit()
    else:
        for file in files:
            if file.endswith(".pdf"):
                scan_pdf(file, working_path)
                fh.folderize(working_path)
            else:
                scan_image(file)
                fh.folderize(working_path)
