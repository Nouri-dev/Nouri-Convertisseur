from PySide6 import QtWidgets, QtCore, QtGui
from controller.image_converter_controller import ConversionTask
from PySide6.QtGui import QAction


class ImageConvertUI(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.thread = None
        self.conversion_task = None
        self.prg_dialog = None
        self.lbl_quality = None
        self.spn_quality = None
        self.lbl_size = None
        self.spn_size = None
        self.lbl_dossierOut = None
        self.le_dossierOut = None
        self.lw_files = None
        self.btn_convert = None
        self.btn_browse_folder = None
        self.lbl_dropInfo = None
        self.main_layout = None
        self.setWindowTitle("😄NourConvertisseur😄")
        self.setup_ui()

    def create_widgets(self):
        self.lbl_quality = QtWidgets.QLabel("Qualité:")
        self.spn_quality = QtWidgets.QSpinBox()
        self.lbl_size = QtWidgets.QLabel("Taille:")
        self.spn_size = QtWidgets.QSpinBox()
        self.lbl_dossierOut = QtWidgets.QLabel("Chemin de sortie:")
        self.btn_browse_folder = QtWidgets.QPushButton("Parcourir")
        self.le_dossierOut = QtWidgets.QLineEdit()
        self.lw_files = QtWidgets.QListWidget()
        self.lbl_dropInfo = QtWidgets.QLabel("Déposez les images ici ^")
        self.btn_convert = QtWidgets.QPushButton("Conversion")

    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.lbl_quality, 0, 0, 1, 1)
        self.main_layout.addWidget(self.spn_quality, 0, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_size, 1, 0, 1, 1)
        self.main_layout.addWidget(self.spn_size, 1, 1, 1, 1)
        self.main_layout.addWidget(self.lbl_dossierOut, 2, 0, 1, 1)
        self.main_layout.addWidget(self.le_dossierOut, 2, 1, 1, 1)
        self.main_layout.addWidget(self.btn_browse_folder, 3, 0, 1, 1)
        self.main_layout.addWidget(self.lw_files, 4, 0, 1, 2)
        self.main_layout.addWidget(self.lbl_dropInfo, 5, 0, 1, 2)
        self.main_layout.addWidget(self.btn_convert, 6, 0, 1, 2)

    def modify_widgets(self):
        css_file = "/Chemin absolu vers le fichier/assets/style/style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

        self.spn_quality.setAlignment(QtCore.Qt.AlignRight)
        self.spn_size.setAlignment(QtCore.Qt.AlignRight)
        self.le_dossierOut.setAlignment(QtCore.Qt.AlignRight)

        self.spn_quality.setRange(1, 100)
        self.spn_quality.setValue(75)
        self.spn_size.setRange(1, 100)
        self.spn_size.setValue(50)

        self.le_dossierOut.setPlaceholderText("Choisir ou créer un dossier")
        self.le_dossierOut.setText("")
        self.le_dossierOut.setReadOnly(True)
        self.lbl_dropInfo.setVisible(True)

        self.setAcceptDrops(True)
        self.lw_files.setAlternatingRowColors(True)
        self.lw_files.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)

    def create_menu(self):
        menubar = QtWidgets.QMenuBar(self)
        file_menu = menubar.addMenu("Fichier")

        open_action = QAction("Ouvrir...", self)
        open_action.triggered.connect(self.browse_folder)
        file_menu.addAction(open_action)

        quit_action = QAction(" &Quitter", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        self.layout().setMenuBar(menubar)

    def setup_connections(self):
        QtGui.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_files, self.delete_selected_items)
        self.btn_convert.clicked.connect(self.start_image_conversion)
        self.btn_browse_folder.clicked.connect(self.browse_folder)

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.modify_widgets()
        self.create_menu()
        self.setup_connections()

    def start_image_conversion(self):
        quality = self.spn_quality.value()
        size = self.spn_size.value() / 100.0
        folder = self.le_dossierOut.text()

        if folder == "":
            msg_box = QtWidgets.QMessageBox()
            msg_box.warning(self, "Dossier de sortie manquant", "Veuillez choisir ou créer un dossier de sortie.")
            msg_box.exec()
            return

        lw_items = [self.lw_files.item(index) for index in range(self.lw_files.count())]
        images_a_convertir = [1 for lw_item in lw_items if not lw_item.processed]
        if not images_a_convertir:
            msg_box = QtWidgets.QMessageBox()
            msg_box.information(self, "Aucune image à convertir", "Toutes les images ont déjà été converties.")
            msg_box.exec()
            return

        self.thread = QtCore.QThread()

        self.conversion_task = ConversionTask(images_to_convert=lw_items, quality=quality, size=size, folder=folder)

        self.conversion_task.moveToThread(self.thread)
        self.conversion_task.image_converted.connect(self.image_converted)
        self.thread.started.connect(self.conversion_task.convert_images)
        self.conversion_task.finished.connect(self.thread.quit)
        self.conversion_task.conversion_finished.connect(self.hide_progress_dialog)

        self.thread.start()

        self.prg_dialog = QtWidgets.QProgressDialog("Conversion des images", "Annuler...", 1, len(images_a_convertir))
        self.prg_dialog.canceled.connect(self.cancel_conversion)
        self.prg_dialog.show()

    def hide_progress_dialog(self):
        if self.prg_dialog is not None:
            self.prg_dialog.hide()
            self.prg_dialog = None

    def cancel_conversion(self):
        self.conversion_task.runs = False
        self.thread.quit()

    def image_converted(self, lw_item, success):
        if success:
            lw_item.setIcon(self.ctx.img_checked)
            lw_item.processed = True
        else:
            lw_item.setIcon(self.ctx.img_cancel)
        self.prg_dialog.setValue(self.prg_dialog.value() + 1)

    def delete_selected_items(self):
        for lw_item in self.lw_files.selectedItems():
            row = self.lw_files.row(lw_item)
            self.lw_files.takeItem(row)

    def dragEnterEvent(self, event):
        self.lbl_dropInfo.setVisible(True)
        event.accept()

    def dragLeaveEvent(self, event):
        self.lbl_dropInfo.setVisible(False)

    def dropEvent(self, event):
        event.accept()
        for url in event.mimeData().urls():
            path = url.toLocalFile()

            if not path.lower().endswith(".jpg"):
                msg_box = QtWidgets.QMessageBox()
                msg_box.warning(self, "Fichier invalide",
                                "Seuls les fichiers avec une extension .jpg sont pris en charge.")
                msg_box.exec()
                return

            self.add_icone(path)

        self.lbl_dropInfo.setVisible(False)

    def add_icone(self, path):
        items = [self.lw_files.item(index).text() for index in range(self.lw_files.count())]
        if path not in items:
            lw_item = QtWidgets.QListWidgetItem(path)
            lw_item.setIcon(self.ctx.img_cancel)
            lw_item.processed = False
            self.lw_files.addItem(lw_item)

    def browse_folder(self):
        folder_dialog = QtWidgets.QFileDialog.getExistingDirectory(self, "Sélectionner un dossier de sortie")
        if folder_dialog:
            self.le_dossierOut.setText(folder_dialog)