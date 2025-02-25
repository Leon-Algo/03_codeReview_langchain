from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_unit_test_generation_chain(llm):
    """
    创建单元测试生成Chain
    
    Args:
        llm: 大语言模型实例
        
    Returns:
        LLMChain: 单元测试生成Chain
    """
    prompt_template = """
    你是一位测试驱动开发专家，请根据以下信息生成Python单元测试代码。
    
    业务需求:
    {business_requirement}
    
    改进后的代码:
    {improved_code}
    
    测试用例:
    {test_cases}
    
    请使用pytest框架生成单元测试代码，确保:
    1. 测试覆盖所有测试用例中描述的场景
    2. 包含适当的断言
    3. 使用合适的测试夹具（fixtures）
    4. 测试代码清晰易读
    5. 包含必要的注释
    
    请只输出单元测试代码，不要包含任何解释。
    
    单元测试代码:
    """
    
    prompt = PromptTemplate(
        input_variables=["business_requirement", "improved_code", "test_cases"],
        template=prompt_template
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="unit_tests",
        verbose=True
    ) 