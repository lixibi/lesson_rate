from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联到调查表
    surveys = db.relationship('Survey', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # 问卷问题字段
    content_preparation = db.Column(db.String(20), nullable=False)  # 授课内容是否精心准备
    practical_relevance = db.Column(db.String(20), nullable=False)  # 授课内容与实际工作结合
    overall_score = db.Column(db.Integer, nullable=False)  # 综合教学效果评价分数
    suggestions = db.Column(db.Text)  # 改进建议
    
    # 提交信息
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # 记录IP地址
    
    def __repr__(self):
        return f'<Survey {self.id} for Course {self.course_id}>'
