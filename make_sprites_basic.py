from PIL import Image, ImageDraw, ImageFont
import numpy

tile_width, tile_height = (48, 100)
background_color = (73, 109, 137)
border_color = (255, 255, 0)
font_color = (0, 0, 0)
padding_size = 6


def make_sprite(character, font_size=44):
    border_rect_size = (tile_width - padding_size * 2, tile_height - padding_size * 2)
    # inner_image_size = (border_rect_size[0] + 1, border_rect_size[1] + 1)
    inner_image_size = (tile_width, tile_height)
    border_shape = ((padding_size, padding_size), border_rect_size)

    fnt = ImageFont.truetype('LeagueSpartan-Regular.ttf', font_size)
    img = Image.new('RGBA', (tile_width, tile_height), color=background_color)
    d = ImageDraw.Draw(img)

    inner_img = Image.new('RGBA', inner_image_size, color=background_color)

    inner_draw = ImageDraw.Draw(inner_img)
    # inner_draw.rectangle((0, 0, inner_image_size[0], inner_image_size[1]), fill=(100, 100, 200))

    inner_draw.rectangle(border_shape, outline=border_color, fill=border_color)

    w, h = inner_draw.textsize(character, font=fnt)
    inner_draw.text((((inner_image_size[0] - w) // 2) - 1, ((inner_image_size[1] - h) // 2) - 1), character,
                    fill=font_color, font=fnt)

    img.paste(inner_img, (padding_size // 2, padding_size // 2))
    return img


def make_sheet(font_size=44):
    full_sheet_img = Image.new("RGBA", (tile_width * 3, tile_height * 4), color=background_color)

    for i in range(10):
        img = make_sprite(f"{i}", font_size=44)
        #img.save(f'char_sprites/pil_text_{i}.png')
        coords = (((i%3) * tile_width), ((i//3) * tile_height))
        print(coords)
        full_sheet_img.paste(img, coords)

    img = make_sprite(f":", font_size=44)
    coords = (((10 % 3) * tile_width), ((10 // 3) * tile_height))
    full_sheet_img.paste(img, coords)


    full_sheet_img = full_sheet_img.convert(mode="P", palette=Image.WEB)
    full_sheet_img.save("full_sheet.bmp")

make_sheet(font_size=44)