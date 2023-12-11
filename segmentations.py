from abc import ABC, abstractmethod


class _PageMap(ABC):
    page_map = {
        4: [[4, 1], [2, 3]],
        8: [[8, 1, 5, 4], [2, 7, 3, 6]],
        16: [[16, 1, 4, 13, 9, 8, 5, 12], [10, 7, 6, 11, 15, 2, 3, 14]],
        32: [
            [20, 13, 12, 21, 29, 4, 5, 28, 32, 1, 8, 25, 17, 16, 9, 24],
            [22, 11, 14, 19, 27, 6, 3, 30, 26, 7, 2, 31, 23, 10, 15, 18],
        ],
        64: [
            [44, 21, 28, 37, 40, 25, 24, 41, 53, 12, 5, 60, 57, 8, 9, 56, 52, 13, 4, 61, 64, 1, 16, 49, 45, 20, 29,
             36, 33, 32, 17, 48
             ],
            [46, 19, 30, 35, 34, 31, 18, 47, 51, 14, 3, 62, 63, 2, 15, 50, 54, 11, 6, 59, 58, 7, 10, 55, 43, 22, 27,
             38, 39, 26, 23, 42,
             ],
        ],
        12: [[12, 1, 9, 4, 8, 5], [2, 11, 3, 10, 6, 7]],
        24: [
            [24, 1, 12, 13, 21, 4, 9, 16, 20, 5, 8, 17],
            [14, 11, 2, 23, 15, 10, 3, 22, 18, 7, 6, 19],
        ],
    }

    rotation_matrix = {
        4: [[0, 0], [0, 0]],
        8: [[0, 0, 1, 1], [0, 0, 1, 1]],
        16: [[0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1]],
        32: [[], []],
        64: [[], []],
        12: [[], []],
        24: [[], []]
    }

    def __init__(self, mapping: int, final_page_format: list[float, float], print_page_format: list[float, float]):
        self._mapping = mapping
        self._final_page_format = final_page_format
        self._print_page_format = print_page_format
        self._coords = self.calc_coords()

    def calc_coords(self):
        total_pages = len(self.page_map[self._mapping][0])
        pages_per_row = int(len(self.page_map[self._mapping][0]) / 2)
        if pages_per_row > 1:
            coords = []
            for r in range(1, -1, -1):
                for x in range(0, pages_per_row):
                    coords.append([x * self._final_page_format[0], r * self._final_page_format[1]])
        else:
            coords = [[0.0, 0.0], [self._final_page_format[0], 0.0]]
        return coords

    @property
    @abstractmethod
    def mapping_front(self):
        return self.page_map[self._mapping][0]

    @property
    @abstractmethod
    def mapping_back(self):
        return self.page_map[self._mapping][1]

    @property
    @abstractmethod
    def rotation_front(self):
        return self.rotation_matrix[self._mapping][0]

    @property
    @abstractmethod
    def rotation_back(self):
        return self.rotation_matrix[self._mapping][1]
    @property
    @abstractmethod
    def final_page_format(self):
        return self._final_page_format

    @property
    @abstractmethod
    def print_page_format(self):
        return self._print_page_format

    @property
    @abstractmethod
    def get_coords(self):
        return self._coords


class S2x2(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(4, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S4x4(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(8, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().rotation_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S8x8(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(16, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S16x16(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(32, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S32x32(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(64, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S6x6(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(12, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords

class S12x12(_PageMap, ABC):
    def __init__(self, final_page_format, print_page_format):
        super().__init__(24, final_page_format, print_page_format)

    @property
    def mapping_front(self):
        return super().mapping_front

    @property
    def mapping_back(self):
        return super().mapping_back

    @property
    def rotation_front(self):
        return super().rotation_front

    @property
    def rotation_back(self):
        return super().mapping_back

    @property
    def final_page_format(self):
        return super().final_page_format

    @property
    def print_page_format(self):
        return super().print_page_format

    @property
    def get_coords(self):
        return super().get_coords