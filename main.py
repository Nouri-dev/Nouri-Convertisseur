import sys
from view.image_converter_ui import ImageConvertUI
from PySide6.QtWidgets import QApplication
from utils.icone import IconeConvert


class AppContext(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.icones = IconeConvert()

    def run(self):
        mainInterface = ImageConvertUI(ctx=self)
        mainInterface.resize(int(1920 / 4), int(1200 / 2))
        mainInterface.show()
        return self.exec()

    @property
    def img_checked(self):
        return self.icones.img_checked

    @property
    def img_cancel(self):
        return self.icones.img_cancel


if __name__ == '__main__':
    app = AppContext(sys.argv)
    sys.exit(app.run())
