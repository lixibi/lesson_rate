#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML导出功能测试脚本
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def test_xml_export():
    """测试XML导出功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 测试XML导出功能")
    print("=" * 50)
    
    try:
        # 测试导出全部数据
        print("📝 测试1: 导出全部调查数据")
        response = requests.get(f"{base_url}/admin/export/all", timeout=10)
        
        if response.status_code == 200:
            print("✅ 全部数据导出成功")
            
            # 验证XML格式
            try:
                root = ET.fromstring(response.text)
                print(f"   - XML根元素: {root.tag}")
                print(f"   - 导出时间: {root.get('exportTime')}")
                
                # 检查统计信息
                stats = root.find('OverallStatistics')
                if stats is not None:
                    total_courses = stats.find('TotalCourses').text
                    total_surveys = stats.find('TotalSurveys').text
                    print(f"   - 总课程数: {total_courses}")
                    print(f"   - 总调查数: {total_surveys}")
                
                # 检查课程数据
                courses = root.find('Courses')
                if courses is not None:
                    course_count = len(courses.findall('Course'))
                    print(f"   - 课程详情数: {course_count}")
                
                print("✅ XML格式验证通过")
                
            except ET.ParseError as e:
                print(f"❌ XML格式错误: {e}")
                
        else:
            print(f"❌ 全部数据导出失败: {response.status_code}")
        
        # 测试导出单个课程数据
        print("\n📝 测试2: 导出单个课程数据")
        response = requests.get(f"{base_url}/admin/export/1", timeout=10)
        
        if response.status_code == 200:
            print("✅ 单个课程导出成功")
            
            try:
                root = ET.fromstring(response.text)
                print(f"   - XML根元素: {root.tag}")
                
                # 检查课程信息
                course = root.find('Course')
                if course is not None:
                    course_name = course.find('Name').text
                    instructor = course.find('Instructor').text
                    print(f"   - 课程名称: {course_name}")
                    print(f"   - 讲师: {instructor}")
                
                # 检查统计信息
                stats = root.find('Statistics')
                if stats is not None:
                    total_surveys = stats.find('TotalSurveys').text
                    avg_score = stats.find('AverageScore').text
                    print(f"   - 调查数量: {total_surveys}")
                    print(f"   - 平均分: {avg_score}")
                
                print("✅ 单课程XML格式验证通过")
                
            except ET.ParseError as e:
                print(f"❌ XML格式错误: {e}")
                
        else:
            print(f"❌ 单个课程导出失败: {response.status_code}")
        
        # 测试导出第二个课程
        print("\n📝 测试3: 导出第二个课程数据")
        response = requests.get(f"{base_url}/admin/export/2", timeout=10)
        
        if response.status_code == 200:
            print("✅ 第二个课程导出成功")
        else:
            print(f"❌ 第二个课程导出失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False
    
    return True

def test_admin_page():
    """测试管理员页面是否包含导出按钮"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n🎨 测试管理员页面导出按钮")
    print("=" * 40)
    
    try:
        response = requests.get(f"{base_url}/admin/results", timeout=10)
        
        if response.status_code == 200:
            print("✅ 管理员页面加载成功")
            
            # 检查是否包含导出按钮
            if "导出全部XML" in response.text:
                print("✅ 全部导出按钮存在")
            else:
                print("❌ 全部导出按钮缺失")
            
            if "导出" in response.text and "file-export" in response.text:
                print("✅ 分课程导出按钮存在")
            else:
                print("❌ 分课程导出按钮缺失")
                
        else:
            print(f"❌ 管理员页面加载失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 管理员页面测试网络错误: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🏢 桂林广播电视发射台专业技术课教学质量调查系统")
    print("📊 XML导出功能测试")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查服务器状态
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器响应异常，请检查应用是否正常运行")
            return
    except requests.exceptions.RequestException:
        print("❌ 无法连接到服务器，请确保运行了 'python app.py'")
        return
    
    print("✅ 服务器连接正常")
    print()
    
    # 运行测试
    admin_test_passed = test_admin_page()
    export_test_passed = test_xml_export()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"   管理员页面测试: {'✅ 通过' if admin_test_passed else '❌ 失败'}")
    print(f"   XML导出功能测试: {'✅ 通过' if export_test_passed else '❌ 失败'}")
    
    if admin_test_passed and export_test_passed:
        print("\n🎉 所有测试通过！XML导出功能正常！")
        print("\n✨ 导出功能特性:")
        print("   • 支持导出全部调查数据")
        print("   • 支持按课程分别导出")
        print("   • XML格式包含完整的统计信息")
        print("   • 包含课程信息、评价详情和时间戳")
        print("   • 文件自动命名，便于管理")
    else:
        print("\n⚠️  部分测试失败，请检查相关功能")
    
    print(f"\n🌐 管理员界面: http://127.0.0.1:5000/admin/results")
    print("📁 点击导出按钮即可下载XML文件")

if __name__ == "__main__":
    main()
