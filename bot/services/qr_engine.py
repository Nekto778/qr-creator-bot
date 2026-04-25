import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import pil as pil_drawers
from qrcode.image.svg import SvgPathImage
from PIL import Image
import numpy as np
import io


class QREngine:
    DOT_STYLES = {
        "square": pil_drawers.SquareModuleDrawer,
        "rounded": pil_drawers.RoundedModuleDrawer,
        "circle": pil_drawers.CircleModuleDrawer,
        "gapped": pil_drawers.GappedSquareModuleDrawer,
    }

    ERROR_LEVELS = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    DEFAULT = {
        "fill_color": "#000000",
        "bg_color": "#FFFFFF",
        "bg_transparent": False,
        "dot_style": "square",
        "format": "png",
        "error_correction": "H",
        "gradient_enabled": False,
        "gradient_start": "#000000",
        "gradient_end": "#0066FF",
        "gradient_direction": "horizontal",
        "bg_gradient_enabled": False,
        "bg_gradient_start": "#FFFFFF",
        "bg_gradient_end": "#DDDDFF",
        "bg_gradient_direction": "vertical",
        "icon_path": None,
        "icon_size": 0.2,
    }

    @staticmethod
    def parse_hex(hex_str: str):
        h = hex_str.lstrip("#")
        if len(h) == 3:
            h = h[0]*2 + h[1]*2 + h[2]*2
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def create_gradient(self, size, start_hex, end_hex, direction):
        w, h = size
        sr, sg, sb = self.parse_hex(start_hex)
        er, eg, eb = self.parse_hex(end_hex)
        arr = np.zeros((h, w, 4), dtype=np.uint8)

        y_idx, x_idx = np.mgrid[0:h, 0:w]

        if direction == "horizontal":
            t = x_idx / max(w - 1, 1)
        elif direction == "vertical":
            t = y_idx / max(h - 1, 1)
        elif direction == "diagonal":
            t = (x_idx + y_idx) / max(w + h - 2, 1)
        elif direction == "radial":
            cx, cy = w // 2, h // 2
            dist = np.sqrt((x_idx - cx) ** 2 + (y_idx - cy) ** 2)
            max_r = np.sqrt(cx**2 + cy**2)
            t = np.clip(dist / max_r, 0, 1)
        else:
            t = x_idx / max(w - 1, 1)

        arr[:, :, 0] = (sr + (er - sr) * t).astype(np.uint8)
        arr[:, :, 1] = (sg + (eg - sg) * t).astype(np.uint8)
        arr[:, :, 2] = (sb + (eb - sb) * t).astype(np.uint8)
        arr[:, :, 3] = 255
        return Image.fromarray(arr, "RGBA")

    def generate(self, data: str, settings: dict = None) -> io.BytesIO:
        s = {**self.DEFAULT, **(settings or {})}
        if s["format"] == "svg":
            return self._gen_svg(data, s)
        return self._gen_png(data, s)

    def _gen_svg(self, data, s):
        ec = self.ERROR_LEVELS.get(s["error_correction"], qrcode.constants.ERROR_CORRECT_H)
        qr = qrcode.QRCode(error_correction=ec, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        fill = s["fill_color"] if not s["gradient_enabled"] else "#000000"
        back = s["bg_color"] if not s["bg_transparent"] else "#FFFFFF"
        img = qr.make_image(image_factory=SvgPathImage, fill_color=fill, back_color=back)
        buf = io.BytesIO()
        img.save(buf)
        buf.seek(0)
        buf.name = "qr_code.svg"
        return buf

    def _gen_png(self, data, s):
        ec = self.ERROR_LEVELS.get(s["error_correction"], qrcode.constants.ERROR_CORRECT_H)
        qr = qrcode.QRCode(error_correction=ec, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        drawer_cls = self.DOT_STYLES.get(s["dot_style"], pil_drawers.SquareModuleDrawer)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer_cls(),
            fill_color="black",
            back_color="white",
        ).get_image().convert("RGBA")

        arr = np.array(img, dtype=np.float64)
        brightness = np.mean(arr[:, :, :3], axis=2)
        module_mask = (255 - brightness) / 255.0

        if s.get("bg_transparent"):
            bg_arr = np.zeros_like(arr)
        elif s.get("bg_gradient_enabled"):
            bg_img = self.create_gradient(
                img.size, s["bg_gradient_start"], s["bg_gradient_end"], s["bg_gradient_direction"]
            )
            bg_arr = np.array(bg_img, dtype=np.float64)
        else:
            r, g, b = self.parse_hex(s["bg_color"])
            bg_arr = np.zeros((*arr.shape[:2], 4), dtype=np.float64)
            bg_arr[:, :, 0] = r
            bg_arr[:, :, 1] = g
            bg_arr[:, :, 2] = b
            bg_arr[:, :, 3] = 255

        if s.get("gradient_enabled"):
            fg_img = self.create_gradient(
                img.size, s["gradient_start"], s["gradient_end"], s["gradient_direction"]
            )
            fg_arr = np.array(fg_img, dtype=np.float64)
        else:
            r, g, b = self.parse_hex(s["fill_color"])
            fg_arr = np.zeros((*arr.shape[:2], 4), dtype=np.float64)
            fg_arr[:, :, 0] = r
            fg_arr[:, :, 1] = g
            fg_arr[:, :, 2] = b
            fg_arr[:, :, 3] = 255

        mask_3d = module_mask[:, :, np.newaxis]
        result_arr = (fg_arr * mask_3d + bg_arr * (1 - mask_3d)).astype(np.uint8)
        result = Image.fromarray(result_arr, "RGBA")

        if s.get("icon_path"):
            result = self._overlay_icon(result, s["icon_path"], s.get("icon_size", 0.2))

        buf = io.BytesIO()
        result.save(buf, format="PNG")
        buf.seek(0)
        buf.name = "qr_code.png"
        return buf

    def _overlay_icon(self, qr_img, icon_path, size_ratio=0.2):
        try:
            icon = Image.open(icon_path).convert("RGBA")
        except Exception:
            return qr_img
        qr_w, qr_h = qr_img.size
        icon_size = int(min(qr_w, qr_h) * size_ratio)
        if icon_size < 10:
            return qr_img
        icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
        border = max(int(icon_size * 0.1), 2)
        bordered_size = icon_size + border * 2
        bordered = Image.new("RGBA", (bordered_size, bordered_size), (255, 255, 255, 255))
        bordered.paste(icon, (border, border), icon)
        pos_x = (qr_w - bordered_size) // 2
        pos_y = (qr_h - bordered_size) // 2
        qr_img.paste(bordered, (pos_x, pos_y), bordered)
        return qr_img


qr_engine = QREngine()


def encode_qr_data(qr_type: str, raw: str, extra: dict = None) -> str:
    extra = extra or {}
    if qr_type == "url":
        return raw if raw.startswith(("http://", "https://", "tg://")) else f"https://{raw}"
    if qr_type == "text":
        return raw
    if qr_type == "phone":
        return f"tel:{raw}"
    if qr_type == "email":
        return f"mailto:{raw}"
    if qr_type == "sms":
        parts = raw.split(":", 1)
        phone = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        return f"sms:{phone}?body={body}" if body else f"sms:{phone}"
    if qr_type == "wifi":
        ssid = extra.get("ssid", raw)
        password = extra.get("password", "")
        enc = extra.get("encryption", "WPA")
        hidden = extra.get("hidden", "false")
        return f"WIFI:T:{enc};S:{ssid};P:{password};H:{hidden};;"
    if qr_type == "vcard":
        name = extra.get("name", raw)
        phone = extra.get("phone", "")
        email = extra.get("email", "")
        parts = name.split(" ", 1)
        last = parts[0]
        first = parts[1] if len(parts) > 1 else ""
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{last};{first}",
            f"FN:{name}",
        ]
        if phone:
            lines.append(f"TEL;TYPE=CELL:{phone}")
        if email:
            lines.append(f"EMAIL:{email}")
        lines.append("END:VCARD")
        return "\n".join(lines)
    return raw
