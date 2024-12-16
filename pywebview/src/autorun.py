# TODO добавить логику включения/выключения автозапуска
class Autorun:
    def __init__(self):
        self.__autorun = False
    
    def set_autorun(self, flag: bool):
        self.__autorun = flag
    
    def get_autorrun(self) -> bool:
        return self.__autorun