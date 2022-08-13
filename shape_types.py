import pygame
import graphics as graphics
import math


def change_to_square(shape, color, rect, real=False):
    shape.color = color
    shape.rect = rect
    shape.real = real


def draw_square(self):
    if self.real:
        pygame.draw.rect(self.game_graphics.screen.screen, self.color, self.rect)
        return None
    pos = self.game_graphics.camera.vr_to_real((self.rect[0], self.rect[1]))
    w = self.game_graphics.camera.zoom*self.rect[2]
    h = self.game_graphics.camera.zoom*self.rect[3]
    pygame.draw.rect(self.game_graphics.screen.screen, self.color, (pos[0], pos[1], w, h))


def move_square(self, movement):
    self.rect = (self.rect[0] + movement[0], self.rect[1] + movement[1], self.rect[2], self.rect[3])


square = graphics.Type("square", draw_square, move=move_square)
graphics.add_type(square)


def change_to_line(shape, start_point, end_point, color, width=1, real=False):
    shape.start_point = start_point
    shape.end_point = end_point
    shape.color = color
    shape.width = width
    shape.real = real


def draw_line(self):
    if self.real:
        pygame.draw.line(self.game_graphics.screen.screen, self.color, self.start_point, self.end_point, self.width)
        return None
    start_point = self.game_graphics.camera.vr_to_real(self.start_point)
    end_point = self.game_graphics.camera.vr_to_real(self.end_point)
    width = math.ceil(self.game_graphics.camera.zoom * self.width)
    pygame.draw.line(self.game_graphics.screen.screen, self.color, start_point, end_point, width)


def move_line(self, movement):
    self.start_point = (self.start_point[0] + movement[0], self.start_point[1] + movement[1])
    self.end_point = (self.end_point[0] + movement[0], self.end_point[1] + movement[1])


line = graphics.Type("line", draw_line, move=move_line)
graphics.add_type(line)


def change_to_circle(shape, center, radius, color, real=False):
    shape.center = center
    shape.radius = radius
    shape.color = color
    shape.real = real


def draw_circle(self):
    if self.real:
        pygame.draw.circle(self.game_graphics.screen.screen, self.color, self.center, self.radius)
        return None
    center = self.game_graphics.camera.vr_to_real(self.center)
    radius = self.game_graphics.camera.zoom * self.radius
    pygame.draw.circle(self.game_graphics.screen.screen, self.color, center, radius)


def move_circle(self, movement):
    self.center = (self.center[0] + movement[0], self.center[1] + movement[1])


circle = graphics.Type("circle", draw_circle, move=move_circle)
graphics.add_type(circle)


def change_to_image(shape, x, y, file_name, image=None, dimensions=None, real=False, load=True):
    shape.x = x
    shape.y = y
    shape.real = real
    shape.file_name = file_name

    if load:
        if not image:
            shape.image = pygame.image.load(file_name)
        else:
            shape.image = image

        shape.dimensions = dimensions
        if dimensions is not None:
            shape.image = pygame.transform.scale(shape.image, dimensions)
        else:
            shape.dimensions = (shape.image.get_width(), shape.image.get_height())
    else:
        shape.image = None
        shape.dimensions = (0, 0)

    shape.previous_zoom = 1


def draw_image(self):
    screen_rect = pygame.Rect(0, 0, self.game_graphics.screen.width, self.game_graphics.screen.height)
    image_rect = pygame.Rect(self.x, self.y, 200, 200)

    if self.real:
        if image_rect.colliderect(screen_rect):
            self.game_graphics.screen.screen.blit(self.image, (self.x, self.y))
        return None

    pos = self.game_graphics.camera.vr_to_real((self.x, self.y))
    image_rect = pygame.Rect(pos[0], pos[1], 200, 200)

    if self.previous_zoom != self.game_graphics.camera.zoom:
        self.previous_zoom = self.game_graphics.camera.zoom
        dimensions = (self.dimensions[0] * self.previous_zoom, self.dimensions[1] * self.previous_zoom)
        self.image = pygame.transform.scale(self.image, dimensions)
        image_rect = pygame.Rect(pos[0], pos[1], dimensions[0], dimensions[1])

    if image_rect.colliderect(screen_rect):
        self.game_graphics.screen.screen.blit(self.image, pos)


def move_image(self, movement):
    self.x += movement[0]
    self.y += movement[1]


image = graphics.Type("image", draw_image, move=move_image)
graphics.add_type(image)
