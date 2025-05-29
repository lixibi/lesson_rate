from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from models import db, Course, Survey
from config import Config
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库
db.init_app(app)

def init_db():
    """初始化数据库并添加测试数据"""
    with app.app_context():
        db.create_all()

        # 检查是否已有数据
        if Course.query.count() == 0:
            # 添加课程数据
            course1 = Course(
                name="调频广播发射机原理解析",
                instructor="郭龙",
                description="深入讲解调频广播发射机的工作原理、技术特点和应用场景"
            )

            course2 = Course(
                name="调频广播发射机的常见故障分析和处理",
                instructor="薛松",
                description="分析调频广播发射机常见故障类型，提供实用的故障诊断和处理方法"
            )

            db.session.add(course1)
            db.session.add(course2)

            # 添加一些测试调查数据
            test_survey1 = Survey(
                course_id=1,
                content_preparation="准备充分",
                practical_relevance="非常好",
                overall_score=10,
                suggestions="课程内容很实用，希望能增加更多实际案例",
                ip_address="127.0.0.1"
            )

            test_survey2 = Survey(
                course_id=2,
                content_preparation="比较充分",
                practical_relevance="比较好",
                overall_score=9,
                suggestions="故障分析很详细，建议增加视频演示",
                ip_address="127.0.0.1"
            )

            db.session.add(test_survey1)
            db.session.add(test_survey2)
            db.session.commit()

@app.route('/')
def index():
    """首页 - 显示课程列表"""
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/survey/<int:course_id>')
def survey(course_id):
    """调查问卷页面"""
    course = Course.query.get_or_404(course_id)
    return render_template('survey.html', course=course)

@app.route('/submit_survey', methods=['POST'])
def submit_survey():
    """提交调查问卷"""
    try:
        course_id = request.form.get('course_id')
        content_preparation = request.form.get('content_preparation')
        practical_relevance = request.form.get('practical_relevance')
        overall_score = request.form.get('overall_score')
        suggestions = request.form.get('suggestions', '')

        # 验证必填字段
        if not all([course_id, content_preparation, practical_relevance, overall_score]):
            flash('请完成所有必填项', 'error')
            return redirect(url_for('survey', course_id=course_id))

        # 创建调查记录
        survey = Survey(
            course_id=int(course_id),
            content_preparation=content_preparation,
            practical_relevance=practical_relevance,
            overall_score=int(overall_score),
            suggestions=suggestions,
            ip_address=request.remote_addr
        )

        db.session.add(survey)
        db.session.commit()

        return render_template('thank_you.html')

    except Exception as e:
        flash('提交失败，请重试', 'error')
        return redirect(url_for('survey', course_id=request.form.get('course_id', 1)))

@app.route('/admin/results')
def admin_results():
    """管理员查看调查结果"""
    surveys = Survey.query.join(Course).all()
    return render_template('admin_results.html', surveys=surveys)

