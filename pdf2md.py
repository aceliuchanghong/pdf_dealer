import os
import cv2
import pytesseract
import re
import argparse
import numpy as np
import random

if __name__ == '__main__':
    """
    python pdf2md.py --input_md_path xx.pdf
    """
    parser = argparse.ArgumentParser(description='开始识别')
    parser.add_argument('--input_md_path', type=str, help='输入pdf路径')
    args = parser.parse_args()
