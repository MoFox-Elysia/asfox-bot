# -*- coding: utf-8 -*-
"""
打印服务模块
处理打印功能
"""

import os
from kivy.utils import platform

class PrintService:
    """打印服务"""

    @staticmethod
    def print_image(image_path):
        """打印图片"""
        try:
            if platform == 'android':
                # Android 打印
                PrintService.print_android(image_path)
            elif platform == 'win':
                # Windows 打印
                PrintService.print_windows(image_path)
            elif platform == 'linux':
                # Linux 打印
                PrintService.print_linux(image_path)
            elif platform == 'macosx':
                # macOS 打印
                PrintService.print_macos(image_path)
            else:
                return False, '不支持的平台'
            return True, '打印任务已发送'

        except Exception as e:
            return False, str(e)

    @staticmethod
    def print_android(image_path):
        """Android 打印"""
        try:
            from jnius import autoclass
            from android import activity

            # 获取当前Activity
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            current_activity = PythonActivity.mActivity

            # 创建打印意图
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            # 创建图片文件URI
            image_file = File(image_path)
            image_uri = Uri.fromFile(image_file)

            # 创建打印意图
            print_intent = Intent()
            print_intent.setAction(Intent.ACTION_SEND)
            print_intent.setType('image/*')
            print_intent.putExtra(Intent.EXTRA_STREAM, image_uri)

            # 启动打印选择器
            current_activity.startActivity(
                Intent.createChooser(print_intent, '选择打印机')
            )

        except Exception as e:
            raise Exception(f"Android打印失败: {str(e)}")

    @staticmethod
    def print_windows(image_path):
        """Windows 打印"""
        try:
            import subprocess
            import win32print
            import win32api

            # 获取默认打印机
            printer_name = win32print.GetDefaultPrinter()

            # 使用默认打印机打印图片
            # 方法1: 使用系统默认图片查看器打印
            os.startfile(image_path, 'print')

            # 方法2: 使用Windows打印命令
            # subprocess.run(['rundll32.exe', 'shimgvw.dll,ImageView_PrintTo',
            #                image_path, printer_name])

        except Exception as e:
            raise Exception(f"Windows打印失败: {str(e)}")

    @staticmethod
    def print_linux(image_path):
        """Linux 打印"""
        try:
            import subprocess

            # 使用lp命令打印
            subprocess.run(['lp', image_path], check=True)

        except Exception as e:
            raise Exception(f"Linux打印失败: {str(e)}")

    @staticmethod
    def print_macos(image_path):
        """macOS 打印"""
        try:
            import subprocess

            # 使用lp命令打印
            subprocess.run(['lp', image_path], check=True)

        except Exception as e:
            raise Exception(f"macOS打印失败: {str(e)}")

    @staticmethod
    def print_pdf(pdf_path):
        """打印PDF文件"""
        try:
            if platform == 'android':
                # Android 打印PDF
                PrintService.print_pdf_android(pdf_path)
            elif platform == 'win':
                # Windows 打印PDF
                PrintService.print_pdf_windows(pdf_path)
            elif platform == 'linux':
                # Linux 打印PDF
                PrintService.print_pdf_linux(pdf_path)
            elif platform == 'macosx':
                # macOS 打印PDF
                PrintService.print_pdf_macos(pdf_path)
            else:
                return False, '不支持的平台'
            return True, '打印任务已发送'

        except Exception as e:
            return False, str(e)

    @staticmethod
    def print_pdf_android(pdf_path):
        """Android 打印PDF"""
        try:
            from jnius import autoclass

            # 获取当前Activity
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            current_activity = PythonActivity.mActivity

            # 创建打印意图
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            File = autoclass('java.io.File')

            # 创建PDF文件URI
            pdf_file = File(pdf_path)
            pdf_uri = Uri.fromFile(pdf_file)

            # 创建打印意图
            print_intent = Intent()
            print_intent.setAction(Intent.ACTION_SEND)
            print_intent.setType('application/pdf')
            print_intent.putExtra(Intent.EXTRA_STREAM, pdf_uri)

            # 启动打印选择器
            current_activity.startActivity(
                Intent.createChooser(print_intent, '选择打印机')
            )

        except Exception as e:
            raise Exception(f"Android打印PDF失败: {str(e)}")

    @staticmethod
    def print_pdf_windows(pdf_path):
        """Windows 打印PDF"""
        try:
            # 使用默认PDF阅读器打印
            os.startfile(pdf_path, 'print')

        except Exception as e:
            raise Exception(f"Windows打印PDF失败: {str(e)}")

    @staticmethod
    def print_pdf_linux(pdf_path):
        """Linux 打印PDF"""
        try:
            import subprocess

            # 使用lp命令打印
            subprocess.run(['lp', pdf_path], check=True)

        except Exception as e:
            raise Exception(f"Linux打印PDF失败: {str(e)}")

    @staticmethod
    def print_pdf_macos(pdf_path):
        """macOS 打印PDF"""
        try:
            import subprocess

            # 使用lp命令打印
            subprocess.run(['lp', pdf_path], check=True)

        except Exception as e:
            raise Exception(f"macOS打印PDF失败: {str(e)}")
