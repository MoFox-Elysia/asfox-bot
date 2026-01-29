# -*- coding: utf-8 -*-
"""
试卷库模块
用于管理和查看用户编辑的试卷
包含科目、年级、卷组的目录结构
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.clock import Clock
import os

class PaperItem(BoxLayout):
    """试卷项组件"""
    paper_data = None
    parent_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 400
        self.spacing = 10
        self.padding = 10

        # 创建背景
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # 图片
        self.image = Image(
            source=self.paper_data['image_path'] if self.paper_data else '',
            size_hint_y=0.7,
            allow_stretch=True
        )
        self.add_widget(self.image)

        # 信息标签
        info_text = self.format_info()
        info_label = Label(
            text=info_text,
            font_size='18sp',
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
            font_size='18sp'
        )
        btn_view.bind(on_press=self.view_paper)

        btn_export_pdf = Button(
            text='导出PDF',
            font_size='18sp'
        )
        btn_export_pdf.bind(on_press=self.export_pdf)

        btn_delete = Button(
            text='删除',
            font_size='18sp'
        )
        btn_delete.bind(on_press=self.delete_paper)

        button_layout.add_widget(btn_view)
        button_layout.add_widget(btn_export_pdf)
        button_layout.add_widget(btn_delete)
        self.add_widget(button_layout)

    def update_rect(self, instance, value):
        """更新背景矩形"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def format_info(self):
        """格式化试卷信息"""
        if not self.paper_data:
            return ''

        info_parts = []
        info_parts.append(f"名称: {self.paper_data.get('name', '未知')}")
        info_parts.append(f"科目: {self.paper_data.get('subject_name', '未知')}")
        info_parts.append(f"年级: {self.paper_data.get('grade', '未知')}")
        info_parts.append(f"卷组: {self.paper_data.get('paper_group', '未知')}")

        return '\n'.join(info_parts)

    def view_paper(self, instance):
        """查看试卷详情"""
        self.parent_screen.view_paper_detail(self.paper_data)

    def export_pdf(self, instance):
        """导出为PDF"""
        self.parent_screen.export_paper_to_pdf(self.paper_data)

    def delete_paper(self, instance):
        """删除试卷"""
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
        app.db.delete_paper(self.paper_data['id'])

        # 刷新列表
        self.parent_screen.load_papers()

