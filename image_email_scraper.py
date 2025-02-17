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

import re
import requests
import logging
import pytesseract
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Supported image formats
VALID_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

# Ser email regex
EMAIL_REGEX = r'[\w.+-]+@[\w-]+\.[\w.-]+'


def is_valid_image(source: str) -> bool:
    """
    Validates if the provided source corresponds to a supported image format.

    Args:
        source (str): A file path or URL pointing to an image.

    Returns:
        bool: True if the file has a valid image extension, False otherwise.
    """

    # Defined parse url
    parsed_url = urlparse(source)

    if parsed_url.scheme:
        # It's a link
        file_extension = Path(parsed_url.path).suffix.lower()

    else:
        # It's a file
        file_extension = Path(source).suffix.lower()

    return file_extension in VALID_IMAGE_EXTENSIONS


def get_image_data(source: str) -> BytesIO:
    """
    Retrieve image data from a local file or a URL.

    Args:
        source (str): A file path or URL pointing to an image.

    Returns:
        BytesIO: A binary stream containing the image data.

    Raises:
        ValueError: If the source is not a valid image file.
        RuntimeError: If an error occurs while retrieving the image.
    """

    try:

        if source.startswith("http://") or source.startswith("https://"):
            # Source is a URL
            logging.info(f"Downloading image from URL: {source}")

            # Validate image format
            if not is_valid_image(source):
                # Not valid image type
                raise ValueError("Invalid file type. Please provide a valid image file URL.")

            # Download image
            response = requests.get(source, stream=True)
            response.raise_for_status()
            image = BytesIO(response.content)

        else:
            # Source is a local file
            logging.info(f"Loading image from file: {source}")

            # Validate image format
            if not is_valid_image(source):
                # Not valid image type
                raise ValueError("Invalid file type. Please provide a valid image file.")

            # Read image from file
            image = BytesIO(Path(source).read_bytes())

    except Exception as error:
        # Error
        logging.error(f"Failed to retrieve image from {source}: {error}")
        raise RuntimeError(f"Failed to retrieve image from {source}: {error}")

    else:
        # All success
        return image


def extract_emails_from_image(image_data: BytesIO) -> list[str]:
    """
    Extract unique email addresses from an image using OCR.

    Args:
        image_data (BytesIO): A binary stream containing the image data.

    Returns:
        list[str]: A list of unique email addresses found in the image.

    Raises:
        RuntimeError: If an error occurs while processing the image.
    """

    try:
        # Open the image
        image = Image.open(image_data)

        # Perform OCR to extract text
        text = pytesseract.image_to_string(image)

        # Extract email addresses from recognized text
        emails = list(set(re.findall(EMAIL_REGEX, text)))

        # Log extracted emails
        logging.info(f"Extracted {len(emails)} email(s) from the image.")

    except Exception as error:
        logging.error(f"Failed to process image: {error}")
        raise RuntimeError(f"Failed to process image: {error}")

    else:
        # All success
        return emails


def main() -> None:
    """
    Main function to extract and display email addresses from an image.

    Raises:
        RuntimeError: If an error occurs while retrieving or processing the image.
    """

    # Get input from user
    source = input("Enter the URL or file path of the image: ").strip()

    if not source:
        # Nof found source
        logging.error("No input provided.")
        print("Error: No input provided.")
        return

    try:
        # Retrieve image data
        image_data = get_image_data(source)

        # Extract emails from the image
        emails = extract_emails_from_image(image_data)

        if emails:
            # Found emails
            print("Extracted email(s):")
            print("\n".join(emails))

        else:
            # Not found emails
            print("No emails found in the image.")

    except RuntimeError as error:
        # Print error
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
