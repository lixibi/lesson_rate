# 部署指南

## Docker 部署

### 1. 构建镜像
```bash
docker build -t survey-app .
```

### 2. 运行容器
```bash
docker run -d -p 5000:5000 --name survey-container survey-app
```

### 3. 使用 Docker Compose（推荐）
```bash
docker-compose up -d
```

### 4. 查看日志
```bash
docker logs survey-container
```

### 5. 停止容器
```bash
docker stop survey-container
# 或使用 docker-compose
docker-compose down
```

## Vercel 部署

### 1. 准备 GitHub 仓库
```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Survey app with XML export"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/yourusername/survey-app.git

# 推送到 GitHub
git push -u origin main
```

### 2. 连接 Vercel
1. 访问 [vercel.com](https://vercel.com)
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 选择您的 survey-app 仓库
5. 点击 "Deploy"

### 3. 环境变量配置（可选）
在 Vercel 项目设置中添加环境变量：
- `SECRET_KEY`: 您的密钥
- `FLASK_ENV`: production

### 4. 自动部署
每次推送到 main 分支时，Vercel 会自动重新部署。

## 本地开发

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python app.py
```

### 3. 访问应用
- 用户界面: http://localhost:5000
- 管理员界面: http://localhost:5000/admin/results

## 功能测试

### XML 导出功能
1. 访问管理员页面: `/admin/results`
2. 点击 "导出全部XML" 下载所有数据
3. 点击单个课程的导出按钮下载特定课程数据

### 导出文件格式
- 文件名: `survey_results_课程名_时间戳.xml`
- 包含: 课程信息、统计数据、详细评价记录

## 注意事项

### Docker 部署
- 数据持久化：使用 volume 保存数据库文件
- 端口映射：确保 5000 端口未被占用
- 环境变量：生产环境请修改 SECRET_KEY

### Vercel 部署
- 数据库：Vercel 是无服务器环境，SQLite 数据不会持久化
- 建议：生产环境使用外部数据库（如 PostgreSQL）
- 限制：文件上传和长时间运行的任务可能受限

### 安全建议
1. 修改默认的 SECRET_KEY
2. 添加管理员认证
3. 配置 HTTPS
4. 定期备份数据库

## 故障排除

### Docker 常见问题
```bash
# 查看容器状态
docker ps -a

# 查看容器日志
docker logs survey-container

# 进入容器调试
docker exec -it survey-container /bin/bash
```

### Vercel 常见问题
1. 构建失败：检查 requirements.txt 和 Python 版本
2. 路由错误：确认 vercel.json 配置正确
3. 数据库问题：考虑使用外部数据库服务

## 扩展建议

### 生产环境优化
1. 使用 PostgreSQL 或 MySQL 数据库
2. 添加 Redis 缓存
3. 配置负载均衡
4. 添加监控和日志系统

### 功能扩展
1. 用户认证系统
2. 多语言支持
3. 数据可视化图表
4. 邮件通知功能
