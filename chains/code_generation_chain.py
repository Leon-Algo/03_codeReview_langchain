from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_code_generation_chain(llm):
    """
    创建代码生成Chain
    
    Args:
        llm: 大语言模型实例
        
    Returns:
        LLMChain: 代码生成Chain
    """
    prompt_template = """
    你是一位专业的软件工程师，请根据以下业务需求生成高质量的Python函数代码。
    
    业务需求:
    {business_requirement}
    
    请生成符合以下标准的代码:
    1. 代码应该遵循PEP 8规范
    2. 包含详细的文档字符串
    3. 包含适当的错误处理
    4. 代码应该简洁、高效且易于理解
    5. 使用合适的设计模式和最佳实践
    
    请只输出代码，不要包含任何解释。
    
    生成的代码:
    """
    
    prompt = PromptTemplate(
        input_variables=["business_requirement"],
        template=prompt_template
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="generated_code",
        verbose=True
    ) 