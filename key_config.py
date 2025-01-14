from abc import ABC, abstractmethod


class InputConfig(ABC):
    @abstractmethod
    def get_keyzone_layout():
        pass

    @abstractmethod
    def get_airzone_layout():
        pass


class Umiguri32KeyZone(InputConfig):
    def __init__(self):
        super().__init__()
        self._UMIGIRI_32_KEYZONE_LAYOUT = {
            31: "a",
            30: "1",
            29: "z",
            28: "q",
            27: "s",
            26: "2",
            25: "x",
            24: "w",
            23: "d",
            22: "3",
            21: "c",
            20: "e",
            19: "f",
            18: "4",
            17: "v",
            16: "r",
            15: "g",
            14: "5",
            13: "b",
            12: "t",
            11: "h",
            10: "6",
            9: "n",
            8: "y",
            7: "j",
            6: "7",
            5: "m",
            4: "u",
            3: "k",
            2: "8",
            1: "9",
            0: "i",
        }

        self._UMIGIRI_32_AIRZONE_LAYOUT = {
            0: "o",
            1: "0",
            2: "p",
            3: "l",
            4: ",",
            5: ".",
        }
    
    def get_keyzone_layout(self):
        return self._UMIGIRI_32_KEYZONE_LAYOUT

    def get_airzone_layout(self):
        return self._UMIGIRI_32_AIRZONE_LAYOUT
