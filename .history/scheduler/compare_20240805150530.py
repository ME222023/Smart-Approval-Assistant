import json
json_data_1 = """

"""
# 将 JSON 字符串解析为 Python 字典
data_1 = json.loads(json_data_1)
data_2 = json.loads(json_data_2)

def compare_dicts(dict1, dict2, path="root"):
    differences = []
    keys1 = set(dict1.keys())
    keys2 = set(dict2.keys())
    
    # 找出 dict1 中有但 dict2 中没有的键
    for key in keys1 - keys2:
        differences.append(f"{path}.{key} is only in the first JSON.")
    
    # 找出 dict2 中有但 dict1 中没有的键
    for key in keys2 - keys1:
        differences.append(f"{path}.{key} is only in the second JSON.")
    
    # 比较相同的键
    for key in keys1 & keys2:
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            differences.extend(compare_dicts(dict1[key], dict2[key], f"{path}.{key}"))
        elif dict1[key] != dict2[key]:
            differences.append(f"{path}.{key} differs: {dict1[key]} vs {dict2[key]}")
    
    return differences

# 比较两份 JSON 数据
differences = compare_dicts(data_1, data_2)

# 打印差异
if differences:
    print("Differences found:")
    for diff in differences:
        print(diff)
else:
    print("The two JSON data are identical in structure and values.")