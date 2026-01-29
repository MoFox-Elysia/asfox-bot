# -*- coding: utf-8 -*-
"""
草稿箱模块
用于保存和管理用户上传的图片
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
import os

class DraftItem(BoxLayout):
    """草稿项组件"""
    image_path = StringProperty('')
    draft_id = None
    parent_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 300
        self.spacing = 10
        self.padding = 10

        # 图片
        self.image = Image(
            source=self.image_path,
            size_hint_y=0.8,
            allow_stretch=True
        )
        self.add_widget(self.image)

        # 按钮布局
        button_layout = BoxLayout(size_hint_y=0.2, spacing=5)

        btn_add_question = Button(
            text='添加错题',
            font_size='18sp'
        )
        btn_add_question.bind(on_press=self.add_to_question)

        btn_delete = Button(
            text='删除',
            font_size='18sp'
        )
        btn_delete.bind(on_press=self.delete_draft)

        button_layout.add_widget(btn_add_question)
        button_layout.add_widget(btn_delete)
        self.add_widget(button_layout)

    def add_to_question(self, instance):
        """添加到错题库"""
        question_edit_screen = self.parent_screen.manager.get_screen('question_edit')
        question_edit_screen.set_new_question_image(self.image_path)
        self.parent_screen.manager.current = 'question_edit'

    def delete_draft(self, instance):
        """删除草稿"""
        # 删除数据库记录
        from main import App
        app = App.get_running_app()
        app.db.delete_draft(self.draft_id)

        # 删除文件
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

        # 刷新界面
        self.parent_screen.load_drafts()

class DraftScreen(Screen):
    """草稿箱界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'draft'
        self.build_ui()

    def build_ui(self):
        """构建界面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 顶部工具栏
        top_bar = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_back = Button(
            text='返回',
            font_size='24sp',
            size_hint_x=0.3
        )
        btn_back.bind(on_press=self.go_back)

        btn_refresh = Button(
            text='刷新',
            font_size='24sp',
            size_hint_x=0.7
        )
        btn_refresh.bind(on_press=self.load_drafts)

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_refresh)

        layout.add_widget(top_bar)

        # 草稿列表
        scroll_view = ScrollView()
        self.draft_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        self.draft_grid.bind(minimum_height=self.draft_grid.setter('height'))
        scroll_view.add_widget(self.draft_grid)
        layout.add_widget(scroll_view)

        # 空状态提示
        self.empty_label = Label(
            text='暂无草稿',
            font_size='28sp',
            color=(0.5, 0.5, 0.5, 1)
        )

        self.add_widget(layout)

        # 延迟加载数据
        Clock.schedule_once(lambda dt: self.load_drafts())

    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'

    def load_drafts(self, instance=None):
        """加载草稿列表"""
        from main import App
        app = App.get_running_app()

        # 清空列表
        self.draft_grid.clear_widgets()

        # 获取所有草稿
        drafts = app.db.get_all_drafts()

        if not drafts:
            # 显示空状态
            if self.empty_label.parent:
                self.empty_label.parent.remove_widget(self.empty_label)
            self.draft_grid.add_widget(self.empty_label)
            return

        # 添加草稿项
        for draft in drafts:
            if os.path.exists(draft['image_path']):
                item = DraftItem(image_path=draft['image_path'])
                item.draft_id = draft['id']
                item.parent_screen = self
                self.draft_grid.add_widget(item)
