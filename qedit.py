from PyQt5 import QtWidgets, QtCore         # импорт ядра и винджетов
from PyQt5.QtWidgets import *       # импорт виджетов
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *
import sys

# CSS стили
css_style = '''
* {
font-family: sans-serif;
font-size: 15px;
}
'''
textedit_css = '''
font-family: sans-serif;
font-size: 16px;
'''
dark_theme = '''
background: #242424;
color: white;
'''
light_theme = '''
background: lightgray;
color: black;
'''


class Window(QMainWindow):
    """ Класс окна """
    def __init__(self):
        """ Инициадизация окна при создании """
        super(Window, self).__init__()      # наследуем класс

        # Настройки окна
        self.setWindowTitle('QEdit GNU')
        self.setGeometry(300, 250, 350, 200)
        self.setStyleSheet(css_style)

        # Виджеты
        self.menu_bar = QMenuBar(self)
        self.fontSizeBox = QSpinBox()
        self.edit_text = QtWidgets.QTextEdit(self)
        font = QFont('Times', 24)
        self.edit_text.setFont(font)
        self.path = ""
        self.setCentralWidget(self.edit_text)
        self.showMaximized()
        self.edit_text.setFontPointSize(24)

        self.createToolBar()
        self.setCentralWidget(self.edit_text)
        self.edit_text.setStyleSheet(textedit_css)

        # Меню
        self.createMenuBar()

    def setFontSize(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)

    def setFont(self):
        font = self.fontBox.currentText()
        self.editor.setCurrentFont(QFont(font))

    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not (state))

    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not (state))

    def boldText(self):
        if self.editor.fontWeight != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)

    def createToolBar(self):
        """ Создание бара инструментов """
        toolbar = QToolBar()

        undoBtn = QAction(QIcon('undo.png'), 'undo', self)
        undoBtn.triggered.connect(self.edit_text.undo)
        toolbar.addAction(undoBtn)

        redoBtn = QAction(QIcon('redo.png'), 'redo', self)
        redoBtn.triggered.connect(self.edit_text.redo)
        toolbar.addAction(redoBtn)

        copyBtn = QAction(QIcon('copy.png'), 'copy', self)
        copyBtn.triggered.connect(self.edit_text.copy)
        toolbar.addAction(copyBtn)

        cutBtn = QAction(QIcon('cut.png'), 'cut', self)
        cutBtn.triggered.connect(self.edit_text.cut)
        toolbar.addAction(cutBtn)

        pasteBtn = QAction(QIcon('paste.png'), 'paste', self)
        pasteBtn.triggered.connect(self.edit_text.paste)
        toolbar.addAction(pasteBtn)

        self.fontBox = QComboBox(self)
        self.fontBox.addItems(
            ["Courier Std", "Hellentic Typewriter Regular", "Helvetica", "Arial", "SansSerif", "Helvetica", "Times",
             "Monospace"])
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)

        self.fontSizeBox.setValue(24)
        self.fontSizeBox.valueChanged.connect(self.setFontSize)
        toolbar.addWidget(self.fontSizeBox)

        rightAllign = QAction(QIcon('right-align.png'), 'Right Allign', self)
        rightAllign.triggered.connect(lambda: self.edit_text.setAlignment(Qt.AlignRight))
        toolbar.addAction(rightAllign)

        leftAllign = QAction(QIcon('left-align.png'), 'left Allign', self)
        leftAllign.triggered.connect(lambda: self.edit_text.setAlignment(Qt.AlignLeft))
        toolbar.addAction(leftAllign)

        centerAllign = QAction(QIcon('center-align.png'), 'Center Allign', self)
        centerAllign.triggered.connect(lambda: self.edit_text.setAlignment(Qt.AlignCenter))
        toolbar.addAction(centerAllign)

        toolbar.addSeparator()

        boldBtn = QAction(QIcon('bold.png'), 'Bold', self)
        boldBtn.triggered.connect(self.boldText)
        toolbar.addAction(boldBtn)

        underlineBtn = QAction(QIcon('underline.png'), 'underline', self)
        underlineBtn.triggered.connect(self.underlineText)
        toolbar.addAction(underlineBtn)

        italicBtn = QAction(QIcon('italic.png'), 'italic', self)
        italicBtn.triggered.connect(self.italicText)
        toolbar.addAction(italicBtn)

        self.addToolBar(toolbar)

    def createMenuBar(self):
        """ Этот метод создает меню """
        self.setMenuBar(self.menu_bar)

        # Меню файла
        file_menu = QMenu("&Файл", self)
        self.menu_bar.addMenu(file_menu)

        file_menu.addAction('Открыть', self.action_menu)
        file_menu.addAction('Сохранить', self.action_menu)

    @QtCore.pyqtSlot()
    def action_menu(self):
        """ Действия для меню """
        action = self.sender().text()

        """ Проверка действия """
        if action == 'Открыть':
            filename = QFileDialog.getOpenFileName(self)[0]

            try:
                with open(filename, 'r') as file:
                    self.edit_text.setText(file.read())
            except Exception as ex:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Произошла ошибка при открытии файла")
                msg.setInformativeText(f'Ошибка: {ex}')
                msg.setWindowTitle("QEdit Ошибка")
                msg.exec_()
        elif action == 'Сохранить':
            filename = QFileDialog.getSaveFileName(self)[0]

            try:
                with open(filename, 'w') as file:
                    file.write(self.edit_text.toPlainText())
            except Exception as ex:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Произошла ошибка при открытии файла")
                msg.setInformativeText(f'Ошибка: {ex}')
                msg.setWindowTitle("QEdit Ошибка")
                msg.exec_()


def application():
    """ Конфигурация окна и приложение """
    app = QApplication(sys.argv)
    window = Window()

    """ Старт приложения """
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    """ Если этот файл запускается главным """
    application()
