# 使用Python作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt /app/

# 安装Python依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . /app/

# 创建数据库目录
RUN mkdir -p /app/instance

# 暴露端口
EXPOSE 5000

# 设置启动命令
CMD ["python", "app.py"]
