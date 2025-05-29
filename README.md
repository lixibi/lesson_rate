# 桂林广播电视发射台专业技术课教学质量调查系统

一个基于Flask和SQLite的现代化调查问卷应用，专为桂林广播电视发射台的专业技术课程教学质量评价而设计。

## 功能特性

### 🎯 核心功能
- **课程选择** - 用户可以选择不同的专业技术课程进行评价
- **问卷调查** - 包含4个核心问题的教学质量评价表单
- **数据存储** - 使用SQLite数据库安全存储所有调查数据
- **结果统计** - 管理员可以查看详细的调查结果和统计信息
- **XML导出** - 支持分课程导出和全部导出，包含完整的评价数据

### 📱 用户体验
- **响应式设计** - 完美适配手机、平板和桌面设备
- **现代化UI** - 采用Bootstrap 5和自定义CSS，界面美观大气
- **交互动画** - 流畅的页面切换和表单交互效果
- **表单验证** - 客户端和服务端双重验证确保数据完整性

### 🎨 设计特色
- **渐变背景** - 专业的蓝紫色渐变背景
- **卡片式布局** - 清晰的信息层次和视觉分组
- **图标系统** - 丰富的FontAwesome图标增强用户体验
- **色彩系统** - 统一的品牌色彩和状态指示

## 技术栈

- **后端**: Flask 2.3.3
- **数据库**: SQLite + Flask-SQLAlchemy 3.0.5
- **前端**: HTML5 + CSS3 + JavaScript
- **UI框架**: Bootstrap 5.1.3
- **图标**: FontAwesome 6.0.0

## 项目结构

```
调查/
├── app.py                 # Flask主应用
├── models.py             # 数据库模型
├── config.py             # 配置文件
├── requirements.txt      # 依赖包列表
├── README.md            # 项目说明
├── static/              # 静态资源
│   ├── css/
│   │   └── style.css    # 自定义样式
│   └── js/
│       └── main.js      # JavaScript功能
├── templates/           # HTML模板
│   ├── base.html        # 基础模板
│   ├── index.html       # 课程选择页面
│   ├── survey.html      # 调查问卷页面
│   ├── thank_you.html   # 提交成功页面
│   └── admin_results.html # 管理员结果页面
└── instance/
    └── survey.db        # SQLite数据库文件
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python app.py
```

### 3. 访问应用
- 用户界面: http://127.0.0.1:5000
- 管理员界面: http://127.0.0.1:5000/admin/results
- XML导出: 在管理员页面点击导出按钮

## 部署方式

### 🐳 Docker 部署
```bash
# 构建镜像
docker build -t survey-app .

# 运行容器
docker run -d -p 5000:5000 survey-app

# 或使用 docker-compose
docker-compose up -d
```

### ☁️ Vercel 部署
1. 推送代码到 GitHub
2. 连接 Vercel 账号
3. 导入项目并部署

详细部署说明请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 课程信息

### 课程1: 调频广播发射机原理解析
- **讲师**: 郭龙
- **内容**: 深入讲解调频广播发射机的工作原理、技术特点和应用场景

### 课程2: 调频广播发射机的常见故障分析和处理
- **讲师**: 薛松
- **内容**: 分析调频广播发射机常见故障类型，提供实用的故障诊断和处理方法

## 调查问卷内容

1. **授课内容准备情况** (单选)
   - 准备充分
   - 比较充分
   - 一般

2. **内容与实际工作结合度** (单选)
   - 非常好
   - 比较好
   - 一般

3. **综合教学效果评分** (单选)
   - 10分 (★★★★★)
   - 9分 (★★★★☆)
   - 8分 (★★★★☆)
   - 7分 (★★★☆☆)

4. **改进建议** (文本)
   - 开放式文本输入

## 数据库设计

### Course表 (课程信息)
- id: 主键
- name: 课程名称
- instructor: 讲师姓名
- description: 课程描述
- created_at: 创建时间

### Survey表 (调查记录)
- id: 主键
- course_id: 课程ID (外键)
- content_preparation: 内容准备评价
- practical_relevance: 实际结合评价
- overall_score: 综合评分
- suggestions: 改进建议
- submitted_at: 提交时间
- ip_address: 提交者IP

## 特色功能

### 🎨 美观的界面设计
- 现代化的卡片式布局
- 渐变色背景和阴影效果
- 响应式设计适配各种设备
- 流畅的动画过渡效果

### 📊 智能数据统计
- 实时统计总评价数
- 自动计算平均分
- 高分评价数量统计
- 建议数量统计

### 🔒 数据安全保障
- 表单验证防止无效数据
- IP地址记录便于追踪
- SQLite数据库安全存储

### 📱 移动端优化
- 触摸友好的交互设计
- 移动端专用样式优化
- 自适应字体和间距

## 开发说明

### 添加新课程
在 `app.py` 的 `init_db()` 函数中添加新的Course对象。

### 修改问卷问题
在 `templates/survey.html` 中修改问题内容，同时需要更新 `models.py` 中的Survey模型。

### 自定义样式
在 `static/css/style.css` 中修改CSS变量和样式规则。

## 部署建议

### 生产环境部署
1. 使用Gunicorn或uWSGI作为WSGI服务器
2. 配置Nginx作为反向代理
3. 使用PostgreSQL或MySQL替代SQLite
4. 启用HTTPS加密传输

### 安全配置
1. 修改 `config.py` 中的SECRET_KEY
2. 配置数据库访问权限
3. 启用防火墙和访问控制

## 许可证

本项目仅供桂林广播电视发射台内部使用。

## 联系方式

如有问题或建议，请联系技术支持团队。
