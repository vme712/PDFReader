import re
import uuid

import numpy as np
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def save_file(file_dir, img):
    file_path = f'{file_dir}/{uuid.uuid4()}.jpg'
    cv2.imwrite(file_path, img)
    return file_path


def get_gray_img(img):
    if img.ndim == 2:
        return img
    else:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_tesseract_text(img_for_read):
    text1 = pytesseract.image_to_string(img_for_read, lang="rus", config='--psm 6')

    # Удалить специальные символы
    text1 = re.findall(r'[^\*"/:?\\|<>″′‖©〈\n]', text1, re.S)
    return "".join(text1)


def get_tesseract_number(img_for_read):
    text1 = pytesseract.image_to_string(img_for_read,
                                        lang="rus",
                                        config='--psm 6 -c tessedit_char_whitelist=0123456789,')

    # Удалить специальные символы
    text1 = re.findall(r'[^\*"/:?\\|<>″′‖©〈\n]', text1, re.S)
    return "".join(text1)


def clear_img_for_color(img):
    colorLow = np.array([0, 200, 0])
    colorHigh = np.array([255, 255, 255])
    mask = cv2.inRange(img, colorLow, colorHigh)
    return mask


def crop_img(img, h, w):
    crop_percent = 0.05
    h, w = int(h - h * crop_percent), int(w - w * crop_percent)
    x, y, h, w = int(0 + w * crop_percent), int(0 + h * crop_percent), int(h - h * crop_percent), int(
        w - w * crop_percent)
    img = img[y:y + h, x:x + w]
    h, w = img.shape[:2]
    return img, h, w


def get_config_keys(config):
    valid_config = {}
    for key in config:
        if config[key] is not None:
            valid_config.update({f'{key}': config[key]})
    return valid_config


def get_key(config, col_index):
    col_key, col_number = None, None
    for key in config:
        if col_index == config[key] - 1:
            col_key, col_number = key, config[key]
            break
    return col_key, col_number
