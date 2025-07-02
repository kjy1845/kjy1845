"""
开发环境启动脚本
"""
import sys
import os
import uvicorn

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    print("启动健康管理系统开发服务器...")
    print("API文档地址: http://localhost:8000/docs")
    print("交互式文档: http://localhost:8000/redoc")
    print("按 Ctrl+C 停止服务器")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )