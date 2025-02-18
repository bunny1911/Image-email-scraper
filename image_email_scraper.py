"""
Email Extractor from Images

This script extracts email addresses from images using Optical Character Recognition (OCR).
It supports both local image files and images from URLs.

Features:
- Validates whether the provided source is an image.
- Retrieves image data from a file path or URL.
- Uses OCR to extract text from the image.
- Identifies and extracts unique email addresses.
- Displays the extracted emails in the console.


Usage:
    Run the script and enter an image URL or file path when prompted.
"""

import logging
import re
from io import BytesIO
from pathlib import Path
from urllib.parse import urlparse

import pytesseract
import requests
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

VALID_IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp"}
EMAIL_REGEX = r"[\w.+-]+@[\w-]+\.[\w.-]+"


def save_emails_to_file(emails: list[str], output_path: str) -> None:
    """
    Saves extracted email addresses to a file.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(emails))

    logging.info(f"Emails saved to {output_file.resolve()}")


def is_valid_image(source: str) -> bool:
    """
    Checks if the provided path or URL is a valid image file.
    """

    parsed_url = urlparse(source)

    if parsed_url.scheme:
        # It's a link
        file_extension = Path(parsed_url.path).suffix.lower()

    else:
        # It's a file
        file_extension = Path(source).suffix.lower()

    return file_extension in VALID_IMAGE_TYPES


def get_image_data(source: str) -> BytesIO:
    """
    Retrieves image data from a local file or URL.
    """

    if not is_valid_image(source):
        raise ValueError("Invalid file type. Provide a valid image file.")

    if source.startswith(("http://", "https://")):
        response = requests.get(source, stream=True)
        response.raise_for_status()
        return BytesIO(response.content)

    return BytesIO(Path(source).read_bytes())


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocesses the image to improve text recognition.
    """

    image = image.convert("L")  # Grayscale
    image = ImageEnhance.Contrast(image).enhance(2.0)  # Increase contrast

    # Apply blur if the image has noise
    image = image.filter(ImageFilter.GaussianBlur(1))

    # Convert to binary (B/W)
    return ImageOps.autocontrast(image)


def extract_emails_from_image(image_data: BytesIO) -> list[str]:
    """
    Extracts unique email addresses from an image.
    """

    try:
        image = Image.open(image_data)
        image = preprocess_image(image)
        text = pytesseract.image_to_string(image, config="--oem 3 --psm 6")
        emails = list(set(re.findall(EMAIL_REGEX, text)))

        logging.info(f"Extracted {len(emails)} email(s).")
        return emails

    except Exception as error:
        raise RuntimeError(f"Failed to process image: {error}") from error


def main() -> None:
    """
    Main function to extract and save email addresses.
    """

    source = input("Enter the URL or file path of the image: ").strip()
    output_path = input("Enter the file path to save the extracted emails: ").strip()

    if not source or not output_path:
        logging.error("Missing input.")
        return

    try:
        emails = extract_emails_from_image(get_image_data(source))

        if emails:
            save_emails_to_file(emails, output_path)

        else:
            logging.info("No emails found.")

    except RuntimeError as error:
        logging.error(str(error))


if __name__ == "__main__":
    main()
