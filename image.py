from PIL import Image
from constants import *
import numpy as np
from datetime import datetime


class ImageProcessor:
    def __init__(self, image_name):
        self.image_path = input_path + image_name
        self.image = None
        self.load_image()

    def load_image(self):
        self.image = Image.open(self.image_path)

    # 获取图片最低二进制位
    def image_decode(self):
        pixels = np.array(self.image)
        binary_ends = pixels[..., 2] % 2
        return binary_ends

    # 将最低二进制位写入图片
    def image_encode(self, binary_ends):
        encoded_image = self.image.copy()
        pixels = np.array(encoded_image)
        pixels[..., 2] = (pixels[..., 2] & 0xFE) | binary_ends
        encoded_image = Image.fromarray(pixels)

        current_time = datetime.now()
        formatted_time = current_time.strftime('%y%m%d%H%M%S')

        output_image_path = output_path + "OutputImage_" + formatted_time + ".png"
        encoded_image.save(output_image_path)  # 保存编码后的图片
