# -*- coding: utf-8 -*-
"""
拍照/图片切割模块
用于框选题目并保存
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
from PIL import Image as PILImage
import os
from datetime import datetime
from main import IMAGES_DIR

class CroppingBox(BoxLayout):
    """裁剪框组件"""
    x1 = NumericProperty(0)
    y1 = NumericProperty(0)
    x2 = NumericProperty(0)
    y2 = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos = (0, 0)
        self.draw_box()

    def draw_box(self):
        """绘制裁剪框"""
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0, 1)  # 红色边框
            Line(rectangle=(0, 0, self.width, self.height), width=2)
            Color(1, 0, 0, 0.2)
            Rectangle(pos=(0, 0), size=self.size)

class PhotoScreen(Screen):
    """拍照/图片切割界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'photo'
        self.current_image = None
        self.current_image_path = None
        self.cropping_boxes = []
        self.is_selecting = False
        self.selection_start = None
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

        btn_select_image = Button(
            text='选择图片',
            font_size='24sp',
            size_hint_x=0.7
        )
        btn_select_image.bind(on_press=self.select_image)

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_select_image)

        layout.add_widget(top_bar)

        # 图片显示区域
        self.image_container = BoxLayout()
        self.image_label = Label(
            text='请选择或拍照获取图片',
            font_size='28sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.image_container.add_widget(self.image_label)
        layout.add_widget(self.image_container)

        # 操作按钮
        button_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_crop = Button(
            text='框选题目',
            font_size='24sp',
            disabled=True
        )
        self.btn_crop = btn_crop
        btn_crop.bind(on_press=self.start_cropping)

        btn_save_draft = Button(
            text='保存到草稿箱',
            font_size='24sp',
            disabled=True
        )
        self.btn_save_draft = btn_save_draft
        btn_save_draft.bind(on_press=self.save_to_draft)

        btn_save_question = Button(
            text='保存为错题',
            font_size='24sp',
            disabled=True
        )
        self.btn_save_question = btn_save_question
        btn_save_question.bind(on_press=self.save_as_question)

        button_layout.add_widget(btn_crop)
        button_layout.add_widget(btn_save_draft)
        button_layout.add_widget(btn_save_question)

        layout.add_widget(button_layout)

        # 说明文字
        hint_label = Label(
            text='框选题目后，可以保存到草稿箱或直接添加到错题库',
            font_size='20sp',
            size_hint_y=None,
            height=60,
            color=(0.5, 0.5, 0.5, 1)
        )
        layout.add_widget(hint_label)

        self.add_widget(layout)

    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'

    def select_image(self, instance):
        """选择图片"""
        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self.handle_file_selection,
                filters=['*.png', '*.jpg', '*.jpeg', '*.bmp']
            )
        except Exception as e:
            # 如果无法使用文件选择器，使用测试图片
            self.load_test_image()

    def handle_file_selection(self, selection):
        """处理文件选择"""
        if selection:
            self.load_image(selection[0])

    def load_test_image(self):
        """加载测试图片（用于开发测试）"""
        # 创建一个空白测试图片
        test_image = PILImage.new('RGB', (800, 600), color='white')
        test_path = os.path.join(IMAGES_DIR, 'test_image.png')
        test_image.save(test_path)
        self.load_image(test_path)

    def load_image(self, image_path):
        """加载图片"""
        self.current_image_path = image_path
        self.current_image = PILImage.open(image_path)

        # 清空之前的裁剪框
        self.cropping_boxes = []

        # 显示图片
        self.image_container.clear_widgets()
        scatter = Scatter(
            do_rotation=False,
            do_scale=True,
            do_translation=True
        )

        img = Image(source=image_path, allow_stretch=True)
        scatter.add_widget(img)
        self.image_container.add_widget(scatter)

        # 启用按钮
        self.btn_crop.disabled = False
        self.btn_save_draft.disabled = False
        self.btn_save_question.disabled = False

    def start_cropping(self, instance):
        """开始框选"""
        if not self.current_image:
            return

        # 简化版：直接裁剪整个图片
        # 在实际应用中，这里应该实现触摸框选功能
        self.crop_full_image()

    def crop_full_image(self):
        """裁剪整个图片（简化版）"""
        if not self.current_image:
            return

        # 保存裁剪后的图片
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        crop_filename = f'crop_{timestamp}.png'
        crop_path = os.path.join(IMAGES_DIR, crop_filename)

        # 保存原图
        self.current_image.save(crop_path)

        # 显示成功提示
        from kivy.uix.toast import Toast
        toast = Toast(text='图片已保存')
        toast.show()

        # 询问用户下一步操作
        self.ask_next_action(crop_path)

    def ask_next_action(self, image_path):
        """询问用户下一步操作"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn_save_draft = Button(
            text='保存到草稿箱',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_save_draft.bind(on_press=lambda instance: self.perform_save_draft(image_path, popup))

        btn_save_question = Button(
            text='添加到错题库',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_save_question.bind(on_press=lambda instance: self.perform_save_question(image_path, popup))

        content.add_widget(btn_save_draft)
        content.add_widget(btn_save_question)

        popup = Popup(
            title='选择操作',
            content=content,
            size_hint=(0.8, 0.5)
        )
        popup.open()

    def perform_save_draft(self, image_path, popup):
        """执行保存到草稿箱"""
        popup.dismiss()

        # 保存到数据库
        from main import App
        app = App.get_running_app()
        app.db.add_draft(image_path)

        from kivy.uix.toast import Toast
        toast = Toast(text='已保存到草稿箱')
        toast.show()

    def perform_save_question(self, image_path, popup):
        """执行保存为错题"""
        popup.dismiss()

        # 跳转到错题编辑界面
        question_edit_screen = self.manager.get_screen('question_edit')
        question_edit_screen.set_new_question_image(image_path)
        self.manager.current = 'question_edit'

    def save_to_draft(self, instance):
        """保存到草稿箱"""
        if not self.current_image_path:
            return

        self.perform_save_draft(self.current_image_path, None)

    def save_as_question(self, instance):
        """保存为错题"""
        if not self.current_image_path:
            return

        self.perform_save_question(self.current_image_path, None)
