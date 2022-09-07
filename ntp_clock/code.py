import board
from displayio import Group, TileGrid, Palette, Bitmap
import adafruit_imageload
import time
import socketpool
import wifi
import adafruit_ntp
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
from flip_clock import FlipClock


wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=-5)

cur_time = ntp.datetime


CHANGE_ANIM_DELAY = 0.02

display = board.DISPLAY

static_spritesheet, static_palette = adafruit_imageload.load("static_sheet.bmp")
static_palette.make_transparent(0)

top_animation_spritesheet, top_animation_palette = adafruit_imageload.load("grey_top_animation_sheet.bmp")
bottom_animation_spritesheet, bottom_animation_palette = adafruit_imageload.load("grey_bottom_animation_sheet.bmp")

# digit = FlipDigit(
#     static_spritesheet, static_palette,
#     top_animation_spritesheet, top_animation_palette,
#     bottom_animation_spritesheet, bottom_animation_palette,
#     64, 55, anim_delay=0.0251, transparent_indexes=range(11),
#     brighter_level=0.99, darker_level=0.5, medium_level=0.90
# )
#
# digit.x = 100

clock = FlipClock(
    static_spritesheet, static_palette,
    top_animation_spritesheet, top_animation_palette,
    bottom_animation_spritesheet, bottom_animation_palette,
    48, 50, anim_delay=0.01, transparent_indexes=range(11),
    brighter_level=0.99, darker_level=0.5, medium_level=0.90
)
clock.y = 0
clock.anchor_point = (0.5, 0.5)
clock.anchored_position = (display.width//2, display.height//2)
#


main_group = Group()
main_group.append(clock)
board.DISPLAY.show(main_group)

# clock.first_pair = str(cur_time.tm_hour)
# clock.second_pair = str(cur_time.tm_minute)

while True:
    # cur_val = clock.first_pair
    # next_val = int(cur_val) + 1
    # clock.first_pair = str(next_val)
    #
    # cur_val = clock.second_pair
    # next_val = int(cur_val) + 1
    # clock.second_pair = str(next_val)
    # time.sleep(0.5)

    cur_time = ntp.datetime
    clock.first_pair = str(cur_time.tm_hour)
    clock.second_pair = str(cur_time.tm_min)
    time.sleep(10)

