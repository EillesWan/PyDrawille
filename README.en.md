# 瞽字象形 PyDrawille

Using Unicode braille characters to draw pixel graphics in a console.

此自述文件亦可见于诸下文字\
The README is also in\
[🇨🇳 Chinese 汉语](./README.md)

The aim of the library's development is to avoid the [drawille](https://github.com/asciimoo/drawille) library's [AGPLv3](https://github.com/asciimoo/drawille/blob/master/LICENSE) license trapping. We use a totally different logic to achieve the same functionality, in the hope of creating a fully independent and free software. To preserve the original source's independence, we did not use the API of drawille library, and did not use the same code logic, allowing a completely entirely new way to present the braille characters' graphics.

### Function description

#### Class definition

This library defines a `CanvasSurface` as the base class for drawing pixel canvas. It provides various methods to operate on the canvas and finally convert it to braille strings or images.

#### Basic attributes

- `_width`: Canvas width, used internally, should not be directly modified.
- `_height`: Canvas height, used internally, should not be directly modified.
- `data`: Canvas data, stored in a NumPy array, Boolean type, `True` represents the point's existence and `False` represents the oppsite.

#### Constructors

- `__init__`: Initialize canvas, which can specify width, height, initial data and fill value. By default, the width is twice that of the terminal width, and the height is four times that of the terminal height.

- `from_image`: Create a canvas from an image, with all its pixels will be converted to bw colors.

#### Attributes

- `surface_width`: Get canvas width.
- `surface_height`: Get canvas height.
- `surface_size`: Get canvas size and return a tuple (width, height).

### Instance function

- `reshape_canvas`: Resizes canvas without scaling content.
- `resize_image`: Scales entire canvas, supports multiple interpolation methods.
- `stack`: Stacks another canvas object on top of current canvas, supports horizontal and vertical stacking. (Stitching canvas)
- `rorate`: Rotates canvas and its image, supports rotation by 90 degrees, 180 degrees, or 270 degrees.
- `reset`: Resets canvas. get_pixel: Gets pixel at specified coordinates.
- `set_pixel`: Sets pixel at specified coordinates.
- `set_pixels`: Uses X and Y sequences to set multiple pixels faster than set_points.
- `set_points`: Uses sets of coordinates to set multiple pixels.
- `set_line`: Sets a row of pixels. set_column: Sets a column of pixels.
- `set_block`: Sets pixels in an area. set_canvas: Sets all pixels on canvas.
- `reverse_pixel`: Flips pixel at specified coordinates. (Invert color of one point)
- `reverse_line`: Flips line of pixels. (Invert color of one row)
- `reverse_column`: Flips column of pixels. (Invert color of one column)
- `reverse_block`: Flips pixels in an area. (Invert color of one region)
- `reverse_canvas`: Flips all pixels on canvas.
- `dump_lines`: Braille character string iterator divided by lines.
- `dump`: Generates braille character string from all pixels on canvas.
- `dump_singleline`: Generates braille character string for specified line, iterating each character.
- `to_image`: Generates image from canvas.
- `dump_image`: Generates braille character string image from canvas, supporting specifying font, background color, and foreground color.

### Static functions

- `walk_line`: A linear iterator that returns all coordinates on a line.

### Example usage

```python
# Create a canvas
canvas = CanvasSurface(width=100, height=50)

# Set some pixels
canvas.set_pixel(10, 10, True)
canvas.set_pixel(15, 15, True)

# Make a braille character drawing string
braille_art = canvas.dump()
print(braille_art)

# Dumps to a image
image = canvas.to_image()
image.show()

# Make a braille character drawing image
font = ImageFont.truetype("FontSupportsBraille.ttf", 24)
braille_image = canvas.dump_image(font, backgrand_color=0, foreground_color=255)
braille_image.show()
```

### Acknowledgements

1.  Thanks for the outstanding contribution of the [_FSF_ (Free Software Foundation)](https://www.fsf.org) in promoting software non-freedom. The so-called _free software_ is meaningless if it merely relies on developers' non-freedom. In the self-introduction “The Free Software Foundation (FSF) is a nonprofit with a worldwide mission to promote computer user freedom. We defend the rights of all software users.” by the Free Software Foundation, I believe they indeed try to protect computer users' freedom and also attempt to deprive developers of their right to freely develop software. I believe that true freedom can only be called real freedom when it is established on the breadth of humanity. Partial freedom cannot be called freedom; it's just a form of slavery over others. We need to defend developers' freedom and their right to rationally manage their intellectual property.

