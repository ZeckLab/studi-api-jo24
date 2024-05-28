import qrcode
import qrcode.base
import qrcode.constants
import qrcode.image.svg

method = "basic"

def generate_qrcode(data: str) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(data, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, image_factory = factory)
    return img.to_string()