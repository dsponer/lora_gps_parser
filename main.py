import cv2, requests, sys, os, serial
import math, random, io
import mercantile


# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.

class MapParams:
    def __init__(self):
        self.lat = 43.0286  # Координаты центра карты на старте. Задал координаты университета
        self.lon = 131.8929

        self.west = 131.8797
        self.south = 43.0227
        self.east = 131.9089
        self.north = 43.0373

        self.zoom = 16  # Масштаб карты на старте
        self.type = "map"  # Другие значения "sat", "sat,skl"

        self.tiles = list(mercantile.tiles(self.west, self.south, self.east, self.north, self.zoom))

        self.min_x = min([t.x for t in self.tiles])
        self.min_y = min([t.y for t in self.tiles])
        self.max_x = max([t.x for t in self.tiles])
        self.max_y = max([t.y for t in self.tiles])

        self.bounds = {
            "west": min([mercantile.bounds(t).west for t in self.tiles]),
            "east": max([mercantile.bounds(t).east for t in self.tiles]),
            "south": min([mercantile.bounds(t).south for t in self.tiles]),
            "north": max([mercantile.bounds(t).north for t in self.tiles]),
        }

    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    # Создание карты с соответствующими параметрами.
    def load_map(self):

        # tiles = list(mercantile.tiles(self.west, self.south, self.east, self.north, self.zoom))
        #
        # self.min_x = min([t.x for t in tiles])
        # self.min_y = min([t.y for t in tiles])
        # self.max_x = max([t.x for t in tiles])
        # self.max_y = max([t.y for t in tiles])
        #
        # self.bounds = {
        #     "west": min([mercantile.bounds(t).west for t in tiles]),
        #     "east": max([mercantile.bounds(t).east for t in tiles]),
        #     "south": min([mercantile.bounds(t).south for t in tiles]),
        #     "north": max([mercantile.bounds(t).north for t in tiles]),
        # }
        # # https://yandex.ru/maps/?ll=131.895499%2C43.028739&z=16.07
        # map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=self.ll(), z=self.zoom,
        #                                                                                 type=self.type)
        # response = requests.get(map_request)
        # if not response:
        #     print("Ошибка выполнения запроса:")
        #     print(map_request)
        #     print("Http статус:", response.status_code, "(", response.reason, ")")
        #     sys.exit(1)
        #
        # # Запись полученного изображения в файл.
        # map_file = "map.png"
        # try:
        #     with open(map_file, "wb") as file:
        #         file.write(response.content)
        # except IOError as ex:
        #     print("Ошибка записи временного файла:", ex)
        #     sys.exit(2)
        # return map_file
        return

    def parse_coordinate(self, size_im, coordinate):
        scale = 6324
        h, w = size_im[:2]
        y, x = coordinate
        x, y = mercantile.xy(y, x)
        # рассчитываем координаты углов в веб-меркаторе
        leftTop = mercantile.xy(self.bounds['west'], self.bounds['north'])
        rightBottom = mercantile.xy(self.bounds['east'], self.bounds['south'])

        # расчитываем коэффициенты
        kx = h / (rightBottom[0] - leftTop[0])
        ky = w / (rightBottom[1] - leftTop[1])

        x = (x - leftTop[0]) * kx * 1.24
        y = (y - leftTop[1]) * ky * 0.76

        print(x, y)
        return int(abs(x)), int(abs(y))

    def map_coordinate(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def convert2float(self, value_str):
        value_str = value_str[2].split(';')




def main():
    # Инициализируем pygame
    cv2.namedWindow('test')
    mp = MapParams()
    # Создаем файл
    ser = serial.Serial(port="/dev/cu.usbserial-14310", baudrate="9600")
    while True:
        data = str()
        while ser.inWaiting() > 0:
            line = ser.readline()
            if line:
                data = line.decode().strip().split()
        if len(data) == 3:
            data = data[2].split(';')
            lon, lat = mp.convert2float(data[0]), mp.convert2float(data[1])

        coordinate = lon, lat

        im = cv2.imread('map.png')
        size_im = im.shape

        coordinate = mp.parse_coordinate(size_im, coordinate)

        cv2.circle(im, (size_im[1] // 2, size_im[0] // 2), 3, (0, 0, 255), -1)
        cv2.circle(im, coordinate, 3, (255, 0, 0), -1)

        # Рисуем картинку, загружаемую из только что созданного файла.
        cv2.imshow('test', im)
        #
        # mp.change_coordinate(0.1, 0.1)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    # Удаляем файл с изображением.
    # os.remove(map_file)


if __name__ == "__main__":
    main()
