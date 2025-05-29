from app import app, init_db

# 确保数据库初始化
try:
    init_db()
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")

# Vercel需要这个变量
application = app

# For Vercel serverless functions
def handler(request):
    return app(request.environ, request.start_response)

if __name__ == "__main__":
    app.run()
