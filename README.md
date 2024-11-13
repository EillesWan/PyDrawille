# 瞽字象形 PyDrawille

采用万国码之盲文字符在控制台或终端应用中绘制点阵图。

此自述文件亦可见于诸下文字\
The README is also in\
[🇬🇧 英文 English](./README.en.md)

此库开发，实为避 [drawille](https://github.com/asciimoo/drawille) 库之 [AGPLv3](https://github.com/asciimoo/drawille/blob/master/LICENSE) 协议绑架。抽丝剥茧，以新逻辑呈同种功能，是为完全独一的软件，意欲完全避开其法律风险。为正本清源，不采用其应用程序接口，不采用同种代码逻辑，以全新之面貌呈现盲文点阵图。

### 功能说明

#### 类定义

本库定义了一个 `CanvasSurface` 作为绘制像素画布的基础类。提供多种方法来操作画布，并课最终转为盲文字符串或图像。

#### 基础属性

- `_width`: 画布宽度，内部使用，不应直接修改。
- `_height`: 画布高度，内部使用，不应直接修改。
- `data`: 画布数据，使用 `numpy` 数组存储，布尔类型，`True` 表示该像素为突出（存在），`False` 表示相反。

#### 构造函数

- `__init__`: 初始化画布，可以指定宽度、高度、初始数据和填充值。默认情况下，宽度为终端宽度的两倍，高度为终端高度的四倍。

#### 属性

- `surface_width`: 获取画布宽度。
- `surface_height`: 获取画布高度。
- `surface_size`: 获取画布尺寸，返回一个元组 `(width, height)`。

#### 类函数

- `from_image`: 从图片创建画布，将图片转换为布尔数组。

#### 实例函数

- `reshape_canvas`: 重新设置画布大小，不缩放内容。
- `resize_image`: 缩放整个画布，支持多种插值方法。
- `stack`: 将另一个画布对象堆叠到当前画布上，支持水平和垂直堆叠。（拼接画布）
- `rorate`: 旋转画布及其图像，支持 90 度、180 度和 270 度旋转。
- `reset`: 重置画布。
- `get_pixel`: 获取指定坐标的像素。
- `set_pixel`: 设置指定坐标的像素。
- `set_pixels`: 使用 `x` 和 `y` 序列设置多个像素，比 `set_points` 更快。
- `set_points`: 使用多组坐标对设置多个像素。
- `set_line`: 设置一行像素。
- `set_column`: 设置一列像素。
- `set_block`: 设置一个区域的像素。
- `set_canvas`: 设置画布所有像素。
- `reverse_pixel`: 翻转指定坐标的像素。（反色某点）
- `reverse_line`: 翻转一行像素。（反色某行）
- `reverse_column`: 翻转一列像素。（反色某列）
- `reverse_block`: 翻转一个区域的像素。（反色某区域）
- `reverse_canvas`: 翻转整个画布的像素。（反色画布）
- `dump_lines`: 以行为分割的盲文字符画字符串迭代器。
- `dump`: 将画布上的所有像素生成盲文字符画。
- `dump_singleline`: 为指定的行生成盲文字符画，迭代每个字符。
- `to_image`: 将画布生成图片。
- `dump_image`: 将画布生成盲文字符画图片，支持指定字体、背景色和前景色。

#### 静态函数

- `walk_line`: 直线迭代器，返回一条直线上的所有坐标。

### 示例用法

```python
# 创建一个画布
canvas = CanvasSurface(width=100, height=50)

# 设置一些像素
canvas.set_pixel(10, 10, True)
canvas.set_pixel(15, 15, True)

# 生成盲文字符画
braille_art = canvas.dump()
print(braille_art)

# 生成图片
image = canvas.to_image()
image.show()

# 生成盲文字符画图片
font = ImageFont.truetype("FontSupportsBraille.ttf", 24)
braille_image = canvas.dump_image(font, backgrand_color=0, foreground_color=255)
braille_image.show()
```

## 致谢

1.  感谢 [_自由软件基金会_ FSF](https://www.fsf.org) 在促进软件非自由化方面取得的杰出贡献；所谓的自由软件，倘若仅仅建立于开发者的非自由之上，则无谓之以自由。在 _自由软件基金会_ 的自介辞“我们的使命是在全球范围内促进计算机用户的自由。我们捍卫所有软件用户的权利。”中，我相信他们的的确确在其各类协议中试图保护计算机用户之自由，同时也试图剥夺开发者自由开发软件的权利。我相信，**真正的自由，只有建立在全人类的广度之上，才可以称得上是真正的自由**，一部分人的自由不叫自由，那只不过是他们对其他人的奴役。我们需要捍卫开发者的自由，捍卫开发者合理化自己知识产权的权利！

<!-- 2.  感谢 [**asciimoo**](https://github.com/asciimoo) 在 [**drawille**](https://github.com/asciimoo/drawille) 项目中使用的 [**AGPLv3**](https://github.com/asciimoo/drawille/blob/master/LICENSE) 协议，敦促我们不得不使用全新的逻辑，以完全避免其法律风险。感谢 TA 提供了这么良好的契机，使得我能够有想法去探求这个项目的代码实现。 -->
