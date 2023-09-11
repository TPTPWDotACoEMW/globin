from PyQt6.QtGui import QImage, QPainter, QColor
import math

class TowerRenderer:
    def __init__(self, wog_dir):
        #TODO 2x images?
        self.ball_image   = QImage(wog_dir + "/game/res/balls/Drained/body.png")
        self.strand_image = QImage(wog_dir + "/game/res/balls/Drained/spring_goo.png")
        self.ground_image = QImage(wog_dir + "/game/res/levels/wogcd/groundTile.png")
        self.sky_image    = QImage(wog_dir + "/game/res/levels/wogcd/skytile.png")

        #Balls need to be nudged so they are centered on the given position.
        self.ball_nudge_x = -(self.ball_image.width()  // 2)
        self.ball_nudge_y = -(self.ball_image.height() // 2)

        #Strands need to be drawn with origin on their start point, and stretched
        self.strand_height   = self.strand_image.height()
        self.strand_x_offset = -(self.strand_image.width() // 2)

        self.world_scale_to_pixels = 2

    def render_tower(self, tower):
        bound_left   = 0
        bound_right  = 0
        bound_bottom = 0
        bound_top    = 0

        for ball in tower.balls:
            if ball.in_structure:
                bound_left   = min(bound_left,   ball.x_pos)
                bound_right  = max(bound_right,  ball.x_pos)
                bound_bottom = min(bound_bottom, ball.y_pos)
                bound_top    = max(bound_top,    ball.y_pos)
        
        padding_x = 0
        padding_y = 0

        tower_width  = (bound_right - bound_left)   / self.world_scale_to_pixels
        tower_height = (bound_top   - bound_bottom) / self.world_scale_to_pixels

        tower_x_offset = -bound_left / self.world_scale_to_pixels
        tower_y_offset =  bound_top  / self.world_scale_to_pixels

        #Half a ball hangs off each side, so we add a full ball's width and shift accordingly
        tower_width    += self.ball_image.width()
        tower_height   += self.ball_image.height()
        tower_x_offset += self.ball_image.width() / 2
        tower_y_offset += self.ball_image.height() / 2

        tower_width    += padding_x * 2
        tower_height   += padding_y * 2
        tower_x_offset += padding_x
        tower_y_offset += padding_y

        tower_image = QImage(int(tower_width), int(tower_height), QImage.Format.Format_ARGB32_Premultiplied)
        tower_image.fill(QColor(0, 0, 0, 0))

        tower_painter = QPainter(tower_image)

        self.draw_strands(tower, tower_painter, tower_x_offset, tower_y_offset)
        self.draw_balls(tower, tower_painter, tower_x_offset, tower_y_offset)

        composed_image = self.draw_composed_image(tower_image)
        tower_painter.end()

        return composed_image        
    
    def draw_strands(self, tower, tower_painter, x_offset, y_offset):
        for strand in tower.strands:
            first_ball_x,  first_ball_y  = self.world_to_pixel_coords(strand.first_ball.x_pos,  strand.first_ball.y_pos,  x_offset, y_offset)
            second_ball_x, second_ball_y = self.world_to_pixel_coords(strand.second_ball.x_pos, strand.second_ball.y_pos, x_offset, y_offset)
            self.draw_strand(tower_painter, first_ball_x, first_ball_y, second_ball_x, second_ball_y)

    def draw_balls(self, tower, tower_painter, x_offset, y_offset):
        for ball in tower.balls:
            if ball.in_structure:
                ball_x, ball_y = self.world_to_pixel_coords(ball.x_pos, ball.y_pos, x_offset, y_offset)
                self.draw_ball(tower_painter, ball_x, ball_y)

    def world_to_pixel_coords(self, x, y, x_offset, y_offset):
        x2 = int(x / self.world_scale_to_pixels + x_offset)
        y2 = int(y_offset - y / self.world_scale_to_pixels)
        return x2, y2

    def draw_strand(self, tower_painter, start_x, start_y, end_x, end_y):
        strand_angle = math.atan2(end_y - start_y, end_x - start_x) - math.pi / 2
        strand_angle = math.degrees(strand_angle)

        scale_width  = end_x - start_x
        scale_height = end_y - start_y
        strand_length = math.sqrt(scale_width * scale_width + scale_height * scale_height)

        strand_scale = strand_length / self.strand_height

        #Draw the strand rotated and stretched
        tower_painter.translate(start_x, start_y)
        tower_painter.rotate(strand_angle)
        tower_painter.scale(1.0, strand_scale)

        tower_painter.drawImage(self.strand_x_offset, 0, self.strand_image)
        tower_painter.resetTransform()

    def draw_ball(self, tower_painter, ball_x, ball_y):
        tower_painter.drawImage(ball_x + self.ball_nudge_x, ball_y + self.ball_nudge_y, self.ball_image)

    def draw_composed_image(self, tower_image):
        composed_padding_x          = 40
        composed_padding_y          = 40 #Top only
        composed_skip_ground_height = 50

        width  = tower_image.width() + 2 * composed_padding_x
        height = tower_image.height() + self.ground_image.height() + self.ball_nudge_y + composed_padding_y - composed_skip_ground_height

        composed_image = QImage(width, height, QImage.Format.Format_ARGB32)
        composed_image.fill(QColor(0, 0, 0, 255))

        composed_image_painter = QPainter(composed_image)

        sky_y = 0
        while sky_y < height:
            sky_x = 0
            while sky_x < width:
                composed_image_painter.drawImage(sky_x, sky_y, self.sky_image)
                sky_x += self.sky_image.width()

            sky_y += self.sky_image.height()

        ground_x = 0
        ground_y = tower_image.height() + composed_padding_y + self.ball_nudge_y #Shift it back up so balls don't float midair
        while ground_x < width:
            composed_image_painter.drawImage(ground_x, ground_y, self.ground_image)
            ground_x += self.ground_image.width() - 1
        
        composed_image_painter.drawImage(composed_padding_x, composed_padding_y, tower_image)
        composed_image_painter.end()

        return composed_image