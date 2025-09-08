#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid图表转PNG转换器
将Mermaid序列图转换为PNG格式，线条和文字为黑色
"""

import os
import subprocess
import tempfile
import json
from pathlib import Path


def create_mermaid_content():
    """创建修改后的Mermaid内容（黑色线条和文字）"""
    mermaid_content = '''%%{init: {'theme':'base', 'themeVariables': { 
    'primaryColor': '#ffffff', 
    'primaryTextColor': '#000000', 
    'primaryBorderColor': '#000000', 
    'lineColor': '#000000', 
    'secondaryColor': '#f0f0f0', 
    'tertiaryColor': '#e0e0e0', 
    'background': '#ffffff', 
    'mainBkg': '#ffffff', 
    'secondBkg': '#f8f8f8', 
    'tertiaryBkg': '#f0f0f0',
    'actorTextColor': '#000000',
    'actorLineColor': '#000000',
    'signalColor': '#000000',
    'signalTextColor': '#000000',
    'labelBoxBkgColor': '#ffffff',
    'labelTextColor': '#000000',
    'loopTextColor': '#000000',
    'noteBorderColor': '#000000',
    'noteTextColor': '#000000',
    'activationBorderColor': '#000000',
    'activationBkgColor': '#f0f0f0',
    'sequenceNumberColor': '#000000'
}}}%%

sequenceDiagram
    participant U as 👤 用户
    participant W as 🔥 热钱包系统
    participant S1 as 🖥️ 服务器节点
    participant S2 as 📱 用户设备
    participant S3 as 🏦 第三方托管节点
    participant BC as ⛓️ 区块链网络

    rect rgb(240, 240, 240, 0.3)
        note over S1, S3: 🔐 阶段1: 密钥初始化 (MPC分布式密钥生成)
        S1->>S2: 启动密钥生成协议 (t/n门限)
        S1->>S3: 分发密钥生成参数
        S2->>S1: 生成密钥分片1 + 承诺
        S3->>S1: 生成密钥分片2 + 承诺
        S1->>S1: 生成密钥分片3 + 验证

        S1->>S2: 交换验证信息
        S2->>S3: 密钥分片验证
        S3->>S1: 确认分片有效性

        note over S1, S3: ✅ 公钥生成完成，私钥分片分布存储
    end

    rect rgb(245, 245, 245, 0.3)
        note over U, BC: 📤 阶段2: 交易发起与签名请求
        U->>W: 发起转账交易请求
        W->>W: 构造交易数据 & 计算哈希

        W->>S1: 分发签名请求 (交易哈希)
        W->>S2: 分发签名请求 (交易哈希)
        W->>S3: 分发签名请求 (交易哈希)

        S1-->>W: 确认参与签名
        S2-->>W: 确认参与签名
        S3-->>W: 确认参与签名

        note over W: ✅ 满足门限要求 (≥t个节点同意)
    end

    rect rgb(248, 248, 248, 0.3)
        note over S1, S3: 🔄 阶段3: MPC协作计算 (多轮交互)

        loop 阈值签名协议计算
            S1->>S2: 交换加密中间值 (随机数承诺)
            S2->>S3: 传递计算参数
            S3->>S1: 返回部分签名数据

            S1->>S1: 本地私钥分片计算
            S2->>S2: 本地私钥分片计算  
            S3->>S3: 本地私钥分片计算
        end

        note over S1, S3: 🔒 全程无私钥分片明文暴露
    end

    rect rgb(250, 250, 250, 0.3)
        note over S1, W: ⚡ 阶段4: 签名合成与验证
        S1->>W: 提交部分签名结果
        S2->>W: 提交部分签名结果
        S3->>W: 提交部分签名结果

        W->>W: 合成完整数字签名
        W->>W: 本地验证签名有效性

        note over W: ✅ 生成标准ECDSA签名 (与单签名等价)
    end

    rect rgb(252, 252, 252, 0.3)
        note over W, BC: 🚀 阶段5: 交易提交与确认
        W->>BC: 广播签名交易到区块链
        BC->>BC: 验证签名 & 执行交易
        BC-->>W: 交易确认回执
        W-->>U: 交易完成通知

        note over U, BC: 🎉 资产转移完成，全程无完整私钥暴露
    end

    note over U, BC: 💡 优势总结:<br/>✅ 链下计算，无额外链上开销<br/>✅ 分布式安全，无单点风险<br/>✅ 用户体验与传统钱包一致
'''
    return mermaid_content


def convert_mermaid_to_png(output_path="mpc_wallet_flow.png", width=1200, height=1600):
    """
    将Mermaid图表转换为PNG格式

    参数:
        output_path: 输出PNG文件路径
        width: 图片宽度（像素）
        height: 图片高度（像素）
    """

    # 检查必要的依赖
    dependencies = {
        'mmdc': 'mermaid-cli (npm install -g @mermaid-js/mermaid-cli)',
        'node': 'Node.js'
    }

    for cmd, install_info in dependencies.items():
        if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
            print(f"❌ 缺少依赖: {cmd}")
            print(f"   安装方法: {install_info}")
            return False

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(create_mermaid_content())
        temp_mermaid_path = temp_file.name

    try:
        # 创建Mermaid配置文件
        config = {
            "theme": "base",
            "themeVariables": {
                "primaryColor": "#ffffff",
                "primaryTextColor": "#000000",
                "primaryBorderColor": "#000000",
                "lineColor": "#000000",
                "secondaryColor": "#f0f0f0",
                "tertiaryColor": "#e0e0e0",
                "background": "#ffffff",
                "mainBkg": "#ffffff",
                "secondBkg": "#f8f8f8",
                "tertiaryBkg": "#f0f0f0",
                "actorTextColor": "#000000",
                "actorLineColor": "#000000",
                "signalColor": "#000000",
                "signalTextColor": "#000000",
                "labelBoxBkgColor": "#ffffff",
                "labelTextColor": "#000000",
                "loopTextColor": "#000000",
                "noteBorderColor": "#000000",
                "noteTextColor": "#000000",
                "activationBorderColor": "#000000",
                "activationBkgColor": "#f0f0f0",
                "sequenceNumberColor": "#000000"
            }
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as config_file:
            json.dump(config, config_file, indent=2)
            temp_config_path = config_file.name

        # 使用mmdc命令转换
        cmd = [
            'mmdc',
            '-i', temp_mermaid_path,
            '-o', output_path,
            '-t', 'default',
            '-c', temp_config_path,
            '-w', str(width),
            '-H', str(height),
            '--backgroundColor', 'white'
        ]

        print(f"🔄 正在转换Mermaid图表为PNG...")
        print(f"   命令: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ 转换成功！PNG文件已保存为: {output_path}")
            print(f"   文件大小: {os.path.getsize(output_path)} bytes")
            return True
        else:
            print(f"❌ 转换失败:")
            print(f"   错误信息: {result.stderr}")
            print(f"   输出信息: {result.stdout}")
            return False

    except Exception as e:
        print(f"❌ 转换过程出错: {str(e)}")
        return False

    finally:
        # 清理临时文件
        try:
            os.unlink(temp_mermaid_path)
            os.unlink(temp_config_path)
        except:
            pass


def install_dependencies():
    """安装必要的依赖"""
    print("🔧 安装依赖项...")

    # 检查Node.js
    if subprocess.run(['which', 'node'], capture_output=True).returncode != 0:
        print("❌ 请先安装Node.js: https://nodejs.org/")
        return False

    # 安装mermaid-cli
    print("📦 安装mermaid-cli...")
    result = subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'],
                            capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ mermaid-cli安装成功!")
        return True
    else:
        print(f"❌ mermaid-cli安装失败: {result.stderr}")
        return False


if __name__ == "__main__":
    print("🚀 MPC热钱包流程图转换器")
    print("=" * 50)

    # 检查并安装依赖
    if subprocess.run(['which', 'mmdc'], capture_output=True).returncode != 0:
        print("⚠️  未找到mermaid-cli，是否需要安装? (y/n): ", end="")
        if input().lower() == 'y':
            if not install_dependencies():
                exit(1)
        else:
            print("请手动安装: npm install -g @mermaid-js/mermaid-cli")
            exit(1)

    # 设置输出参数
    output_file = "mpc_wallet_flow_black.png"
    width = 1400
    height = 1800

    print(f"📊 转换参数:")
    print(f"   输出文件: {output_file}")
    print(f"   图片尺寸: {width}x{height}")
    print(f"   颜色设置: 黑色线条和文字")

    # 执行转换
    success = convert_mermaid_to_png(output_file, width, height)

    if success:
        print("\n🎉 转换完成!")
        print(f"   PNG文件: {os.path.abspath(output_file)}")
        print("   线条和文字已设置为黑色")
    else:
        print("\n❌ 转换失败，请检查错误信息")
        exit(1)