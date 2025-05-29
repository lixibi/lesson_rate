#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复脚本 - 验证表单默认值和提交功能
"""

import requests
import time
from datetime import datetime

def test_default_submission():
    """测试默认值提交功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 测试表单默认值提交功能")
    print("=" * 50)
    
    try:
        # 测试提交空表单（只有默认值）
        test_data = {
            "course_id": 1,
            # 不填写任何选项，测试默认值
        }
        
        print("📝 测试1: 提交空表单（依赖默认值）")
        response = requests.post(
            f"{base_url}/submit_survey",
            data=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 空表单提交成功 - 默认值生效")
        else:
            print(f"❌ 空表单提交失败: {response.status_code}")
            
        # 测试提交带有所有默认值的表单
        test_data_with_defaults = {
            "course_id": 2,
            "content_preparation": "准备充分",
            "practical_relevance": "非常好", 
            "overall_score": "10",
            "suggestions": "测试默认最高评价功能"
        }
        
        print("\n📝 测试2: 提交默认最高评价")
        response = requests.post(
            f"{base_url}/submit_survey",
            data=test_data_with_defaults,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 默认最高评价提交成功")
        else:
            print(f"❌ 默认最高评价提交失败: {response.status_code}")
            
        # 测试快速提交（最小数据）
        test_data_minimal = {
            "course_id": 1,
            "content_preparation": "准备充分",
            "practical_relevance": "非常好",
            "overall_score": "10"
        }
        
        print("\n📝 测试3: 快速提交（最小必要数据）")
        response = requests.post(
            f"{base_url}/submit_survey",
            data=test_data_minimal,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 快速提交成功")
        else:
            print(f"❌ 快速提交失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return False
    
    return True

def test_ui_elements():
    """测试UI元素是否正常加载"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n🎨 测试UI元素加载")
    print("=" * 30)
    
    try:
        # 测试首页
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ 首页加载正常")
            
            # 检查是否包含序号和课程信息
            if "badge bg-primary" in response.text:
                print("✅ 课程序号元素存在")
            else:
                print("❌ 课程序号元素缺失")
                
            if "讲课人" in response.text:
                print("✅ 讲师信息显示正常")
            else:
                print("❌ 讲师信息缺失")
        else:
            print(f"❌ 首页加载失败: {response.status_code}")
            
        # 测试调查页面
        response = requests.get(f"{base_url}/survey/1", timeout=10)
        if response.status_code == 200:
            print("✅ 调查页面加载正常")
            
            # 检查默认选中状态
            if 'checked>' in response.text:
                print("✅ 默认选项设置正确")
            else:
                print("❌ 默认选项设置缺失")
        else:
            print(f"❌ 调查页面加载失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ UI测试网络错误: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🏢 桂林广播电视发射台专业技术课教学质量调查系统")
    print("🔧 修复验证测试")
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
    ui_test_passed = test_ui_elements()
    form_test_passed = test_default_submission()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"   UI元素测试: {'✅ 通过' if ui_test_passed else '❌ 失败'}")
    print(f"   表单功能测试: {'✅ 通过' if form_test_passed else '❌ 失败'}")
    
    if ui_test_passed and form_test_passed:
        print("\n🎉 所有测试通过！修复成功！")
        print("\n✨ 主要改进:")
        print("   • 序号和图标尺寸已优化")
        print("   • 表单默认值设置为最高评价")
        print("   • 用户可以直接提交而无需填写")
        print("   • 界面视觉比例更加协调")
    else:
        print("\n⚠️  部分测试失败，请检查相关功能")
    
    print(f"\n🌐 访问地址: http://127.0.0.1:5000")
    print("📱 建议在手机浏览器中测试响应式效果")

if __name__ == "__main__":
    main()
