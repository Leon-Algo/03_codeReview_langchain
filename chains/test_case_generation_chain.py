from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_test_case_generation_chain(llm):
    """
    创建测试用例生成Chain
    
    Args:
        llm: 大语言模型实例
        
    Returns:
        LLMChain: 测试用例生成Chain
    """
    prompt_template = """
    你是一位测试专家，请根据以下业务需求和代码生成全面的测试用例。
    
    业务需求:
    {business_requirement}
    
    改进后的代码:
    {improved_code}
    
    请生成至少5个测试用例，每个测试用例应包含:
    1. 测试用例ID和名称
    2. 测试目的
    3. 前置条件
    4. 测试步骤
    5. 预期结果
    6. 测试数据
    
    测试用例应覆盖:
    - 正常流程
    - 边界条件
    - 异常情况
    - 性能测试（如适用）
    
    测试用例:
    """
    
    prompt = PromptTemplate(
        input_variables=["business_requirement", "improved_code"],
        template=prompt_template
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="test_cases",
        verbose=True
    ) 