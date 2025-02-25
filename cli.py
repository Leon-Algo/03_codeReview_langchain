import os
import argparse
from dotenv import load_dotenv
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

def generate_code(business_requirement):
    """生成代码"""
    llm = initialize_llm()
    chain = create_code_generation_chain(llm)
    return chain.invoke({"business_requirement": business_requirement})

def review_code(business_requirement, generated_code):
    """评审代码"""
    llm = initialize_llm()
    chain = create_code_review_chain(llm)
    return chain.invoke({
        "business_requirement": business_requirement,
        "generated_code": generated_code
    })

def improve_code(business_requirement, generated_code, code_review):
    """改进代码"""
    llm = initialize_llm()
    chain = create_code_improvement_chain(llm)
    return chain.invoke({
        "business_requirement": business_requirement,
        "generated_code": generated_code,
        "code_review": code_review
    })

def generate_test_cases(business_requirement, improved_code):
    """生成测试用例"""
    llm = initialize_llm()
    chain = create_test_case_generation_chain(llm)
    return chain.invoke({
        "business_requirement": business_requirement,
        "improved_code": improved_code
    })

def generate_unit_tests(business_requirement, improved_code, test_cases):
    """生成单元测试"""
    llm = initialize_llm()
    chain = create_unit_test_generation_chain(llm)
    return chain.invoke({
        "business_requirement": business_requirement,
        "improved_code": improved_code,
        "test_cases": test_cases
    })

def save_to_file(content, filename):
    """保存内容到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"内容已保存到 {filename}")

def main():
    parser = argparse.ArgumentParser(description='基于LangChain的高质量代码生成器')
    parser.add_argument('--requirement', '-r', type=str, help='业务需求')
    parser.add_argument('--code', '-c', type=str, help='已有代码文件路径')
    parser.add_argument('--review', '-v', action='store_true', help='生成代码评审')
    parser.add_argument('--improve', '-i', action='store_true', help='生成改进代码')
    parser.add_argument('--test-cases', '-t', action='store_true', help='生成测试用例')
    parser.add_argument('--unit-tests', '-u', action='store_true', help='生成单元测试')
    parser.add_argument('--all', '-a', action='store_true', help='执行所有步骤')
    parser.add_argument('--output-dir', '-o', type=str, default='output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建输出目录
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # 获取业务需求
    business_requirement = args.requirement
    if not business_requirement:
        business_requirement = input("请输入业务需求: ")
    
    # 获取已有代码
    generated_code = None
    if args.code:
        with open(args.code, 'r', encoding='utf-8') as f:
            generated_code = f.read()
    
    # 执行步骤
    if args.all or not (args.review or args.improve or args.test_cases or args.unit_tests):
        # 如果选择了--all或没有选择任何特定步骤，执行所有步骤
        
        # 步骤1: 生成代码
        if not generated_code:
            print("步骤1: 生成代码...")
            result = generate_code(business_requirement)
            generated_code = result["generated_code"]
            save_to_file(generated_code, f"{args.output_dir}/generated_code.py")
        
        # 步骤2: 代码评审
        print("步骤2: 代码评审...")
        result = review_code(business_requirement, generated_code)
        code_review = result["code_review"]
        save_to_file(code_review, f"{args.output_dir}/code_review.md")
        
        # 步骤3: 改进代码
        print("步骤3: 改进代码...")
        result = improve_code(business_requirement, generated_code, code_review)
        improved_code = result["improved_code"]
        save_to_file(improved_code, f"{args.output_dir}/improved_code.py")
        
        # 步骤4: 生成测试用例
        print("步骤4: 生成测试用例...")
        result = generate_test_cases(business_requirement, improved_code)
        test_cases = result["test_cases"]
        save_to_file(test_cases, f"{args.output_dir}/test_cases.md")
        
        # 步骤5: 生成单元测试
        print("步骤5: 生成单元测试...")
        result = generate_unit_tests(business_requirement, improved_code, test_cases)
        unit_tests = result["unit_tests"]
        save_to_file(unit_tests, f"{args.output_dir}/test_{args.output_dir}.py")
        
    else:
        # 单独执行选择的步骤
        
        # 步骤1: 生成代码（如果没有提供）
        if not generated_code:
            print("生成代码...")
            result = generate_code(business_requirement)
            generated_code = result["generated_code"]
            save_to_file(generated_code, f"{args.output_dir}/generated_code.py")
        
        code_review = None
        improved_code = None
        test_cases = None
        
        # 步骤2: 代码评审
        if args.review:
            print("生成代码评审...")
            result = review_code(business_requirement, generated_code)
            code_review = result["code_review"]
            save_to_file(code_review, f"{args.output_dir}/code_review.md")
        
        # 步骤3: 改进代码
        if args.improve:
            if not code_review and args.review:
                print("需要先生成代码评审...")
                result = review_code(business_requirement, generated_code)
                code_review = result["code_review"]
                save_to_file(code_review, f"{args.output_dir}/code_review.md")
            
            print("生成改进代码...")
            result = improve_code(business_requirement, generated_code, code_review or "")
            improved_code = result["improved_code"]
            save_to_file(improved_code, f"{args.output_dir}/improved_code.py")
        
        # 步骤4: 生成测试用例
        if args.test_cases:
            print("生成测试用例...")
            result = generate_test_cases(business_requirement, improved_code or generated_code)
            test_cases = result["test_cases"]
            save_to_file(test_cases, f"{args.output_dir}/test_cases.md")
        
        # 步骤5: 生成单元测试
        if args.unit_tests:
            if not test_cases and args.test_cases:
                print("需要先生成测试用例...")
                result = generate_test_cases(business_requirement, improved_code or generated_code)
                test_cases = result["test_cases"]
                save_to_file(test_cases, f"{args.output_dir}/test_cases.md")
            
            print("生成单元测试...")
            result = generate_unit_tests(
                business_requirement, 
                improved_code or generated_code, 
                test_cases or ""
            )
            unit_tests = result["unit_tests"]
            save_to_file(unit_tests, f"{args.output_dir}/test_{args.output_dir}.py")
    
    print("完成！")

if __name__ == "__main__":
    main() 