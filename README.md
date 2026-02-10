# DevEcho: 开发者反馈智能转化 Agent

一个基于 Streamlit 的 AI Agent 原型工具，将零散的开发者反馈（Bug、建议、吐槽）转化为标准化的产品需求文档（PRD）。

## ✨ 核心功能

- **智能反馈解析**：从混乱的开发者反馈中提取技术关键点
- **专业PRD生成**：输出标准化的产品需求文档，包含技术实现方案
- **思考过程可视化**：展示Agent如何拆解反馈、识别意图
- **多平台支持**：处理GitHub Issues、Discord讨论、微信群聊等来源的反馈
- **双AI提供商**：支持OpenAI和DeepSeek API

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
streamlit run app.py
```

### 3. 配置使用
1. 在侧边栏输入API Key（OpenAI或DeepSeek）
2. 选择模型和调整参数
3. 粘贴开发者反馈到主输入框
4. 点击"开始智能解析"
5. 查看Agent思考过程和生成的PRD

## ☁️ 部署到 Streamlit Cloud

### 方法一：一键部署（推荐）
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

1. Fork 本仓库到您的 GitHub 账户
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 点击 "New app" → 选择本仓库
4. 配置以下设置：
   - **Main file path**: `app.py`
   - **Python version**: 3.10 (自动检测)
5. 点击 "Deploy"

### 方法二：手动部署
```bash
# 克隆仓库
git clone https://github.com/your-username/DevEcho.git
cd DevEcho

# 部署到 Streamlit Cloud
# 通过 Web 界面或 CLI 工具部署
```

### 配置 Secrets（API 密钥安全存储）
在 Streamlit Cloud 上，通过以下方式安全设置 API 密钥：

1. **在线编辑器**：App → Settings → Secrets
2. **CLI 工具**：使用 `streamlit secrets` 命令
3. **文件上传**：上传 `.streamlit/secrets.toml`

#### secrets.toml 格式：
```toml
# OpenAI
OPENAI_API_KEY = "sk-..."

# DeepSeek
DEEPSEEK_API_KEY = "sk-..."
```

### 环境变量配置
也可以在 Streamlit Cloud 的 "Settings" → "Secrets" 中设置环境变量。

### 注意事项
- ⚠️ **不要**将包含密钥的 `secrets.toml` 提交到 Git
- ✅ 使用 `.gitignore` 保护敏感文件
- 🔒 Streamlit Cloud 提供安全的 Secrets 管理
- 🌐 应用将获得一个永久的公共 URL

## 🎯 使用场景

### 场景1：GitHub Issues处理
将杂乱的Issue描述转化为清晰的开发任务：
```
"页面加载太慢了，尤其是用户列表，有1000个用户时要等10秒才能显示。"
↓
✅ 生成包含性能优化方案的PRD
```

### 场景2：Discord社区反馈
整合多个用户的吐槽和建议：
```
"A说：文档找不到OAuth配置
B说：API返回500错误没具体信息
C说：需要批量操作功能"
↓
✅ 生成综合PRD，包含三个需求的优先级评估
```

### 场景3：内部开发团队反馈
将开发者的技术建议产品化：
```
"如果能优化数据库查询，用户列表加载能快3倍。
当前的全表扫描太浪费资源了。"
↓
✅ 生成技术方案详细的PRD，包含SQL优化建议
```

## 🛠️ 技术架构

### 前端 (Streamlit)
- **侧边栏**：API配置、参数调节、示例库
- **主界面**：反馈输入、解析按钮、结果展示
- **状态管理**：Session状态保持用户体验

### AI Agent核心
```python
# 三步分析框架
1. 信息提取 → 2. 问题结构化 → 3. 需求转化

# 专业提示词工程
- 技术导向的系统提示词
- 结构化输出要求
- 思考过程与PRD分离
```

### API集成
- **OpenAI兼容**：支持GPT-4、GPT-3.5
- **DeepSeek集成**：国内用户友好
- **参数透传**：温度、深度分析等配置

## 📋 PRD输出格式

生成的PRD包含以下标准部分：

### 需求名称
简明扼要的需求标题

### 用户痛点
- 用户身份、使用场景、当前问题、期望结果

### 优先级评估
- P0/P1/P2/P3分级
- 影响范围、紧急程度、解决成本

### 功能描述
- 功能概要、详细需求、交互流程、边界条件

### 验收标准
- 功能验收、性能验收、兼容性验收

### 技术实现方案
- 架构影响、API设计、数据变更、前端改动、测试建议

### 风险与依赖
- 技术风险、依赖项、回滚方案

## ⚙️ 配置选项

### API设置
- **提供商**：OpenAI / DeepSeek
- **模型**：GPT-4 Turbo、DeepSeek Chat等
- **API Key**：本地安全存储

### 参数调节
- **创造力**：控制Agent的创新程度 (0.0-1.0)
- **深度分析**：启用更详细的分析和拆解

### 示例库
- 文档问题、API错误、功能请求、性能问题、复杂反馈
- 一键填充测试

## 🤝 贡献指南

欢迎提交Issue和Pull Request改进项目：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的Python Web框架
- [OpenAI](https://openai.com/) - GPT API服务
- [DeepSeek](https://www.deepseek.com/) - 国产AI大模型

---

**DevEcho** - 让开发者的声音被听见，让反馈转化为行动 🚀