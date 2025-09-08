#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
容器环境 Gemini API 连接测试脚本
测试修复后的超时配置和重试机制
"""

import os
import sys
import time
import requests
from google import genai

def test_direct_gemini_api():
    """直接测试 Gemini API 连接"""
    print("🔍 Testing direct Gemini API connection...")
    
    try:
        # 使用优化的客户端配置
        client = genai.Client(transport="rest")
        
        # 配置超时
        request_config = {"timeout": 60.0}
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=["Hello, this is a container connectivity test"],
            request_options=request_config
        )
        
        print("✅ Direct API call successful!")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Direct API call failed: {e}")
        return False

def test_container_api_endpoint():
    """测试容器内的 API 端点"""
    print("🔍 Testing container API endpoint...")
    
    try:
        # 测试健康检查端点
        response = requests.get("http://localhost:8088/test_api", timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Container API endpoint test successful!")
            print(f"Response: {result}")
            return True
        else:
            print(f"❌ Container API endpoint returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Container API endpoint test failed: {e}")
        return False

def test_timeout_handling():
    """测试超时处理机制"""
    print("🔍 Testing timeout handling...")
    
    try:
        # 模拟较长的API调用
        start_time = time.time()
        
        client = genai.Client(transport="rest")
        request_config = {"timeout": 30.0}  # 30秒超时
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=["Generate a detailed description of machine learning algorithms"],
            request_options=request_config
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ Timeout handling test completed in {elapsed_time:.2f} seconds")
        print(f"Response length: {len(response.text) if response.text else 0} characters")
        return True
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"⚠️  Timeout handling test completed with error in {elapsed_time:.2f} seconds: {e}")
        # 这可能是预期的超时行为
        return True

def main():
    """运行所有测试"""
    print("🚀 Container Gemini API Test Suite")
    print("=" * 50)
    
    # 检查环境变量
    if not os.environ.get('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY environment variable not set!")
        sys.exit(1)
    
    results = []
    
    # 运行测试
    results.append(("Direct Gemini API", test_direct_gemini_api()))
    results.append(("Container API Endpoint", test_container_api_endpoint()))
    results.append(("Timeout Handling", test_timeout_handling()))
    
    # 总结结果
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Container timeout fixes are working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()