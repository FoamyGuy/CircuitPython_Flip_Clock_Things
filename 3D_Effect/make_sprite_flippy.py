from PIL import Image, ImageDraw, ImageFont
import numpy


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


W, H = (120, 135)
background_color = (73, 109, 137)
border_color = (255, 255, 0)
font_color = (255, 255, 0)

padding_size = 30

border_rect_size = (W - padding_size // 2, H - padding_size // 2)
# inner_image_size = (border_rect_size[0] + 1, border_rect_size[1] + 1)
inner_image_size = (W, H)
border_shape = ((padding_size // 2, padding_size // 2), border_rect_size)

fnt = ImageFont.truetype('LeagueSpartan-Regular.ttf', 72)
img = Image.new('RGBA', (W, H), color=background_color)
d = ImageDraw.Draw(img)

inner_img = Image.new('RGBA', inner_image_size)

inner_draw = ImageDraw.Draw(inner_img)
#inner_draw.rectangle((0, 0, inner_image_size[0], inner_image_size[1]), fill=(100, 100, 200))

inner_draw.rectangle(border_shape, outline=border_color)

w, h = inner_draw.textsize("1", font=fnt)
inner_draw.text(((inner_image_size[0] - w) / 2, (inner_image_size[1] - h) / 2), "1", fill=font_color, font=fnt)

coeffs = find_coeffs(
    [(0, 0), (inner_image_size[0], 0), (inner_image_size[0], inner_image_size[1]), (0, inner_image_size[1])],
    [(40, -50), (inner_image_size[0] - 40, -50), (inner_image_size[0], inner_image_size[1]), (0, inner_image_size[1])])

inner_img = inner_img.transform(inner_image_size, Image.PERSPECTIVE, coeffs,
                    Image.BICUBIC)
inner_img.save("inner_after_transform.png")

img.paste(inner_img, (padding_size // 2, padding_size // 2))

img.save('pil_text.png')
