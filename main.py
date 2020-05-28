import cv2, requests, sys, os


# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.

class MapParams:
    def __init__(self):
        self.lat = 43.029910  # Координаты центра карты на старте. Задал координаты университета
        self.lon = 131.892108
        self.zoom = 15 # Масштаб карты на старте. Изменяется от 1 до 19
        self.type = "map"  # Другие значения "sat", "sat,skl"

    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def change_coordinate(self, x, y):
        self.lat += x
        self.lon += y


# Создание карты с соответствующими параметрами.
def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file


def main():
    # Инициализируем pygame
    cv2.namedWindow('test')
    mp = MapParams()
    while True:

        # Создаем файл
        map_file = load_map(mp)
        im = cv2.imread(map_file)
        shape_im = im.shape

        cv2.circle(im, (shape_im[1] // 2, shape_im[0] // 2), 1, (0, 0, 255), -1)
        # Рисуем картинку, загружаемую из только что созданного файла.
        cv2.imshow('test', im)
        #
        # mp.change_coordinate(0.1, 0.1)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    # Удаляем файл с изображением.
    os.remove(map_file)


if __name__ == "__main__":
    main()


