# -*- coding: utf-8 -*-
"""
错题信息编辑模块
提供学科、年级、章节/知识点/专题、重要性等编辑选项
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import os

class QuestionEditScreen(Screen):
    """错题信息编辑界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'question_edit'
        self.current_question_id = None
        self.new_question_image = None
        self.build_ui()

    def build_ui(self):
        """构建界面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 顶部工具栏
        top_bar = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_back = Button(
            text='取消',
            font_size='24sp',
            size_hint_x=0.3
        )
        btn_back.bind(on_press=self.cancel_edit)

        btn_save = Button(
            text='保存',
            font_size='24sp',
            size_hint_x=0.7
        )
        btn_save.bind(on_press=self.save_question)

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_save)

        layout.add_widget(top_bar)

        # 滚动视图
        scroll_view = ScrollView()
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)

        # 图片预览
        self.image_container = BoxLayout(size_hint_y=None, height=300)
        self.image_label = Label(
            text='无图片',
            font_size='24sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        self.image_container.add_widget(self.image_label)
        content_layout.add_widget(self.image_container)

        # 科目（必填）
        subject_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        subject_layout.add_widget(Label(text='科目*:', font_size='22sp', size_hint_x=0.3))
        self.subject_spinner = Spinner(
            text='选择科目',
            values=[],
            font_size='22sp',
            size_hint_x=0.7
        )
        subject_layout.add_widget(self.subject_spinner)
        content_layout.add_widget(subject_layout)

        # 新建科目按钮
        btn_new_subject = Button(
            text='+ 新建科目',
            font_size='20sp',
            size_hint_y=None,
            height=60
        )
        btn_new_subject.bind(on_press=self.show_new_subject_dialog)
        content_layout.add_widget(btn_new_subject)

        # 年级（必填）
        grade_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        grade_layout.add_widget(Label(text='年级*:', font_size='22sp', size_hint_x=0.3))
        self.grade_spinner = Spinner(
            text='选择年级',
            values=['小学', '初中', '高中'],
            font_size='22sp',
            size_hint_x=0.7
        )
        grade_layout.add_widget(self.grade_spinner)
        content_layout.add_widget(grade_layout)

        # 章节（可选）
        chapter_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        chapter_layout.add_widget(Label(text='章节:', font_size='22sp', size_hint_x=0.3))
        self.chapter_input = TextInput(
            text='',
            font_size='22sp',
            size_hint_x=0.7,
            multiline=False,
            hint_text='输入章节名称'
        )
        chapter_layout.add_widget(self.chapter_input)
        content_layout.add_widget(chapter_layout)

        # 知识点（可选）
        knowledge_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        knowledge_layout.add_widget(Label(text='知识点:', font_size='22sp', size_hint_x=0.3))
        self.knowledge_input = TextInput(
            text='',
            font_size='22sp',
            size_hint_x=0.7,
            multiline=False,
            hint_text='输入知识点'
        )
        knowledge_layout.add_widget(self.knowledge_input)
        content_layout.add_widget(knowledge_layout)

        # 专题（可选）
        topic_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        topic_layout.add_widget(Label(text='专题:', font_size='22sp', size_hint_x=0.3))
        self.topic_input = TextInput(
            text='',
            font_size='22sp',
            size_hint_x=0.7,
            multiline=False,
            hint_text='输入专题'
        )
        topic_layout.add_widget(self.topic_input)
        content_layout.add_widget(topic_layout)

        # 重要性（可选）
        importance_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        importance_layout.add_widget(Label(text='重要性:', font_size='22sp', size_hint_x=0.3))
        self.importance_spinner = Spinner(
            text='普通',
            values=['普通', '重要', '非常重要', '紧急'],
            font_size='22sp',
            size_hint_x=0.7
        )
        importance_layout.add_widget(self.importance_spinner)
        content_layout.add_widget(importance_layout)

        # 提示信息
        hint_label = Label(
            text='注：章节、知识点、专题至少填写一个',
            font_size='18sp',
            size_hint_y=None,
            height=50,
            color=(0.8, 0.4, 0.4, 1)
        )
        content_layout.add_widget(hint_label)

        content_layout.bind(minimum_height=content_layout.setter('height'))
        scroll_view.add_widget(content_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

        # 加载科目列表
        Clock.schedule_once(lambda dt: self.load_subjects())

    def load_subjects(self):
        """加载科目列表"""
        from main import App
        app = App.get_running_app()
        subjects = app.db.get_all_subjects()
        subject_names = [s['name'] for s in subjects]
        self.subject_spinner.values = subject_names
        if subject_names:
            self.subject_spinner.text = subject_names[0]

    def set_new_question_image(self, image_path):
        """设置新错题的图片"""
        self.new_question_image = image_path
        self.current_question_id = None

        # 显示图片
        self.image_container.clear_widgets()
        img = Image(source=image_path, allow_stretch=True)
        self.image_container.add_widget(img)

        # 重置表单
        self.reset_form()

    def load_question(self, question_id):
        """加载错题信息"""
        from main import App
        app = App.get_running_app()
        question = app.db.get_question_by_id(question_id)

        if not question:
            return

        self.current_question_id = question_id
        self.new_question_image = None

        # 显示图片
        self.image_container.clear_widgets()
        img = Image(source=question['image_path'], allow_stretch=True)
        self.image_container.add_widget(img)

        # 填充表单
        self.subject_spinner.text = question['subject_name']
        self.grade_spinner.text = question['grade']
        self.chapter_input.text = question['chapter'] or ''
        self.knowledge_input.text = question['knowledge_point'] or ''
        self.topic_input.text = question['topic'] or ''

        # 设置重要性
        importance_map = {
            0: '普通',
            1: '普通',
            2: '重要',
            3: '重要',
            4: '非常重要',
            5: '紧急'
        }
        self.importance_spinner.text = importance_map.get(question['importance'], '普通')

    def reset_form(self):
        """重置表单"""
        self.subject_spinner.text = '选择科目'
        self.grade_spinner.text = '小学'
        self.chapter_input.text = ''
        self.knowledge_input.text = ''
        self.topic_input.text = ''
        self.importance_spinner.text = '普通'

    def show_new_subject_dialog(self, instance):
        """显示新建科目对话框"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        input_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        input_layout.add_widget(Label(text='科目名称:', font_size='22sp', size_hint_x=0.4))

        subject_name_input = TextInput(
            text='',
            font_size='22sp',
            size_hint_x=0.6,
            multiline=False
        )
        input_layout.add_widget(subject_name_input)
        content.add_widget(input_layout)

        # 按钮
        button_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_add = Button(
            text='添加',
            font_size='24sp'
        )
        btn_add.bind(on_press=lambda instance: self.add_subject(subject_name_input.text, popup))

        btn_cancel = Button(
            text='取消',
            font_size='24sp'
        )
        btn_cancel.bind(on_press=lambda instance: popup.dismiss())

        button_layout.add_widget(btn_add)
        button_layout.add_widget(btn_cancel)
        content.add_widget(button_layout)

        popup = Popup(
            title='新建科目',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def add_subject(self, subject_name, popup):
        """添加科目"""
        if not subject_name.strip():
            from kivy.uix.toast import Toast
            toast = Toast(text='请输入科目名称')
            toast.show()
            return

        from main import App
        app = App.get_running_app()
        app.db.add_subject(subject_name.strip())

        # 刷新科目列表
        self.load_subjects()
        self.subject_spinner.text = subject_name.strip()

        popup.dismiss()

        from kivy.uix.toast import Toast
        toast = Toast(text='科目添加成功')
        toast.show()

    def cancel_edit(self, instance):
        """取消编辑"""
        self.manager.current = 'question_library'

    def save_question(self, instance):
        """保存错题"""
        # 验证必填字段
        if self.subject_spinner.text == '选择科目':
            from kivy.uix.toast import Toast
            toast = Toast(text='请选择科目')
            toast.show()
            return

        # 验证至少填写一个分类
        chapter = self.chapter_input.text.strip()
        knowledge = self.knowledge_input.text.strip()
        topic = self.topic_input.text.strip()

        if not chapter and not knowledge and not topic:
            from kivy.uix.toast import Toast
            toast = Toast(text='章节、知识点、专题至少填写一个')
            toast.show()
            return

        # 获取科目ID
        from main import App
        app = App.get_running_app()
        subjects = app.db.get_all_subjects()
        subject_id = None
        for s in subjects:
            if s['name'] == self.subject_spinner.text:
                subject_id = s['id']
                break

        if not subject_id:
            from kivy.uix.toast import Toast
            toast = Toast(text='科目不存在')
            toast.show()
            return

        # 获取重要性
        importance_map = {
            '普通': 1,
            '重要': 2,
            '非常重要': 4,
            '紧急': 5
        }
        importance = importance_map.get(self.importance_spinner.text, 1)

        # 确定图片路径
        if self.new_question_image:
            image_path = self.new_question_image
        elif self.current_question_id:
            question = app.db.get_question_by_id(self.current_question_id)
            image_path = question['image_path']
        else:
            from kivy.uix.toast import Toast
            toast = Toast(text='请先拍照或选择图片')
            toast.show()
            return

        # 保存或更新错题
        if self.current_question_id:
            # 更新
            app.db.update_question(
                self.current_question_id,
                subject_id,
                self.grade_spinner.text,
                chapter if chapter else None,
                knowledge if knowledge else None,
                topic if topic else None,
                importance
            )
        else:
            # 新增
            app.db.add_question(
                image_path,
                subject_id,
                self.grade_spinner.text,
                chapter if chapter else None,
                knowledge if knowledge else None,
                topic if topic else None,
                importance
            )

        from kivy.uix.toast import Toast
        toast = Toast(text='保存成功')
        toast.show()

        # 返回错题库
        self.manager.current = 'question_library'
