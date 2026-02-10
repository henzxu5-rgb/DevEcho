"""
DevEcho: 开发者反馈智能转化 Agent
将零散的开发者反馈（Bug、建议、吐槽）转化为标准化的产品需求文档（PRD）
"""

import streamlit as st
import openai
import os
from typing import Dict, Any

# 页面配置
st.set_page_config(
    page_title="DevEcho: 开发者反馈智能转化 Agent",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("DevEcho: 开发者反馈智能转化 Agent")
st.markdown("---")

# 初始化session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prd_result" not in st.session_state:
    st.session_state.prd_result = None
if "agent_thinking" not in st.session_state:
    st.session_state.agent_thinking = ""
if "example_feedback" not in st.session_state:
    st.session_state.example_feedback = ""

# ========== 侧边栏配置 ==========
with st.sidebar:
    st.header("⚙️ 配置")

    # API配置
    st.subheader("API 配置")

    # API提供商选择
    api_provider = st.selectbox(
        "选择API提供商",
        ["OpenAI", "DeepSeek"],
        help="DeepSeek使用OpenAI兼容的API格式"
    )

    # API密钥输入 - 支持环境变量、Secrets和手动输入
    default_api_key = ""

    # 尝试从Streamlit Secrets获取
    try:
        if api_provider == "OpenAI" and "OPENAI_API_KEY" in st.secrets:
            default_api_key = st.secrets["OPENAI_API_KEY"]
        elif api_provider == "DeepSeek" and "DEEPSEEK_API_KEY" in st.secrets:
            default_api_key = st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        pass  # 如果没有配置secrets，继续使用环境变量

    # 如果Secrets中没有，尝试从环境变量获取
    if not default_api_key:
        if api_provider == "OpenAI":
            default_api_key = os.environ.get("OPENAI_API_KEY", "")
        elif api_provider == "DeepSeek":
            default_api_key = os.environ.get("DEEPSEEK_API_KEY", "")

    # 显示输入框，预填充从Secrets或环境变量获取的值
    api_key = st.text_input(
        f"{api_provider} API Key",
        value=default_api_key,
        type="password",
        help="输入您的API密钥。也可以通过在环境变量或Secrets中设置来自动加载。"
    )

    # 显示提示信息
    if default_api_key:
        source = "环境变量"
        try:
            # 检查是否来自Secrets
            if api_provider == "OpenAI" and "OPENAI_API_KEY" in st.secrets:
                source = "Secrets"
            elif api_provider == "DeepSeek" and "DEEPSEEK_API_KEY" in st.secrets:
                source = "Secrets"
        except Exception:
            pass
        st.caption(f"✅ API Key已从{source}自动加载。您可以直接使用或修改。")

    # 模型选择
    if api_provider == "OpenAI":
        model_options = ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"]
        default_model = "gpt-4-turbo-preview"
    else:  # DeepSeek
        model_options = ["deepseek-chat", "deepseek-coder"]
        default_model = "deepseek-chat"

    model = st.selectbox(
        "选择模型",
        model_options,
        index=model_options.index(default_model) if default_model in model_options else 0
    )

    # 核心参数调节
    st.subheader("核心参数调节")

    temperature = st.slider(
        "创造力 (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="值越高，回答越有创造性；值越低，回答越确定"
    )

    analysis_depth = st.toggle(
        "深度分析模式",
        value=True,
        help="启用后，Agent会进行更详细的分析和拆解"
    )

    # 示例反馈
    st.markdown("---")
    st.subheader("📋 示例反馈")

    example_choice = st.selectbox(
        "选择示例反馈",
        ["无", "文档问题", "API错误", "功能请求", "性能问题", "复杂反馈"],
        help="选择示例快速测试"
    )

    # 示例反馈内容
    examples = {
        "无": "",
        "文档问题": "这个SDK的文档太乱了，根本找不到怎么配置OAuth。示例代码也是老的，跟最新API不兼容。",
        "API错误": "每次调用/users端点都返回500错误，日志里只看到'Internal Server Error'，没有具体信息。",
        "功能请求": "如果能加个批量操作的功能就好了，现在一个一个点太麻烦了。比如批量删除用户、批量修改权限。",
        "性能问题": "页面加载太慢了，尤其是用户列表，有1000个用户时要等10秒才能显示。",
        "复杂反馈": "我们在生产环境遇到两个问题：1) 上传大文件经常超时 2) WebSocket连接不稳定，经常断连 3) 文档里没说清楚怎么配置HTTPS"
    }

    # 如果选择了示例，将其填充到主输入框
    if example_choice != "无" and st.button("使用此示例", type="secondary", use_container_width=True):
        # 这里需要使用session state来传递值到主输入框
        # 由于Streamlit的限制，我们无法直接设置text_area的值
        # 但我们可以使用session state来存储示例，然后在主输入框中显示
        st.session_state.example_feedback = examples[example_choice]
        st.rerun()  # 重新运行以更新输入框

    # 辅助信息
    st.markdown("---")
    st.caption("💡 提示")
    st.caption("1. 将GitHub Issue、Discord讨论或微信群反馈粘贴到主界面")
    st.caption("2. 点击'开始智能解析'按钮")
    st.caption("3. 查看Agent的思考过程和生成的PRD")

# ========== 主界面 ==========

# 输入区域
st.header("📥 输入反馈内容")
feedback_input = st.text_area(
    "请粘贴来自 GitHub Issue、Discord 或微信群的原始反馈...",
    height=200,
    value=st.session_state.example_feedback,
    placeholder="例如：\n"
    "'这个SDK的文档太乱了，根本找不到怎么配置OAuth。'\n"
    "'每次调用API都返回500错误，日志里看不到具体原因。'\n"
    "'如果能加个批量操作的功能就好了，现在一个一个点太麻烦了。'",
    help="可以粘贴多条反馈，Agent会自动识别和分类"
)

# 解析按钮
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    parse_button = st.button(
        "🚀 开始智能解析",
        type="primary",
        use_container_width=True
    )

# ========== Agent逻辑 ==========
def analyze_feedback(feedback: str, api_key: str, model: str, temperature: float, deep_analysis: bool, api_provider: str) -> Dict[str, Any]:
    """分析开发者反馈并生成PRD"""

    # 检查输入有效性
    if not feedback or len(feedback.strip()) < 10:
        return {
            "error": "输入内容太短或为空。请提供更详细的反馈，以便Agent进行有效分析。",
            "thinking": "检测到输入内容过短，无法进行有意义的分析。"
        }

    # 构建系统提示词
    system_prompt = """你是一位资深的技术产品经理和全栈工程师，专门处理开发者反馈。你的核心能力是从混乱、零散、情绪化的反馈中提取技术本质和产品需求。

你的任务是：将原始开发者反馈（GitHub Issues、Discord讨论、微信群吐槽等）转化为**可直接用于开发团队**的标准产品需求文档（PRD）。

## 分析框架（请严格遵循）：

### 第一阶段：信息提取
1. **上下文识别**：识别反馈的来源平台、技术栈、使用场景
2. **情感分析**：判断用户情绪（沮丧、困惑、期待、赞赏）
3. **事实提取**：分离事实描述（错误代码、操作步骤）与主观评价

### 第二阶段：问题结构化
4. **问题分类**：Bug（前端/后端/API/文档）、功能请求、体验优化、性能问题
5. **影响评估**：影响用户范围（单个用户/团队/全部用户）、频率（偶尔/经常/必现）
6. **根本原因推测**：基于技术经验推测可能的技术原因

### 第三阶段：需求转化
7. **PRD结构**：按照标准PRD模板组织
8. **技术方案**：提供具体、可落地的技术实现思路
9. **优先级评估**：P0（阻塞开发）、P1（核心功能缺陷）、P2（重要优化）、P3（锦上添花）

## 输出格式要求（必须包含以下部分）：

### 需求名称
【简明扼要的需求标题】

### 用户痛点
- 用户身份：（开发者、测试、运维等）
- 使用场景：（具体操作流程）
- 当前问题：（详细描述问题现象）
- 期望结果：（用户希望达到的效果）

### 优先级评估
- 优先级：（P0/P1/P2/P3）
- 影响范围：（受影响的用户比例）
- 紧急程度：（需要多快解决）
- 解决成本：（开发工作量预估）

### 功能描述
- 功能概要：（一句话说明）
- 详细需求：（分点描述具体需求）
- 交互流程：（用户操作步骤）
- 边界条件：（特殊场景处理）

### 验收标准
- 功能验收：（功能是否正常）
- 性能验收：（响应时间、资源占用）
- 兼容性验收：（不同环境下的表现）

### 技术实现方案
- 架构影响：（需要修改的模块）
- API设计：（新增/修改的API接口）
- 数据变更：（数据库表结构变更）
- 前端改动：（UI/交互修改）
- 测试建议：（测试重点和场景）

### 风险与依赖
- 技术风险：（可能遇到的技术难题）
- 依赖项：（需要其他团队配合的部分）
- 回滚方案：（如果出问题如何恢复）

## 特别注意：
1. 保持技术专业性，避免产品经理的模糊表述
2. 给出的技术方案要具体到模块/函数层面
3. 考虑实际开发团队的落地可行性
4. 如果是多个反馈，请分别分析再给出综合方案

请现在开始分析。"""

    # 用户提示词（根据深度分析模式调整）
    if deep_analysis:
        user_prompt = f"""请分析以下开发者反馈，并严格按照要求输出。

## 反馈内容：
```
{feedback}
```

## 输出要求：
请分为两部分输出：

### 第一部分：思考过程（用于展示给用户看）
请详细描述你的分析思路，包括：
1. **第一遍阅读**：整体印象，识别主要问题和次要问题
2. **第二遍阅读**：提取技术关键词、业务上下文、用户身份
3. **第三遍阅读**：关联现有系统架构，推测技术实现难度
4. **第四遍阅读**：评估优先级和影响范围
5. **第五遍阅读**：构思解决方案和权衡取舍

### 第二部分：PRD文档
请按照系统提示词中的完整格式输出PRD文档。

请确保两部分之间用"---PRD_START---"分隔，这样我们可以正确解析。"""
    else:
        user_prompt = f"""请分析以下开发者反馈，并输出PRD。

反馈内容：
```
{feedback}
```

请先简要说明分析思路（3-5句话），然后用"---PRD_START---"分隔，最后输出完整PRD。"""

    # 构建消息
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        # 配置OpenAI客户端
        client = openai.OpenAI(api_key=api_key)

        # 对于DeepSeek，需要设置base_url
        if api_provider == "DeepSeek":
            client.base_url = "https://api.deepseek.com/v1"

        # 调用API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000
        )

        # 解析响应
        result = response.choices[0].message.content

        # 分割思考过程和PRD内容
        if "---PRD_START---" in result:
            parts = result.split("---PRD_START---")
            thinking = parts[0].strip()
            prd_content = parts[1].strip() if len(parts) > 1 else result
        else:
            # 如果没有分隔符，尝试智能分割
            thinking = "Agent正在分析反馈内容..."

            # 尝试找到PRD的标题位置
            prd_markers = ["### 需求名称", "## 需求名称", "# 需求名称", "需求名称："]
            prd_content = result
            for marker in prd_markers:
                if marker in result:
                    idx = result.find(marker)
                    if idx > 0:
                        thinking = result[:idx].strip()
                        prd_content = result[idx:].strip()
                        break

        return {
            "thinking": thinking,
            "prd": prd_content,
            "error": None
        }

    except Exception as e:
        return {
            "error": f"API调用失败: {str(e)}",
            "thinking": f"遇到错误: {str(e)}"
        }

