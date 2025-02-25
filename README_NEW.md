# 基于LangChain的高质量代码生成器

这是一个基于LangChain的高质量代码生成器，可以根据业务需求生成代码、进行代码评审、改进代码、生成测试用例和单元测试。

## 功能特点

1. **代码生成**：根据用户提交的业务需求，生成高质量的Python函数代码
2. **代码评审**：对生成的代码进行全面评审，提供改进建议
3. **代码改进**：根据评审结果，生成改进后的代码
4. **测试用例生成**：根据业务需求和代码，生成全面的测试用例
5. **单元测试生成**：根据业务需求、代码和测试用例，生成对应的单元测试代码

## 安装

1. 克隆仓库：

```bash
git clone <仓库URL>
cd <仓库目录>
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

创建一个`.env`文件，添加以下内容：

```
SILICONFLOW_API_KEY="你的API密钥"
SILICONFLOW_BASE_URL="https://api.siliconflow.cn/v1/"
```

## 使用方法

### 命令行界面

```bash
# 执行所有步骤
python cli.py --requirement "你的业务需求" --all

# 只执行特定步骤
python cli.py --requirement "你的业务需求" --review --improve

# 使用已有代码
python cli.py --requirement "你的业务需求" --code path/to/code.py --review

# 指定输出目录
python cli.py --requirement "你的业务需求" --all --output-dir my_output
```

可用的命令行参数：

- `--requirement`, `-r`: 业务需求
- `--code`, `-c`: 已有代码文件路径
- `--review`, `-v`: 生成代码评审
- `--improve`, `-i`: 生成改进代码
- `--test-cases`, `-t`: 生成测试用例
- `--unit-tests`, `-u`: 生成单元测试
- `--all`, `-a`: 执行所有步骤
- `--output-dir`, `-o`: 输出目录（默认为"output"）

### Web界面

```bash
streamlit run web_app.py
```

在Web界面中，您可以：

1. 输入业务需求
2. 选择要执行的步骤
3. 查看和下载生成的代码、代码评审、改进后的代码、测试用例和单元测试
4. 编辑生成的测试用例

## 项目结构

```
.
├── app.py                  # 主应用程序
├── cli.py                  # 命令行界面
├── web_app.py              # Web界面
├── chains/                 # LangChain组件
│   ├── __init__.py
│   ├── code_generation_chain.py
│   ├── code_review_chain.py
│   ├── code_improvement_chain.py
│   ├── test_case_generation_chain.py
│   └── unit_test_generation_chain.py
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明
```

## 示例

### 业务需求示例

```
创建一个函数，用于解析CSV文件并提取特定列的数据，然后计算这些数据的平均值、最大值和最小值。
```

### 生成的代码示例

```python
def parse_csv_and_analyze(file_path, column_name):
    """
    解析CSV文件并提取特定列的数据，然后计算这些数据的平均值、最大值和最小值。
    
    Args:
        file_path (str): CSV文件的路径
        column_name (str): 要分析的列名
        
    Returns:
        dict: 包含平均值、最大值和最小值的字典
        
    Raises:
        FileNotFoundError: 如果文件不存在
        ValueError: 如果列名不存在或数据无法转换为数值
    """
    import csv
    
    # 检查文件是否存在
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # 创建CSV读取器
            reader = csv.DictReader(csvfile)
            
            # 检查列名是否存在
            if column_name not in reader.fieldnames:
                raise ValueError(f"列名 '{column_name}' 不存在于CSV文件中")
            
            # 提取数据
            data = []
            for row in reader:
                try:
                    value = float(row[column_name])
                    data.append(value)
                except ValueError:
                    raise ValueError(f"无法将值 '{row[column_name]}' 转换为数值")
            
            # 检查是否有数据
            if not data:
                return {
                    "average": None,
                    "maximum": None,
                    "minimum": None
                }
            
            # 计算统计值
            average = sum(data) / len(data)
            maximum = max(data)
            minimum = min(data)
            
            return {
                "average": average,
                "maximum": maximum,
                "minimum": minimum
            }
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 '{file_path}' 不存在")
```

## 贡献

欢迎贡献代码、报告问题或提出改进建议。

## 许可证

[MIT](LICENSE) 