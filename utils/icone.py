from PySide6 import QtGui
from utils.ressource_path import RessourcePath
from utils.cached_property import CachedProperty


class IconeConvert:

    @CachedProperty()
    def img_checked(self):
        return QtGui.QIcon(RessourcePath.get_resource("/Chemin absolu vers le fichier/assets/images/check.png"))

    @CachedProperty()
    def img_cancel(self):
        return QtGui.QIcon(RessourcePath.get_resource("/Chemin absolu vers le fichier/assets/images/cancel.png"))