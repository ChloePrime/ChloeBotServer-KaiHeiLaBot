from typing import Optional

from aiohttp import *
from PIL import Image
from urllib.parse import urlencode
import io


def _fix_str(s: str) -> str:
    s = s.replace("-", "--")
    s = s.replace("_", "__")
    s = s.replace(" ", "_")
    return s


async def make(
        label: str, message: str, color: str | int, http_client: ClientSession,
        style: Optional[str] = "plastic", logo: Optional[str] = None
) -> Image:
    if isinstance(color, int):
        color = hex(color)

    label = _fix_str(label)
    message = _fix_str(message)

    url = f"https://raster.shields.io/badge/{label}-{message}-{color}"
    if style is not None or logo is not None:
        params = {}
        if style is not None:
            params["style"] = style
        if logo is not None:
            params["logo"] = logo
        url = url + "?" + urlencode(params)

    resp = await http_client.get(url)

    img_bytes = await resp.read()
    return Image.open(io.BytesIO(img_bytes))


def join(*images: Image, margin=0) -> Image:
    """
    横向拼接给定的图片。
    :param images: 图片序列
    :param margin: 两张图片间的间距，单位 px
    :return: 横向拼接好的图片
    """
    total_width = sum((img.width for img in images)) + margin * len(images) - 1
    total_height = max((img.height for img in images))

    joined = Image.new("RGBA", (total_width, total_height))
    cur_x = 0
    y = 0
    for img in images:
        joined.paste(img, (cur_x, y))
        cur_x += img.width + margin

    return joined
