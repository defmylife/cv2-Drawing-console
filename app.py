import sys
import cv2
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import Qt, QLocale
from qt_material import apply_stylesheet
from rich import print
from rich.markdown import Markdown

# Set the locale to English
QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

class CV2PutTextTuner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('assets/app.ui', self)

        self.image = cv2.imread("assets/blank.png")  # Load a blank image
        self.text = "Hello, world!"
        self.font_face = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 18
        self.font_color = (0, 61, 255)
        self.font_bg_color = (234, 239, 255)
        self.position_x = 140
        self.position_y = 240
        self.thickness = 2

        self.w, self.h = 640, 480
        self.scale_up_ratio = 2.0
        self.scale_down_ratio = 0.5

        self.image_label : QLabel
        self.text_edit : QLineEdit
        self.font_face_combobox : QComboBox
        self.font_size_spinbox : QSpinBox
        self.thickness_spinbox : QSpinBox
        self.font_color_button : QPushButton
        self.bg_toggle_button : QCheckBox
        self.bg_color_button : QPushButton
        self.bg_padding_spinbox : QSpinBox

        # self.position_x_spinbox = QSpinBox()
        # self.position_y_spinbox = QSpinBox()

        self.setup_ui()
        self.update_image()

    def setup_ui(self):
        # layout = QVBoxLayout()
        # layout = self.putText.layout()

        self.image_label.setAlignment(Qt.AlignCenter)
        # layout.addWidget(self.image_label)

        # text_layout = QHBoxLayout()
        # text_layout.addWidget(QLabel("Text:"))
        # text_layout.addWidget(self.text_edit)
        self.text_edit.setText(self.text)
        self.text_edit.setFocusPolicy(Qt.ClickFocus)  # Set focus policy
        self.text_edit.textChanged.connect(self.set_text)
        # layout.addLayout(text_layout)

        # font_face_layout = QHBoxLayout()
        # font_face_layout.addWidget(QLabel("Font Face:"))
        self.font_face_combobox : QComboBox
        self.font_face_combobox.addItems(["FONT_HERSHEY_SIMPLEX", "FONT_HERSHEY_PLAIN", "FONT_HERSHEY_DUPLEX", "FONT_HERSHEY_COMPLEX", "FONT_HERSHEY_TRIPLEX", "FONT_HERSHEY_COMPLEX_SMALL", "FONT_HERSHEY_SCRIPT_SIMPLEX", "FONT_HERSHEY_SCRIPT_COMPLEX"])
        self.font_face_combobox.currentIndexChanged.connect(self.set_font_face)
        # font_face_layout.addWidget(self.font_face_combobox)
        # layout.addLayout(font_face_layout)

        # font_size_layout = QHBoxLayout()
        # font_size_layout.addWidget(QLabel("Font Size:"))
        self.font_size_spinbox.setFocusPolicy(Qt.ClickFocus)  # Set focus policy
        self.font_size_spinbox.setValue(self.font_size)
        self.font_size_spinbox.valueChanged.connect(self.set_font_size)
        # font_size_layout.addWidget(self.font_size_spinbox)
        # layout.addLayout(font_size_layout)

        # font_color_layout = QHBoxLayout()
        # font_color_layout.addWidget(QLabel("Font Color:"))
        self.font_color_button.clicked.connect(self.set_font_color)
        # font_color_layout.addWidget(self.font_color_button)
        # layout.addLayout(font_color_layout)

        # Add toggle button for text background
        # bg_toggle_layout = QHBoxLayout()
        # bg_toggle_layout.addWidget(QLabel("Toggle Font Background:"))
        # self.bg_toggle_button.setCheckable(True)
        self.bg_toggle_button.setChecked(True)
        self.bg_toggle_button.clicked.connect(self.toggle_background)
        # bg_toggle_layout.addWidget(self.bg_toggle_button)
        # self.putText.layout().addLayout(bg_toggle_layout, 4, 1)

        # Add button to choose text background color
        # font_bg_color_layout = QHBoxLayout()
        # font_bg_color_layout.addWidget(QLabel("Font Background Color:"))
        self.bg_color_button.clicked.connect(self.set_background_color)
        # font_bg_color_layout.addWidget(self.bg_color_button)
        # self.putText.layout().addLayout(font_bg_color_layout, 5, 1)

        # Add spin box for text background padding
        self.bg_padding_spinbox.setMinimum(0)
        self.bg_padding_spinbox.setMaximum(100)  # Adjust maximum as needed
        self.bg_padding_spinbox.setValue(20)  # Default padding value
        self.bg_padding_spinbox.valueChanged.connect(self.update_image)
        # padding_layout = QHBoxLayout()
        # padding_layout.addWidget(QLabel("Font Background Padding:"))
        # padding_layout.addWidget(self.bg_padding_spinbox)
        # self.putText.layout().addLayout(padding_layout, 6, 1)

        # thickness_layout = QHBoxLayout()
        # thickness_layout.addWidget(QLabel("Thickness:"))
        self.thickness_spinbox.setFocusPolicy(Qt.ClickFocus)  # Set focus policy
        self.thickness_spinbox.setValue(self.thickness)
        self.thickness_spinbox.valueChanged.connect(self.set_thickness)
        # thickness_layout.addWidget(self.thickness_spinbox)
        # self.putText.layout().addLayout(thickness_layout, 7, 1)

        # position_layout = QHBoxLayout()
        # position_layout.addWidget(QLabel("Position X:"))
        # self.position_x_spinbox.setMaximum(self.w)
        # self.position_x_spinbox.setFocusPolicy(Qt.ClickFocus)  # Set focus policy
        # self.position_x_spinbox.setValue(self.position_x)
        # self.position_x_spinbox.valueChanged.connect(self.set_position_x)
        # position_layout.addWidget(self.position_x_spinbox)
        # position_layout.addWidget(QLabel("Position Y:"))
        # self.position_y_spinbox.setMaximum(self.h)
        # self.position_y_spinbox.setFocusPolicy(Qt.ClickFocus)  # Set focus policy
        # self.position_y_spinbox.setValue(self.position_y)
        # self.position_y_spinbox.valueChanged.connect(self.set_position_y)
        # position_layout.addWidget(self.position_y_spinbox)
        # self.putText.layout().addLayout(position_layout, 8, 1)

        # self.setLayout(layout)


    def update_image(self):
        # image = self.image.copy()

        # Scale up the image
        scaled_up_image = cv2.resize(self.image, None, fx=self.scale_up_ratio, fy=self.scale_up_ratio, interpolation=cv2.INTER_LINEAR)

        ####Drawing pipeline####
        draw_image = self.draw(scaled_up_image)
        ####Drawing pipeline####

        # Scale down the image to fit label
        image = cv2.resize(draw_image, None, fx=self.scale_down_ratio, fy=self.scale_down_ratio, interpolation=cv2.INTER_LINEAR)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = image_rgb.shape
        self.w, self.h = w, h
        bytes_per_line = ch * w
        q_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def draw(self, image):
        print(Markdown("# Copy Code Here", style="blue bold"))
        code = f'text = "{self.text}"\nposition_x, position_y = {self.position_x, self.position_y}\n'

        # Draw text background if toggle is on
        if self.bg_toggle_button.isChecked():
            text_size, _ = cv2.getTextSize(self.text, self.font_face, self.font_size / 10, self.thickness)
            text_width, text_height = text_size

            # Add padding to text background
            padding = self.bg_padding_spinbox.value()
            cv2.rectangle(image, 
                        (self.position_x - padding, self.position_y + padding), 
                        (self.position_x + padding + text_width, self.position_y - text_height - padding), 
                        self.font_bg_color, 
                        -1,
                        )
            code += f'''
text_size, _ = cv2.getTextSize(text, {self.font_face}, {self.font_size / 10}, {self.thickness})
text_width, text_height = text_size

cv2.rectangle(img=image, 
            pt1=(position_x - {padding}, position_y + {padding}), 
            pt2=(position_x + text_width + {padding}, position_y - text_height - {padding}), 
            color={self.font_bg_color}, 
            thickness=-1,
            )'''

        # Draw text
        cv2.putText(image, 
                    self.text, 
                    (self.position_x, self.position_y), 
                    self.font_face, 
                    self.font_size / 10, 
                    self.font_color, 
                    self.thickness,
                    )

        code += f'''
cv2.putText(img=image, 
            text=text, 
            org=(position_x, position_y), 
            fontFace={self.font_face}, 
            fontScale={self.font_size / 10}, 
            color={self.font_color}, 
            thickness={self.thickness},
            )'''
        
        print(code)
        return image

    def set_text(self):
        self.text = self.text_edit.text()
        self.update_image()

    def set_font_face(self, index):
        font_faces = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX, cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, cv2.FONT_HERSHEY_SCRIPT_COMPLEX]
        self.font_face = font_faces[index]
        self.update_image()

    def set_font_size(self, size):
        self.font_size = size
        self.update_image()

    def set_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # Convert color to RGB format
            self.font_color = color.getRgb()[:-1]  # Remove the alpha channel            
            self.font_color = self.font_color[::-1] # Convert RGB to BGR
            self.update_image()

    def toggle_background(self):
        self.update_image()

    def set_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # Convert color to RGB format
            self.font_bg_color = color.getRgb()[:-1]  # Remove the alpha channel    
            self.font_bg_color = self.font_bg_color[::-1] # Convert RGB to BGR
            self.update_image()

    def set_position_x(self, x):
        self.position_x = x
        self.update_image()

    def set_position_y(self, y):
        self.position_y = y
        self.update_image()

    def set_thickness(self, thickness):
        self.thickness = thickness
        self.update_image()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CV2PutTextTuner()

    # setup stylesheet
    apply_stylesheet(app, theme='light_orange.xml', 
                    #  css_file='style.qss'
                     )
    window.setWindowTitle("CV2 putText Parameters Tuner")
    window.show()
    sys.exit(app.exec_())
