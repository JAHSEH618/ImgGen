#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 plan.md 学习计划解析并生成可导入苹果日历的 .ics 文件
"""

import re
from datetime import datetime, timedelta
from pathlib import Path
import uuid


def parse_plan_md(file_path):
    """
    解析 plan.md 文件，提取所有学习任务

    返回格式: [
        {
            'date': '2025-10-20',
            'weekday': '一',
            'title': '掌握 FastAPI 基础',
            'time_range': '21:00-23:30',  # 新增时间段
            'study': '学习资源描述',
            'practice': '实践任务描述',
            'week': 'W1',
            'week_title': '环境脚手架与结构化输出'
        },
        ...
    ]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = []
    current_week = None
    current_week_title = None

    # 匹配周标题，例如: ### **W1 | 2025-10-20 ~ 10-26 | 环境脚手架与结构化输出**
    week_pattern = re.compile(r'###\s+\*\*([W]\d+)\s+\|.*?\|\s+(.+?)\*\*')

    # 分割内容为行
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # 检查是否是周标题
        week_match = week_pattern.search(line)
        if week_match:
            current_week = week_match.group(1)
            current_week_title = week_match.group(2).strip()

        # 检查是否是表格行（包含日期的任务行）
        # 新格式: | **10-20** | 一   | **(21:00-23:30)** 掌握 FastAPI 基础 | ...
        # 或旧格式: | **10-20** | 一   | 掌握 FastAPI 基础 | ...
        if line.startswith('| **') and current_week:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:  # 至少要有日期、星期、目标、学习、实践列
                date_str = parts[1].replace('**', '').strip()
                weekday = parts[2].strip()
                title_with_time = parts[3].strip()
                study = parts[4].strip()
                practice = parts[5].strip()

                # 解析标题中的时间段
                # 格式: **(21:00-23:30)** 掌握 FastAPI 基础
                # 或: **(全天)** 项目冲刺
                # 或: **项目冲刺** (周末，无时间标注)
                time_range = None
                title = title_with_time

                # 匹配时间段格式 (HH:MM-HH:MM)
                time_match = re.search(r'\*\*\((\d{1,2}:\d{2}-\d{1,2}:\d{2})\)\*\*\s+(.+)', title_with_time)
                if time_match:
                    time_range = time_match.group(1)
                    title = time_match.group(2)
                else:
                    # 匹配"全天"格式
                    fullday_match = re.search(r'\*\*\(全天\)\*\*\s+(.+)', title_with_time)
                    if fullday_match:
                        time_range = '全天'
                        title = fullday_match.group(1)
                    else:
                        # 匹配项目冲刺格式（可能包含上午/下午时间）
                        project_match = re.search(r'\*\*(.+?)\*\*', title_with_time)
                        if project_match:
                            title = project_match.group(1)
                            # 判断是否为周末（六或日）
                            if weekday in ['六', '日']:
                                # 检查practice字段是否包含时间信息
                                if '上午' in practice and '下午' in practice:
                                    time_range = '9:00-17:00'  # 周末全天项目
                                else:
                                    time_range = '9:00-12:00'  # 默认上午
                            else:
                                time_range = '21:00-23:30'  # 工作日默认晚间

                # 如果没有解析到时间，根据weekday和任务类型设置默认时间
                if not time_range:
                    if weekday in ['六', '日']:
                        time_range = '9:00-17:00'  # 周末默认全天
                    else:
                        time_range = '21:00-23:30'  # 工作日默认晚间

                # 转换日期格式
                if len(date_str.split('-')) == 2:  # 格式如 "10-20"
                    date_str = f"2025-{date_str}"
                elif len(date_str.split('-')) == 1 and len(date_str) == 5:  # 格式如 "10-20"
                    month_day = date_str.split('-')
                    if len(month_day) == 2:
                        date_str = f"2025-{date_str}"

                # 检测是否跨年（2026年的日期）
                try:
                    month = int(date_str.split('-')[1])
                    if month <= 4:  # 1-4月属于2026年
                        date_str = date_str.replace('2025-', '2026-')
                except Exception:
                    pass

                tasks.append({
                    'date': date_str,
                    'weekday': weekday,
                    'title': title,
                    'time_range': time_range,
                    'study': study,
                    'practice': practice,
                    'week': current_week,
                    'week_title': current_week_title
                })

        i += 1

    return tasks


