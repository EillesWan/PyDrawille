"""
版权所有 © 2025 金羿ELS
Copyright (R) 2025 Eilles(EillesWan@outlook.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from os import get_terminal_size
from typing import Iterable, Iterator, Optional, Tuple

import numpy as np
from numpy._typing._array_like import _ArrayLikeInt_co
from numpy.typing import NDArray
from PIL import Image, ImageFont


class CanvasSurface(object):

    _width: int
    """
    切勿直接操作
    """
    _height: int
    """
    切勿直接操作
    """

    # _bg_char: bytes
    data: NDArray[np.bool]
    """
    画布数据，避免直接操作
    """

    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        data: Optional[NDArray[np.bool]] = None,
        fill_value: bool = False,
        # background_char: int | bytes | str = " ",
        # str_encoding: str = "utf-8",
        # ignore_warnings: bool = False,
    ):
        """
        画布界面

        参数
        ====

        `width`: int, optional
            界面宽度，默认为终端宽度的 2 倍
        `height`: int, optional
            界面高度，默认为终端高度的 4 倍
        `data`: NDArray[np.bool], optional
            画布数据，若留空则创建空白画布
        `fill_value`: bool, optional
            画布初始值，默认为假
        """
        if not width:
            width = (get_terminal_size().columns - 1) * 2
        if not height:
            height = (get_terminal_size().lines - 1) * 4
        # if isinstance(background_char, int):
        #     self._bg_char = background_char.to_bytes(length=1, byteorder=byteorder)
        # elif isinstance(background_char, str):
        #     self._bg_char = background_char.encode(
        #         encoding=str_encoding, errors="ignore" if ignore_warnings else "strict"
        #     )
        # elif isinstance(background_char, memoryview):
        #     self._bg_char = memoryview(background_char).tobytes()
        # elif isinstance(background_char, str):
        #     self._bg_char = background_char
        # else:
        #     self._bg_char = b" "
        # if not ignore_warnings:
        #     if len(self._bg_char) > 1:
        #         raise ValueError(
        #             "底字须为单字符\nBackground must be a single character"
        #         )

        self._width = width
        self._height = height
        self.data = (
            data
            if data
            else np.full(
                shape=(width, height),
                fill_value=fill_value,
                dtype=np.bool,
            ).reshape(width, height)
        )

    @property
    def surface_width(self):
        return self._width

    @property
    def surface_height(self):
        return self._height

    @property
    def surface_size(self):
        return self._width, self._height

    @classmethod
    def from_image(cls, image: Image.Image) -> "CanvasSurface":
        """
        从图片创建画布

        参数
        ====
        `image`: Image.Image
            图片对象
        """

        width_, height_ = image.size

        return cls(
            width=width_,
            height=height_,
            data=np.array(image.convert("1"), dtype=np.bool).reshape(width_, height_),
        )

    def reshape_canvas(
        self,
        width_: Optional[int],
        height_: Optional[int],
        fill_value_: bool = False,
    ):
        """
        重设画布大小，不缩放内容

        参数
        ====
        `width_`: int, optional
            宽度新值，若留空则不变
        `height_`: int, optional
            高度新值，若留空则不变
        `fill_value_`: bool, optional
            画布新增区域的填充值，默认为假
        """

        if not width_:
            width_ = self.surface_width
        if not height_:
            height_ = self.surface_height

        if width_ > self.surface_width:
            self.data = np.pad(
                self.data,
                ((0, width_ - self.surface_width), (0, 0)),
                mode="constant",
                constant_values=fill_value_,
            )
        else:
            self.data = self.data[:width_, :]
        if height_ > self.surface_height:
            self.data = np.pad(
                self.data,
                ((0, 0), (0, height_ - self.surface_height)),
                mode="constant",
                constant_values=fill_value_,
            )
        else:
            self.data = self.data[:, :height_]
        # self.data = np.pad(self.data, ((0, width_ - self.surface_width), (0, height_ - self.surface_height)), mode="constant", constant_values=False)

        self._width = width_
        self._height = height_

    def resize_image(
        self,
        width_: Optional[int],
        height_: Optional[int],
        resampling_method: Optional[Image.Resampling],
    ):
        """
        缩放画布界面

        参数
        ====

        `width_`: int, optional
            宽度新值，若留空则不变
        `height_`: int, optional
            高度新值，若留空则不变
        `resampling_method`: Image.Resampling, optional
            缩放采样，默认为最近邻居插值，可为以下值：
                :py:data:`Resampling.NEAREST`   最近邻居插值
                :py:data:`Resampling.BOX`       同权近邻插值
                :py:data:`Resampling.BILINEAR`  双线性插值法
                :py:data:`Resampling.HAMMING`   线性纠错插值
                :py:data:`Resampling.BICUBIC`   双三次插值法
                :py:data:`Resampling.LANCZOS`   兰佐斯插值法

        """

        if not width_:
            width_ = self.surface_width
        if not height_:
            height_ = self.surface_height
        if not resampling_method:
            resampling_method = Image.Resampling.NEAREST

        self.data = np.array(
            Image.fromarray(obj=self.data, mode="1").resize(
                size=(width_, height_),
                resample=resampling_method,
            ),
            np.bool,
        ).reshape(width_, height_)
        # self.data.resize(width_, height_)
        self._width = width_
        self._height = height_

    def stack(
        self,
        other: "CanvasSurface",
        axis: str = "horizontal",
    ):
        """
        将另一个画布对象堆叠拼接到当前画布上

        参数
        ====
        `other`: CanvasSurface
            另一个画布对象
        `axis`: str
            堆叠方向，可选值：
                `horizontal`: 水平堆叠
                `vertical`: 垂直堆叠
        """
        if axis == "horizontal":
            self.data = np.hstack((self.data, other.data), dtype=np.bool)
            # self.data = np.concatenate((self.data, other.data), axis=0,dtype=np.bool)
        elif axis == "vertical":
            self.data = np.vstack((self.data, other.data), dtype=np.bool)
            # self.data = np.concatenate((self.data, other.data), axis=1,dtype=np.bool)

    def rorate(self, x90angle: int):
        """
        旋转画布极其图像

        参数
        ====
        `x90angle`: int
            旋转角度，可选值：
                `1`: 顺时针旋转90度
                `2`: 顺时针旋转180度
                `3`: 顺时针旋转270度
        """

        self.data = np.rot90(self.data, x90angle)

    def reset(self, value: bool = False):
        """
        重置画布界面（以指定颜色填充画布）
        """
        self.data.fill(value)

    def get_pixel(self, x: int, y: int) -> bool:
        """
        获取像素

        参数
        ====
        `x`: int
            x 坐标
        `y`: int
            y 坐标

        返回
        ====
        bool
            像素值，真为设立像素存在
        """
        return self.data[x, y]

    def set_pixel(self, x: int, y: int, value: bool = True):
        """
        设置像素

        参数
        ====
        `x`: int
            x 坐标
        `y`: int
            y 坐标
        `value`: bool
            像素值，真为设立像素存在
        """
        self.data[x, y] = value

    def set_pixels(
        self,
        x_: _ArrayLikeInt_co,
        y_: _ArrayLikeInt_co,
        value: bool = True,
    ):
        """
        使用`x`、`y`双下标序列的形式提供坐标，设置多个像素，相较于 `set_points`，此函数速度更快

        请注意，`x_`序列与`y_`序列须一一对应，且长度应一致

        参数
        ====
        `x_`: np._ArrayLikeInt
            x 坐标数组
        `y_`: np._ArrayLikeInt
            y 坐标数组
        `value`: bool
            像素值，真为设立像素存在
        """

        self.data[x_, y_] = value

    def set_points(self, points: Iterable[Tuple[int, int]], value: bool = True):
        """
        使用多组坐标对来设置多个像素，速度相较于 `set_pixels` 更慢

        参数
        ====
        `points`: Iterable[Tuple[int, int]]
            坐标数组，元素为元组，形如：(x, y)
        `value`: bool
            像素值，真为设立像素存在
        """

        for x, y in points:
            self.data[x, y] = value

    def set_line(self, y: int, value: bool = True):
        """
        设置一行像素

        参数
        ====
        `y`: int
            y 坐标
        """
        self.data[:, y] = value

    def set_column(self, x: int, value: bool = True):
        """
        设置一列像素

        参数
        ====
        `x`: int
            x 坐标
        """
        self.data[x, :] = value

    def set_canvas(self, value: bool = True):
        """
        设置画布所有像素

        `value`: bool
            像素值，真为设立像素存在
        """
        self.data.fill(value)

    def reverse_pixel(self, x: int, y: int):
        """
        翻转（反色）像素

        参数
        ====
        `x`: int
            x 坐标
        `y`: int
            y 坐标
        """

        self.data[x, y] = not self.data[x, y]

    def set_block(self, x: int, y: int, width: int, height: int, value: bool = True):
        """
        设置一个区域的像素

        参数
        ====
        `x`: int
            x 坐标
        `y`: int
            y 坐标
        `width`: int
            宽度
        `height`: int
            高度
        `value`: bool
            像素值，真为设立像素存在
        """
        self.data[x : x + width, y : y + height] = value

    def reverse_line(self, y: int):
        """
        翻转（反色）一行像素

        参数
        ====
        `y`: int
            y 坐标
        """
        self.data[:, y] = np.logical_not(self.data[:, y])

    def reverse_column(self, x: int):
        """
        翻转（反色）一列像素

        参数
        ====
        `x`: int
            x 坐标
        """
        self.data[x, :] = np.logical_not(self.data[x, :])

    def reverse_block(self, x: int, y: int, width: int, height: int):
        """
        翻转（反色）一个区域的像素

        参数
        ====
        `x`: int
            x 坐标
        `y`: int
            y 坐标
        `width`: int
            宽度
        `height`: int
            高度
        """
        self.data[x : x + width, y : y + height] = np.logical_not(
            self.data[x : x + width, y : y + height]
        )

    def reverse_canvas(self):
        """
        翻转（反色）整个画布的像素
        """
        self.data = np.logical_not(self.data)

    # def get_character(self, x: int, y: int) -> str:
    #     """
    #     获取字符

    #     参数
    #     ====
    #     `x`: int
    #         控制台列坐标（第 x 列）
    #     `y`: int
    #         控制台行坐标（第 y 行）

    #     返回
    #     ====
    #     bool
    #         字符值，真为设立像素存在
    #     """
    #     return chr(
    #             10240
    #             + int(
    #                 strlist[x,y][:5:-1]
    #                 + strlist[x,y][5::-2]
    #                 + strlist[x,y][4::-2],
    #                 2,
    #             )
    #         )

    def dump_lines(
        self,
    ) -> Iterator[str]:
        """
        以行为分割的盲文字符画字符串迭代器

        如要指定行号，请使用 `dump_singleline` 函数

        返回
        ====
        str
            字符串
        """

        # strlist: NDArray[np.character] = np.chararray(
        #     (mapshape := np.ceil([self.surface_height // 4, self.surface_width // 2])),
        #     itemsize=7,
        #     unicode=True,
        #     # fill_value="",
        #     # dtype=str,
        # )

        swidth_ = self.surface_width // 2
        strlist = ["" for _ in range(swidth_)]
        line_strlist = strlist.copy()

        lines_ = 0
        for y in range(self.surface_height):
            if lines_ < y // 4:
                yield "".join(
                    [
                        chr(
                            10240
                            + int(
                                line_strlist[i][:5:-1]
                                + line_strlist[i][5::-2]
                                + line_strlist[i][4::-2],
                                2,
                            )
                        )
                        for i in range(swidth_)
                    ]
                )
                lines_ += 1
                line_strlist = strlist.copy()
            for x in range(self.surface_width):
                line_strlist[x // 2] += "1" if self.data[x, y] else "0"

        # swidth_ = self.surface_width // 2
        # strlist = [0 for _ in range(swidth_)]
        # line_strlist = strlist.copy()

        # lines_ = 0
        # for y in range(self.surface_height):
        #     if lines_ < y // 4:
        #         yield "".join(
        #             [
        #                 chr(
        #                     10240
        #                     + ((line_strlist[i] & 1) << 7)
        #                     + (((line_strlist[i] >> 1) & 1) << 6)
        #                     + (((line_strlist[i] >> 2) & 1) << 5)
        #                     + (((line_strlist[i] >> 4) & 1) << 4)
        #                     + (((line_strlist[i] >> 6) & 1) << 3)
        #                     + (((line_strlist[i] >> 3) & 1) << 2)
        #                     + (((line_strlist[i] >> 5) & 1) << 1)
        #                     + ((line_strlist[i] >> 7) & 1)
        #                 )
        #                 for i in range(swidth_)
        #             ]
        #         )
        #         lines_ += 1
        #         line_strlist = strlist.copy()
        #     for x in range(self.surface_width):
        #         line_strlist[x_] = binarry_add(
        #             line_strlist[x_ := x // 2], self.data[x, y]
        #         )

        # def form(x, y):
        #     rr = ""
        #     for x_, y_ in (
        #         (x * 2, y * 4 + 3),
        #         (x * 2, y * 4 + 2),
        #         (x * 2, y * 4 + 1),
        #         (x * 2, y * 4),
        #         (x * 2 + 1, y * 4 + 3),
        #         (x * 2 + 1, y * 4 + 2),
        #         (x * 2 + 1, y * 4 + 1),
        #         (x * 2 + 1, y * 4),
        #     ):
        #         rr += "1" if self.data[x_, y_] else "0"
        #     return rr

        # for i in range(self.surface_height // 4):
        #     finalstr = ""
        #     for ii in range(self.surface_width // 2):
        #         stt = form(ii, i)
        #         finalstr += chr(
        #             10240
        #             + int(
        #                 stt[:5:-1]
        #                 + stt[5::-2]
        #                 + stt[4::-2],
        #                 2,
        #             )
        #         )

        #     yield finalstr

    def dump(self) -> str:
        """
        将画布上的所有像素生成盲文字符画
        """

        return "\n".join(self.dump_lines())

    def dump_singleline(self, y: int) -> Iterator[str]:
        """
        为指定的行生成盲文字符画，每个字符一迭代

        参数
        ====
        `y`: int
            行坐标
        """

        swidth_ = self.surface_width // 2
        line_strlist = ["" for _ in range(swidth_)]

        for y_ in range(y * 4, y * 4 + 4):
            for x in range(self.surface_width):
                line_strlist[x // 2] += "1" if self.data[x, y_] else "0"

        for i in range(swidth_):
            yield chr(
                10240
                + int(
                    line_strlist[i][:5:-1]
                    + line_strlist[i][5::-2]
                    + line_strlist[i][4::-2],
                    2,
                )
            )

    def to_image(
        self,
    ) -> Image.Image:
        """
        将画布生成图片
        """

        return Image.fromarray(obj=self.data, mode="1")

    def dump_image(
        self,
        font_: ImageFont.FreeTypeFont,
        backgrand_color: int = 0,
        foreground_color: int = 255,
    ) -> Image.Image:
        """
        将画布生成盲文字符画图片，理论上只能支持黑白二色

        参数
        ====
        `font_`: ImageFont.FreeTypeFont
            字体对象
        `backgrand_color`: int
            背景色
        `foreground_color`: int
            前景色
        """
        # ImageFont.FreeTypeFont(font_path,)
        # ImageFont.load_default()

        simple_image = Image.new(
            mode="1",
            size=(
                int(
                    np.ceil(
                        font_.getlength(
                            "⠤",
                            mode="1",
                        )
                        * self.surface_width
                        // 2
                    ),
                ),
                int(
                    np.ceil(self.surface_height // 4 * font_.size),
                ),
            ),
            color=backgrand_color,
        )
        # to_draw = ImageDraw.Draw(simple_image)
        for index_, line_ in enumerate(self.dump_lines()):
            # to_draw.text((0, round(index_ * font_.size,)), line_, font=font_,fill=255)
            im_mask: Image.Image = font_.getmask(
                line_,
                mode="L",
                ink=foreground_color,
            )

            simple_image.paste(
                im=im_mask,
                box=(
                    0,
                    kr := round(
                        index_ * font_.size,
                    ),
                    im_mask.size[0],
                    kr + im_mask.size[1],
                ),
            )
        return simple_image

    @staticmethod
    def walk_line(x0: int, y0: int, x1: int, y1: int) -> Iterator[Tuple[int, int]]:
        """
        直线迭代器

        参数
        ====
        `x0`: int
            起点 x 坐标
        `y0`: int
            起点 y 坐标
        `x1`: int
            终点 x 坐标
        `y1`: int
            终点 y 坐标

        返回
        ====
        Iterator[Tuple[int, int]]
            迭代器，返回 (x, y) 坐标
        """
        euclidean_distance = np.linalg.norm(
            [x1 - x0, y1 - y0],
            ord=2,
        )
        xd = x1 - x0
        yd = y1 - y0
        for i in range(int(np.ceil(euclidean_distance))):
            yield (
                int(x0 + xd * i / euclidean_distance),
                int(y0 + yd * i / euclidean_distance),
            )
