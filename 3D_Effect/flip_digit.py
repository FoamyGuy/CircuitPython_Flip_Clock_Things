import time

from adafruit_displayio_layout.widgets.widget import Widget
from displayio import TileGrid, Palette

from cedargrove_palettefader import PaletteFader


class FlipDigit(Widget):
    VALID_CHARACTERS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9)
    TOP_HALF_SPRITE_INDEX_MAP = {
        0: 0, 1: 1, 2: 2,
        3: 6, 4: 7, 5: 8,
        6: 12, 7: 13, 8: 14,
        9: 18
    }
    BOTTOM_HALF_SPRITE_INDEX_MAP = {
        0: 3, 1: 4, 2: 5,
        3: 9, 4: 10, 5: 11,
        6: 15, 7: 16, 8: 17,
        9: 21
    }

    def __init__(self, static_spritesheet, static_spritesheet_palette, top_anim_spritesheet,
                 top_anim_palette, bottom_anim_spritesheet, bottom_anim_palette,
                 tile_width, tile_height, anim_frame_count=10, anim_delay=.02):
        super().__init__()
        self.anim_delay = anim_delay


        self.anim_frame_count = anim_frame_count
        #print(hex(static_spritesheet_palette[0]))

        self.darker_static_palette = Palette(len(static_spritesheet_palette))
        for i in range(len(static_spritesheet_palette)):
            self.darker_static_palette[i] = static_spritesheet_palette[i]

        self.darker_static_palette.make_transparent(0)

        self.static_fader = PaletteFader(static_spritesheet_palette, 0.8, 1.0)

        #print(hex(self.static_fader.palette[0]))
        #print(hex(static_spritesheet_palette[0]))
        self.darker_static_fader = PaletteFader(self.darker_static_palette, 0.6, 1.0)
        #print(hex(self.static_fader.palette[0]))
        print(hex(self.darker_static_fader.palette[0]))

        self.top_static_tilegrid = TileGrid(static_spritesheet,
                                            pixel_shader=self.static_fader.palette,
                                            height=1,
                                            width=1,
                                            tile_width=tile_width, tile_height=tile_height)

        self.bottom_static_tilegrid = TileGrid(static_spritesheet,
                                               pixel_shader=self.static_fader.palette,
                                               height=1,
                                               default_tile=3,
                                               width=1,
                                               tile_width=tile_width, tile_height=tile_height)

        self.bottom_anim_fader = PaletteFader(bottom_anim_palette, 0.85, 1.0)
        self.top_anim_fader = PaletteFader(top_anim_palette, 0.6, 1.0)

        self.top_anim_tilegrid = TileGrid(top_anim_spritesheet,
                                          pixel_shader=self.top_anim_fader.palette,
                                          height=1,
                                          width=1,
                                          tile_width=tile_width, tile_height=tile_height)

        self.bottom_anim_tilegrid = TileGrid(bottom_anim_spritesheet,
                                             pixel_shader=self.bottom_anim_fader.palette,
                                             height=1,
                                             width=1,
                                             tile_width=tile_width, tile_height=tile_height)





        self.append(self.top_static_tilegrid)
        self.append(self.bottom_static_tilegrid)
        self.bottom_static_tilegrid.y = tile_height

        self.top_anim_tilegrid.hidden = True
        self.bottom_anim_tilegrid.hidden = True
        self.append(self.top_anim_tilegrid)
        self.append(self.bottom_anim_tilegrid)
        self.bottom_anim_tilegrid.y = tile_height

        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if type(new_value) == int and \
                0 <= new_value <= 9 and \
                new_value in FlipDigit.VALID_CHARACTERS:

            _old_value = self.value
            self._value = new_value

            # animations and things

            self.top_anim_tilegrid[0] = new_value * 10
            self.top_anim_tilegrid.hidden = False
            self.top_static_tilegrid[0] = FlipDigit.TOP_HALF_SPRITE_INDEX_MAP[new_value]

            self.bottom_static_tilegrid.pixel_shader = self.darker_static_fader.palette

            self.top_flip_animate(value=_old_value)
            self.top_anim_tilegrid.hidden = True

            self.bottom_anim_tilegrid[0] = new_value * 10
            self.bottom_anim_tilegrid.hidden = False


            self.bottom_flip_animate(value=new_value)
            self.bottom_static_tilegrid[0] = FlipDigit.BOTTOM_HALF_SPRITE_INDEX_MAP[new_value]
            self.bottom_anim_tilegrid.hidden = True
            self.bottom_static_tilegrid.pixel_shader = self.static_fader.palette

        else:
            raise ValueError(f"Invalid new value: {type(new_value)}: {new_value}. Must be int 0-9")

    def top_flip_animate(self, value):
        for i in range(self.anim_frame_count):
            self.top_anim_tilegrid[0] = i + (value*10)
            time.sleep(self.anim_delay)


    def bottom_flip_animate(self, value):
        for i in range(self.anim_frame_count):
            self.bottom_anim_tilegrid[0] = i + (value * 10)
            time.sleep(self.anim_delay)

