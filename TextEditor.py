import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QAction, QFileDialog, QFontDialog, QColorDialog, QToolBar, QActionGroup,QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from datetime import datetime



class TextEditor(QMainWindow):
    ################konst ########
    def __init__(self):
        super().__init__()

        self.current_file = None  
        self.init_start_screen()
        self.init_clock()  
        self.stats_label = QLabel('', self)
        self.statusBar().addWidget(self.stats_label)
################ekran startowy#############
    def init_start_screen(self):    
        self.central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 30)
        self.clock_label = QLabel('', self)
        self.clock_label.setAlignment(Qt.AlignCenter)
        font = self.clock_label.font()
        font.setPointSize(50)  
        self.clock_label.setFont(font)
        layout.addWidget(self.clock_label)
        

        new_doc_button = QPushButton('Nowy dokument', self)
        new_doc_button.setShortcut('Ctrl+N')
        new_doc_button.clicked.connect(lambda: self.open_editor())######
        new_doc_button.setStyleSheet("font-size: 20px; padding: 10px 20px;")  


        load_button = QPushButton('Wczytaj', self)
        load_button.clicked.connect(self.open_file)
        load_button.setShortcut('Ctrl+O')
        load_button.setStyleSheet("font-size: 20px; padding: 10px 20px;")  

        welcome_label = QLabel('Witaj w programie text editor 3000', self)
        welcome_label.setAlignment(Qt.AlignCenter)  
        welcome_label.setStyleSheet("font-size: 30px;")  


        layout.addWidget(welcome_label)
        layout.addWidget(new_doc_button)
        layout.addWidget(load_button)
        

        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle('Strona główna')

        self.setGeometry(100, 100, 800, 600)
        self.show()
###########################licznik slow ##########################
    def update_text_stats(self):
        text = self.text_edit.toPlainText() 
        word_count = len(text.split())
        char_count = len(text)
        self.stats_label.setText(f'Słowa - {word_count}, Znaki - {char_count}')
        

#################################skróty do programu itp wiadomo##################################
    def init_text_edit_actions(self):
        

        undo_action = QAction('Cofnij', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)

        redo_action = QAction('Ponów', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit.redo)

       
        self.addAction(undo_action)
        self.addAction(redo_action)
############################### otworz w nowym oknie ######################
    def open_file_in_new_window(self):
        file_dialog, _ = QFileDialog.getOpenFileName(self, 'Otwórz plik')
        if file_dialog:
            new_window = TextEditor() 
            with open(file_dialog, 'r') as file:
                text = file.read()
                new_window.open_editor()  
                new_window.text_edit.setText(text)
                new_window.current_file = file_dialog
                new_window.setWindowTitle(file_dialog)  
                new_window.show()  
########################################otwieranie edytora glowny ################################
    def open_editor(self):
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("QTextEdit { margin: 25px; }")
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.text_edit.textChanged.connect(self.update_text_stats)
        self.setCentralWidget(self.text_edit)

        if not hasattr(self, 'menu_initialized'):
            self.init_menu_bar()
            self.menu_initialized = True

        if not hasattr(self, 'tool_bar_initialized'):
            self.init_tool_bar()
            self.init_format_toolbar()
            self.tool_bar_initialized = True

        self.init_text_edit_actions()

        self.setWindowTitle('Nowy dokument')  
        self.show()
######################################### wstawianie obrazu ##########################
    def insert_image(self):
        file_dialog, _ = QFileDialog.getOpenFileName(self, 'Wstaw obraz', filter="Obrazy (*.png *.jpg )")
        if file_dialog:
            image_label = QLabel(self)
            pixmap = QPixmap(file_dialog)
            pixmap = pixmap.scaledToWidth(300)  
            image_label.setPixmap(pixmap)
            cursor = self.text_edit.textCursor()
            cursor.insertHtml(f"<img src='{file_dialog}' alt='obraz'>")  
################################ #wszystko z zegarem ##################################
    def init_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  

    def update_clock(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.setText(f'{current_date}\n{current_time}')

        #self.central_widget.adjustSize()
#################### PASEK ZADAN ##########################
    def init_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Plik')

        new_action = QAction('Nowy', self)
        new_action.triggered.connect(lambda: self.open_editor())##########################
        new_action.setShortcut('Ctrl+N')

        file_menu.addAction(new_action)

        open_action = QAction('Otwórz', self)
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)

        open_in_new_window_action = QAction('Otwórz w nowym oknie', self)
        open_in_new_window_action.triggered.connect(self.open_file_in_new_window)
        file_menu.addAction(open_in_new_window_action)

        save_action = QAction('Zapisz', self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)

        self.menu_initialized = True
##############################MENU GORA##################
    def init_tool_bar(self):
        self.tool_bar = QToolBar('gora')
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar)
       
        font_button = QAction('Czcionka', self)
        font_button.triggered.connect(self.change_font)
        self.tool_bar.addAction(font_button)
        self.tool_bar.addSeparator()
        bold_button = QAction('Pogrubienie', self)
        bold_button.triggered.connect(self.toggle_bold)
        self.tool_bar.addAction(bold_button)
        self.tool_bar.addSeparator()
        italic_button = QAction('Kursywa', self)
        italic_button.triggered.connect(self.toggle_italic)
        self.tool_bar.addAction(italic_button)
        self.tool_bar.addSeparator()
        underline_button = QAction('Podkreślenie', self)
        underline_button.triggered.connect(self.toggle_underline)
        self.tool_bar.addAction(underline_button)
        self.tool_bar.addSeparator()
        font_color_action = QAction('Kolor czcionki', self)
        font_color_action.triggered.connect(self.change_font_color)
        self.tool_bar.addAction(font_color_action)
        self.tool_bar.addSeparator()
        insert_image_action = QAction('Wstaw obraz', self)
        insert_image_action.triggered.connect(self.insert_image)
        self.tool_bar.addAction(insert_image_action)

        
        
