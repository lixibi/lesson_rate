#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库查看工具 - 桂林广播电视发射台专业技术课教学质量调查系统
"""

import sqlite3
import os
from datetime import datetime

def view_database():
    """查看数据库内容"""
    db_path = "instance/survey.db"
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在，请先运行应用创建数据库")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🏢 桂林广播电视发射台专业技术课教学质量调查系统")
        print("📊 数据库内容查看")
        print("=" * 60)
        
        # 查看课程信息
        print("\n📚 课程信息:")
        print("-" * 40)
        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()
        
        if courses:
            print(f"{'ID':<3} {'课程名称':<25} {'讲师':<10} {'创建时间':<20}")
            print("-" * 60)
            for course in courses:
                print(f"{course[0]:<3} {course[1]:<25} {course[2]:<10} {course[4]:<20}")
        else:
            print("暂无课程数据")
        
        # 查看调查统计
        print("\n📋 调查统计:")
        print("-" * 40)
        cursor.execute("SELECT COUNT(*) FROM survey")
        total_surveys = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(overall_score) FROM survey")
        avg_score = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM survey WHERE overall_score >= 9")
        high_scores = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM survey WHERE suggestions != ''")
        with_suggestions = cursor.fetchone()[0]
        
        print(f"总评价数: {total_surveys}")
        print(f"平均分: {avg_score:.1f}" if avg_score else "平均分: 暂无数据")
        print(f"高分评价(≥9分): {high_scores}")
        print(f"有建议的评价: {with_suggestions}")
        
        # 查看详细调查记录
        print("\n📝 详细调查记录:")
        print("-" * 80)
        cursor.execute("""
            SELECT s.id, c.name, c.instructor, s.content_preparation, 
                   s.practical_relevance, s.overall_score, s.submitted_at, s.suggestions
            FROM survey s
            JOIN course c ON s.course_id = c.id
            ORDER BY s.submitted_at DESC
        """)
        surveys = cursor.fetchall()
        
        if surveys:
            print(f"{'ID':<3} {'课程':<20} {'讲师':<6} {'内容准备':<8} {'实际结合':<8} {'评分':<4} {'提交时间':<16} {'建议':<20}")
            print("-" * 90)
            for survey in surveys:
                suggestions = survey[7][:15] + "..." if survey[7] and len(survey[7]) > 15 else survey[7] or "无"
                print(f"{survey[0]:<3} {survey[1][:18]:<20} {survey[2]:<6} {survey[3]:<8} {survey[4]:<8} {survey[5]:<4} {survey[6][:16]:<16} {suggestions:<20}")
        else:
            print("暂无调查记录")
        
        # 按课程分组统计
        print("\n📈 按课程分组统计:")
        print("-" * 50)
        cursor.execute("""
            SELECT c.name, c.instructor, COUNT(s.id) as survey_count, 
                   AVG(s.overall_score) as avg_score
            FROM course c
            LEFT JOIN survey s ON c.id = s.course_id
            GROUP BY c.id, c.name, c.instructor
        """)
        course_stats = cursor.fetchall()
        
        for stat in course_stats:
            print(f"课程: {stat[0]}")
            print(f"讲师: {stat[1]}")
            print(f"评价数: {stat[2]}")
            print(f"平均分: {stat[3]:.1f}" if stat[3] else "平均分: 暂无评价")
            print("-" * 30)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ 数据库错误: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

def export_data():
    """导出数据为CSV格式"""
    db_path = "instance/survey.db"
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 导出调查数据
        cursor.execute("""
            SELECT s.id, c.name, c.instructor, s.content_preparation, 
                   s.practical_relevance, s.overall_score, s.submitted_at, s.suggestions
            FROM survey s
            JOIN course c ON s.course_id = c.id
            ORDER BY s.submitted_at DESC
        """)
        surveys = cursor.fetchall()
        
        if surveys:
            filename = f"survey_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w', encoding='utf-8-sig') as f:
                # 写入表头
                f.write("ID,课程名称,讲师,内容准备,实际结合,综合评分,提交时间,改进建议\n")
                
                # 写入数据
                for survey in surveys:
                    # 处理建议中的换行符和逗号
                    suggestions = survey[7].replace('\n', ' ').replace(',', '，') if survey[7] else ''
                    f.write(f"{survey[0]},{survey[1]},{survey[2]},{survey[3]},{survey[4]},{survey[5]},{survey[6]},{suggestions}\n")
            
            print(f"✅ 数据已导出到: {filename}")
        else:
            print("❌ 暂无数据可导出")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 导出失败: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export_data()
    else:
        view_database()
        print("\n💡 提示:")
        print("- 运行 'python db_viewer.py export' 可导出数据为CSV文件")
        print("- 访问 http://127.0.0.1:5000/admin/results 查看网页版统计")
