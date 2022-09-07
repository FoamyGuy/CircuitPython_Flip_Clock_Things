import board
from displayio import Group, TileGrid, Palette, Bitmap
import adafruit_imageload
import time

#CHANGE_ANIM_DELAY = 1 / 60
from flip_digit import FlipDigit

CHANGE_ANIM_DELAY = 0.02

static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

top_animation_spritesheet, top_animation_palette = adafruit_imageload.load("top_animation_sheet.bmp")
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load("bottom_animation_sheet.bmp")

digit = FlipDigit(
    static_spritesheet, static_palette,
    top_animation_spritesheet, top_animation_palette,
    bottom_animation_spritesheet, bottom_animation_palette,
    48, 50, anim_delay=0.025
)

digit.x = 100

main_group = Group()
main_group.append(digit)
board.DISPLAY.show(main_group)

for i in range(7):
    top_animation_palette.make_transparent(i)
    bottom_animation_palette.make_transparent(i)

while True:
    for i in range(10):
        digit.value = i
        time.sleep(1.0)
