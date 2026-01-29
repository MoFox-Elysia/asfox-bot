# -*- coding: utf-8 -*-
"""
主界面模块
包含6个主要功能入口
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.clock import Clock
import os

class MainButton(Button):
    """自定义主界面按钮"""
    icon_text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.2, 0.6, 1, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = '28sp'
        self.size_hint_y = None
        self.height = 120
        self.pos_hint = {'center_x': 0.5}

class MainScreen(Screen):
    """主界面 - 包含6个功能入口"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        self.build_ui()

    def build_ui(self):
        """构建主界面"""
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 标题
        title_label = Label(
            text='错题整理',
            font_size='48sp',
            size_hint_y=None,
            height=100,
            color=(0.1, 0.1, 0.1, 1)
        )
        main_layout.add_widget(title_label)

        # 按钮网格 - 2列3行
        button_grid = GridLayout(
            cols=2,
            spacing=15,
            size_hint_y=0.8
        )

        # 创建6个功能按钮
        buttons = [
            ('📷 拍错题', 'photo'),
            ('📝 组卷', 'paper_edit'),
            ('📚 错题库', 'question_library'),
            ('📄 试卷库', 'paper_library'),
            ('🗑️ 草稿箱', 'draft'),
            ('🔄 导入导出', 'import_export')
        ]

        for text, screen_name in buttons:
            btn = MainButton(text=text)
            btn.bind(on_press=lambda instance, name=screen_name: self.go_to_screen(name))
            button_grid.add_widget(btn)

        main_layout.add_widget(button_grid)

        # 底部提示
        hint_label = Label(
            text='点击按钮开始使用',
            font_size='20sp',
            size_hint_y=None,
            height=60,
            color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(hint_label)

        self.add_widget(main_layout)

    def go_to_screen(self, screen_name):
        """跳转到指定屏幕"""
        if screen_name == 'import_export':
            # 导入导出功能（需要单独实现）
            self.show_import_export_dialog()
        else:
            self.manager.current = screen_name

    def show_import_export_dialog(self):
        """显示导入导出对话框"""
        # 这里可以添加导入导出对话框
        # 暂时显示提示
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn_export = Button(
            text='导出全部数据',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_export.bind(on_press=self.export_all_data)

        btn_import = Button(
            text='导入数据',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_import.bind(on_press=self.import_data)

        btn_close = Button(
            text='关闭',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_close.bind(on_press=lambda instance: popup.dismiss())

        content.add_widget(btn_export)
        content.add_widget(btn_import)
        content.add_widget(btn_close)

        popup = Popup(
            title='导入导出',
            content=content,
            size_hint=(0.8, 0.6)
        )
        popup.open()

    def export_all_data(self, instance):
        """导出全部数据"""
        import zipfile
        import shutil
        from datetime import datetime
        from main import EXPORT_DIR

        try:
            # 创建导出文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_file = os.path.join(EXPORT_DIR, f'错题整理备份_{timestamp}.zip')

            # 创建压缩包
            with zipfile.ZipFile(export_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 添加数据库
                from main import DATA_DIR
                db_file = os.path.join(DATA_DIR, 'questions.db')
                if os.path.exists(db_file):
                    zipf.write(db_file, 'questions.db')

                # 添加图片
                from main import IMAGES_DIR
                if os.path.exists(IMAGES_DIR):
                    for root, dirs, files in os.walk(IMAGES_DIR):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, IMAGES_DIR)
                            zipf.write(file_path, f'images/{arcname}')

            from kivy.uix.toast import Toast
            toast = Toast(text='导出成功！')
            toast.show()

        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'导出失败: {str(e)}')
            toast.show()

    def import_data(self, instance):
        """导入数据"""
        # 这里需要实现文件选择器和数据导入逻辑
        from kivy.uix.toast import Toast
        toast = Toast(text='请选择要导入的压缩包')
        toast.show()
