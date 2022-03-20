import os

import cv2
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes

from utils import get_gray_img, save_file, get_tesseract_text, clear_img_for_color, get_config_keys, get_key

poppler_path = r'poppler-0.68.0/bin'

if not os.path.exists('static'):
    os.mkdir('static')

save_file_path = r'static'

config = {
    'line_direction': True,
    'cols': {
        'direction': None,
        'org_name': 2,
        'inn': 4,
        'project_name': 5,
        'ball': 6,
        'sum_pay': None
    }
}

config['cols'] = get_config_keys(config['cols'])


class Image:
    def __init__(self, img):
        self.img = img
        self.height, self.weight = self.img.shape[:2]

        cols, rows = self.get_col_row(self.img)
        self.img = self.rotate_img(cols + rows)

        self.img_clear = clear_img_for_color(self.img)
        self.x_arr, self.y_arr = self.get_col_row_array(self.img_clear)
        print(f'col - {len(self.x_arr)} - {self.x_arr}')
        print(f'row - {len(self.y_arr)} - {self.y_arr}')

        self.direction = None

    def rotate_img(self, img):
        counters, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = (self.weight // 2, self.height // 2)
        angle = 0
        for item in counters:
            if len(item) >= 2:
                _, _, angle = cv2.minAreaRect(item)
                break
        # _, _, angle = cv2.minAreaRect(counters[0])
        if 90 >= angle >= 45:
            angle = angle - 90
        elif 180 == angle:
            angle = 0
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(self.img, M, (int(self.weight), int(self.height)), flags=cv2.INTER_CUBIC,
                              borderMode=cv2.BORDER_DEFAULT, borderValue=(255, 255, 255))

    def search_cols(self, index):
        img = self.get_crop_row(index, row=True, col=True, isRow=True, append=True)
        gray_img = get_gray_img(img)
        binary = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        rows, cols = binary.shape

        # Получите основную ценность адаптивно
        # Определите горизонтальные линии:
        scale = int(rows - rows * 0.95)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows - scale))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_col = cv2.dilate(eroded, kernel, iterations=1)

        ys, xs = np.where(dilated_col > 0)
        x_point_arr = []
        sort_x_point = np.sort(xs)
        for i in range(len(sort_x_point) - 1):
            if sort_x_point[i + 1] - sort_x_point[i] > 10:
                x_point_arr.append(sort_x_point[i])
        # Чтобы добавить последнюю точку
        if len(sort_x_point):
            x_point_arr.append(sort_x_point[-1])
        return len(x_point_arr)

    def get_col_row(self, img):
        gray_img = get_gray_img(img)
        binary = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        rows, cols = binary.shape
        scale = 40

        # Получите основную ценность адаптивно
        # Определите горизонтальные линии:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_col = cv2.dilate(eroded, kernel, iterations=1)

        # Определите вертикальную линию:
        scale = 40
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_row = cv2.dilate(eroded, kernel, iterations=1)

        return dilated_col, dilated_row

    def get_col_row_array(self, img):
        dilated_col, dilated_row = self.get_col_row(img)

        # Объедините идентифицированные горизонтальные и вертикальные линии
        bitwise_and = cv2.bitwise_and(dilated_col, dilated_row)

        ys, xs = np.where(bitwise_and > 0)

        # Массив горизонтальных и вертикальных координат
        y_point_arr = []
        x_point_arr = []
        # При сортировке похожие пиксели исключаются, и берется только последняя точка с похожими значениями Это 10 -
        # это расстояние между двумя пикселями. Оно не фиксировано. Оно будет регулироваться в соответствии с разными
        # изображениями. Это в основном высота (переходы по координате y) и длина (переходы по координате x) таблицы
        # ячеек
        sort_x_point = np.sort(xs)
        for i in range(len(sort_x_point) - 1):
            if sort_x_point[i + 1] - sort_x_point[i] > 10:
                x_point_arr.append(sort_x_point[i])
        # Чтобы добавить последнюю точку
        if len(sort_x_point):
            x_point_arr.append(sort_x_point[-1])

        sort_y_point = np.sort(ys)
        for i in range(len(sort_y_point) - 1):
            if sort_y_point[i + 1] - sort_y_point[i] > 10:
                y_point_arr.append(sort_y_point[i])
        if len(sort_y_point):
            y_point_arr.append(sort_y_point[-1])
        return x_point_arr, y_point_arr

    def get_crop_row(self, index_i, index_j=None, col=False, row=False, isRow=False, append=False, save=False):
        if index_j is not None:
            x = int(self.x_arr[index_j])
            w = int(self.x_arr[index_j + 1])
        else:
            x = int(self.x_arr[0])
            w = int(self.x_arr[len(self.x_arr) - 1])
        y = int(self.y_arr[index_i])
        h = int(self.y_arr[index_i + 1])
        col_percent, row_percent = 0.90, 0.98
        if isRow:
            col_percent = 0.95
        crop_px_h = int((h - y) - (h - y) * col_percent)
        crop_px_w = int((w - x) - (w - x) * row_percent)

        if col:
            if append and not save:
                y = y + crop_px_h
                h = h - crop_px_h
            else:
                y = y - crop_px_h
                h = h + crop_px_h
        if row:
            if append:
                x = x - crop_px_w
                w = w + crop_px_w
            else:
                x = x + crop_px_w
                w = w - crop_px_w
        return self.img[y:h, x:w]

    def find_table(self):
        # Проверка на наличие таблицы и если таблица найдена, больше ли 3 столбцов в ней
        if len(self.x_arr) <= 4 or len(self.x_arr) == 0 or len(self.y_arr) == 0:
            return False
        else:
            return True

    def get_data_table(self):
        # Цикл координаты y, таблица разделения координат x
        data = []
        for i in range(len(self.y_arr) - 1):
            # Определяем число столбцов в строке и проверяем есть ли столбцы внутри строки:
            # если нет, то берем как направление
            if self.search_cols(i) == 2 and config['line_direction']:
                col_img = self.get_crop_row(i, row=True, isRow=True)
                self.direction = get_tesseract_text(col_img)
            # если есть, то читаем каждый столбец
            elif config['line_direction'] and self.direction is None:
                pass
            else:
                # Получаем строку для сохранения
                crop_row = self.get_crop_row(i, col=True, row=True, append=True, save=True)
                path_row_file = save_file(save_file_path, crop_row)
                print(path_row_file)
                data.append({'file': path_row_file})

                if config['line_direction']:
                    data[-1].update({'direction': self.direction})

                for j in range(len(self.x_arr) - 1):
                    col_img = self.get_crop_row(i, j, row=True)
                    text = get_tesseract_text(col_img)

                    col_key, col_number = get_key(config['cols'], j)
                    if col_key is not None and col_number is not None:
                        data[-1].update({f'{col_key}': text})

                print(data[-1])
                cv2.imshow(f'sub_pic_{i}', crop_row)
                cv2.waitKey(0)
        for item in data:
            print(item)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # pages = convert_from_path(f'protocol_clear.pdf', 120, poppler_path=poppler_path)
    pages = convert_from_path(f'Протокол с приложениями.pdf', 120, poppler_path=poppler_path)
    for i, page in enumerate(pages):
        if i >= 22:
            image = Image(cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR))
            if image.find_table():
                image.get_data_table()
