"""Reuse a Stellaris reward border and fit a monochrome symbol into both frames.

Requires Pillow. Extraction/compositing only; this script does not generate artwork.
"""
import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


def extract_symbol(image, threshold=90, margin=0.113, min_area=0.00025):
    """Discard border components touching the outer margin of the source frame."""
    gray = image.convert('L')
    width, height = image.size
    values = gray.tobytes()
    alpha = image.getchannel('A').tobytes()
    active = bytearray(v > threshold and a > 128 for v, a in zip(values, alpha))
    selected = bytearray(width * height)
    for start in range(len(active)):
        if not active[start]:
            continue
        active[start] = 0
        queue = deque([start])
        component = []
        xmin, ymin, xmax, ymax = width, height, 0, 0
        while queue:
            index = queue.popleft()
            component.append(index)
            x, y = index % width, index // width
            xmin, ymin = min(xmin, x), min(ymin, y)
            xmax, ymax = max(xmax, x), max(ymax, y)
            neighbors = []
            if x: neighbors.append(index - 1)
            if x + 1 < width: neighbors.append(index + 1)
            if y: neighbors.append(index - width)
            if y + 1 < height: neighbors.append(index + width)
            for neighbor in neighbors:
                if active[neighbor]:
                    active[neighbor] = 0
                    queue.append(neighbor)
        if (len(component) > width * height * min_area
                and xmin > width * margin and xmax < width * (1 - margin)
                and ymin > height * margin and ymax < height * (1 - margin)):
            for index in component:
                selected[index] = values[index]
    mask = Image.frombytes('L', image.size, bytes(selected))
    bounds = mask.getbbox()
    if not bounds:
        raise ValueError('No separate interior symbol found; use --symbol-box or adjust extraction thresholds.')
    return mask.crop(bounds)


def compose(template, symbol, size=46, dim=128):
    if template.size != (144, 72):
        raise ValueError('Template must be a 144 x 72 two-frame reward texture.')
    # This polygon matches the clear interior of the current AIO reward frame.
    interior = Image.new('L', template.size)
    draw = ImageDraw.Draw(interior)
    for offset in (0, 72):
        draw.polygon([(offset + 36, 6), (offset + 62, 21),
                      (offset + 62, 51), (offset + 36, 66),
                      (offset + 10, 51), (offset + 10, 21)], fill=255)
    output = template.copy()
    output.paste((0, 0, 0, 255), (0, 0, 144, 72), interior)
    symbol = symbol.copy()
    symbol.thumbnail((size, size), Image.Resampling.LANCZOS)
    for offset, shade in ((0, 255), (72, dim)):
        mask = Image.new('L', template.size)
        mask.paste(symbol, (offset + 36 - symbol.width // 2, 36 - symbol.height // 2))
        mask = ImageChops.multiply(mask, interior)
        output.paste((shade, shade, shade, 255), (0, 0, 144, 72), mask)
    outside = ImageChops.invert(interior)
    for before, after in zip(template.split(), output.split()):
        if ImageChops.multiply(ImageChops.difference(before, after), outside).getbbox():
            raise AssertionError('Template border pixels changed.')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-frames', type=int, choices=(1, 2), default=2,
                        help='Use the left frame of a two-frame source (default: 2).')
    parser.add_argument('--symbol-box', type=int, nargs=4, metavar=('LEFT', 'TOP', 'RIGHT', 'BOTTOM'),
                        help='Explicit crop within the first source frame; bypasses connected-component extraction.')
    parser.add_argument('--size', type=int, default=46, help='Maximum symbol width/height in game pixels.')
    parser.add_argument('--dim', type=int, default=128, help='Disabled symbol brightness, 0..255.')
    parser.add_argument('--threshold', type=int, default=90)
    parser.add_argument('--margin', type=float, default=0.113)
    parser.add_argument('--min-area', type=float, default=0.00025)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if not 1 <= args.size <= 60 or not 0 <= args.dim <= 255 or not 0 <= args.threshold <= 255:
        parser.error('Invalid size, dim, or threshold.')
    if not 0 <= args.margin < 0.5 or not 0 <= args.min_area < 1:
        parser.error('Invalid margin or min-area.')
    if args.output.suffix.lower() not in ('.dds', '.png'):
        parser.error('Output must be DDS or PNG.')
    if args.output.resolve() in (args.template.resolve(), args.source.resolve()):
        parser.error('Output must not overwrite the template or source.')
    if args.output.exists() and not args.overwrite:
        parser.error('Output already exists; pass --overwrite explicitly.')
    with Image.open(args.template) as image:
        template = image.convert('RGBA')
    with Image.open(args.source) as image:
        source = image.convert('RGBA')
    if args.source_frames == 2:
        if source.width != source.height * 2:
            parser.error('Two-frame source must have a 2:1 aspect ratio.')
        source = source.crop((0, 0, source.width // 2, source.height))
    if args.symbol_box:
        left, top, right, bottom = args.symbol_box
        if not (0 <= left < right <= source.width and 0 <= top < bottom <= source.height):
            parser.error('Symbol box is outside the first source frame.')
        crop = source.crop(args.symbol_box)
        symbol = ImageChops.multiply(crop.convert('L'), crop.getchannel('A'))
    else:
        symbol = extract_symbol(source, args.threshold, args.margin, args.min_area)
    output = compose(template, symbol, args.size, args.dim)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output)
    with Image.open(args.output) as saved:
        if saved.size != (144, 72) or saved.mode != 'RGBA':
            raise AssertionError('Unexpected output size or mode.')
    print(f'Saved {args.output}: 144x72 RGBA, two frames; original border preserved.')


if __name__ == '__main__':
    main()