############################PASEK PO PRAWO#############################
    def init_format_toolbar(self):
        format_toolbar = QToolBar('prawo')
        self.addToolBar(Qt.RightToolBarArea, format_toolbar)
        
        

        alignment_group = QActionGroup(self)

        left_align_action = QAction('Wyrównaj do lewej', self)
        left_align_action.setCheckable(True)
        left_align_action.triggered.connect(lambda: self.set_alignment(Qt.AlignLeft))
        alignment_group.addAction(left_align_action)
        format_toolbar.addAction(left_align_action)
        
        center_align_action = QAction('Wyrównaj do środka', self)
        center_align_action.setCheckable(True)
        center_align_action.triggered.connect(lambda: self.set_alignment(Qt.AlignCenter))
        alignment_group.addAction(center_align_action)
        format_toolbar.addAction(center_align_action)

        right_align_action = QAction('Wyrównaj do prawej', self)
        right_align_action.setCheckable(True)
        right_align_action.triggered.connect(lambda: self.set_alignment(Qt.AlignRight))
        alignment_group.addAction(right_align_action)
        format_toolbar.addAction(right_align_action)

        justify_action = QAction('Wyjustuj', self)
        justify_action.setCheckable(True)
        justify_action.triggered.connect(lambda: self.set_alignment(Qt.AlignJustify))
        alignment_group.addAction(justify_action)
        format_toolbar.addAction(justify_action)

        self.alignment_group = alignment_group
################################ 
    #def new_file(self):
     #   self.open_editor()
####################################  
    def open_file(self):
        file_dialog, _ = QFileDialog.getOpenFileName(self, 'Otwórz plik')
        if file_dialog:
            self.open_editor()
            with open(file_dialog, 'r') as file:
                text = file.read()
                self.text_edit.setText(text)
                self.current_file = file_dialog
                self.setWindowTitle(file_dialog) 
####################################
    def save_file(self):
        if self.current_file is None:
            file_dialog, _ = QFileDialog.getSaveFileName(self, 'Zapisz plik', filter="Plik HTML (*.HTML)")
            if file_dialog:
                text = self.text_edit.toHtml()
                with open(file_dialog, 'w') as file:
                    file.write(text)
                    self.current_file = file_dialog
                    self.setWindowTitle(file_dialog)  
        else:
            text = self.text_edit.toHtml()
            with open(self.current_file, 'w') as file:
                file.write(text)
#################################### czcionka zmiana 
    def change_font(self):
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return

        font, ok = QFontDialog.getFont(self.text_edit.font(), self)
        if ok:
            selected_text = cursor.selection().toPlainText()  # Zapisanie zaznaczonego tekstu
            new_font = font  

            current_char_format = cursor.charFormat()
            current_font = current_char_format.font()

        
            new_font.setFamily(current_font.family())

            new_font.setBold(current_font.bold())
            new_font.setItalic(current_font.italic())
            new_font.setUnderline(current_font.underline())

            text_char_format = cursor.charFormat()
            text_char_format.setFont(new_font)

            cursor.mergeCharFormat(text_char_format)
            cursor.insertText(selected_text)  
#################################### pogrob 
    def toggle_bold(self): 
        text_char_format = self.text_edit.currentCharFormat()
        font = text_char_format.font()
        font.setBold(not font.bold())
        text_char_format.setFont(font)
        self.text_edit.mergeCurrentCharFormat(text_char_format)
#################################### kursywa
    def toggle_italic(self):
        text_char_format = self.text_edit.currentCharFormat()
        font = text_char_format.font()
        font.setItalic(not font.italic())
        text_char_format.setFont(font) 
        self.text_edit.mergeCurrentCharFormat(text_char_format)
#################################### podkres
    def toggle_underline(self):
        text_char_format = self.text_edit.currentCharFormat()
        text_char_format.setFontUnderline(not text_char_format.fontUnderline())
        self.text_edit.mergeCurrentCharFormat(text_char_format)
####################################kolor 
    def change_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_edit.setTextColor(color)
####################################
    def set_alignment(self, alignment):
        cursor = self.text_edit.textCursor()
        text_block_format = cursor.blockFormat()
        text_block_format.setAlignment(alignment)
        cursor.mergeBlockFormat(text_block_format)
####################################
    def closeEvent(self, event):
        if self.current_file is not None:
            reply = QMessageBox.question(self, 'Zakończ pracę',
                "Czy chcesz zapisać pracę przed zakończeniem?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save)

            if reply == QMessageBox.Save:
                self.save_file()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

        if self.current_file is None:
            reply = QMessageBox.question(self, 'Zakończ pracę',
                "Czy chcesz zapisać pracę przed zakończeniem?",
                QMessageBox.Save | QMessageBox.Discard ,
                QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save_file()
            elif reply == QMessageBox.Discard:
                event.accept()    
##############################    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())