@app.route('/admin/export/<int:course_id>')
def export_course_results(course_id):
    """导出指定课程的调查结果为XML"""
    course = Course.query.get_or_404(course_id)
    surveys = Survey.query.filter_by(course_id=course_id).all()

    # 创建XML根元素
    root = ET.Element("SurveyResults")
    root.set("exportTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 课程信息
    course_elem = ET.SubElement(root, "Course")
    ET.SubElement(course_elem, "ID").text = str(course.id)
    ET.SubElement(course_elem, "Name").text = course.name
    ET.SubElement(course_elem, "Instructor").text = course.instructor
    ET.SubElement(course_elem, "Description").text = course.description or ""
    ET.SubElement(course_elem, "CreatedAt").text = course.created_at.strftime("%Y-%m-%d %H:%M:%S")

    # 统计信息
    stats_elem = ET.SubElement(root, "Statistics")
    ET.SubElement(stats_elem, "TotalSurveys").text = str(len(surveys))
    if surveys:
        avg_score = sum(s.overall_score for s in surveys) / len(surveys)
        ET.SubElement(stats_elem, "AverageScore").text = f"{avg_score:.2f}"
        high_scores = len([s for s in surveys if s.overall_score >= 9])
        ET.SubElement(stats_elem, "HighScoreCount").text = str(high_scores)
        with_suggestions = len([s for s in surveys if s.suggestions])
        ET.SubElement(stats_elem, "SuggestionsCount").text = str(with_suggestions)
    else:
        ET.SubElement(stats_elem, "AverageScore").text = "0"
        ET.SubElement(stats_elem, "HighScoreCount").text = "0"
        ET.SubElement(stats_elem, "SuggestionsCount").text = "0"

    # 调查详情
    surveys_elem = ET.SubElement(root, "Surveys")
    for survey in surveys:
        survey_elem = ET.SubElement(surveys_elem, "Survey")
        survey_elem.set("id", str(survey.id))

        ET.SubElement(survey_elem, "ContentPreparation").text = survey.content_preparation
        ET.SubElement(survey_elem, "PracticalRelevance").text = survey.practical_relevance
        ET.SubElement(survey_elem, "OverallScore").text = str(survey.overall_score)
        ET.SubElement(survey_elem, "Suggestions").text = survey.suggestions or ""
        ET.SubElement(survey_elem, "SubmittedAt").text = survey.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
        ET.SubElement(survey_elem, "IPAddress").text = survey.ip_address or ""

    # 生成XML字符串
    xml_str = ET.tostring(root, encoding='unicode', method='xml')

    # 格式化XML（添加缩进）
    try:
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_str)
        formatted_xml = dom.toprettyxml(indent="  ", encoding=None)
        # 移除空行
        formatted_xml = '\n'.join([line for line in formatted_xml.split('\n') if line.strip()])
    except:
        formatted_xml = xml_str

    # 生成文件名
    filename = f"survey_results_{course.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
    filename = filename.replace(' ', '_').replace('/', '_')

    return Response(
        formatted_xml,
        mimetype='application/xml',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

@app.route('/admin/export/all')
def export_all_results():
    """导出所有课程的调查结果为XML"""
    courses = Course.query.all()

    # 创建XML根元素
    root = ET.Element("AllSurveyResults")
    root.set("exportTime", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # 总体统计
    all_surveys = Survey.query.all()
    overall_stats = ET.SubElement(root, "OverallStatistics")
    ET.SubElement(overall_stats, "TotalCourses").text = str(len(courses))
    ET.SubElement(overall_stats, "TotalSurveys").text = str(len(all_surveys))
    if all_surveys:
        avg_score = sum(s.overall_score for s in all_surveys) / len(all_surveys)
        ET.SubElement(overall_stats, "OverallAverageScore").text = f"{avg_score:.2f}"

    # 各课程详情
    courses_elem = ET.SubElement(root, "Courses")
    for course in courses:
        course_surveys = Survey.query.filter_by(course_id=course.id).all()

        course_elem = ET.SubElement(courses_elem, "Course")
        course_elem.set("id", str(course.id))

        # 课程基本信息
        info_elem = ET.SubElement(course_elem, "Information")
        ET.SubElement(info_elem, "Name").text = course.name
        ET.SubElement(info_elem, "Instructor").text = course.instructor
        ET.SubElement(info_elem, "Description").text = course.description or ""

        # 课程统计
        stats_elem = ET.SubElement(course_elem, "Statistics")
        ET.SubElement(stats_elem, "SurveyCount").text = str(len(course_surveys))
        if course_surveys:
            avg_score = sum(s.overall_score for s in course_surveys) / len(course_surveys)
            ET.SubElement(stats_elem, "AverageScore").text = f"{avg_score:.2f}"
        else:
            ET.SubElement(stats_elem, "AverageScore").text = "0"

        # 课程调查详情
        surveys_elem = ET.SubElement(course_elem, "Surveys")
        for survey in course_surveys:
            survey_elem = ET.SubElement(surveys_elem, "Survey")
            survey_elem.set("id", str(survey.id))

            ET.SubElement(survey_elem, "ContentPreparation").text = survey.content_preparation
            ET.SubElement(survey_elem, "PracticalRelevance").text = survey.practical_relevance
            ET.SubElement(survey_elem, "OverallScore").text = str(survey.overall_score)
            ET.SubElement(survey_elem, "Suggestions").text = survey.suggestions or ""
            ET.SubElement(survey_elem, "SubmittedAt").text = survey.submitted_at.strftime("%Y-%m-%d %H:%M:%S")

    # 生成格式化XML
    xml_str = ET.tostring(root, encoding='unicode', method='xml')
    try:
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_str)
        formatted_xml = dom.toprettyxml(indent="  ", encoding=None)
        formatted_xml = '\n'.join([line for line in formatted_xml.split('\n') if line.strip()])
    except:
        formatted_xml = xml_str

    filename = f"all_survey_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

    return Response(
        formatted_xml,
        mimetype='application/xml',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
