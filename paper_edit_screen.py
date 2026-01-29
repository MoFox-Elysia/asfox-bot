# -*- coding: utf-8 -*-
"""
组卷模块
提供A4/A3模板，支持拖拽错题到模板任意位置
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.clock import Clock
from PIL import Image as PILImage
from PIL import ImageDraw
import os
from datetime import datetime
from main import IMAGES_DIR, EXPORT_DIR

class DraggableQuestion(Scatter):
    """可拖动的错题组件"""
    question_data = None
    parent_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_rotation = False
        self.do_scale = True
        self.do_translation = True
        self.auto_bring_to_front = True

        # 设置大小
        self.size_hint = (None, None)
        self.size = (200, 150)

        # 添加图片
        img = Image(
            source=self.question_data['image_path'] if self.question_data else '',
            allow_stretch=True
        )
        self.add_widget(img)

        # 添加边框
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.border = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, instance, value):
        """更新边框"""
        self.border.pos = instance.pos
        self.border.size = instance.size

    def on_touch_down(self, touch):
        """触摸事件"""
        if self.collide_point(*touch.pos):
            # 记录起始位置
            self.start_pos = self.pos
        return super().on_touch_down(touch)

class QuestionSelectorItem(BoxLayout):
    """错题选择器项"""
    question_data = None
    parent_screen = None
    is_selected = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 250
        self.spacing = 5
        self.padding = 5

        # 选择按钮
        self.select_btn = ToggleButton(
            text='选择',
            font_size='18sp',
            size_hint_y=None,
            height=40
        )
        self.select_btn.bind(on_press=self.toggle_select)
        self.add_widget(self.select_btn)

        # 图片
        img = Image(
            source=self.question_data['image_path'] if self.question_data else '',
            size_hint_y=0.8,
            allow_stretch=True
        )
        self.add_widget(img)

        # 信息
        info_text = f"{self.question_data.get('subject_name', '')} | {self.question_data.get('grade', '')}"
        info_label = Label(
            text=info_text,
            font_size='14sp',
            size_hint_y=None,
            height=30
        )
        self.add_widget(info_label)

    def toggle_select(self, instance):
        """切换选择状态"""
        self.is_selected = instance.state == 'down'
        if self.is_selected:
            self.parent_screen.add_to_candidate(self.question_data)
        else:
            self.parent_screen.remove_from_candidate(self.question_data['id'])

class PaperEditScreen(Screen):
    """组卷编辑界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'paper_edit'
        self.selected_questions = []  # 选中的错题
        self.candidate_questions = []  # 候选栏中的错题
        self.paper_size = 'A4'  # A4 或 A3
        self.build_ui()

    def build_ui(self):
        """构建界面"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 顶部工具栏
        top_bar = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_back = Button(
            text='返回',
            font_size='24sp',
            size_hint_x=0.2
        )
        btn_back.bind(on_press=self.go_back)

        btn_select_questions = Button(
            text='选择错题',
            font_size='24sp',
            size_hint_x=0.4
        )
        btn_select_questions.bind(on_press=self.show_question_selector)

        btn_save = Button(
            text='保存试卷',
            font_size='24sp',
            size_hint_x=0.4
        )
        btn_save.bind(on_press=self.save_paper)

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_select_questions)
        top_bar.add_widget(btn_save)

        layout.add_widget(top_bar)

        # 模板选择和编辑区域
        edit_layout = BoxLayout(orientation='horizontal', spacing=10)

        # 左侧：编辑区域
        left_layout = BoxLayout(orientation='vertical', spacing=10)

        # 纸张大小选择
        paper_size_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        paper_size_layout.add_widget(Label(text='纸张:', font_size='20sp', size_hint_x=0.3))

        self.paper_size_spinner = BoxLayout(size_hint_x=0.7)

        btn_a4 = Button(
            text='A4',
            font_size='20sp'
        )
        btn_a4.bind(on_press=lambda instance: self.set_paper_size('A4'))

        btn_a3 = Button(
            text='A3',
            font_size='20sp'
        )
        btn_a3.bind(on_press=lambda instance: self.set_paper_size('A3'))

        self.paper_size_spinner.add_widget(btn_a4)
        self.paper_size_spinner.add_widget(btn_a3)
        paper_size_layout.add_widget(self.paper_size_spinner)
        left_layout.add_widget(paper_size_layout)

        # 试卷模板区域
        self.paper_container = BoxLayout(
            size_hint_y=0.8,
            padding=10
        )
        self.create_paper_template()
        left_layout.add_widget(self.paper_container)

        # 说明
        hint_label = Label(
            text='拖动错题到模板上，可缩放和移动位置',
            font_size='18sp',
            size_hint_y=None,
            height=60,
            color=(0.5, 0.5, 0.5, 1)
        )
        left_layout.add_widget(hint_label)

        edit_layout.add_widget(left_layout)

        # 右侧：候选栏
        right_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.3)

        right_header = Label(
            text='候选错题',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        right_layout.add_widget(right_header)

        scroll_view = ScrollView()
        self.candidate_grid = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.candidate_grid.bind(minimum_height=self.candidate_grid.setter('height'))
        scroll_view.add_widget(self.candidate_grid)
        right_layout.add_widget(scroll_view)

        edit_layout.add_widget(right_layout)

        layout.add_widget(edit_layout)

        self.add_widget(layout)

    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'

    def set_paper_size(self, size):
        """设置纸张大小"""
        self.paper_size = size
        self.create_paper_template()

    def create_paper_template(self):
        """创建试卷模板"""
        self.paper_container.clear_widgets()

        # 根据纸张大小设置尺寸
        if self.paper_size == 'A4':
            width, height = 2480, 3508  # A4 @ 300 DPI
        else:  # A3
            width, height = 3508, 4961  # A3 @ 300 DPI

        # 创建背景
        template = BoxLayout(
            size_hint=(None, None),
            size=(width * 0.3, height * 0.3),  # 缩小显示
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        with template.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=template.pos, size=template.size)

        # 添加已放置的错题
        for question in self.candidate_questions:
            if 'position' in question:
                draggable = DraggableQuestion(question_data=question)
                draggable.parent_screen = self
                draggable.pos = question['position']
                template.add_widget(draggable)

        self.paper_container.add_widget(template)

    def show_question_selector(self, instance):
        """显示错题选择器"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 筛选工具栏
        filter_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_refresh = Button(
            text='刷新',
            font_size='20sp'
        )
        btn_refresh.bind(on_press=lambda instance: self.load_selector_questions())

        btn_confirm = Button(
            text='确认选择',
            font_size='20sp'
        )
        btn_confirm.bind(on_press=lambda instance: self.confirm_selection(popup))

        btn_close = Button(
            text='关闭',
            font_size='20sp'
        )
        btn_close.bind(on_press=lambda instance: popup.dismiss())

        filter_layout.add_widget(btn_refresh)
        filter_layout.add_widget(btn_confirm)
        filter_layout.add_widget(btn_close)
        content.add_widget(filter_layout)

        # 错题列表
        scroll_view = ScrollView()
        self.selector_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        self.selector_grid.bind(minimum_height=self.selector_grid.setter('height'))
        scroll_view.add_widget(self.selector_grid)
        content.add_widget(scroll_view)

        popup = Popup(
            title='选择错题',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

        # 加载错题列表
        Clock.schedule_once(lambda dt: self.load_selector_questions())

    def load_selector_questions(self):
        """加载错题选择器列表"""
        from main import App
        app = App.get_running_app()

        # 清空列表
        self.selector_grid.clear_widgets()

        # 获取所有错题
        questions = app.db.get_questions_by_filters()

        # 添加错题项
        for question in questions:
            item = QuestionSelectorItem(question_data=question)
            item.parent_screen = self
            self.selector_grid.add_widget(item)

    def add_to_candidate(self, question_data):
        """添加到候选栏"""
        # 检查是否已存在
        for q in self.candidate_questions:
            if q['id'] == question_data['id']:
                return

        # 添加到候选列表
        self.candidate_questions.append({
            **question_data,
            'position': (100, 100)  # 默认位置
        })

        # 更新候选栏显示
        self.update_candidate_display()

    def remove_from_candidate(self, question_id):
        """从候选栏移除"""
        self.candidate_questions = [q for q in self.candidate_questions if q['id'] != question_id]
        self.update_candidate_display()

    def update_candidate_display(self):
        """更新候选栏显示"""
        self.candidate_grid.clear_widgets()

        for question in self.candidate_questions:
            item = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=5)

            # 图片
            img = Image(
                source=question['image_path'],
                allow_stretch=True
            )
            item.add_widget(img)

            # 删除按钮
            btn_remove = Button(
                text='移除',
                font_size='16sp',
                size_hint_y=None,
                height=40
            )
            btn_remove.bind(on_press=lambda instance, q=question: self.remove_from_candidate(q['id']))
            item.add_widget(btn_remove)

            self.candidate_grid.add_widget(item)

    def confirm_selection(self, popup):
        """确认选择"""
        popup.dismiss()

        # 在模板上添加错题
        self.create_paper_template()

        # 将错题添加到模板
        template = self.paper_container.children[0]
        for question in self.candidate_questions:
            if 'position' not in question:
                draggable = DraggableQuestion(question_data=question)
                draggable.parent_screen = self
                draggable.pos = (100, 100)
                question['position'] = (100, 100)
                template.add_widget(draggable)

    def save_paper(self, instance):
        """保存试卷"""
        if not self.candidate_questions:
            from kivy.uix.toast import Toast
            toast = Toast(text='请先选择错题')
            toast.show()
            return

        # 显示保存对话框
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # 试卷名称
        name_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        name_layout.add_widget(Label(text='试卷名称:', font_size='22sp', size_hint_x=0.4))

        name_input = BoxLayout(size_hint_x=0.6)
        from kivy.uix.textinput import TextInput
        self.paper_name_input = TextInput(
            text=f'试卷_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            font_size='22sp',
            multiline=False
        )
        name_input.add_widget(self.paper_name_input)
        name_layout.add_widget(name_input)
        content.add_widget(name_layout)

        # 保存选项
        save_options = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_save_local = Button(
            text='保存到相册',
            font_size='22sp'
        )
        btn_save_local.bind(on_press=lambda instance: self.save_to_local(popup))

        btn_save_library = Button(
            text='保存到题库',
            font_size='22sp'
        )
        btn_save_library.bind(on_press=lambda instance: self.save_to_library(popup))

        save_options.add_widget(btn_save_local)
        save_options.add_widget(btn_save_library)
        content.add_widget(save_options)

        btn_cancel = Button(
            text='取消',
            font_size='22sp',
            size_hint_y=None,
            height=60
        )
        btn_cancel.bind(on_press=lambda instance: popup.dismiss())
        content.add_widget(btn_cancel)

        popup = Popup(
            title='保存试卷',
            content=content,
            size_hint=(0.8, 0.5)
        )
        popup.open()

    def generate_paper_image(self):
        """生成试卷图片"""
        # 根据纸张大小创建画布
        if self.paper_size == 'A4':
            width, height = 2480, 3508  # A4 @ 300 DPI
        else:  # A3
            width, height = 3508, 4961  # A3 @ 300 DPI

        # 创建白色背景
        paper = PILImage.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(paper)

        # 在画布上绘制错题
        for question in self.candidate_questions:
            if 'position' in question:
                try:
                    # 打开错题图片
                    q_img = PILImage.open(question['image_path'])

                    # 缩放图片（适配显示）
                    display_size = (200, 150)
                    scale_x = width / (2480 if self.paper_size == 'A4' else 3508)
                    scale_y = height / (3508 if self.paper_size == 'A4' else 4961)

                    # 计算实际位置和大小
                    x = int(question['position'][0] / 0.3 / scale_x)
                    y = int(question['position'][1] / 0.3 / scale_y)
                    w = int(display_size[0] / 0.3 / scale_x)
                    h = int(display_size[1] / 0.3 / scale_y)

                    # 缩放错题图片
                    q_img = q_img.resize((w, h), PILImage.Resampling.LANCZOS)

                    # 粘贴到试卷上
                    paper.paste(q_img, (x, y))

                except Exception as e:
                    print(f"Error drawing question: {e}")
                    continue

        return paper

    def save_to_local(self, popup):
        """保存到本地相册"""
        popup.dismiss()

        try:
            # 生成试卷图片
            paper = self.generate_paper_image()

            # 保存到导出目录
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'试卷_{timestamp}.png'
            filepath = os.path.join(EXPORT_DIR, filename)
            paper.save(filepath, dpi=(300, 300))

            from kivy.uix.toast import Toast
            toast = Toast(text='已保存到相册')
            toast.show()

        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'保存失败: {str(e)}')
            toast.show()

    def save_to_library(self, popup):
        """保存到题库"""
        popup.dismiss()

        # 显示输入卷组对话框
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # 卷组名称
        group_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)
        group_layout.add_widget(Label(text='卷组名称:', font_size='22sp', size_hint_x=0.4))

        from kivy.uix.textinput import TextInput
        group_input = TextInput(
            text='默认卷组',
            font_size='22sp',
            multiline=False
        )
        group_layout.add_widget(group_input)
        content.add_widget(group_layout)

        # 确认按钮
        btn_confirm = Button(
            text='确认',
            font_size='22sp',
            size_hint_y=None,
            height=60
        )
        btn_confirm.bind(on_press=lambda instance: self.perform_save_to_library(group_input.text, popup2))
        content.add_widget(btn_confirm)

        btn_cancel = Button(
            text='取消',
            font_size='22sp',
            size_hint_y=None,
            height=60
        )
        btn_cancel.bind(on_press=lambda instance: popup2.dismiss())
        content.add_widget(btn_cancel)

        popup2 = Popup(
            title='输入卷组名称',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup2.open()

    def perform_save_to_library(self, paper_group, popup):
        """执行保存到题库"""
        popup.dismiss()

        try:
            # 生成试卷图片
            paper = self.generate_paper_image()

            # 保存图片
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'试卷_{timestamp}.png'
            filepath = os.path.join(IMAGES_DIR, filename)
            paper.save(filepath, dpi=(300, 300))

            # 确定年级（取最高年级）
            grade_order = {'小学': 1, '初中': 2, '高中': 3}
            max_grade = max(self.candidate_questions, key=lambda q: grade_order.get(q['grade'], 0))
            grade = max_grade['grade']

            # 确定科目（取第一题的科目）
            subject_id = self.candidate_questions[0]['subject_id']

            # 保存到数据库
            from main import App
            app = App.get_running_app()
            paper_id = app.db.add_paper(
                self.paper_name_input.text,
                subject_id,
                grade,
                paper_group,
                filepath
            )

            # 保存错题关联
            for question in self.candidate_questions:
                # 计算相对位置
                if self.paper_size == 'A4':
                    paper_width, paper_height = 2480, 3508
                else:
                    paper_width, paper_height = 3508, 4961

                x = question.get('position', [0, 0])[0] / paper_width
                y = question.get('position', [0, 0])[1] / paper_height

                # 这里简化处理，实际应该保存精确的位置信息
                pass

            from kivy.uix.toast import Toast
            toast = Toast(text='已保存到试卷库')
            toast.show()

            # 清空候选栏
            self.candidate_questions = []
            self.update_candidate_display()
            self.create_paper_template()

        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'保存失败: {str(e)}')
            toast.show()
