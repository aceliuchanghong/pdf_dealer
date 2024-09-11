import os
import cv2
import pytesseract
import re
import argparse
import numpy as np
import random


def detect_text_orientation(image_path, output_dir='./z_test/pics'):
    # 打开图像并将其转换为灰度图像
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"无法加载图像: {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 预处理图像，增加精度
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # 去噪
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 二值化处理

    # 使用 Tesseract 进行 OCR 以检测文本方向
    osd = pytesseract.image_to_osd(gray)  # 使用二值化图像进行OCR
    rotation = int(re.search('(?<=Rotate: )\d+', osd).group(0))

    # 根据检测的旋转角度来调整图像
    if rotation == 90:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif rotation == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    elif rotation == 270:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # 保存或显示旋转后的图像
    if output_dir is not None and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    random_integer1 = random.randint(10000, 200000)
    random_integer2 = random.randint(10, 2000)
    corrected_image_path = os.path.join(f"{output_dir}", f"{random_integer1}_{random_integer2}.png")

    cv2.imwrite(corrected_image_path, img)
    file_name = os.path.basename(image_path)
    if os.path.exists(os.path.join(output_dir, f"{file_name}")):
        os.remove(os.path.join(output_dir, f"{file_name}"))
    os.rename(corrected_image_path, os.path.join(output_dir, f"{file_name}"))

    return os.path.join(output_dir, f"{file_name}")


if __name__ == '__main__':
    """
    python z_utils/rotate_fix_pic.py --image_path z_using_files/pics/test2.jpg --output_dir ./z_test/pics
    """
    parser = argparse.ArgumentParser(description='检测并修正图像的文本方向')
    parser.add_argument('--image_path', type=str, help='输入图像的路径')
    parser.add_argument('--output_dir', type=str, help='输出图像的路径')
    args = parser.parse_args()
    corrected_image = detect_text_orientation(args.image_path, args.output_dir)
    print(f"Corrected image saved as: {corrected_image}")
