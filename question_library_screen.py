# -*- coding: utf-8 -*-
"""
错题库模块
用于整理和查找错题
包含科目、年级、章节/知识点/专题的目录结构
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

class QuestionItem(BoxLayout):
    """错题项组件"""
    question_data = None
    parent_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 350
        self.spacing = 10
        self.padding = 10

        # 创建背景
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # 图片
        from kivy.uix.image import Image
        self.image = Image(
            source=self.question_data['image_path'] if self.question_data else '',
            size_hint_y=0.7,
            allow_stretch=True
        )
        self.add_widget(self.image)

        # 信息标签
        info_text = self.format_info()
        info_label = Label(
            text=info_text,
            font_size='16sp',
            size_hint_y=0.15,
            halign='left',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        self.add_widget(info_label)

        # 按钮布局
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)

        btn_view = Button(
            text='查看',
            font_size='16sp'
        )
        btn_view.bind(on_press=self.view_question)

        btn_edit = Button(
            text='编辑',
            font_size='16sp'
        )
        btn_edit.bind(on_press=self.edit_question)

        btn_delete = Button(
            text='删除',
            font_size='16sp'
        )
        btn_delete.bind(on_press=self.delete_question)

        button_layout.add_widget(btn_view)
        button_layout.add_widget(btn_edit)
        button_layout.add_widget(btn_delete)
        self.add_widget(button_layout)

    def update_rect(self, instance, value):
        """更新背景矩形"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def format_info(self):
        """格式化错题信息"""
        if not self.question_data:
            return ''

        info_parts = []
        info_parts.append(f"科目: {self.question_data.get('subject_name', '未知')}")
        info_parts.append(f"年级: {self.question_data.get('grade', '未知')}")

        if self.question_data.get('chapter'):
            info_parts.append(f"章节: {self.question_data['chapter']}")
        if self.question_data.get('knowledge_point'):
            info_parts.append(f"知识点: {self.question_data['knowledge_point']}")
        if self.question_data.get('topic'):
            info_parts.append(f"专题: {self.question_data['topic']}")

        if self.question_data.get('importance', 0) > 0:
            importance = '★' * self.question_data['importance']
            info_parts.append(f"重要性: {importance}")

        return ' | '.join(info_parts)

    def view_question(self, instance):
        """查看错题详情"""
        self.parent_screen.view_question_detail(self.question_data)

    def edit_question(self, instance):
        """编辑错题"""
        question_edit_screen = self.parent_screen.manager.get_screen('question_edit')
        question_edit_screen.load_question(self.question_data['id'])
        self.parent_screen.manager.current = 'question_edit'

    def delete_question(self, instance):
        """删除错题"""
        # 确认对话框
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn_confirm = Button(
            text='确认删除',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_confirm.bind(on_press=lambda instance: self.perform_delete(popup))

        btn_cancel = Button(
            text='取消',
            font_size='24sp',
            size_hint_y=None,
            height=80
        )
        btn_cancel.bind(on_press=lambda instance: popup.dismiss())

        content.add_widget(btn_confirm)
        content.add_widget(btn_cancel)

        popup = Popup(
            title='确认删除',
            content=content,
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def perform_delete(self, popup):
        """执行删除"""
        popup.dismiss()

        from main import App
        app = App.get_running_app()
        app.db.delete_question(self.question_data['id'])

        # 刷新列表
        self.parent_screen.load_questions()

class QuestionLibraryScreen(Screen):
    """错题库界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'question_library'
        self.current_subject_id = None
        self.current_grade = None
        self.current_filter_type = None  # 'chapter', 'knowledge_point', 'topic'
        self.current_filter_value = None
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

        btn_filter = Button(
            text='筛选',
            font_size='24sp',
            size_hint_x=0.7
        )
        btn_filter.bind(on_press=self.show_filter_dialog)

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_filter)

        layout.add_widget(top_bar)

        # 当前筛选条件显示
        self.filter_label = Label(
            text='全部错题',
            font_size='22sp',
            size_hint_y=None,
            height=50,
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(self.filter_label)

        # 错题列表（2列）
        scroll_view = ScrollView()
        self.question_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None
        )
        self.question_grid.bind(minimum_height=self.question_grid.setter('height'))
        scroll_view.add_widget(self.question_grid)
        layout.add_widget(scroll_view)

        # 空状态提示
        self.empty_label = Label(
            text='暂无错题',
            font_size='28sp',
            color=(0.5, 0.5, 0.5, 1)
        )

        self.add_widget(layout)

        # 延迟加载数据
        Clock.schedule_once(lambda dt: self.load_questions())

    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'

    def show_filter_dialog(self, instance):
        """显示筛选对话框"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # 科目选择
        subject_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        subject_layout.add_widget(Label(text='科目:', font_size='20sp', size_hint_x=0.3))

        from kivy.uix.spinner import Spinner
        subjects = self.get_subjects()
        subject_names = ['全部'] + [s['name'] for s in subjects]
        self.subject_spinner = Spinner(
            text='全部',
            values=subject_names,
            font_size='20sp',
            size_hint_x=0.7
        )
        subject_layout.add_widget(self.subject_spinner)
        content.add_widget(subject_layout)

        # 年级选择
        grade_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        grade_layout.add_widget(Label(text='年级:', font_size='20sp', size_hint_x=0.3))

        grade_names = ['全部', '小学', '初中', '高中']
        self.grade_spinner = Spinner(
            text='全部',
            values=grade_names,
            font_size='20sp',
            size_hint_x=0.7
        )
        grade_layout.add_widget(self.grade_spinner)
        content.add_widget(grade_layout)

        # 筛选类型
        filter_type_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        filter_type_layout.add_widget(Label(text='分类:', font_size='20sp', size_hint_x=0.3))

        filter_types = ['全部', '章节', '知识点', '专题']
        self.filter_type_spinner = Spinner(
            text='全部',
            values=filter_types,
            font_size='20sp',
            size_hint_x=0.7
        )
        filter_type_layout.add_widget(self.filter_type_spinner)
        content.add_widget(filter_type_layout)

        # 筛选值
        filter_value_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        filter_value_layout.add_widget(Label(text='值:', font_size='20sp', size_hint_x=0.3))

        self.filter_value_spinner = Spinner(
            text='全部',
            values=['全部'],
            font_size='20sp',
            size_hint_x=0.7
        )
        filter_value_layout.add_widget(self.filter_value_spinner)
        content.add_widget(filter_value_layout)

        # 监听筛选类型变化，更新筛选值列表
        self.filter_type_spinner.bind(text=self.on_filter_type_change)

        # 按钮
        button_layout = BoxLayout(size_hint_y=None, height=80, spacing=10)

        btn_apply = Button(
            text='应用筛选',
            font_size='24sp'
        )
        btn_apply.bind(on_press=self.apply_filter)

        btn_reset = Button(
            text='重置',
            font_size='24sp'
        )
        btn_reset.bind(on_press=self.reset_filter)

        button_layout.add_widget(btn_apply)
        button_layout.add_widget(btn_reset)
        content.add_widget(button_layout)

        popup = Popup(
            title='筛选错题',
            content=content,
            size_hint=(0.8, 0.7)
        )
        popup.open()

    def get_subjects(self):
        """获取所有科目"""
        from main import App
        app = App.get_running_app()
        return app.db.get_all_subjects()

    def on_filter_type_change(self, instance, value):
        """筛选类型变化时更新筛选值"""
        if value == '全部':
            self.filter_value_spinner.values = ['全部']
            self.filter_value_spinner.text = '全部'
            return

        field_map = {
            '章节': 'chapter',
            '知识点': 'knowledge_point',
            '专题': 'topic'
        }
        field = field_map.get(value)

        # 获取当前选中的科目和年级
        subject_id = None
        if self.subject_spinner.text != '全部':
            subjects = self.get_subjects()
            for s in subjects:
                if s['name'] == self.subject_spinner.text:
                    subject_id = s['id']
                    break

        grade = None
        if self.grade_spinner.text != '全部':
            grade = self.grade_spinner.text

        # 获取筛选值
        from main import App
        app = App.get_running_app()
        values = app.db.get_all_unique_values(field, subject_id, grade)

        self.filter_value_spinner.values = ['全部'] + values
        self.filter_value_spinner.text = '全部'

    def apply_filter(self, instance):
        """应用筛选"""
        # 获取筛选条件
        subject_id = None
        if self.subject_spinner.text != '全部':
            subjects = self.get_subjects()
            for s in subjects:
                if s['name'] == self.subject_spinner.text:
                    subject_id = s['id']
                    break

        grade = None
        if self.grade_spinner.text != '全部':
            grade = self.grade_spinner.text

        filter_type = self.filter_type_spinner.text
        filter_value = None
        if filter_type != '全部' and self.filter_value_spinner.text != '全部':
            field_map = {
                '章节': 'chapter',
                '知识点': 'knowledge_point',
                '专题': 'topic'
            }
            filter_value = self.filter_value_spinner.text
            self.current_filter_type = field_map[filter_type]
        else:
            self.current_filter_type = None

        self.current_filter_value = filter_value

        # 更新筛选标签
        filter_parts = []
        if subject_id:
            filter_parts.append(self.subject_spinner.text)
        if grade:
            filter_parts.append(grade)
        if self.current_filter_type and filter_value:
            filter_parts.append(f"{filter_type}: {filter_value}")

        self.filter_label.text = ' | '.join(filter_parts) if filter_parts else '全部错题'

        # 加载错题
        self.load_questions()

        # 关闭弹窗
        instance.parent.parent.parent.dismiss()

    def reset_filter(self, instance):
        """重置筛选"""
        self.subject_spinner.text = '全部'
        self.grade_spinner.text = '全部'
        self.filter_type_spinner.text = '全部'
        self.filter_value_spinner.text = '全部'

    def load_questions(self):
        """加载错题列表"""
        from main import App
        app = App.get_running_app()

        # 清空列表
        self.question_grid.clear_widgets()

        # 获取错题
        questions = app.db.get_questions_by_filters(
            subject_id=self.current_subject_id,
            grade=self.current_grade,
            chapter=self.current_filter_value if self.current_filter_type == 'chapter' else None,
            knowledge_point=self.current_filter_value if self.current_filter_type == 'knowledge_point' else None,
            topic=self.current_filter_value if self.current_filter_type == 'topic' else None
        )

        if not questions:
            # 显示空状态
            if self.empty_label.parent:
                self.empty_label.parent.remove_widget(self.empty_label)
            self.question_grid.add_widget(self.empty_label)
            return

        # 添加错题项（2列）
        for question in questions:
            item = QuestionItem()
            item.question_data = question
            item.parent_screen = self
            self.question_grid.add_widget(item)

    def view_question_detail(self, question_data):
        """查看错题详情（最大化预览）"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 图片
        from kivy.uix.image import Image
        img = Image(
            source=question_data['image_path'],
            allow_stretch=True,
            size_hint_y=0.8
        )
        content.add_widget(img)

        # 信息
        info_text = f"科目: {question_data.get('subject_name', '未知')}\n"
        info_text += f"年级: {question_data.get('grade', '未知')}\n"
        if question_data.get('chapter'):
            info_text += f"章节: {question_data['chapter']}\n"
        if question_data.get('knowledge_point'):
            info_text += f"知识点: {question_data['knowledge_point']}\n"
        if question_data.get('topic'):
            info_text += f"专题: {question_data['topic']}\n"
        if question_data.get('importance', 0) > 0:
            importance = '★' * question_data['importance']
            info_text += f"重要性: {importance}\n"
        info_text += f"时间: {question_data.get('created_at', '未知')}"

        info_label = Label(
            text=info_text,
            font_size='18sp',
            size_hint_y=0.15,
            halign='left',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        content.add_widget(info_label)

        # 按钮
        button_layout = BoxLayout(size_hint_y=0.05, spacing=10)

        btn_print = Button(
            text='打印',
            font_size='18sp'
        )
        btn_print.bind(on_press=lambda instance: self.print_question(question_data['image_path']))

        btn_export = Button(
            text='导出',
            font_size='18sp'
        )
        btn_export.bind(on_press=lambda instance: self.export_question(question_data['image_path']))

        btn_close = Button(
            text='关闭',
            font_size='18sp'
        )
        btn_close.bind(on_press=lambda instance: popup.dismiss())

        button_layout.add_widget(btn_print)
        button_layout.add_widget(btn_export)
        button_layout.add_widget(btn_close)
        content.add_widget(button_layout)

        popup = Popup(
            title='错题详情',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def print_question(self, image_path):
        """打印错题"""
        from kivy.uix.toast import Toast
        toast = Toast(text='正在调用打印机...')
        toast.show()
        # 实际打印功能需要根据平台实现

    def export_question(self, image_path):
        """导出错题为图片"""
        import shutil
        from datetime import datetime
        from main import EXPORT_DIR

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_path = os.path.join(EXPORT_DIR, f'错题_{timestamp}.png')
            shutil.copy2(image_path, export_path)

            from kivy.uix.toast import Toast
            toast = Toast(text='已导出到相册')
            toast.show()
        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'导出失败: {str(e)}')
            toast.show()
