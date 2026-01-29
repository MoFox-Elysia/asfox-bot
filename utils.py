# -*- coding: utf-8 -*-
"""
工具模块
提供通用的辅助函数
"""

from PIL import Image as PILImage
import os

def create_thumbnail(image_path, size=(200, 150)):
    """创建缩略图"""
    try:
        img = PILImage.open(image_path)
        img.thumbnail(size, PILImage.Resampling.LANCZOS)

        # 生成缩略图路径
        base, ext = os.path.splitext(image_path)
        thumb_path = f"{base}_thumb{ext}"

        img.save(thumb_path)
        return thumb_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return image_path

def get_image_size(image_path):
    """获取图片尺寸"""
    try:
        img = PILImage.open(image_path)
        return img.size
    except Exception as e:
        print(f"Error getting image size: {e}")
        return (0, 0)

def resize_image(image_path, max_width=None, max_height=None):
    """调整图片大小"""
    try:
        img = PILImage.open(image_path)
        original_width, original_height = img.size

        # 计算新尺寸
        if max_width and max_height:
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        elif max_width:
            ratio = max_width / original_width
            new_width = max_width
            new_height = int(original_height * ratio)
        elif max_height:
            ratio = max_height / original_height
            new_width = int(original_width * ratio)
            new_height = max_height
        else:
            return image_path

        # 调整大小
        img_resized = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

        # 保存
        img_resized.save(image_path)
        return image_path

    except Exception as e:
        print(f"Error resizing image: {e}")
        return image_path

def crop_image(image_path, x, y, width, height):
    """裁剪图片"""
    try:
        img = PILImage.open(image_path)
        cropped = img.crop((x, y, x + width, y + height))
        cropped.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error cropping image: {e}")
        return image_path

def validate_image(image_path):
    """验证图片是否有效"""
    try:
        img = PILImage.open(image_path)
        img.verify()
        return True
    except Exception as e:
        print(f"Invalid image: {e}")
        return False

def get_file_size(file_path):
    """获取文件大小（字节）"""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        print(f"Error getting file size: {e}")
        return 0

def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def ensure_directory(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def delete_file(file_path):
    """删除文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def copy_file(source, destination):
    """复制文件"""
    try:
        import shutil
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def move_file(source, destination):
    """移动文件"""
    try:
        import shutil
        shutil.move(source, destination)
        return True
    except Exception as e:
        print(f"Error moving file: {e}")
        return False
