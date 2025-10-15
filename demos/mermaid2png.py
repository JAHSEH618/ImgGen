import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建图形和轴
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# 定义颜色方案
colors = {
    'user': '#FF6B6B',           # 用户端 - 红色
    'payment_entry': '#4ECDC4',   # 付款接入层 - 青色
    'traditional': '#45B7D1',     # 传统轨道 - 蓝色
    'modern': '#96CEB4',          # 新兴轨道 - 绿色
    'settlement': '#FFEAA7',      # 收款结算层 - 黄色
    'mto': '#DDA0DD',            # 专业汇款 - 紫色
    'support': '#F8B500'         # 支撑服务 - 橙色
}

def draw_rounded_box(ax, x, y, width, height, text, color, text_size=9):
    """绘制圆角矩形框"""
    box = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.1",
        facecolor=color,
        edgecolor='black',
        linewidth=1.5,
        alpha=0.8
    )
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text,
            ha='center', va='center', fontsize=text_size,
            weight='bold', wrap=True)

def draw_arrow(ax, start_x, start_y, end_x, end_y, style='solid', color='black'):
    """绘制箭头连接线"""
    if style == 'dashed':
        arrow = ConnectionPatch((start_x, start_y), (end_x, end_y), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc=color, linestyle='--', alpha=0.7)
    else:
        arrow = ConnectionPatch((start_x, start_y), (end_x, end_y), "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc=color, linewidth=2)
    ax.add_patch(arrow)

# ========== 绘制各层级 ==========

# 用户端
draw_rounded_box(ax, 0.5, 10.5, 1.5, 0.8, '买家/付款人', colors['user'])
draw_rounded_box(ax, 8, 10.5, 1.5, 0.8, '卖家/收款人', colors['user'])

# 付款接入层
ax.text(2.5, 9.5, '付款接入层', fontsize=12, weight='bold', ha='center')
draw_rounded_box(ax, 0.5, 8.5, 1.2, 0.6, '支付网关', colors['payment_entry'])
draw_rounded_box(ax, 2, 8.5, 1.2, 0.6, '数字钱包', colors['payment_entry'])
draw_rounded_box(ax, 3.5, 8.5, 1.2, 0.6, '数字银行', colors['payment_entry'])
draw_rounded_box(ax, 5, 8.5, 1.2, 0.6, '收单机构', colors['payment_entry'])

# 跨境基础设施层
ax.text(5, 7.2, '跨境基础设施层', fontsize=12, weight='bold', ha='center')

# 传统轨道
ax.text(2.5, 6.5, '传统轨道', fontsize=10, weight='bold', ha='center')
draw_rounded_box(ax, 1.5, 5.8, 1, 0.5, '卡网络', colors['traditional'])
draw_rounded_box(ax, 2.8, 5.8, 1, 0.5, '银行网络', colors['traditional'])

# 新兴轨道
ax.text(7.5, 6.5, '新兴轨道', fontsize=10, weight='bold', ha='center')
draw_rounded_box(ax, 6.5, 5.8, 1, 0.5, '即时支付', colors['modern'])
draw_rounded_box(ax, 7.8, 5.8, 1, 0.5, '链上资产', colors['modern'])

# 收款结算层
ax.text(5, 4.5, '收款结算层', fontsize=12, weight='bold', ha='center')
draw_rounded_box(ax, 3, 3.5, 1.5, 0.6, '跨境收款平台', colors['settlement'])
draw_rounded_box(ax, 5, 3.5, 1.3, 0.6, '外汇服务商', colors['settlement'])
draw_rounded_box(ax, 6.8, 3.5, 1, 0.6, '发卡行', colors['settlement'])

# 专业汇款通道
ax.text(1.5, 4.5, '专业汇款通道', fontsize=12, weight='bold', ha='center')
draw_rounded_box(ax, 0.8, 3.5, 1.3, 0.6, '汇款运营商', colors['mto'])

# 支撑服务层
ax.text(5, 2.2, '支撑服务层', fontsize=12, weight='bold', ha='center')
draw_rounded_box(ax, 2, 1.2, 1.2, 0.6, '合规风控', colors['support'])
draw_rounded_box(ax, 3.5, 1.2, 1.8, 0.6, '支付服务商基础设施', colors['support'])
draw_rounded_box(ax, 5.8, 1.2, 1.2, 0.6, '监管框架', colors['support'])

# ========== 绘制连接线 ==========

# 用户发起
draw_arrow(ax, 1.25, 10.5, 2.5, 9.1)

# 付款接入到基础设施
draw_arrow(ax, 1.1, 8.5, 2, 6.3)  # 支付网关到传统轨道
draw_arrow(ax, 1.1, 8.5, 7, 6.3)  # 支付网关到新兴轨道
draw_arrow(ax, 2.6, 8.5, 2, 6.3)  # 数字钱包到卡网络
draw_arrow(ax, 2.6, 8.5, 7, 6.3)  # 数字钱包到即时支付
draw_arrow(ax, 4.1, 8.5, 3.3, 6.3)  # 数字银行到银行网络
draw_arrow(ax, 4.1, 8.5, 7, 6.3)  # 数字银行到即时支付
draw_arrow(ax, 5.6, 8.5, 2, 6.3)  # 收单机构到卡网络

# 基础设施到结算
draw_arrow(ax, 2, 5.8, 3.7, 4.1)  # 卡网络到结算
draw_arrow(ax, 3.3, 5.8, 3.7, 4.1)  # 银行网络到结算
draw_arrow(ax, 7, 5.8, 5.2, 4.1)  # 即时支付到结算
draw_arrow(ax, 8.3, 5.8, 5.2, 4.1, style='dashed')  # 链上资产到结算

# 结算内部流程
draw_arrow(ax, 4.5, 3.8, 5, 3.8)  # 跨境收款平台到外汇服务商
draw_arrow(ax, 4.5, 3.5, 8.2, 10.5)  # 跨境收款平台到卖家
draw_arrow(ax, 5.6, 3.5, 8.2, 10.5)  # 外汇服务商到卖家
draw_arrow(ax, 7.3, 3.5, 3.3, 5.8)  # 发卡行到银行网络

# 专业汇款独立通道
draw_arrow(ax, 1.25, 10.5, 1.4, 4.1, color='purple')  # 买家到汇款运营商
draw_arrow(ax, 2.1, 3.8, 8, 10.5, color='purple')  # 汇款运营商到卖家

# 支撑关系 (虚线)
draw_arrow(ax, 2.6, 1.8, 1.1, 8.5, style='dashed', color='gray')  # 合规到支付网关
draw_arrow(ax, 2.6, 1.8, 5.6, 8.5, style='dashed', color='gray')  # 合规到收单机构
draw_arrow(ax, 2.6, 1.8, 3.7, 3.5, style='dashed', color='gray')  # 合规到跨境收款平台
draw_arrow(ax, 2.6, 1.8, 1.4, 3.5, style='dashed', color='gray')  # 合规到汇款运营商

draw_arrow(ax, 4.4, 1.8, 2, 5.8, style='dashed', color='gray')  # PSP基础设施到卡网络
draw_arrow(ax, 4.4, 1.8, 5.6, 8.5, style='dashed', color='gray')  # PSP基础设施到收单机构

# 监管覆盖 (虚线)
draw_arrow(ax, 6.4, 1.8, 2.5, 8.5, style='dashed', color='red')  # 监管到付款接入层
draw_arrow(ax, 6.4, 1.8, 5, 5.8, style='dashed', color='red')  # 监管到基础设施
draw_arrow(ax, 6.4, 1.8, 5, 3.5, style='dashed', color='red')  # 监管到结算层

# 添加标题
plt.title('跨境支付系统架构流程图', fontsize=16, weight='bold', pad=20)

# 添加图例
legend_elements = [
    mpatches.Patch(color=colors['user'], label='用户端'),
    mpatches.Patch(color=colors['payment_entry'], label='付款接入层'),
    mpatches.Patch(color=colors['traditional'], label='传统轨道'),
    mpatches.Patch(color=colors['modern'], label='新兴轨道'),
    mpatches.Patch(color=colors['settlement'], label='收款结算层'),
    mpatches.Patch(color=colors['mto'], label='专业汇款'),
    mpatches.Patch(color=colors['support'], label='支撑服务')
]

ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1),
          fontsize=10, frameon=True, fancybox=True, shadow=True)

# 调整布局并保存
plt.tight_layout()
plt.savefig('跨境支付系统流程图.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.show()

print("跨境支付系统流程图已生成并保存为 '跨境支付系统流程图.png'")