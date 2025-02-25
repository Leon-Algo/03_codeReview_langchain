from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_code_review_chain(llm):
    """
    创建代码评审Chain
    
    Args:
        llm: 大语言模型实例
        
    Returns:
        LLMChain: 代码评审Chain
    """
    prompt_template = """
    你是一位经验丰富的代码评审专家，请对以下代码进行全面的代码评审。
    
    业务需求:
    {business_requirement}
    
    生成的代码:
    {generated_code}
    
    请从以下几个方面进行评审:
    1. 代码质量 - 代码是否遵循PEP 8规范，是否简洁、高效
    2. 功能完整性 - 代码是否完全满足业务需求
    3. 错误处理 - 是否有适当的错误处理机制
    4. 安全性 - 是否存在安全隐患
    5. 可维护性 - 代码是否易于理解和维护
    6. 性能 - 是否有性能优化的空间
    
    请提供具体的改进建议，包括代码中需要修改的部分。
    
    代码评审结果:
    """
    
    prompt = PromptTemplate(
        input_variables=["business_requirement", "generated_code"],
        template=prompt_template
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="code_review",
        verbose=True
    ) 