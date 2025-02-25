from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def create_code_improvement_chain(llm):
    """
    创建代码改进Chain
    
    Args:
        llm: 大语言模型实例
        
    Returns:
        LLMChain: 代码改进Chain
    """
    prompt_template = """
    你是一位专业的软件工程师，请根据以下信息改进代码。
    
    业务需求:
    {business_requirement}
    
    原始代码:
    {generated_code}
    
    代码评审结果:
    {code_review}
    
    请根据代码评审结果对原始代码进行改进，生成新版本的代码。新代码应该:
    1. 解决代码评审中指出的所有问题
    2. 保持代码的可读性和可维护性
    3. 确保完全满足业务需求
    4. 遵循Python最佳实践
    
    请只输出改进后的代码，不要包含任何解释。
    
    改进后的代码:
    """
    
    prompt = PromptTemplate(
        input_variables=["business_requirement", "generated_code", "code_review"],
        template=prompt_template
    )
    
    return LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="improved_code",
        verbose=True
    ) 