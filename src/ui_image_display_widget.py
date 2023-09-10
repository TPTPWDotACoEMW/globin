from PyQt6.QtCore import Qt, QRect, QPoint, QPointF, QSize, QStandardPaths
from PyQt6.QtWidgets import QWidget, QMenu, QFileDialog
from PyQt6.QtGui import QPixmap, QWheelEvent, QGuiApplication, QAction
from .ui.image_display_widget import Ui_image_display_widget
import math

class ImageDisplayWidget(QWidget):
    def __init__(self, image_to_display):
        super(QWidget, self).__init__()

        self.ui = Ui_image_display_widget()
        self.ui.setupUi(self)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.displayed_image = QPixmap.fromImage(image_to_display)

        image_width  = image_to_display.width()
        image_height = image_to_display.height()

        min_scaled_width  = 200
        min_scaled_height = 300
        min_image_scale = min(min_scaled_width / image_width, min_scaled_height / image_height)

        min_image_scale = min(min_image_scale, 1)
        self.ui.labelImage.setMinimumSize(image_width * min_image_scale, image_height * min_image_scale)

        self.ui.labelImage.setPixmap(self.displayed_image)

        #Max zoom level => image is 3x size the screen
        screen_size = QGuiApplication.primaryScreen().size()
        max_zoom_factor = 3 * max(screen_size.width() / image_width, screen_size.height() / image_height)

        self.min_zoom_level = 0
        self.max_zoom_level = math.log2(max_zoom_factor)
        
        #Make initial zoom level as small as it can be (it'll clamp to the closest normal value in resizeEvent)
        self.zoom_level  = -float('inf')
        self.crop_center = QPointF(image_width / 2, image_height / 2)

        #Initial window size: fit image 1:1 unless window gets bigger than 75% of screen size 
        initial_window_max_size = screen_size * 0.75
        initial_image_scale = min(initial_window_max_size.width() / image_width, initial_window_max_size.height() / image_height)
        initial_image_scale = min(initial_image_scale, 1)

        initial_window_size = QSize(image_width * initial_image_scale, image_height * initial_image_scale)

        self.prev_mouse_pos = QPoint(0, 0)

        self.crop_rect = QRect(QPoint(0, 0), initial_window_size)
        self.resize(initial_window_size)

    def resizeEvent(self, event):
        #Min zoom level => image fits into the window
        min_zoom_factor = min(self.ui.labelImage.width() / self.displayed_image.width(), self.ui.labelImage.height() / self.displayed_image.height())
        self.min_zoom_level = math.log2(min_zoom_factor)
        self.min_zoom_level = min(self.min_zoom_level, 0)

        self.zoom_level = max(self.min_zoom_level, self.zoom_level)
        self.update_image()

        return super().resizeEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        image_size        = self.ui.labelImage.pixmap().size()
        image_margin_size = self.ui.labelImage.size() - image_size
        image_rect        = QRect(image_margin_size.width() // 2, image_margin_size.height() // 2, image_size.width(), image_size.height())
        
        if not image_rect.contains(int(event.position().x()), int(event.position().y())):
            return

        normalized_event_x = (event.position().x() - image_rect.left()) / image_rect.width()
        normalized_event_y = (event.position().y() - image_rect.top())  / image_rect.height()
        
        old_zoom_level = self.zoom_level

        self.zoom_level += 0.001 * event.angleDelta().y()
        self.zoom_level = max(self.zoom_level, self.min_zoom_level)
        self.zoom_level = min(self.zoom_level, self.max_zoom_level)

        if self.zoom_level > old_zoom_level:
            self.crop_center.setX(self.crop_rect.x() + normalized_event_x * self.crop_rect.width())
            self.crop_center.setY(self.crop_rect.y() + normalized_event_y * self.crop_rect.height())

        self.update_image()

        return super().wheelEvent(event)
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta_x = event.pos().x() - self.prev_mouse_pos.x()
            delta_y = event.pos().y() - self.prev_mouse_pos.y()

            zoom_factor = 2 ** self.zoom_level

            delta_x = delta_x / zoom_factor
            delta_y = delta_y / zoom_factor

            self.crop_center.setX(self.crop_center.x() - delta_x)
            self.crop_center.setY(self.crop_center.y() - delta_y)

            self.update_image()
            
            self.prev_mouse_pos = event.pos()

        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.prev_mouse_pos = event.pos()

        return super().mousePressEvent(event)
    
    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        save_action = QAction("Save...", self)
        save_action.triggered.connect(self.save_image)
        context_menu.addAction(save_action)

        context_menu.exec(self.mapToGlobal(pos))

    def save_image(self):
        image_path_result = QFileDialog.getSaveFileName(self, "Select a file", QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation), "Images (*.png)")
        image_path = image_path_result[0]

        if len(image_path) != 0:
            self.displayed_image.save(image_path, "PNG")

    def update_image(self):
        zoom_factor = 2 ** self.zoom_level

        crop_width  = self.ui.labelImage.width()  / zoom_factor
        crop_height = self.ui.labelImage.height() / zoom_factor

        crop_width  = min(crop_width,  self.displayed_image.width())
        crop_height = min(crop_height, self.displayed_image.height())

        crop_width_half  = crop_width  / 2
        crop_height_half = crop_height / 2

        self.crop_center.setX(max(self.crop_center.x(), crop_width_half))
        self.crop_center.setX(min(self.crop_center.x(), self.displayed_image.width() - crop_width_half))

        self.crop_center.setY(max(self.crop_center.y(), crop_height_half))
        self.crop_center.setY(min(self.crop_center.y(), self.displayed_image.height() - crop_height_half))

        crop_left = int(self.crop_center.x() - crop_width_half)
        crop_top  = int(self.crop_center.y() - crop_height_half)

        crop_left   = max(crop_left, 0)
        crop_top    = max(crop_top,  0)
        crop_width  = min(crop_width,  self.displayed_image.width()  - crop_left)
        crop_height = min(crop_height, self.displayed_image.height() - crop_top)

        self.crop_rect = QRect(crop_left, crop_top, crop_width, crop_height)

        cropped_image = self.displayed_image.copy(self.crop_rect)
        self.ui.labelImage.setPixmap(cropped_image.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))   