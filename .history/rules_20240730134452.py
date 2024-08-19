from pydantic import BaseModel
from datetime import datetime
import ast
from schedule_handle import by_task_id, task_info1

要将提取的函数名变成可执行的函数，你可以使用 globals() 或 locals() 函数来获取当前作用域中的函数对象。以下是一个完整的示例代码，展示如何提取函数名并将其变成可执行的函数：

创建一个 Python 文件（例如 example.py）并定义一些函数：
# example.py

def foo():
    print("foo was called")

def bar():
    print("bar was called")

def baz():
    print("baz was called")
创建一个脚本来解析这个文件，提取函数名，并执行这些函数：
# execute_functions.py

import ast
import example  # 导入你要解析的模块

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def execute_functions(module, function_names):
    for name in function_names:
        func = getattr(module, name, None)
        if callable(func):
            print(f"Executing {name}()")
            func()

if __name__ == "__main__":
    filename = "example.py"  # 替换为你的文件名
    functions = get_function_names(filename)
    print("Functions in {}: {}".format(filename, functions))
    
    # 执行提取到的函数
    execute_functions(example, functions)
运行这个脚本：
python execute_functions.py
输出将会是：

Functions in example.py: ['foo', 'bar', 'baz']
Executing foo()
foo was called
Executing bar()
bar was called
Executing baz()
baz was called
在这个脚本中，我们首先使用 ast 模块解析 example.py 文件并提取函数名。然后，我们使用 getattr 函数从 example 模块中获取函数对象，并确保它们是可调用的（即函数）。最后，我们执行这些函数并打印相应的输出。

在同一个文件执行这些操作，在一个check的函数中变量本文件之外的其他所有函数并执行

要在同一个文件中实现提取并执行所有函数，你可以将所有逻辑都放在一个文件中，并定义一个 check 函数来遍历并执行本文件中的所有其他函数。以下是一个示例代码：

# example.py

import ast

def foo():
    print("foo was called")

def bar():
    print("bar was called")

def baz():
    print("baz was called")

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check():
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    # 执行提取到的函数
    for name in functions:
        func = globals().get(name)
        if callable(func):
            print(f"Executing {name}()")
            func()

if __name__ == "__main__":
    check()
在这个代码中：

我们定义了一些函数：foo、bar 和 baz。
get_function_names 函数用于解析当前文件并提取所有函数名。
check 函数用于遍历并执行除自身之外的所有函数。
在 check 函数中，我们使用 globals().get(name) 来获取当前全局作用域中的函数对象，并确保它们是可调用的。
最后，在 __main__ 块中调用 check 函数。
运行这个脚本：

python example.py
输出将会是：

Executing foo()
foo was called
Executing bar()
bar was called
Executing baz()
baz was called
这样，你就可以在同一个文件中提取并执行所有其他函数。

函数可以传递一个参数msg

要让函数能够接收一个参数 msg，你需要对函数定义进行修改，并在调用这些函数时传递这个参数。以下是修改后的代码示例：

# example.py

import ast

def foo(msg):
    print(f"foo was called with message: {msg}")

def bar(msg):
    print(f"bar was called with message: {msg}")

def baz(msg):
    print(f"baz was called with message: {msg}")

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check(msg):
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    # 执行提取到的函数，并传递参数 msg
    for name in functions:
        func = globals().get(name)
        if callable(func):
            print(f"Executing {name}() with message: {msg}")
            func(msg)

if __name__ == "__main__":
    check("Hello, World!")
在这个代码中：

我们修改了 foo、bar 和 baz 函数，使它们接收一个参数 msg。
在 check 函数中，我们遍历并执行这些函数时，传递了参数 msg。
在 __main__ 块中，我们调用 check 函数并传递了一个字符串 "Hello, World!" 作为参数。
运行这个脚本：

python example.py
输出将会是：

