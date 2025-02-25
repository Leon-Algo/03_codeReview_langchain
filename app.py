import os
from dotenv import load_dotenv
from langchain.chains import SequentialChain
from langchain_openai import ChatOpenAI
from chains.code_generation_chain import create_code_generation_chain
from chains.code_review_chain import create_code_review_chain
from chains.code_improvement_chain import create_code_improvement_chain
from chains.test_case_generation_chain import create_test_case_generation_chain
from chains.unit_test_generation_chain import create_unit_test_generation_chain

# 加载环境变量
load_dotenv()

def initialize_llm():
    """初始化大语言模型"""
    return ChatOpenAI(
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url=os.getenv("SILICONFLOW_BASE_URL"),
        model="Qwen/Qwen2.5-7B-Instruct",
        temperature=0.7
    )

def create_code_generator():
    """创建完整的代码生成器流程"""
    llm = initialize_llm()
    
    # 创建各个Chain
    code_generation_chain = create_code_generation_chain(llm)
    code_review_chain = create_code_review_chain(llm)
    code_improvement_chain = create_code_improvement_chain(llm)
    test_case_generation_chain = create_test_case_generation_chain(llm)
    unit_test_generation_chain = create_unit_test_generation_chain(llm)
    
    # 创建完整的顺序Chain
    code_generator = SequentialChain(
        chains=[
            code_generation_chain,
            code_review_chain,
            code_improvement_chain,
            test_case_generation_chain,
            unit_test_generation_chain
        ],
        input_variables=["business_requirement"],
        output_variables=["generated_code", "code_review", "improved_code", "test_cases", "unit_tests"],
        verbose=True
    )
    
    return code_generator

def main():
    """主函数"""
    print("欢迎使用基于LangChain的高质量代码生成器！")
    print("请输入您的业务需求，我们将为您生成高质量的代码。")
    
    business_requirement = input("请输入业务需求: ")
    
    code_generator = create_code_generator()
    
    print("\n正在处理您的请求，请稍候...\n")
    
    result = code_generator.invoke({"business_requirement": business_requirement})
    
    print("\n=== 生成的代码 ===")
    print(result["generated_code"])
    
    print("\n=== 代码评审 ===")
    print(result["code_review"])
    
    print("\n=== 改进后的代码 ===")
    print(result["improved_code"])
    
    print("\n=== 测试用例 ===")
    print(result["test_cases"])
    
    print("\n=== 单元测试代码 ===")
    print(result["unit_tests"])

if __name__ == "__main__":
    main() 