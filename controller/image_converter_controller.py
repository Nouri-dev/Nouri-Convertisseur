from model.image_processor import ImageProcessor
from PySide6 import QtCore


class ConversionTask(QtCore.QObject):
    image_converted = QtCore.Signal(object, bool)
    finished = QtCore.Signal()
    conversion_finished = QtCore.Signal()

    def __init__(self, images_to_convert, quality, size, folder):
        super().__init__()
        self.images_to_convert = images_to_convert
        self.quality = quality
        self.size = size
        self.folder = folder
        self.runs = True

    @staticmethod
    def convert_images_list(paths, quality, size, folder):
        success_list = []
        image_processor = ImageProcessor()
        for path in paths:
            success = image_processor.image_reduce_convert(path, size, quality, folder)
            success_list.append(success)
        return success_list

    def convert_images(self):
        for image_lw_item in self.images_to_convert:
            if self.runs and not image_lw_item.processed:
                success_list = self.convert_images_list([image_lw_item.text()], self.quality, self.size, self.folder)
                success = success_list[0]
                self.image_converted.emit(image_lw_item, success)

        self.finished.emit()
        self.conversion_finished.emit()