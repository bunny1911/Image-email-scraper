#  Project: Email Extractor from Images

##  Project Overview
This Python project provides an OCR-based solution for extracting email addresses from images. 
The tool supports both **local image files** and **remote images via URLs**, enabling easy extraction of embedded text using **Tesseract OCR**.

### Features
- Extracts email addresses from images.  
- Supports **PNG, JPG, BMP, and TIFF** formats.  
- Works with **local image files** and **image URLs**.  
- Provides **error handling** and **logging** for debugging.  
- Uses **Pytesseract** for OCR processing.  
- Automatically detects and filters valid email addresses.  
- Supports pagination for large-scale processing.  

---

## Technologies Used
- **Python 3.x** – Core programming language.
- **Pytesseract** – Python wrapper for Tesseract OCR.
- **Tesseract OCR** – Optical Character Recognition engine.
- **Pillow (PIL)** – Image processing library.
- **Requests** – HTTP library for handling image URLs.
- **Logging** – Built-in Python logging for error handling.
- **Pathlib** – File system operations.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/email-extractor.git
cd email-extractor
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
Ensure all required Python packages are installed:
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
Tesseract OCR must be installed on your system.
- **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**:
  ```bash
  brew install tesseract
  ```
- **Linux**:
  ```bash
  sudo apt install tesseract-ocr
  ```

---

## 🔹 Usage
Run the script and enter an image URL or a local image file path when prompted:

```bash
python script.py
```
Then enter:
```
Enter the URL or file path of the image: /path/to/image.jpg
```
Or for a remote file:
```
Enter the URL or file path of the image: https://example.com/image.png
```

---

## 🔹 Example Output
```
Extracted email(s):
john.doe@example.com
contact@website.com
```

---

## 🔹 Logging
The script logs actions, warnings, and errors:
- **INFO**: Successful steps (e.g., downloading an image, extracting emails).
- **ERROR**: Issues with file access, invalid images, OCR failures.

---