# ========== 处理按钮点击 ==========
if parse_button:
    if not api_key:
        st.error("⚠️ 请先在侧边栏输入API Key")
    elif not feedback_input:
        st.error("⚠️ 请输入反馈内容")
    else:
        with st.spinner("🔍 Agent正在分析反馈内容..."):
            result = analyze_feedback(
                feedback_input,
                api_key,
                model,
                temperature,
                analysis_depth,
                api_provider
            )

            if result["error"]:
                st.error(f"❌ {result['error']}")
                st.session_state.agent_thinking = result.get("thinking", "")
                st.session_state.prd_result = None
            else:
                st.session_state.agent_thinking = result["thinking"]
                st.session_state.prd_result = result["prd"]

        # 显示成功消息
        st.success("✅ 分析完成！")

# ========== 结果展示区 ==========

# 显示Agent思考逻辑
if st.session_state.agent_thinking:
    st.header("🤔 Agent 思考逻辑")

    # 使用st.status来显示思考过程
    with st.status("Agent分析过程", expanded=True):
        st.markdown("### 🔍 分析进度")

        # 解析思考过程，添加一些格式
        thinking_text = st.session_state.agent_thinking

        # 尝试检测思考过程中的步骤
        lines = thinking_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['第一遍', '第二遍', '第三遍', '第四遍', '第五遍', '步骤', 'step', '分析']):
                st.markdown(f"**{line}**")
            elif line.strip().startswith('-') or line.strip().startswith('*') or line.strip().startswith('•'):
                st.markdown(line)
            elif line.strip() and len(line.strip()) > 10:
                st.markdown(line)

        st.markdown("---")
        st.markdown("### ✅ 分析完成")
        st.markdown("Agent已完成思考过程，下面是详细的PRD文档。")

    # 在展开器中显示完整思考过程
    with st.expander("📝 查看完整思考过程"):
        st.markdown(st.session_state.agent_thinking)