Executing foo() with message: Hello, World!
foo was called with message: Hello, World!
Executing bar() with message: Hello, World!
bar was called with message: Hello, World!
Executing baz() with message: Hello, World!
baz was called with message: Hello, World!
这样，每个函数在被调用时都会接收到并打印传递的消息。

函数返回一个str参数，在check中使用list收集所有函数的返回结果并返回

为了实现函数返回一个字符串参数，并在 check 函数中收集所有函数的返回结果并返回，我们需要对每个函数进行修改，使其返回一个字符串。然后在 check 函数中，我们将这些返回值收集到一个列表中并返回。以下是修改后的代码示例：

# example.py

import ast

def foo(msg):
    return f"foo was called with message: {msg}"

def bar(msg):
    return f"bar was called with message: {msg}"

def baz(msg):
    return f"baz was called with message: {msg}"

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check(msg):
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    results = []
    
    # 执行提取到的函数，并传递参数 msg
    for name in functions:
        func = globals().get(name)
        if callable(func):
            print(f"Executing {name}() with message: {msg}")
            result = func(msg)
            results.append(result)
    
    return results

if __name__ == "__main__":
    results = check("Hello, World!")
    print("Results:", results)
在这个代码中：

我们修改了 foo、bar 和 baz 函数，使它们返回一个字符串。
在 check 函数中，我们遍历并执行这些函数时，传递了参数 msg，并收集每个函数的返回值到一个列表 results 中。
最后，check 函数返回这个 results 列表。
在 __main__ 块中，我们调用 check 函数并打印返回的结果。
运行这个脚本：

python example.py
输出将会是：

Executing foo() with message: Hello, World!
Executing bar() with message: Hello, World!
Executing baz() with message: Hello, World!
Results: ['foo was called with message: Hello, World!', 'bar was called with message: Hello, World!', 'baz was called with message: Hello, World!']
这样，每个函数返回的字符串被收集到一个列表中，并在 check 函数中返回。

如何合并多个dict类型的数据

合并多个 dict 类型的数据有多种方法，具体取决于你使用的 Python 版本以及你希望如何处理重复的键。以下是几种常见的方法：

使用 update 方法
你可以使用 dict 的 update 方法来合并多个字典。请注意，这种方法会修改原始字典，并且在有重复键时，后面的字典会覆盖前面的字典的值。

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 合并到 dict1 中
dict1.update(dict2)
dict1.update(dict3)

print(dict1)  # 输出: {'a': 1, 'b': 3, 'c': 4, 'd': 5}
使用字典解包（Python 3.5+）
从 Python 3.5 开始，你可以使用字典解包（dictionary unpacking）来合并多个字典。

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 使用字典解包合并
merged_dict = {**dict1, **dict2, **dict3}

print(merged_dict)  # 输出: {'a': 1, 'b': 3, 'c': 4, 'd': 5}
使用 collections.ChainMap（Python 3.3+）
collections.ChainMap 可以用于将多个字典合并为一个视图，但它不会实际创建一个新的字典。

from collections import ChainMap

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 使用 ChainMap 合并
merged_dict = ChainMap(dict1, dict2, dict3)

print(merged_dict)  # 输出: ChainMap({'a': 1, 'b': 2}, {'b': 3, 'c': 4}, {'d': 5})
print(dict(merged_dict))  # 转换为字典: {'d': 5, 'b': 2, 'c': 4, 'a': 1}
使用字典合并运算符（Python 3.9+）
从 Python 3.9 开始，字典支持使用 | 运算符进行合并。

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 使用字典合并运算符
merged_dict = dict1 | dict2 | dict3

print(merged_dict)  # 输出: {'a': 1, 'b': 3, 'c': 4, 'd': 5}
自定义合并逻辑
如果你需要自定义合并逻辑，比如在有重复键时执行特定操作，可以使用一个循环来实现。

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 自定义合并逻辑
merged_dict = {}

for d in (dict1, dict2, dict3):
    for key, value in d.items():
        if key in merged_dict:
            # 自定义处理重复键的逻辑
            merged_dict[key] += value  # 例如，累加值
        else:
            merged_dict[key] = value

