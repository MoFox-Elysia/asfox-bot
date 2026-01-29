# -*- coding: utf-8 -*-
"""
错题整理软件 - Android应用
主入口文件
"""

import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import platform

# 添加项目路径
if platform == 'android':
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    Context = autoclass('android.content.Context')
    external_storage = activity.getExternalFilesDir(None)
    BASE_DIR = str(external_storage.getAbsolutePath())
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_DIR = os.path.join(BASE_DIR, '错题整理软件')
DATA_DIR = os.path.join(APP_DIR, 'data')
IMAGES_DIR = os.path.join(APP_DIR, 'images')
EXPORT_DIR = os.path.join(APP_DIR, 'export')

# 创建必要的目录
for dir_path in [APP_DIR, DATA_DIR, IMAGES_DIR, EXPORT_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# 导入各个模块
from database import DatabaseManager
from main_screen import MainScreen
from photo_screen import PhotoScreen
from draft_screen import DraftScreen
from question_library_screen import QuestionLibraryScreen
from question_edit_screen import QuestionEditScreen
from paper_edit_screen import PaperEditScreen
from paper_library_screen import PaperLibraryScreen
import_export_screen = None

class ErrorQuestionApp(App):
    """错题整理应用主类"""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(os.path.join(DATA_DIR, 'questions.db'))
        self.title = '错题整理'

    def build(self):
        """构建应用界面"""
        # 设置窗口大小（仅用于桌面测试）
        if platform != 'android':
            Window.size = (1080, 1920)

        # 创建屏幕管理器
        sm = ScreenManager()

        # 添加各个屏幕
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(PhotoScreen(name='photo'))
        sm.add_widget(DraftScreen(name='draft'))
        sm.add_widget(QuestionLibraryScreen(name='question_library'))
        sm.add_widget(QuestionEditScreen(name='question_edit'))
        sm.add_widget(PaperEditScreen(name='paper_edit'))
        sm.add_widget(PaperLibraryScreen(name='paper_library'))

        return sm

    def on_stop(self):
        """应用停止时关闭数据库连接"""
        self.db.close()

if __name__ == '__main__':
    ErrorQuestionApp().run()
