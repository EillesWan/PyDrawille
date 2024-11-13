from PIL import Image, ImageFont
import numpy as np
from PyDrawille import CanvasSurface

canvas = CanvasSurface()

arr = np.arange(canvas.surface_width)
yarr = np.intc(np.cos(arr / 10) * canvas.surface_height / 3 + canvas.surface_height / 2)

# print(yarr)

mxg = min(canvas.surface_width, canvas.surface_height)
mxgarr = np.arange(mxg)

canvas.set_points(zip(mxgarr, mxgarr))
canvas.set_line(canvas.surface_height // 2)

canvas.set_pixels(
    arr,
    yarr,
)
# canvas.set_pixels(range(80,),range(40,))

print(canvas.dump())

canvas.dump_image(
    ImageFont.truetype(font="./DejaVuSansCondensed.ttf", size=32, encoding="utf-8"),
    0,
    255,
).save(
    "test.png",
)
