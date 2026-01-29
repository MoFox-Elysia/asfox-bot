# -*- coding: utf-8 -*-
"""
导入导出模块
处理数据的导入导出功能
"""

import os
import zipfile
import shutil
from datetime import datetime
from main import DATA_DIR, IMAGES_DIR, EXPORT_DIR

class ImportExportManager:
    """导入导出管理器"""

    @staticmethod
    def export_all_data():
        """导出全部数据为压缩包"""
        try:
            # 创建导出文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = os.path.join(EXPORT_DIR, f'错题整理备份_{timestamp}.zip')

            # 创建压缩包
            with zipfile.ZipFile(export_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加数据库
                db_file = os.path.join(DATA_DIR, 'questions.db')
                if os.path.exists(db_file):
                    zipf.write(db_file, 'questions.db')

                # 添加图片
                if os.path.exists(IMAGES_DIR):
                    for root, dirs, files in os.walk(IMAGES_DIR):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, IMAGES_DIR)
                            zipf.write(file_path, f'images/{arcname}')

            return True, export_file

        except Exception as e:
            return False, str(e)

    @staticmethod
    def import_data(zip_file_path):
        """导入数据"""
        try:
            # 备份现有数据
            backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(EXPORT_DIR, f'backup_{backup_timestamp}')
            os.makedirs(backup_dir, exist_ok=True)

            # 备份数据库
            db_file = os.path.join(DATA_DIR, 'questions.db')
            if os.path.exists(db_file):
                shutil.copy2(db_file, backup_dir)

            # 备份图片
            if os.path.exists(IMAGES_DIR):
                shutil.copytree(IMAGES_DIR, os.path.join(backup_dir, 'images'))

            # 解压文件
            with zipfile.ZipFile(zip_file_path, 'r') as zipf:
                # 提取数据库
                if 'questions.db' in zipf.namelist():
                    zipf.extract('questions.db', DATA_DIR)

                # 提取图片
                for file in zipf.namelist():
                    if file.startswith('images/'):
                        zipf.extract(file, os.path.dirname(IMAGES_DIR))

            return True, '导入成功'

        except Exception as e:
            # 如果导入失败，恢复备份
            if os.path.exists(backup_dir):
                # 恢复数据库
                backup_db = os.path.join(backup_dir, 'questions.db')
                if os.path.exists(backup_db):
                    shutil.copy2(backup_db, db_file)

                # 恢复图片
                backup_images = os.path.join(backup_dir, 'images')
                if os.path.exists(backup_images):
                    if os.path.exists(IMAGES_DIR):
                        shutil.rmtree(IMAGES_DIR)
                    shutil.copytree(backup_images, IMAGES_DIR)

            return False, str(e)

    @staticmethod
    def export_single_item(image_path, item_type='question'):
        """导出单个项目（错题或试卷）为图片"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            item_name = '错题' if item_type == 'question' else '试卷'
            export_path = os.path.join(EXPORT_DIR, f'{item_name}_{timestamp}.png')

            shutil.copy2(image_path, export_path)
            return True, export_path

        except Exception as e:
            return False, str(e)

    @staticmethod
    def export_paper_group_to_pdf(paper_group_name, subject_id=None, grade=None):
        """导出卷组为PDF"""
        try:
            from fpdf import FPDF
            from PIL import Image as PILImage
            from main import App

            app = App.get_running_app()

            # 获取卷组中的所有试卷
            papers = app.db.get_papers_by_group(
                subject_id=subject_id,
                grade=grade,
                paper_group=paper_group_name
            )

            if not papers:
                return False, '卷组中没有试卷'

            # 创建PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=False)

            # 为每张试卷添加页面
            for paper in papers:
                pdf.add_page()

                try:
                    # 加载图片
                    img = PILImage.open(paper['image_path'])

                    # 计算页面尺寸
                    page_width = pdf.w
                    page_height = pdf.h

                    # 计算图片尺寸，保持比例
                    img_width, img_height = img.size
                    ratio = min(page_width / img_width, page_height / img_height)
                    new_width = img_width * ratio
                    new_height = img_height * ratio

                    # 居中放置
                    x = (page_width - new_width) / 2
                    y = (page_height - new_height) / 2

                    # 保存临时图片
                    temp_path = os.path.join(EXPORT_DIR, 'temp_pdf_image.png')
                    img.save(temp_path)

                    # 添加图片到PDF
                    pdf.image(temp_path, x=x, y=y, w=new_width, h=new_height)

                    # 删除临时文件
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                except Exception as e:
                    print(f"Error adding paper to PDF: {e}")
                    continue

            # 保存PDF
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_path = os.path.join(EXPORT_DIR, f'卷组_{paper_group_name}_{timestamp}.pdf')
            pdf.output(pdf_path)

            return True, pdf_path

        except Exception as e:
            return False, str(e)
