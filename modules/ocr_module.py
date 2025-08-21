# modules/ocr_module.py
import pyautogui
import pytesseract
from PIL import Image

# If Tesseract is not on PATH, uncomment & update this:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def capture_screen(output_path="screenshot.png"):
    import pyautogui
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)
    return output_path

    """
    Captures a screenshot of the screen and saves it.
    """
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)
        return save_path
    except Exception as e:
        print(f"[ERROR] Screenshot failed: {e}")
        return None


def extract_text(image_path):
    """
    Extracts text from the given image using Tesseract OCR.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return ""