def create_ics_calendar(tasks, output_path='learning_plan.ics'):
    """
    根据解析的任务创建 .ics 日历文件(直接生成ICS格式,使用本地时间)
    """
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Learning Plan//NONSGML v1.0//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    for task in tasks:
        # 解析日期
        try:
            event_date = datetime.strptime(task['date'], '%Y-%m-%d')
        except ValueError:
            print(f"警告: 无法解析日期 {task['date']}, 跳过此任务")
            continue

        # 解析时间段
        time_range = task.get('time_range', '9:00-17:00')
        is_all_day = (time_range == '全天')

        # 生成唯一ID
        event_uid = str(uuid.uuid4())

        # 设置事件标题
        event_title = f"[{task['week']}] {task['title']}"

        # 设置描述（不包含时间信息）
        description = f"【第{task['week']}周: {task['week_title']}】\\n\\n📚 学习内容:\\n{task['study']}\\n\\n🛠️ 实践任务:\\n{task['practice']}\\n\\n📅 日期: {task['date']} 星期{task['weekday']}"
        description = description.replace('\n', '\\n')

        # 根据时间段设置分类
        weekday = task.get('weekday', '')
        if is_all_day:
            categories = f"{task['week']},AI学习,编程,全天学习"
        elif weekday in ['六', '日']:
            categories = f"{task['week']},AI学习,编程,周末学习"
        else:
            categories = f"{task['week']},AI学习,编程,工作日晚间"

        # 开始构建VEVENT
        ics_lines.append("BEGIN:VEVENT")
        ics_lines.append(f"UID:{event_uid}@ai-learning-plan.org")
        ics_lines.append(f"SUMMARY:{event_title}")
        ics_lines.append(f"DESCRIPTION:{description}")
        ics_lines.append(f"CATEGORIES:{categories}")

        # 设置时间
        if is_all_day:
            # 全天事件使用DATE格式(不带时间)
            date_str = event_date.strftime('%Y%m%d')
            ics_lines.append(f"DTSTART;VALUE=DATE:{date_str}")
            # 全天事件的结束日期是第二天
            next_day = event_date + timedelta(days=1)
            ics_lines.append(f"DTEND;VALUE=DATE:{next_day.strftime('%Y%m%d')}")
        else:
            # 解析时间段格式 HH:MM-HH:MM
            try:
                start_time_str, end_time_str = time_range.split('-')
                start_hour, start_minute = map(int, start_time_str.split(':'))
                end_hour, end_minute = map(int, end_time_str.split(':'))

                # 使用本地时间(不带Z后缀，表示浮动时间)
                start_dt = event_date.replace(hour=start_hour, minute=start_minute, second=0)

                # 处理跨天的情况
                if end_hour == 0 and end_minute == 0:
                    end_dt = (event_date + timedelta(days=1)).replace(hour=0, minute=0, second=0)
                else:
                    end_dt = event_date.replace(hour=end_hour, minute=end_minute, second=0)

                # 格式化为本地时间(不带T后缀表示浮动时间)
                ics_lines.append(f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}")
                ics_lines.append(f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}")

            except Exception as e:
                print(f"警告: 无法解析时间段 {time_range}，使用默认时间 9:00-18:00")
                start_dt = event_date.replace(hour=9, minute=0, second=0)
                end_dt = event_date.replace(hour=18, minute=0, second=0)
                ics_lines.append(f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}")
                ics_lines.append(f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}")

        # 添加提醒
        ics_lines.append("BEGIN:VALARM")
        ics_lines.append("ACTION:DISPLAY")
        ics_lines.append(f"DESCRIPTION:提醒: {event_title}")
        if is_all_day or weekday in ['六', '日']:
            ics_lines.append("TRIGGER:-PT12H")  # 提前12小时
        else:
            ics_lines.append("TRIGGER:-PT2H")   # 提前2小时
        ics_lines.append("END:VALARM")

        ics_lines.append("END:VEVENT")

    ics_lines.append("END:VCALENDAR")

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ics_lines))

    print(f"✅ 成功生成日历文件: {output_path}")
    print(f"📅 共创建 {len(tasks)} 个学习任务")
    return output_path


def main():
    """
    主函数
    """
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    plan_file = script_dir / 'plan.md'
    output_file = script_dir / 'AI_Learning_Plan_2025_2026.ics'

    print("开始解析 plan.md...")
    tasks = parse_plan_md(plan_file)
    print(f"📖 成功解析 {len(tasks)} 个学习任务")

    if tasks:
        # 显示前3个任务作为预览
        print("\n📋 任务预览（前3个）:")
        for i, task in enumerate(tasks[:3], 1):
            print(f"\n{i}. {task['date']} ({task['week']}) - {task['title']}")

        print("\n" + "="*60)
        print("开始生成 .ics 日历文件...")
        create_ics_calendar(tasks, str(output_file))

        print("\n" + "="*60)
        print("🎉 完成！")
        print(f"\n📂 文件位置: {output_file}")
        print("\n💡 使用方法:")
        print("   1. 双击 .ics 文件")
        print("   2. 系统会自动打开日历应用")
        print("   3. 选择要导入到的日历（如：个人、工作等）")
        print("   4. 点击确认导入")
        print("\n⚠️  注意: 如果日历已存在相同事件，可能会提示重复")
    else:
        print("❌ 未找到任何任务，请检查 plan.md 格式")


if __name__ == '__main__':
    main()
