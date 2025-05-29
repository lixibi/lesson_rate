#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示脚本 - 桂林广播电视发射台专业技术课教学质量调查系统
"""

import requests
import json
from datetime import datetime

def demo_survey_submission():
    """演示调查问卷提交功能"""
    base_url = "http://127.0.0.1:5000"
    
    # 模拟调查数据
    demo_surveys = [
        {
            "course_id": 1,
            "content_preparation": "准备充分",
            "practical_relevance": "非常好",
            "overall_score": 10,
            "suggestions": "课程内容非常实用，理论与实践结合得很好。希望能增加更多实际案例分析。"
        },
        {
            "course_id": 1,
            "content_preparation": "比较充分",
            "practical_relevance": "比较好",
            "overall_score": 9,
            "suggestions": "讲解清晰，但希望能有更多互动环节。"
        },
        {
            "course_id": 2,
            "content_preparation": "准备充分",
            "practical_relevance": "非常好",
            "overall_score": 10,
            "suggestions": "故障分析很详细，对实际工作帮助很大。建议增加视频演示。"
        },
        {
            "course_id": 2,
            "content_preparation": "准备充分",
            "practical_relevance": "比较好",
            "overall_score": 8,
            "suggestions": "内容丰富，但时间有点紧张，建议延长课程时间。"
        }
    ]
    
    print("🚀 开始演示调查问卷提交...")
    print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    for i, survey_data in enumerate(demo_surveys, 1):
        try:
            # 提交调查数据
            response = requests.post(
                f"{base_url}/submit_survey",
                data=survey_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ 演示调查 {i} 提交成功")
                print(f"   课程ID: {survey_data['course_id']}")
                print(f"   评分: {survey_data['overall_score']}分")
                print(f"   建议: {survey_data['suggestions'][:30]}...")
            else:
                print(f"❌ 演示调查 {i} 提交失败: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误: {e}")
        
        print("-" * 30)
    
    print("\n📊 查看结果:")
    print(f"   用户界面: {base_url}")
    print(f"   管理员界面: {base_url}/admin/results")
    print("\n🎉 演示完成!")

def check_server_status():
    """检查服务器状态"""
    try:
        response = requests.get("http://127.0.0.1:5000", timeout=5)
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print(f"❌ 服务器响应异常: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务器: {e}")
        print("💡 请确保运行了 'python app.py' 启动服务器")
        return False

if __name__ == "__main__":
    print("🏢 桂林广播电视发射台专业技术课教学质量调查系统")
    print("📋 演示脚本")
    print("=" * 60)
    
    # 检查服务器状态
    if check_server_status():
        # 运行演示
        demo_survey_submission()
    else:
        print("\n🔧 启动说明:")
        print("1. 打开终端")
        print("2. 运行: python app.py")
        print("3. 等待服务器启动")
        print("4. 重新运行此演示脚本")