# 显示PRD结果
if st.session_state.prd_result:
    st.header("📋 生成的PRD文档")

    # 添加下载按钮
    prd_text = st.session_state.prd_result
    st.download_button(
        label="📥 下载PRD文档",
        data=prd_text,
        file_name="devecho_prd.md",
        mime="text/markdown"
    )

    # 美化显示PRD
    st.markdown("---")

    # 使用st.markdown显示内容，确保格式正确
    with st.container():
        st.markdown(prd_text)

elif parse_button and not st.session_state.prd_result:
    # 如果点击了按钮但没有PRD结果，显示等待信息
    st.info("📝 等待生成PRD文档...")

# ========== 底部信息 ==========
st.markdown("---")
st.markdown("### 💡 使用建议")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🔍 反馈来源**")
    st.markdown("- GitHub Issues")
    st.markdown("- Discord 讨论")
    st.markdown("- Slack/微信群聊")

with col2:
    st.markdown("**🎯 最佳实践**")
    st.markdown("- 提供具体的使用场景")
    st.markdown("- 包含错误信息或截图")
    st.markdown("- 描述期望的解决方案")

with col3:
    st.markdown("**⚡ 输出价值**")
    st.markdown("- 标准化需求文档")
    st.markdown("- 优先级评估")
    st.markdown("- 技术实现建议")

# ========== 调试信息（开发时可用） ==========
if st.sidebar.checkbox("显示调试信息", False):
    st.sidebar.write("### 调试信息")
    st.sidebar.write(f"API提供商: {api_provider}")
    st.sidebar.write(f"模型: {model}")
    st.sidebar.write(f"Temperature: {temperature}")
    st.sidebar.write(f"深度分析: {analysis_depth}")
    st.sidebar.write(f"输入长度: {len(feedback_input) if feedback_input else 0}")