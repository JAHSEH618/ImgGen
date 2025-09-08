# -*- coding: utf-8 -*-
"""
Img Gen Backend Services
"""
import os
import sys
import subprocess
import threading
import time
from typing import List, Optional

__version__ = "1.0.0"

class BackendServiceManager:
    """管理后端服务的启动和关闭"""
    
    def __init__(self):
        self.processes = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
    def _run_service(self, script_name, service_name, use_production=None):
        """启动单个服务"""
        # 自动检测生产模式
        if use_production is None:
            use_production = os.environ.get('FLASK_ENV') == 'production'
            
        script_path = os.path.join(self.script_dir, script_name)
        
        if not os.path.exists(script_path):
            print(f"❌ {service_name} script not found: {script_path}")
            return None
            
        try:
            print(f"🚀 Starting {service_name}...")
            
            if use_production:
                # Use gunicorn for production
                if script_name == 'gemini_api.py':
                    cmd = [sys.executable, '-m', 'gunicorn', '-c', 'gunicorn_config.py', 'gemini_api:app']
                elif script_name == 'file.py':
                    cmd = [sys.executable, '-m', 'gunicorn', '-c', 'gunicorn_config_file.py', 'file:app']
                else:
                    cmd = [sys.executable, script_path]
            else:
                # Use development server
                cmd = [sys.executable, script_path]
            
            process = subprocess.Popen(cmd, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                universal_newlines=True, bufsize=1, cwd=self.script_dir)
            
            # 启动监控线程
            monitor_thread = threading.Thread(
                target=self._monitor_service, 
                args=(process, service_name),
                daemon=True
            )
            monitor_thread.start()
            
            self.processes.append(process)
            print(f"✅ {service_name} started (PID: {process.pid})")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start {service_name}: {e}")
            return None
    
    def _monitor_service(self, process, service_name):
        """监控服务输出"""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"[{service_name}] {output.strip()}")
    
    def start_file_service(self):
        """启动文件存储服务 (端口 10086)"""
        return self._run_service('file.py', 'File Storage Service')
    
    def start_gemini_service(self):
        """启动Gemini AI生成服务 (端口 8088)"""
        return self._run_service('gemini_api.py', 'Gemini AI Service')
    
    def start_all_services(self):
        """启动所有后端服务"""
        print("🤖 Img Gen Backend Services Starting...")
        print("=" * 50)
        
        # 启动文件存储服务
        file_service = self.start_file_service()
        time.sleep(1)  # 等待服务启动
        
        # 启动AI生成服务
        gemini_service = self.start_gemini_service()
        time.sleep(1)
        
        if file_service and gemini_service:
            print("=" * 50)
            print("🎉 All services started successfully!")
            print("")
            print("📡 Available Services:")
            print("  • File Storage API: http://localhost:10086")
            print("  • Gemini AI API:    http://localhost:8088")
            print("")
            print("💡 Usage:")
            print("  1. Upload images to storage (port 10086)")
            print("  2. Generate AI art from stored images (port 8088)")
            print("")
            print("🛑 Press Ctrl+C to stop all services")
            print("=" * 50)
            
            # 保持服务运行
            try:
                while True:
                    time.sleep(1)
                    # 检查进程是否还活着
                    for i, process in enumerate(self.processes):
                        if process.poll() is not None:
                            print(f"⚠️ Service {i+1} has stopped unexpectedly")
                            
            except KeyboardInterrupt:
                self.stop_all_services()
        else:
            print("❌ Failed to start some services")
            self.stop_all_services()
    
    def stop_all_services(self):
        """停止所有服务"""
        print("\n🛑 Stopping all services...")
        
        for i, process in enumerate(self.processes):
            try:
                if process.poll() is None:  # 进程还在运行
                    print(f"🔄 Stopping service {i+1} (PID: {process.pid})")
                    process.terminate()
                    
                    # 等待进程优雅退出
                    try:
                        process.wait(timeout=5)
                        print(f"✅ Service {i+1} stopped gracefully")
                    except subprocess.TimeoutExpired:
                        print(f"⚠️ Force killing service {i+1}")
                        process.kill()
                        process.wait()
                        
            except Exception as e:
                print(f"❌ Error stopping service {i+1}: {e}")
        
        self.processes.clear()
        print("🎯 All services stopped")

# 全局服务管理器实例
_service_manager = None

def get_service_manager():
    """获取服务管理器实例"""
    global _service_manager
    if _service_manager is None:
        _service_manager = BackendServiceManager()
    return _service_manager

def start_backend():
    """启动所有后端服务的便捷函数"""
    manager = get_service_manager()
    manager.start_all_services()

def start_file_service():
    """仅启动文件存储服务"""
    manager = get_service_manager()
    return manager.start_file_service()

def start_gemini_service():
    """仅启动AI生成服务"""
    manager = get_service_manager()
    return manager.start_gemini_service()

def stop_backend():
    """停止所有后端服务"""
    manager = get_service_manager()
    manager.stop_all_services()

# 命令行直接运行支持
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Img Gen Backend Services')
    parser.add_argument('--service', choices=['all', 'file', 'gemini'], 
                       default='all', help='Which service to start')
    parser.add_argument('--version', action='version', version=f'Img Gen Backend {__version__}')
    
    args = parser.parse_args()
    
    if args.service == 'all':
        start_backend()
    elif args.service == 'file':
        manager = get_service_manager()
        service = manager.start_file_service()
        if service:
            try:
                service.wait()
            except KeyboardInterrupt:
                manager.stop_all_services()
    elif args.service == 'gemini':
        manager = get_service_manager()
        service = manager.start_gemini_service()
        if service:
            try:
                service.wait()
            except KeyboardInterrupt:
                manager.stop_all_services()