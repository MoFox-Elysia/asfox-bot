# -*- coding: utf-8 -*-
"""
数据库管理模块
处理所有数据库操作
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    """数据库管理器"""

    def __init__(self, db_path: str):
        """初始化数据库连接"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # 返回字典形式

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """创建所有数据表"""
        cursor = self.conn.cursor()

        # 科目表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 错题表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                grade TEXT NOT NULL,  # 小学、初中、高中
                chapter TEXT,
                knowledge_point TEXT,
                topic TEXT,
                importance INTEGER DEFAULT 0,  # 0-5，0为默认
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        ''')

        # 试卷表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                grade TEXT NOT NULL,
                paper_group TEXT NOT NULL,
                image_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        ''')

        # 试卷-错题关联表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paper_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                position_x REAL,
                position_y REAL,
                FOREIGN KEY (paper_id) REFERENCES papers(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')

        # 草稿表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    # ==================== 科目管理 ====================

    def add_subject(self, name: str) -> int:
        """添加科目"""
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO subjects (name) VALUES (?)', (name,))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_subjects(self) -> List[Dict]:
        """获取所有科目"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM subjects ORDER BY name')
        return [dict(row) for row in cursor.fetchall()]

    def get_subject_by_id(self, subject_id: int) -> Optional[Dict]:
        """根据ID获取科目"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # ==================== 错题管理 ====================

    def add_question(self, image_path: str, subject_id: int, grade: str,
                    chapter: str = None, knowledge_point: str = None,
                    topic: str = None, importance: int = 0) -> int:
        """添加错题"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO questions
            (image_path, subject_id, grade, chapter, knowledge_point, topic, importance)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (image_path, subject_id, grade, chapter, knowledge_point, topic, importance))
        self.conn.commit()
        return cursor.lastrowid

    def update_question(self, question_id: int, subject_id: int, grade: str,
                       chapter: str = None, knowledge_point: str = None,
                       topic: str = None, importance: int = None):
        """更新错题信息"""
        cursor = self.conn.cursor()
        fields = ['subject_id = ?', 'grade = ?']
        params = [subject_id, grade]

        if chapter is not None:
            fields.append('chapter = ?')
            params.append(chapter)
        if knowledge_point is not None:
            fields.append('knowledge_point = ?')
            params.append(knowledge_point)
        if topic is not None:
            fields.append('topic = ?')
            params.append(topic)
        if importance is not None:
            fields.append('importance = ?')
            params.append(importance)

        params.append(question_id)

        cursor.execute(f'''
            UPDATE questions SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', params)
        self.conn.commit()

    def delete_question(self, question_id: int):
        """删除错题"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
        self.conn.commit()

    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """根据ID获取错题"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT q.*, s.name as subject_name
            FROM questions q
            LEFT JOIN subjects s ON q.subject_id = s.id
            WHERE q.id = ?
        ''', (question_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_questions_by_filters(self, subject_id: int = None, grade: str = None,
                                chapter: str = None, knowledge_point: str = None,
                                topic: str = None) -> List[Dict]:
        """根据条件筛选错题"""
        cursor = self.conn.cursor()
        conditions = []
        params = []

        if subject_id is not None:
            conditions.append('q.subject_id = ?')
            params.append(subject_id)
        if grade is not None:
            conditions.append('q.grade = ?')
            params.append(grade)
        if chapter is not None:
            conditions.append('q.chapter = ?')
            params.append(chapter)
        if knowledge_point is not None:
            conditions.append('q.knowledge_point = ?')
            params.append(knowledge_point)
        if topic is not None:
            conditions.append('q.topic = ?')
            params.append(topic)

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        cursor.execute(f'''
            SELECT q.*, s.name as subject_name
            FROM questions q
            LEFT JOIN subjects s ON q.subject_id = s.id
            {where_clause}
            ORDER BY q.importance DESC, q.created_at DESC
        ''', params)

        return [dict(row) for row in cursor.fetchall()]

    def get_all_unique_values(self, field: str, subject_id: int = None, grade: str = None) -> List[str]:
        """获取指定字段的所有唯一值"""
        cursor = self.conn.cursor()
        conditions = []
        params = []

        if subject_id is not None:
            conditions.append('subject_id = ?')
            params.append(subject_id)
        if grade is not None:
            conditions.append('grade = ?')
            params.append(grade)

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        cursor.execute(f'''
            SELECT DISTINCT {field} FROM questions
            {where_clause} AND {field} IS NOT NULL AND {field} != ''
            ORDER BY {field}
        ''', params)

        return [row[0] for row in cursor.fetchall()]

    # ==================== 试卷管理 ====================

    def add_paper(self, name: str, subject_id: int, grade: str,
                  paper_group: str, image_path: str) -> int:
        """添加试卷"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO papers (name, subject_id, grade, paper_group, image_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, subject_id, grade, paper_group, image_path))
        self.conn.commit()
        return cursor.lastrowid

    def get_papers_by_group(self, subject_id: int = None, grade: str = None,
                           paper_group: str = None) -> List[Dict]:
        """根据条件获取试卷"""
        cursor = self.conn.cursor()
        conditions = []
        params = []

        if subject_id is not None:
            conditions.append('subject_id = ?')
            params.append(subject_id)
        if grade is not None:
            conditions.append('grade = ?')
            params.append(grade)
        if paper_group is not None:
            conditions.append('paper_group = ?')
            params.append(paper_group)

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        cursor.execute(f'''
            SELECT p.*, s.name as subject_name
            FROM papers p
            LEFT JOIN subjects s ON p.subject_id = s.id
            {where_clause}
            ORDER BY p.created_at DESC
        ''', params)

        return [dict(row) for row in cursor.fetchall()]

    def get_paper_by_id(self, paper_id: int) -> Optional[Dict]:
        """根据ID获取试卷"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.*, s.name as subject_name
            FROM papers p
            LEFT JOIN subjects s ON p.subject_id = s.id
            WHERE p.id = ?
        ''', (paper_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_paper_groups(self, subject_id: int = None, grade: str = None) -> List[str]:
        """获取所有卷组"""
        cursor = self.conn.cursor()
        conditions = []
        params = []

        if subject_id is not None:
            conditions.append('subject_id = ?')
            params.append(subject_id)
        if grade is not None:
            conditions.append('grade = ?')
            params.append(grade)

        where_clause = ' WHERE ' + ' AND '.join(conditions) if conditions else ''

        cursor.execute(f'''
            SELECT DISTINCT paper_group FROM papers
            {where_clause}
            ORDER BY paper_group
        ''', params)

        return [row[0] for row in cursor.fetchall()]

    def delete_paper(self, paper_id: int):
        """删除试卷"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM paper_questions WHERE paper_id = ?', (paper_id,))
        cursor.execute('DELETE FROM papers WHERE id = ?', (paper_id,))
        self.conn.commit()

    # ==================== 草稿管理 ====================

    def add_draft(self, image_path: str) -> int:
        """添加草稿"""
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO drafts (image_path) VALUES (?)', (image_path,))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_drafts(self) -> List[Dict]:
        """获取所有草稿"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM drafts ORDER BY created_at DESC')
        return [dict(row) for row in cursor.fetchall()]

    def delete_draft(self, draft_id: int):
        """删除草稿"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM drafts WHERE id = ?', (draft_id,))
        self.conn.commit()
