import pandas as pd
import json

# 1. 定义文件路径
csv_file_path = '/Users/okonma/Downloads/rrrrr.csv'
json_file_path = '/Users/okonma/Downloads/rsp.json'

try:
    # 2. 使用pandas读取CSV文件
    # 同样，pandas可以很好地处理中文内容
    df = pd.read_csv(csv_file_path)

    # 3. 将所有列转换为字符串类型
    # 这确保了所有数据在JSON中都以字符串形式存储
    # fillna('') 会将 NaN 值替换为空字符串
    df = df.fillna('').astype(str)

    # 4. 将DataFrame转换为JSON字符串
    # - orient='records': 这是关键参数。它指定了JSON的格式。
    #   'records' 会生成一个列表，列表中的每个元素都是一个代表原始数据行的JSON对象。
    #   例如: [{"列1": "值A", "列2": "值B"}, {"列1": "值C", "列2": "值D"}]
    #
    # - force_ascii=False: 确保中文字符在JSON字符串中以原生字符显示，而不是被转义成`\uXXXX`的形式。
    #
    # - indent=4: 让输出的JSON字符串自动缩进4个空格，使其格式优美，易于阅读。
    json_string = df.to_json(orient='records', force_ascii=False, indent=4)

    # 5. 将完整的JSON字符串保存到文件
    # 使用 'w' (写入模式) 和 'utf-8' 编码来保存文件
    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(json_string)

    print(f"文件已成功转换为JSON格式，并保存为 '{json_file_path}'。")
    print(f"所有数据已转换为字符串格式。")

except FileNotFoundError:
    print(f"错误：找不到文件 '{csv_file_path}'。请检查文件名是否正确。")
except Exception as e:
    print(f"处理文件时发生错误：{e}")