# -*- coding: utf-8 -*-
"""
Img Gen Backend Services
"""
import os
import sys
import logging
import subprocess
import threading
import time
from typing import List, Optional

logger = logging.getLogger(__name__)

__version__ = "1.0.0"

class BackendServiceManager:
    """Manages starting and stopping backend services"""

    def __init__(self):
        self.processes = []
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def _run_service(self, module_name, gunicorn_config, service_name, use_production=None):
        """Start a single service"""
        # Auto-detect production mode
        if use_production is None:
            use_production = os.environ.get('FLASK_ENV') == 'production'

        try:
            logger.info("Starting %s...", service_name)

            if use_production:
                # Use gunicorn for production
                cmd = [sys.executable, '-m', 'gunicorn', '-c', gunicorn_config, f'{module_name}:app']
            else:
                # Use development server via module
                cmd = [sys.executable, '-m', module_name]

            process = subprocess.Popen(cmd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True, bufsize=1, cwd=self.script_dir)

            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_service,
                args=(process, service_name),
                daemon=True
            )
            monitor_thread.start()

            self.processes.append(process)
            logger.info("%s started (PID: %d)", service_name, process.pid)
            return process

        except Exception as e:
            logger.error("Failed to start %s: %s", service_name, e)
            return None

    def _monitor_service(self, process, service_name):
        """Monitor service output"""
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logger.info("[%s] %s", service_name, output.strip())

    def start_file_service(self):
        """Start file storage service (port 10086)"""
        return self._run_service(
            'tools.file_storage.routes',
            'gunicorn_config_file.py',
            'File Storage Service'
        )

    def start_gemini_service(self):
        """Start Gemini AI generation service (port 8088)"""
        return self._run_service(
            'tools.img_gen.routes',
            'gunicorn_config.py',
            'Gemini AI Service'
        )

    def start_all_services(self):
        """Start all backend services"""
        logger.info("Img Gen Backend Services Starting...")

        # Start file storage service
        file_service = self.start_file_service()
        time.sleep(1)

        # Start AI generation service
        gemini_service = self.start_gemini_service()
        time.sleep(1)

        if file_service and gemini_service:
            logger.info("All services started successfully!")
            logger.info("File Storage API: http://localhost:10086")
            logger.info("Gemini AI API:    http://localhost:8088")

            # Keep services running
            try:
                while True:
                    time.sleep(1)
                    for i, process in enumerate(self.processes):
                        if process.poll() is not None:
                            logger.warning("Service %d has stopped unexpectedly", i + 1)

            except KeyboardInterrupt:
                self.stop_all_services()
        else:
            logger.error("Failed to start some services")
            self.stop_all_services()

    def stop_all_services(self):
        """Stop all services"""
        logger.info("Stopping all services...")

        for i, process in enumerate(self.processes):
            try:
                if process.poll() is None:
                    logger.info("Stopping service %d (PID: %d)", i + 1, process.pid)
                    process.terminate()

                    try:
                        process.wait(timeout=5)
                        logger.info("Service %d stopped gracefully", i + 1)
                    except subprocess.TimeoutExpired:
                        logger.warning("Force killing service %d", i + 1)
                        process.kill()
                        process.wait()

            except Exception as e:
                logger.error("Error stopping service %d: %s", i + 1, e)

        self.processes.clear()
        logger.info("All services stopped")

# Global service manager instance
_service_manager = None

def get_service_manager():
    """Get service manager instance"""
    global _service_manager
    if _service_manager is None:
        _service_manager = BackendServiceManager()
    return _service_manager

def start_backend():
    """Start all backend services"""
    manager = get_service_manager()
    manager.start_all_services()

def start_file_service():
    """Start file storage service only"""
    manager = get_service_manager()
    return manager.start_file_service()

def start_gemini_service():
    """Start AI generation service only"""
    manager = get_service_manager()
    return manager.start_gemini_service()

def stop_backend():
    """Stop all backend services"""
    manager = get_service_manager()
    manager.stop_all_services()

# CLI support
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

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
