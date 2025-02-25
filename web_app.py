import os
import streamlit as st
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

def main():
    st.set_page_config(
        page_title="代码生成器",
        page_icon="💻",
        layout="wide"
    )
    
    st.title("基于LangChain的高质量代码生成器")
    st.markdown("根据业务需求生成高质量代码、代码评审、测试用例和单元测试")
    
    # 侧边栏
    with st.sidebar:
        st.header("选择要执行的步骤")
        generate_code_step = st.checkbox("1. 生成代码", value=True)
        review_code_step = st.checkbox("2. 代码评审", value=True)
        improve_code_step = st.checkbox("3. 改进代码", value=True)
        generate_test_cases_step = st.checkbox("4. 生成测试用例", value=True)
        generate_unit_tests_step = st.checkbox("5. 生成单元测试", value=True)
    
    # 主界面
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("输入")
        
        # 业务需求输入
        business_requirement = st.text_area(
            "业务需求",
            height=200,
            placeholder="请输入您的业务需求..."
        )
        
        # 已有代码输入（可选）
        existing_code = st.text_area(
            "已有代码（可选）",
            height=200,
            placeholder="如果您已有代码，请在此粘贴..."
        )
        
        # 提交按钮
        if st.button("生成"):
            if not business_requirement:
                st.error("请输入业务需求")
            else:
                with st.spinner("处理中..."):
                    # 初始化会话状态
                    if "generated_code" not in st.session_state:
                        st.session_state.generated_code = None
                    if "code_review" not in st.session_state:
                        st.session_state.code_review = None
                    if "improved_code" not in st.session_state:
                        st.session_state.improved_code = None
                    if "test_cases" not in st.session_state:
                        st.session_state.test_cases = None
                    if "unit_tests" not in st.session_state:
                        st.session_state.unit_tests = None
                    
                    # 步骤1: 生成代码
                    if generate_code_step:
                        if existing_code:
                            st.session_state.generated_code = existing_code
                        else:
                            with st.spinner("生成代码中..."):
                                result = generate_code(business_requirement)
                                st.session_state.generated_code = result["generated_code"]
                    
                    # 步骤2: 代码评审
                    if review_code_step and st.session_state.generated_code:
                        with st.spinner("代码评审中..."):
                            result = review_code(business_requirement, st.session_state.generated_code)
                            st.session_state.code_review = result["code_review"]
                    
                    # 步骤3: 改进代码
                    if improve_code_step and st.session_state.generated_code and st.session_state.code_review:
                        with st.spinner("改进代码中..."):
                            result = improve_code(
                                business_requirement,
                                st.session_state.generated_code,
                                st.session_state.code_review
                            )
                            st.session_state.improved_code = result["improved_code"]
                    
                    # 步骤4: 生成测试用例
                    if generate_test_cases_step and (st.session_state.improved_code or st.session_state.generated_code):
                        with st.spinner("生成测试用例中..."):
                            code_to_use = st.session_state.improved_code or st.session_state.generated_code
                            result = generate_test_cases(business_requirement, code_to_use)
                            st.session_state.test_cases = result["test_cases"]
                    
                    # 步骤5: 生成单元测试
                    if generate_unit_tests_step and (st.session_state.improved_code or st.session_state.generated_code) and st.session_state.test_cases:
                        with st.spinner("生成单元测试中..."):
                            code_to_use = st.session_state.improved_code or st.session_state.generated_code
                            result = generate_unit_tests(
                                business_requirement,
                                code_to_use,
                                st.session_state.test_cases
                            )
                            st.session_state.unit_tests = result["unit_tests"]
    
    with col2:
        st.header("输出")
        
        # 创建选项卡
        tabs = st.tabs(["生成的代码", "代码评审", "改进后的代码", "测试用例", "单元测试"])
        
        # 生成的代码
        with tabs[0]:
            if "generated_code" in st.session_state and st.session_state.generated_code:
                st.code(st.session_state.generated_code, language="python")
                
                # 下载按钮
                st.download_button(
                    label="下载生成的代码",
                    data=st.session_state.generated_code,
                    file_name="generated_code.py",
                    mime="text/plain"
                )
            else:
                st.info("生成的代码将显示在这里")
        
        # 代码评审
        with tabs[1]:
            if "code_review" in st.session_state and st.session_state.code_review:
                st.markdown(st.session_state.code_review)
                
                # 下载按钮
                st.download_button(
                    label="下载代码评审",
                    data=st.session_state.code_review,
                    file_name="code_review.md",
                    mime="text/plain"
                )
            else:
                st.info("代码评审将显示在这里")
        
        # 改进后的代码
        with tabs[2]:
            if "improved_code" in st.session_state and st.session_state.improved_code:
                st.code(st.session_state.improved_code, language="python")
                
                # 下载按钮
                st.download_button(
                    label="下载改进后的代码",
                    data=st.session_state.improved_code,
                    file_name="improved_code.py",
                    mime="text/plain"
                )
            else:
                st.info("改进后的代码将显示在这里")
        
        # 测试用例
        with tabs[3]:
            if "test_cases" in st.session_state and st.session_state.test_cases:
                st.markdown(st.session_state.test_cases)
                
                # 下载按钮
                st.download_button(
                    label="下载测试用例",
                    data=st.session_state.test_cases,
                    file_name="test_cases.md",
                    mime="text/plain"
                )
                
                # 编辑测试用例
                edited_test_cases = st.text_area(
                    "编辑测试用例",
                    value=st.session_state.test_cases,
                    height=300
                )
                
                if edited_test_cases != st.session_state.test_cases:
                    st.session_state.test_cases = edited_test_cases
                    st.success("测试用例已更新")
            else:
                st.info("测试用例将显示在这里")
        
        # 单元测试
        with tabs[4]:
            if "unit_tests" in st.session_state and st.session_state.unit_tests:
                st.code(st.session_state.unit_tests, language="python")
                
                # 下载按钮
                st.download_button(
                    label="下载单元测试",
                    data=st.session_state.unit_tests,
                    file_name="test_code.py",
                    mime="text/plain"
                )
            else:
                st.info("单元测试将显示在这里")

if __name__ == "__main__":
    main() 