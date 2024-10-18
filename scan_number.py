import os
import cv2
import easyocr
import numpy as np
from PIL import Image
import file_handling as fh
from pdf2image import convert_from_path

# to prevent "decompression bomb DOS attack"
Image.MAX_IMAGE_PIXELS = 933120000


def scan_image(file):
    print(f"Scanning image: {file}...")
    # Check if the file exists
    if not os.path.isfile(file):
        print(f"File '{file}' does not exist.")
        exit()

    # Load the image using OpenCV
    img = cv2.imread(file)

    processed_image = process(img, 'save')
    # processed_image = process(img)
    reference_num, date = ocr(processed_image)
    fh.rename_scans(file, f"{reference_num}_{date}.jpeg")


def scan_pdf(file):
    print(f"Scanning pdf: {file}...")
    # Check if the file exists
    if not os.path.isfile(file):
        print(f"File '{file}' does not exist.")
        exit()

    # Load the image using OpenCV
    images = convert_from_path(file)
    i = 0
    image_names = []
    print("Creating temporary images from PDF...")
    for image in images:
        image.save(f"temp_{i}_converted.png", "PNG")
        image_names.append(f"temp_{i}_converted.png")
        i += 1

    img = cv2.imread(f"temp_{0}_converted.png")

    processed_image = process(img, 'save')
    # processed_image = process(img)
    reference_num, date = ocr(processed_image)

    print("Removing temporary images...")
    for possible_temp in os.listdir("."):
        if possible_temp.startswith("temp_"):
            os.remove(possible_temp)
    print("Temporary images removed.")

    fh.rename_scans(file, f"{reference_num}_{date}.pdf")


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
    # 5. Save and view the preprocessed image
    cv2.imwrite(f"{file}_processed.png", image)
    print(f"Processed image saved as {file}_processed.png")
    processed_image = Image.open(f"{file}_processed.png")
    processed_image.show()


def ocr(image):
    print(f"Reading text from processed image: {file}...")

    dates = ""
    reference_num = None
    best_fit = None

    # Initialize the reader. You can specify the languages here (e.g., ['en'] for English).
    reader = easyocr.Reader(["en"])

    # Extract the text
    result = reader.readtext(image)

    # Print the result
    for detection in result:
        # detection[1] contains the text
        print(detection[1]) # Output the detected text
        if (
            "OD" in detection[1]
            and len(detection[1]) == 10
            and detection[1][-4:].isdigit()
        ):
            reference_num = detection[1]
        if (
            "0D" in detection[1]
            and len(detection[1]) == 10
            and detection[1][-4:].isdigit()
        ):
            reference_num = detection[1].replace("0D", "OD")
        if (
            "00" in detection[1]
            and detection[1][2].isdigit()
            and len(detection[1]) == 10
            and detection[1][-4:].isdigit()
        ):
            reference_num = detection[1].replace("00", "OD")

        if "/" in detection[1]:
            date_candidate = detection[1].split(" ")[0]
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
    files = fh.listscans()

    if len(files) == 0:
        print("No scan files found in the current directory.")
        exit()
    else:
        for file in files:
            if file.endswith(".pdf"):
                scan_pdf(file)
                fh.folderize()
            else:
                scan_image(file)
                fh.folderize()