print(merged_dict)  # 输出: {'a': 1, 'b': 5, 'c': 4, 'd': 5}
选择适合你的具体需求的方法来合并字典。

合并之后将dict转成json

将合并后的 dict 转换为 JSON 格式非常简单，可以使用 Python 的 json 模块。以下是一个完整的示例，展示如何合并多个字典并将结果转换为 JSON 字符串：

示例代码
import json
from collections import ChainMap

# 定义多个字典
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 方法1：使用字典解包（适用于Python 3.5+）
merged_dict = {**dict1, **dict2, **dict3}

# 方法2：使用字典合并运算符（适用于Python 3.9+）
# merged_dict = dict1 | dict2 | dict3

# 方法3：使用 collections.ChainMap（适用于Python 3.3+）
# merged_dict = dict(ChainMap(dict1, dict2, dict3))

# 方法4：使用 update 方法
# merged_dict = dict1.copy()
# merged_dict.update(dict2)
# merged_dict.update(dict3)

# 将合并后的字典转换为 JSON 字符串
json_str = json.dumps(merged_dict, ensure_ascii=False, indent=4)

# 打印 JSON 字符串
print(json_str)
解释
合并字典：

方法1：使用字典解包（适用于 Python 3.5+）。
方法2：使用字典合并运算符（适用于 Python 3.9+）。
方法3：使用 collections.ChainMap（适用于 Python 3.3+）。
方法4：使用 update 方法。
转换为 JSON：

使用 json.dumps 方法将合并后的字典转换为 JSON 字符串。
参数 ensure_ascii=False 确保非 ASCII 字符能够正确编码。
参数 indent=4 用于美化输出，使 JSON 字符串更易读。
输出示例
{
    "a": 1,
    "b": 3,
    "c": 4,
    "d": 5
}
你可以根据需要选择适合的合并方法，并将结果转换为 JSON 格式。

转化成json对象后，将所有字段封装成BaseModel的Info类

要将合并后的字典转换为 JSON 对象，并将所有字段封装到一个 BaseModel 的 Info 类中，可以使用 pydantic 库。pydantic 是一个数据验证和设置管理的库，基于 Python 的类型注解。

首先，确保你已经安装了 pydantic 库。如果还没有安装，可以使用以下命令安装：

pip install pydantic
然后，你可以按照以下步骤操作：

合并字典。
将合并后的字典转换为 JSON 对象。
使用 pydantic 定义 BaseModel 和 Info 类。
将 JSON 对象转换为 Info 类的实例。
以下是完整的示例代码：

示例代码
import json
from pydantic import BaseModel
from typing import Any, Dict

# 定义多个字典
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 合并字典（使用字典解包）
merged_dict = {**dict1, **dict2, **dict3}

# 将合并后的字典转换为 JSON 字符串
json_str = json.dumps(merged_dict, ensure_ascii=False, indent=4)

# 将 JSON 字符串转换为 JSON 对象
json_obj = json.loads(json_str)

# 定义 BaseModel 和 Info 类
class Info(BaseModel):
    a: Any = None
    b: Any = None
    c: Any = None
    d: Any = None

class BaseModelWithInfo(BaseModel):
    info: Info

# 将 JSON 对象转换为 Info 类实例
info_instance = Info(**json_obj)

# 将 Info 实例封装到 BaseModelWithInfo 中
base_model_instance = BaseModelWithInfo(info=info_instance)

# 打印 BaseModelWithInfo 实例
print(base_model_instance.json(indent=4, ensure_ascii=False))
解释
合并字典：

使用字典解包的方法合并多个字典。
转换为 JSON：

使用 json.dumps 将合并后的字典转换为 JSON 字符串。
使用 json.loads 将 JSON 字符串转换为 JSON 对象。
定义 BaseModel 和 Info 类：

使用 pydantic 定义 Info 类，其中包含所有可能的字段。
定义一个包含 Info 实例的 BaseModelWithInfo 类。
实例化 Info 类：

