import os

import cv2
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes

from utils import get_gray_img, save_file, get_tesseract_text, clear_img_for_color, get_config_keys, get_key, \
    get_tesseract_number

poppler_path = r'poppler-0.68.0/bin'

if not os.path.exists('static'):
    os.mkdir('static')

save_file_path = r'static'

config_first = {
    'file_path': f'Протокол с приложениями.pdf',
    'tables': [
        {
            'page_start': '6',
            'page_end': '22',
            'line_direction': False,
            'is_winner': False,
            'identifier': 'inn',
            'cols': {
                'direction': 4,
                'org_name': 2,
                'project_name': 5,
            },
            'cols_number': {
                'ball': None,
                'sum_pay': None,
                'request_sum_pay': 7,
                'inn': 6,
            }
        },
        {
            'page_start': '23',
            'page_end': '38',
            'line_direction': True,
            'is_winner': True,
            'identifier': 'inn',
            'cols': {
                'direction': None,
                'org_name': 2,
                'project_name': 5,
            },
            'cols_number': {
                'ball': 6,
                'sum_pay': None,
                'request_sum_pay': None,
                'inn': 4,
            }
        },
        {
            'page_start': '39',
            'page_end': '47',
            'line_direction': True,
            'is_winner': True,
            'identifier': 'inn',
            'cols': {
                'direction': None,
                'org_name': 2,
                'project_name': 5,
            },
            'cols_number': {
                'ball': 6,
                'sum_pay': 7,
                'request_sum_pay': None,
                'inn': 4,
            }
        }]
}

config_two = {
    'file_path': f'Протокол конкурсной комиссии от 11.08.2021.pdf',
    'tables': [{
        'page_start': '17',
        'page_end': '20',
        'line_direction': True,
        'is_winner': False,
        'identifier': 'ogrn',
        'cols': {
            'direction': None,
            'org_name': 4,
            'project_name': 3,
        },
        'cols_number': {
            'ball': 6,
            'sum_pay': 7,
            'request_sum_pay': None,
            'inn': None,
            'ogrn': 5,
        }
    }]
}

config = config_two

for item in config['tables']:
    item['cols'] = get_config_keys(item['cols'])
    item['cols_number'] = get_config_keys(item['cols_number'])


class Image:
    def __init__(self, img, config, page_num, result, identifier, direction):
        self.img = img
        self.config = config
        self.page_num = page_num
        self.result = result
        self.identifier = identifier

        self.height, self.weight = self.img.shape[:2]

        cols, rows = self.get_col_row(self.img)

        self.img = self.rotate_img(cols + rows)

        self.img_clear = clear_img_for_color(self.img)
        self.x_arr, self.y_arr = self.get_col_row_array(self.img_clear)

        self.direction = direction

    def rotate_img(self, img):
        counters, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = (self.weight // 2, self.height // 2)
        # angle = 0
        c = max(counters, key=cv2.contourArea)
        _, params, angle = cv2.minAreaRect(c)

        # for item in counters:
        #     if len(item) >= 2:
        #         # print(cv2.contourArea(item))
        #         _, params, angle_local = cv2.minAreaRect(item)
        #         if (
        #                 ((self.height - self.height * 0.45) <= params[0] <= self.height)
        #                 and ((self.weight - self.weight * 0.45) <= params[1] <= self.weight)
        #         ):
        #             angle = angle_local
        #             break
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
        eroded = cv2.erode(binary, kernel, iterations=3)
        dilated_col = cv2.dilate(eroded, kernel, iterations=2)

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

    def get_col_row(self, img, duplicate=False):
        gray_img = get_gray_img(img)
        binary = cv2.adaptiveThreshold(~gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        rows, cols = binary.shape
        scale = 30

        # Получите основную ценность адаптивно
        # Определите горизонтальные линии:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_col = cv2.dilate(eroded, kernel, iterations=1)

        # Определите вертикальную линию:
        scale = 30
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilated_row = cv2.dilate(eroded, kernel, iterations=1)
        # TODO: Может быть нужно будет удалить
        new_img = dilated_col + dilated_row

        if not duplicate:
            contours, hierarchy = cv2.findContours(new_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(new_img, contours, -1, (255, 0, 0), 2, cv2.LINE_AA, hierarchy, 0)
            self.get_col_row(new_img, True)
        ###

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

        for i in range(len(self.y_arr) - 1):
            # Определяем число столбцов в строке и проверяем есть ли столбцы внутри строки:
            # если нет, то берем как направление
            if self.search_cols(i) == 2 and self.config['line_direction']:
                col_img = self.get_crop_row(i, row=True, isRow=True)
                self.direction = get_tesseract_text(col_img)
            # если есть, то читаем каждый столбец
            elif self.config['line_direction'] and self.direction is None:
                pass
            else:
                data = {}
                # Получаем строку для сохранения
                crop_row = self.get_crop_row(i, col=True, row=True, append=True, save=True)

                path_row_file = save_file(save_file_path, crop_row)
                print(path_row_file)
                data.update({'file': [path_row_file], 'page_num': self.page_num, 'is_winner': self.config['is_winner']})

                if self.config['line_direction']:
                    data.update({'direction': self.direction})
                for j in range(len(self.x_arr) - 1):
                    col_img = self.get_crop_row(i, j, row=True)

                    col_key, col_number = get_key(self.config['cols'], j)
                    if col_key is not None and col_number is not None:
                        data.update({f'{col_key}': get_tesseract_text(col_img)})

                    col_key, col_number = get_key(self.config['cols_number'], j)
                    if col_key is not None and col_number is not None:
                        data.update({f'{col_key}': get_tesseract_number(col_img)})

                is_sequel = False
                if data[self.config['identifier']] == '':
                    is_sequel = True
                    self.result[-1]['file'].append(data['file'][0])
                    del data['file']
                    # self.result[-1].update({'file': self.result[-1]['file'].append(data['file'][0])})
                    for item in data:
                        if data[item] != '':
                            self.result[-1].update({item: f'{self.result[-1][item]} {data[item]}'})

                if not is_sequel:
                    self.result.append(data)

                print(data)


if __name__ == '__main__':
    pages = convert_from_path(config['file_path'], 120, poppler_path=poppler_path)
    result = []
    for conf in config['tables']:
        direction = None
        start_page, end_page = int(conf['page_start']) - 1, int(conf['page_end']) - 1
        for i, page in enumerate(pages):
            if start_page <= i <= end_page:
                image = Image(cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR), conf, i + 1, result,
                              config['identifier'], direction)
                if image.find_table():
                    image.get_data_table()
                    result = image.result
                    direction = image.direction
                print(i + 1, result)
