import numpy as np
from PIL import Image, ImageFont

from PyDrawille import CanvasSurface

# 定义画布 canvas，即实例化 CanvasSurface 类
canvas = CanvasSurface()

# 使用 NumPy 生成一个余弦曲线
arr = np.arange(canvas.surface_width)
yarr = np.intc(np.cos(arr / 10) * canvas.surface_height / 3 + canvas.surface_height / 2)

# 生成一个一次函数曲线
mxg = min(canvas.surface_width, canvas.surface_height)
mxgarr = np.arange(mxg)

# 开始绘制
canvas.set_points(zip(mxgarr, mxgarr)) # type: ignore
canvas.set_pixels(
    arr,
    yarr,
)
# 画一条横穿中心的横线
canvas.set_line(canvas.surface_height // 2)

# 打印在控制台上
print(canvas.dump())

# 生成图片
canvas.dump_image(
    ImageFont.truetype(font="./DejaVuSansCondensed.ttf", size=32, encoding="utf-8"),
    0,
    255,
).save(
    "test.png",
)