使用 Info(**json_obj) 将 JSON 对象转换为 Info 类的实例。
封装到 BaseModelWithInfo 中：

创建 BaseModelWithInfo 的实例，并将 Info 实例传递给它。
打印结果：

使用 base_model_instance.json 方法打印 BaseModelWithInfo 实例的 JSON 表示。
输出示例
{
    "info": {
        "a": 1,
        "b": 3,
        "c": 4,
        "d": 5
    }
}
这样，你就成功地将合并后的字典封装到了一个 BaseModel 的 Info 类中，并可以以 JSON 格式输出。

如何将json对象封装成BaseModel类

将 JSON 对象封装成 pydantic 的 BaseModel 类实例，可以直接利用 pydantic 的数据解析和验证功能。以下是一个完整的示例，展示如何将 JSON 对象封装到一个 BaseModel 类中。

示例代码
安装 pydantic（如果还没有安装）：

pip install pydantic
Python 代码：

import json
from pydantic import BaseModel
from typing import Any

# 定义多个字典
dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5}

# 合并字典（使用字典解包）
merged_dict = {**dict1, **dict2, **dict3}

# 将合并后的字典转换为 JSON 字符串
json_str = json.dumps(merged_dict, ensure_ascii=False, indent=4)

# 将 JSON 字符串转换为 JSON 对象
json_obj = json.loads(json_str)

# 定义 BaseModel 类
class Info(BaseModel):
    a: Any = None
    b: Any = None
    c: Any = None
    d: Any = None

# 将 JSON 对象转换为 Info 类实例
info_instance = Info(**json_obj)

# 打印 Info 实例
print(info_instance.json(indent=4, ensure_ascii=False))

class Info(BaseModel):
    taskid: str  
    taskname: str  
    sql: str
    in_charge: str
    start_t: str
    caution_t: str

# rule1: 告警时间需晚于生效时间
def r1(info:dict) -> str:
    task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    caution_t = task.get("unSuccessOverTime")
    start_t = task.get("startDate")
    # 假设你有一个字符串，格式为 "2022-11-22 03:30:00"
    # 使用 datetime.strptime() 方法将字符串解析为 datetime 对象
    date_object = datetime.strptime(start_t, '%Y-%m-%d %H:%M:%S')
    # 修改时间格式为 "HH:MM"
    start_t = "{:02d}:{:02d}".format(date_object.hour, date_object.minute)
    start_t_cmp = date_object.hour * 60 + date_object.minute
    date_object = datetime.strptime(caution_t, '%H:%M')
    caution_t_cmp = date_object.hour * 60 + date_object.minute
    # 条件1
    if caution_t_cmp <= start_t_cmp:
        return "告警时间需晚于生效时间"

# 任务负责人至少2个
def r2(info:dict) -> str:
    task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    in_charge = task.get("inCharge")
    my_list = in_charge.split(',')
    if len(my_list) < 2:
        return "任务负责人至少2个"

def get_function_names(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names

def check(info:dict) -> list:
    filename = __file__  # 获取当前文件名
    functions = get_function_names(filename)
    
    # 排除 'check' 函数自身
    functions = [f for f in functions if f != 'check' and f != 'get_function_names']
    
    res = []

    # 执行提取到的函数
    for name in functions:
        func = globals().get(name)
        if callable(func):
            print(f"Executing {name}()")
            res.append(func(info))
    return res

if __name__ == "__main__":
    t_id = by_task_id(10007072)
    info = task_info1(t_id)
    data1_task = info.get('data', {}).get('taskDtoLatest', {}).get('task', {})
    data1_map = info.get('data', {}).get('taskDtoLatest', {}).get('map', {})
    # print(data1)
    # print(type(data1))
    data2_task = info.get('data', {}).get('taskDtoOlder', {}).get('task', {})
    data2_map = info.get('data', {}).get('taskDtoOlder', {}).get('map', {})

    # print(check(info))