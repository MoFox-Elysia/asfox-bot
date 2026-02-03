# -*- coding: utf-8 -*-
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.utils import platform

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

for dir_path in [APP_DIR, DATA_DIR, IMAGES_DIR, EXPORT_DIR]:
    os.makedirs(dir_path, exist_ok=True)

from database import DatabaseManager
from main_screen import MainScreen
from photo_screen import PhotoScreen
from draft_screen import DraftScreen
from question_library_screen import QuestionLibraryScreen
from question_edit_screen import QuestionEditScreen
from paper_edit_screen import PaperEditScreen
from paper_library_screen import PaperLibraryScreen

class ErrorQuestionApp(App):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(os.path.join(DATA_DIR, 'questions.db'))
        self.title = '错题整理'

    def build(self):
        if platform != 'android':
            Window.size = (1080, 1920)
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(PhotoScreen(name='photo'))
        sm.add_widget(DraftScreen(name='draft'))
        sm.add_widget(QuestionLibraryScreen(name='question_library'))
        sm.add_widget(QuestionEditScreen(name='question_edit'))
        sm.add_widget(PaperEditScreen(name='paper_edit'))
        sm.add_widget(PaperLibraryScreen(name='paper_library'))
        return sm

    def on_stop(self):
        self.db.close()

if __name__ == '__main__':
    ErrorQuestionApp().run()