class PaperLibraryScreen(Screen):
    """试卷库界面"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'paper_library'
        self.current_subject_id = None
        self.current_grade = None
        self.current_paper_group = None
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
            text='全部试卷',
            font_size='22sp',
            size_hint_y=None,
            height=50,
            color=(0.3, 0.3, 0.3, 1)
        )
        layout.add_widget(self.filter_label)

        # 试卷列表（1列）
        scroll_view = ScrollView()
        self.paper_grid = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )
        self.paper_grid.bind(minimum_height=self.paper_grid.setter('height'))
        scroll_view.add_widget(self.paper_grid)
        layout.add_widget(scroll_view)

        # 空状态提示
        self.empty_label = Label(
            text='暂无试卷',
            font_size='28sp',
            color=(0.5, 0.5, 0.5, 1)
        )

        self.add_widget(layout)

        # 延迟加载数据
        Clock.schedule_once(lambda dt: self.load_papers())

    def go_back(self, instance):
        """返回主界面"""
        self.manager.current = 'main'

    def show_filter_dialog(self, instance):
        """显示筛选对话框"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # 科目选择
        subject_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        subject_layout.add_widget(Label(text='科目:', font_size='20sp', size_hint_x=0.3))

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

        # 卷组选择
        group_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        group_layout.add_widget(Label(text='卷组:', font_size='20sp', size_hint_x=0.3))

        self.paper_group_spinner = Spinner(
            text='全部',
            values=['全部'],
            font_size='20sp',
            size_hint_x=0.7
        )
        group_layout.add_widget(self.paper_group_spinner)
        content.add_widget(group_layout)

        # 监听科目和年级变化，更新卷组列表
        self.subject_spinner.bind(text=self.update_paper_groups)
        self.grade_spinner.bind(text=self.update_paper_groups)

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
            title='筛选试卷',
            content=content,
            size_hint=(0.8, 0.6)
        )
        popup.open()

        # 初始化卷组列表
        Clock.schedule_once(lambda dt: self.update_paper_groups())

    def get_subjects(self):
        """获取所有科目"""
        from main import App
        app = App.get_running_app()
        return app.db.get_all_subjects()

    def update_paper_groups(self, instance=None, value=None):
        """更新卷组列表"""
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

        # 获取卷组
        from main import App
        app = App.get_running_app()
        groups = app.db.get_paper_groups(subject_id, grade)

        self.paper_group_spinner.values = ['全部'] + groups
        self.paper_group_spinner.text = '全部'

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

        paper_group = None
        if self.paper_group_spinner.text != '全部':
            paper_group = self.paper_group_spinner.text

        self.current_subject_id = subject_id
        self.current_grade = grade
        self.current_paper_group = paper_group

        # 更新筛选标签
        filter_parts = []
        if subject_id:
            filter_parts.append(self.subject_spinner.text)
        if grade:
            filter_parts.append(grade)
        if paper_group:
            filter_parts.append(f"卷组: {paper_group}")

        self.filter_label.text = ' | '.join(filter_parts) if filter_parts else '全部试卷'

        # 加载试卷
        self.load_papers()

        # 关闭弹窗
        instance.parent.parent.parent.dismiss()

    def reset_filter(self, instance):
        """重置筛选"""
        self.subject_spinner.text = '全部'
        self.grade_spinner.text = '全部'
        self.paper_group_spinner.text = '全部'

    def load_papers(self):
        """加载试卷列表"""
        from main import App
        app = App.get_running_app()

        # 清空列表
        self.paper_grid.clear_widgets()

        # 获取试卷
        papers = app.db.get_papers_by_group(
            subject_id=self.current_subject_id,
            grade=self.current_grade,
            paper_group=self.current_paper_group
        )

        if not papers:
            # 显示空状态
            if self.empty_label.parent:
                self.empty_label.parent.remove_widget(self.empty_label)
            self.paper_grid.add_widget(self.empty_label)
            return

        # 添加试卷项（1列）
        for paper in papers:
            item = PaperItem()
            item.paper_data = paper
            item.parent_screen = self
            self.paper_grid.add_widget(item)

    def view_paper_detail(self, paper_data):
        """查看试卷详情（最大化预览）"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 图片
        img = Image(
            source=paper_data['image_path'],
            allow_stretch=True,
            size_hint_y=0.8
        )
        content.add_widget(img)

        # 信息
        info_text = f"名称: {paper_data.get('name', '未知')}\n"
        info_text += f"科目: {paper_data.get('subject_name', '未知')}\n"
        info_text += f"年级: {paper_data.get('grade', '未知')}\n"
        info_text += f"卷组: {paper_data.get('paper_group', '未知')}\n"
        info_text += f"创建时间: {paper_data.get('created_at', '未知')}"

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
        btn_print.bind(on_press=lambda instance: self.print_paper(paper_data['image_path']))

        btn_export = Button(
            text='导出图片',
            font_size='18sp'
        )
        btn_export.bind(on_press=lambda instance: self.export_paper_image(paper_data['image_path']))

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
            title='试卷详情',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def print_paper(self, image_path):
        """打印试卷"""
        from kivy.uix.toast import Toast
        toast = Toast(text='正在调用打印机...')
        toast.show()
        # 实际打印功能需要根据平台实现

    def export_paper_image(self, image_path):
        """导出试卷为图片"""
        import shutil
        from datetime import datetime
        from main import EXPORT_DIR

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            export_path = os.path.join(EXPORT_DIR, f'试卷_{timestamp}.png')
            shutil.copy2(image_path, export_path)

            from kivy.uix.toast import Toast
            toast = Toast(text='已导出到相册')
            toast.show()
        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'导出失败: {str(e)}')
            toast.show()

    def export_paper_to_pdf(self, paper_data):
        """导出试卷为PDF"""
        try:
            from fpdf import FPDF
            from PIL import Image as PILImage
            from datetime import datetime
            from main import EXPORT_DIR

            # 创建PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=False)

            # 添加页面
            pdf.add_page()

            # 加载图片
            img = PILImage.open(paper_data['image_path'])

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

            # 保存PDF
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_path = os.path.join(EXPORT_DIR, f'试卷_{timestamp}.pdf')
            pdf.output(pdf_path)

            # 删除临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)

            from kivy.uix.toast import Toast
            toast = Toast(text='PDF导出成功')
            toast.show()

        except Exception as e:
            from kivy.uix.toast import Toast
            toast = Toast(text=f'导出失败: {str(e)}')
            toast.show()
