# AI Agents in Action Codex中文翻译版 · 第1章

## 第1章 代理及其世界

代理（agent）在机器学习和人工智能领域并不是新概念。在强化学习中，代理指的是能够主动决策并学习的智能体；在其他领域中，它更像是代替人类执行某项工作的自动化程序或软件。本章从多个角度拆解代理体系，帮助你理解它们如何被定义、构成与运作。

### 本章内容
- 定义代理这一概念
- 区分代理所依赖的各类组成系统
- 分析“代理时代”兴起的原因
- 拆解 AI 接口的内部结构
- 导览整个代理生态版图

## 1.1 定义代理

可以查阅任何在线词典来了解“agent”的含义。例如，《韦氏词典》给出了如下定义：
- 能够行动或施加力量的实体
- 能够产生或促成某种效果的事物
- 由指挥智能用来实现结果的工具或手段

本书构建强大代理时所使用的“代理”即源自这一词典定义；因此，我们也把“assistant（助手）”视为“agent”的同义词，OpenAI 的 GPT Assistants 等工具同样属于 AI 代理的范畴。之所以避免直接使用“agent”一词，是因为在机器学习的历史中，代理往往意味着自我决策且具备高度自主性。

图 1.1 展示了用户与大型语言模型（LLM）交互的四种典型情境：直接交互、代理/助手代理、代理/助手，以及完全自主代理。它们的区别如下。
- **直接与 LLM 交互**：例如早期的 ChatGPT，用户直接向模型发问，如“请解释代理的定义”，模型便直接作答，不存在任何中间代理。
- **代理/助手代理**：例如通过 ChatGPT 调用 DALL·E 3 生成图像。LLM 会拦截请求并按照任务特性重新组织提示语，例如把“请给我一幅女特工的插画”转换成更适合图像模型的描述。这类代理非常适合帮助用户完成不熟悉的任务或与不同模型对接。
- **代理/助手**：若使用过 ChatGPT 插件或 GPT 助手，就属于这种情形。LLM 事先了解插件/函数的存在，必要时会准备调用它们。在真正执行前，LLM 会征询用户许可；获批后再调用插件，把结果包装成自然语言回复。
- **自主代理**：代理会解释用户需求、制定计划并找出决策点，随后独立执行步骤并做出决定。它可能会在里程碑节点向用户征求反馈，但通常拥有较大的探索和学习空间。由于需要放权，自主代理也带来更多伦理与安全风险。

图 1.1 还用场景化对话说明了这四种模式：从直接让 LLM 解释概念，到由代理重写提示、调用气象 API 获取卡尔加里气温，乃至完全由自主代理筛选邮件、汇报最重要的五封邮件。可以看到，随着代理能力增强，代理在流程中的角色会从“代理用户使用工具”逐渐过渡到“在决策步骤中自主行动”。

为了处理更复杂的问题，往往需要把代理划分为不同的角色或人物设定，每个角色只处理特定任务并具备专门的工具与知识。多个角色协同工作的系统被称为多代理系统。图 1.2 例举了一个包含三名代理的多代理系统：一个控制器（或代理代理）直接对接用户，两个工作代理分别扮演编码者与测试者。控制器负责与用户交互，也可以在获得授权后代替用户运行代码；编码者编写功能，测试者生成单元测试，两者会不断交流并迭代，直至双方对结果满意后提交给用户。

多代理系统既可以完全自主运行，也可以在人工反馈的指导下工作。它与单代理的能力类似但通常被放大：可以并行处理多项任务，彼此交叉评审，从而减少错误。下一节将继续拆解单个代理本身所包含的关键部件，包括人物设定、可用动作、记忆、推理与规划等。

## 1.2 理解代理的组成系统

代理往往由多个组件系统构成，这些组件是代理为了完成目标或任务而调用的工具，也可以用来创造新的任务。它们既可以是简单模块，也可以是复杂系统，大体可分为五类，如图 1.3 所示：人物设定（Profile & Persona）、动作与工具、记忆与知识、推理与评估、规划与反馈。人物设定位于核心，其余系统都围绕着它展开，每个组件还可以细分出不同类型与用途。

> **提示**：代理或助手的“档案”由多个元素组成，其中包括“人物设定”。可以把档案理解为描述代理要完成什么工作、需要哪些工具的一整套说明，而人物设定则偏向角色/系统提示的描述。

图 1.4 深入展示了如何构建代理档案：我们会学习如何明确地定义人物角色及其特征，为代理提供背景和人口统计信息，例如身份、年龄、性别或专业背景；也会比较纯手工、LLM 协助以及依赖数据/进化算法自动生成档案的不同方式，探索基于数据或其他新颖手段构建角色设定的技巧。

图 1.5 则聚焦在动作与工具的组件，强调三类要点。
- **动作目标**：需要搞清楚动作是为了完成任务、探索环境，还是与他者沟通，以便设定清晰的目标。
- **动作空间与影响**：需要了解动作如何影响任务结果、外部环境以及代理的内部状态或自我认知，这有助于做出高效决策。
- **动作生成方式**：动作既可以由人手动指定，也可以从记忆中检索，或按照预定义计划生成。熟悉这些方式能够帮助我们塑造代理行为、提升学习效果。

图 1.6 进一步说明了知识与记忆组件。代理会结合相关背景信息来标注上下文，同时尽量减少 token 消耗。记忆/知识结构既可以统一，也可以采用混合结构，以适配不同的检索方式。其数据格式非常多样：既可以是文本（例如 PDF）、也可以是关系/对象/文档数据库，或者使用向量嵌入以便进行语义相似度搜索，甚至只是简单的列表。代理可以通过增强、语义抽取或压缩等检索操作，把最合适的信息注入上下文。

图 1.7 强调了推理与评估组件。研究与实践都表明 LLM/代理具备一定的推理能力。推理部分可以使用零样本、单样本、少样本、Chain of Thought（逐步思考）、Tree of Thought（思维树）、Skeleton of Thought（骨架式思考）等提示方式，帮助代理在内部“过一遍”任务。评估部分则让代理能够对过程和结果进行自我反思，例如使用自洽性校验或提示链等策略。

图 1.8 展示了规划与反馈组件，它负责组织任务，帮助代理实现更高层级的目标，大致可以分为两类：
- **无反馈规划**：完全自主的代理，自己制定并执行计划，可使用基础规划、顺序规划或结合自动推理和工具使用。
- **有反馈规划**：依据不同来源的输入来监控并调整计划，这些来源可能是环境变化、人工回馈，或者其他 LLM 给出的自适应建设性反馈。

在规划过程中，代理可能采用单路径推理（按部就班完成任务）、序列式推理，或多路径推理（同时探索多种策略并保存高效做法以备后续使用）。外部规划器（可以是代码或其他代理系统）也能参与协作。

无论是代理/助手代理、常规代理还是自主代理，都可能组合使用这些组件。即便不是完全自主的系统，规划能力也能带来显著价值。

## 1.3 代理时代为何崛起

AI 代理和助手迅速从研究领域的热门议题跃迁到主流软件开发实践。工具与平台层出不穷，用以构建并增强代理，对外界而言似乎只是为了抬高某项炫酷技术的价值。但在 ChatGPT 发布后的头几个月里，人们确实发现了提示工程的重要性：通过不断尝试各种提示技巧和模式，可以获得更稳定、更优质的回答。然而，大家也意识到提示工程的能力终究有限。

提示工程仍是直接与 ChatGPT 等 LLM 沟通的好方法，但它通常需要多轮迭代与反思才能达到理想结果。早期的 AutoGPT 等代理系统就是在这样的背景下诞生的，并迅速吸引了社区关注。

图 1.9 展示了 AutoGPT 的原始设计。该自主代理会先从用户目标中推导出一系列任务，再按步骤执行。每完成一轮任务，就会重新评估目标是否达成；若未完成，代理会依据新信息或人工反馈重新规划步骤并更新计划。代理也可以被配置为每次执行任务前都征询一次许可，或每完成若干任务再统一确认。

AutoGPT 首次证明了“规划 + 迭代”在 LLM 中的威力。随后，大量代理系统与框架在社区出现，纷纷采用类似的规划与任务迭代机制。普遍观点认为，对于复杂、多面向的目标，规划、迭代与重复是让 LLM 取得成功的最佳方式。

不过，要让自主代理真正落地，必须信任它的决策过程、护栏/评估机制以及目标定义。这种信任需要时间去建立，因为我们尚未完全理解自主代理的能力边界。

> **提示**：通用人工智能（AGI）通常被定义为可以学习并完成任意人类任务的智能。许多从业者认为，基于自主代理系统的 AGI 是可以达成的目标。

也因此，目前大多数主流、可用于生产的代理工具并非完全自主，但它们仍然可以显著简化使用 GPT（LLM）执行任务的流程。本书将在后续章节继续探讨不同代理形态的实际应用。

## 1.4 拆解 AI 接口

代理范式不仅改变了我们与 LLM 协作的方式，也被视作软件开发与数据处理方式的根本转变。未来的软件和数据系统不再只依赖传统的图形界面（UI）、编程接口（API）或 SQL 等专用查询语言，而是要原生支持自然语言交互。

图 1.10 展示了这种新体系的高层视图，以及 AI 代理所扮演的角色。数据、软件与应用都会适配语义/自然语言接口，代理可以借助这些接口获取数据、与应用互动，甚至与其他代理沟通。这意味着我们与软件的互动方式正转向“自然语言优先”。

所谓 **AI 接口**，本质上是一组函数、工具与数据层，通过自然语言对外暴露服务。过去常用“语义接口”来描述类似方案，但“semantic”一词语义广泛、容易混淆，因此本书统一使用“AI 接口”这一术语。构建 AI 接口可以让代理更可靠地消费这些服务与数据，提升任务完成的准确率，也能打造更值得信赖、更加自主的应用。虽然并非所有软件与数据都适合用 AI 接口包装，但在大量场景中它会成为主流。

图 1.10 还给出了一个典型流程：用户只需以自然语言提出“请生成上一年度销售额的报告”，代理便会
1. 规划并拆解任务（收集数据、标注数据、格式化并生成可视化、呈现报告）；
2. 通过 GPT 数据/函数层以自然语言查询数据库、调用语义函数；
3. 视需要调用外部工具或其他代理（例如自动生成图表的代码）；
4. 最终以自然语言向用户呈现结果。
整个过程中的通信都可以用自然语言完成。

## 1.5 穿越代理生态

GPT 代理彻底改变了用户与开发者处理信息、构建软件和访问数据的方式。几乎每天都会在 GitHub 或论文中出现新的代理框架、组件或接口。对于刚接触代理系统的人来说，要理清它们的关系与用法既庞杂又令人望而生畏。本书后续章节会循序渐进带你穿越这一生态。

## 本章小结

- 代理是一种能够行动、施加力量、产生效果或作为达成结果之工具的实体；在 AI 语境中，它负责自动化地与 LLM 交互。
- “助手”与“代理”同义，涵盖了 OpenAI 的 GPT Assistants 等工具。
- 自主代理能够独立决策，因此与非自主代理的区分至关重要。
- LLM 交互主要有四种：直接交互、代理/助手代理、代理/助手，以及自主代理。
- 多代理系统由多个代理档案协同工作，通常由代理代理统一协调，以完成复杂任务。
- 代理的核心组件包括档案/人物设定、动作、知识/记忆、推理/评估，以及规划/反馈。
- 档案与人物设定会指导代理如何完成任务、如何回答以及其他细节，通常包含背景与人口统计信息。
- 代理可以通过手动指定、记忆回溯或遵循既定计划来生成动作并调用工具。
- 代理依赖多样的知识与记忆结构来优化上下文并减少 token 使用，数据形式可以是文档、数据库或嵌入等。
- 推理与评估系统让代理能够思考并检验解决方案，可结合零样本/单样本/少样本提示等模式。
- 规划与反馈组件通过单路径或多路径推理组织任务，并整合环境、人工等多种反馈。
- AI 代理正在催生新的软件开发范式，推动应用从传统界面转向自然语言接口。
- 了解上述组件与交互方式的演进，有助于我们构建单代理、多代理乃至自主代理系统。


---

# AI Agents in Action Codex中文翻译版 · 第2章

## 第2章 掌握大型语言模型的力量

“大型语言模型”（LLM）已经成为生成式 AI 的代名词。本章聚焦于这些由生成式预训练变换器（GPT）架构驱动的模型，说明它们如何被训练、为何适合作为代理的基础，并展示从 OpenAI API 到本地开源模型的完整使用链路。LLM 属于生成式模型：它们根据输入继续“生成”内容，而不是像预测或分类模型那样只给出标签。图 2.1 用直观示意对比了生成式与预测式模型。

### 本章要点
- 理解 LLM 的组成（数据、架构、训练、微调）及其在代理构建中的角色。
- 学会使用 OpenAI Python SDK 连接 GPT-4 等聊天补全模型，并掌握请求/响应细节。
- 通过 LM Studio 下载、运行并以服务形式托管开源 LLM，构建本地替代方案。
- 系统演练 Prompt Engineering——尤其是“写出清晰指令”策略下的六种战术。
- 根据性能、规模、上下文长度、训练方式等八类指标挑选最适合的模型。
- 通过实操练习巩固：API 集成、提示策略、LM Studio 部署、商用 vs 开源对比等。

LLM 由三大要素构成：训练语料（往往是 TB 到 PB 级别的数据）、模型架构（上下文窗口、token 限制、嵌入维度、参数量等）以及按用途定制的训练流程。最终的微调（fine-tuning）会让模型更契合特定领域或任务。Transformer 架构让 GPT 类模型能够扩展到数百亿参数并搭配 RLHF 等方法进行深度调优，因此尤其适合需要多轮推理、规划的聊天补全场景。本书的大多数代理示例都会使用聊天补全模型，但你也可以尝试其他模型类型，只是需要调整示例代码。

---

## 2.1 熟练掌握 OpenAI API

许多代理或助手项目都以 OpenAI API 为起点。虽然它不是行业标准，但其请求/响应模式已经成为事实规范。本节使用 OpenAI Python SDK 演示如何连接 GPT-4 系列模型，并解释消息结构、温度（temperature）和 token 计费等要点。

### 2.1.1 连接聊天补全模型

1. **准备开发环境**：按照附录 B 搭建 Python + VS Code 环境；附录 A 则介绍如何获取 OpenAI API Key。打开 `chapter_2` 目录并创建虚拟环境。
2. **安装依赖**：
   ```bash
   pip install openai python-dotenv
   ```
3. **配置密钥**：在 `.env` 中添加
   ```bash
   OPENAI_API_KEY='你的-openai-key'
   ```
4. **核心示例 `connecting.py`**（节选）：
   ```python
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   client = OpenAI(api_key=api_key)

   def ask_chatgpt(user_message):
       response = client.chat.completions.create(
           model="gpt-4-1106-preview",
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": user_message}
           ],
           temperature=0.7,
       )
       return response.choices[0].message.content
   ```
   - `load_dotenv()` 读取 `.env` 中的密钥；若缺失，抛出异常。
   - `OpenAI(api_key=...)` 创建客户端；`chat.completions.create` 负责发起请求。
   - `messages` 数组记录聊天历史，`temperature` 控制输出多样性。

调试时按 `F5`（或 VS Code 菜单 Run > Start Debugging）。若请求“法国的首都是哪里？”，模型大概率回答“巴黎”。温度越低结果越稳定（0 几乎恒定），越高越有创意；根据业务场景选择即可。

### 2.1.2 理解请求与响应

**请求结构**（Listing 2.4）重点在 `model`、`messages`、`temperature`：
- `system` 角色：定义全局规则/身份，例如“你是一名乐于助人的助手”。
- `user` 角色：代表用户输入。
- `assistant` 角色：可以回放历史回复或人为注入上下文。

一个请求的 `messages` 可以保存整段对话：
```json
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What is the capital of France?"},
  {"role": "assistant", "content": "The capital of France is Paris."},
  {"role": "user", "content": "What is an interesting fact of Paris."}
]
```
在 `message_history.py` 中多次运行可观察温度差异：`temperature=0.7` 输出多变，调为 `0.0` 则基本一致。

**响应结构**（Listing 2.6）包含：
- `choices`: 可能包含多条候选，每条都有 `message.role=assistant` 与 `content`。
- `model`: 实际使用的模型名称。
- `usage`: `prompt_tokens`（输入）、`completion_tokens`（输出）、`total_tokens` 总量。

监控 token 至关重要，较少的 token 意味着成本低、速度快、输出更集中。本书后续示例都会在此基础上扩展，接下来转向开源 LLM。

---

## 2.2 使用 LM Studio 体验开源 LLM

商用 LLM（如 GPT-4）部署简便、能力强，但需要外部 API、存在成本与数据合规顾虑。开源 LLM 正迅速追赶，配合 LM Studio 这类工具，个人电脑即可下载并运行多种模型。

### 2.2.1 安装与运行 LM Studio

1. 访问 <https://lmstudio.ai/> 下载对应平台版本（Windows/macOS/Linux）。部分版本尚在 beta，安装时可能提示附加依赖。
2. 安装并启动后，会看到如图 2.3 的主页：可浏览热门模型、搜索关键字、查看上下文长度等规格。
3. LM Studio 会自动检测硬件并给出“兼容性猜测”，帮你判断模型是否适配当前机器。
4. 选定模型后点击下载。若硬件有限，可优先尝试体量较小的聊天补全模型，但也鼓励多做实验。
5. 下载完成即可在 Chat 页面加载模型（图 2.5）。顶部下拉可切换模型，右侧可启用 GPU 加速。加载进度条完成后便能直接在界面中与模型对话。

### 2.2.2 将模型以服务形式运行

LM Studio 也能把本地模型暴露为兼容 OpenAI API 的服务：
1. 打开 Server 页，选择已下载的模型并确保 “Server Model Settings” 与之匹配（见图 2.7）。
2. 点击 **Start Server**，日志区会显示端口、推理状态等信息。
3. 示例代码 `chapter_2/lmstudio_server.py`：
   ```python
   from openai import OpenAI

   client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
   completion = client.chat.completions.create(
       model="local-model",
       messages=[
           {"role": "system", "content": "Always answer in rhymes."},
           {"role": "user", "content": "Introduce yourself."}
       ],
       temperature=0.7,
   )
   print(completion.choices[0].message)
   ```
   - 本地服务默认无需真实 API Key，`base_url` 指向 LM Studio。
   - 可随意修改系统/用户提示以验证本地推理效果。

配置不当时（例如服务设置与模型不符）会导致连接失败，记得核对后重启。至此，你既能调用商用 API，也能在本地运行模型，为后续的提示工程与代理开发提供多种选项。

---

## 2.3 用提示工程驱动 LLM

“提示”（prompt）是发送给 LLM 的文本指令，而“提示工程”（prompt engineering）旨在系统化地构造更高质量的指令。OpenAI 总结了若干策略（图 2.8），涵盖清晰指令、引用资料、调用外部工具、拆解复杂任务、给予思考时间、系统化回归测试等。本章专注于最基础也最通用的策略：**Write Clear Instructions（写出清晰指令）**，并实作六种常见战术（图 2.9）。

示例代码位于 `prompt_engineering.py`：
1. 扫描 `prompts/` 目录下的 JSON Lines 文件，把每种战术对应的提示列出供选择。
2. 读取所选文件，将提示转为 `messages` 并送入 LLM。
3. 打印请求与回复，便于观察差异。脚本还预留了连接本地 LLM 的代码，可与前述 LM Studio 服务配合使用。

### 2.3.1 编写细致的提问

`tactics/detailed_queries.jsonl` 展示“模糊 vs 详细”两种提问方式：
- 仅问 “What is an agent?” 得到泛泛定义。
- 详细说明 “What is a GPT Agent? Please give me 3 examples...” 则能获得更有针对性的解释与实例。

原则：尽量提供与任务高度相关的上下文，必要时直接要求示例或输出格式。

### 2.3.2 设定人物角色（Persona）

人物设定是代理档案的核心。`adopting_personas.jsonl` 演示同一问题在不同 persona 下的回答差异：
- 20 岁的女本科生（计算机专业，回答像初级程序员）。
- 38 岁男性注册护士（以医疗专业人士的口吻回答）。

通过 persona 可以获得特定语域、背景或价值观的视角。本书后续会大量用在代理系统提示中。

### 2.3.3 使用分隔符（Delimiter）

`using_delimiters.jsonl` 展示两种写法：
- 三个单引号 `'''` 包裹需要总结的文本。
- XML 标签 `<statement>...</statement>` 用于比较两个观点。

分隔符能让 LLM 清楚知道哪部分是处理对象、哪部分是指令，非常适合含有层次结构或多段文本的场景。

### 2.3.4 明确步骤

`specifying_steps.jsonl` 利用系统提示定义多步流程，例如：
1. 从三引号内文本生成一句“Summary: …”
2. 把 Summary 翻译成西班牙语并加“Translation: …”前缀。

步骤也可以完全不同，如先回答问题再把答案改写成“Dad Joke”。这种“拆分任务 + 明确顺序”非常适合复杂代理或需要多轮交互的提示。

### 2.3.5 提供示例

`providing_examples.jsonl` 中，系统提示要求“所有回复沿用前一次的格式、长度和风格”，并提供示例对话（用户：Teach me about Python. 助手：一句话简介）。之后再问 “Teach me about Java.”，模型就会按照示例限制输出。提供示例是经典的 few-shot 技巧，也可用于约束代码模板、数据结构等。

### 2.3.6 限制输出长度

`specifying_output_length.jsonl` 给出了两种方式：
- 要求“所有回复不超过 10 个词”。
- 要求“所有回复总结成 3 个要点”。

精简输出不仅省 token，也能在多代理对话中减少噪音，让系统保持聚焦。

建议逐一运行所有战术示例，并尝试改写提示观察效果。本书后续章节会继续扩展到“给予思考时间”“使用外部工具”等更进阶策略。

---

## 2.4 挑选最适合的 LLM

构建代理并不需要成为模型训练专家，但理解关键指标有助于做出选择。结合 LM Studio 的经验，我们可以从八个方面评估 LLM（图 2.11）：

1. **模型性能**：是否在目标任务上表现优秀（如代码生成、SAT 推理等）。
2. **参数规模**：参数越多通常越强，但也意味着本地部署对硬件要求更高。幸运的是，越来越多“小而强”的开源模型正在出现。
3. **模型类型/用例**：聊天补全更适合需要迭代、推理的代理；completion、QA、instruct 则偏任务型。构建代理时强烈建议选择聊天补全类模型。
4. **训练语料**：决定模型的领域知识。通用模型适合广泛任务，特定领域（例如医疗、金融）可考虑经过定向微调的模型。
5. **训练/微调方法**：例如是否使用 RLHF、指令微调等。它会影响模型的泛化、推理与规划能力。
6. **上下文 token 长度**：决定模型一次能“记住”多少内容。简单任务 4K token 足矣，多代理协作或长文档处理则需要 16K、32K 甚至更大窗口。
7. **推理速度 / 部署方式**：商用 API 的速度由服务商保证；自建模型则取决于 CPU/GPU 配置。若代理需要实时与用户对话，速度至关重要。
8. **成本 / 预算**：需要权衡 API 计费 vs 自建基础设施成本。教学或个人项目可以混合使用。

在实践中，通常会先锁定 1–2 个候选模型开展原型，再依据性能/成本做最终取舍。选择本地模型时，务必确认硬件（显存、内存、磁盘）是否满足需求。

---

## 2.5 练习

1. **练习 1：掌握 OpenAI API**  
   - 使用 OpenAI Python SDK 连接 GPT-4。  
   - 实现一个根据用户输入生成回复的脚本，并在终端展示结果。  
   - 记录请求/响应结构和 token 使用情况。

2. **练习 2：探索提示工程战术**  
   - 复现本章的六种战术，并为每种撰写不同表述。  
   - 把这些变体送入 LLM，比较输出差异。  
   - 记录最有效的写法及其原因。

3. **练习 3：用 LM Studio 下载并运行 LLM**  
   - 安装 LM Studio，下载一个聊天补全模型。  
   - 启动 LM Studio Server，并通过 Python 代码连接。  
   - 把提示工程示例切换到本地模型，观察表现差异。

4. **练习 4：对比商用与开源 LLM**  
   - 用 GPT-4 Turbo 运行提示工程示例。  
   - 使用同一套提示测试某个开源模型。  
   - 从准确性、一致性、响应速度等维度比较并记录结论。

5. **练习 5：分析多种托管方案**  
   - 调研自建服务器、云端推理、第三方 API 等托管方式。  
   - 比较各方案在成本、性能、维护复杂度上的差异。  
   - 写一份短报告，给出针对特定用例的推荐。

---

## 本章小结
- LLM 采用 GPT（生成式预训练 Transformer）架构，属于生成式模型，与传统预测/分类模型在训练目标上完全不同。
- 模型由数据、架构、训练/微调三要素构成，针对不同用例（聊天、补全、指令等）会有专门配置。
- OpenAI API SDK 为连接 GPT-4 及其它模型提供了统一接口，也可对接兼容协议的开源 LLM。
- Python 环境 + VS Code 足以完成 API 集成、调试和 token 监控，是构建代理的基础技能。
- 开源 LLM 在 LM Studio 等工具加持下可以轻松下载、运行并暴露为本地服务，便于离线或隐私场景。
- 提示工程是一套帮助 LLM 产出更佳答案的技巧，本章围绕“写出清晰指令”示范了六种常用战术。
- LLM 可以支撑从简单聊天机器人到完全自主代理的全谱系应用。
- 选择模型需综合性能、规模、用例、训练语料、上下文长度、速度与成本等多重因素。
- 自建或托管 LLM 需要掌握 GPU、推理服务、配置管理等多方面技能，并权衡与商用 API 的优劣。



---

# AI-Agents-in-Action-Codex中文翻译版-第3章

## 第3章 激活 GPT 助手

OpenAI 在 ChatGPT Plus 中推出的 GPT Assistants 平台，让我们能够用纯图形界面快速定义和发布“类代理”助手。它内置 GPT Store、GPT Builder、文件知识库、Code Interpreter、自定义动作、发布与分享等能力，能够从零完成一个可商业化的智能体。本章带你依次体验：用 ChatGPT 构建 Culinary Companion、美食助手；让 GPT 充当“Data Scout”进行数据科学分析；借助自定义动作把助手与 FastAPI 服务连接；通过文件上传扩展知识；最后把 GPT 发布到 GPT Store，并评估资源成本与商业模式。

### 本章内容
- 通过 GPT Store 与 GPT Builder 设计并调优助手的 persona、指令与规则。
- 使用 Code Interpreter 与文件上传，打造可以分析 CSV 的数据科学家代理。
- 借助自定义动作把助手与自建 FastAPI 服务连接，并通过 ngrok 暴露端点。
- 让 GPT 消化整本书或多份文档，构建具备专属知识的“读书助手”。
- 了解 GPT Store 的分享、资源消耗、发布流程及潜在收益模型。
- 练习题：从第一个 GPT、数据分析、API 扩展、知识助手到发布全流程。

---

## 3.1 通过 ChatGPT 探索 GPT 助手

GPT Store（https://chatgpt.com/gpts）是 ChatGPT Plus 用户管理和探索 GPT 的门户。列表页能查看自己创建的助手、按类别/关键词搜索他人作品、了解使用量等。点击 **Create** 会打开 GPT Builder：你可以像和 ChatGPT 对话一样描述需求，Builder 会生成初始的名称、描述、指令与引导语。

Builder 生成的内容可在 **Configure** 面板中手动微调：修改名称与描述、编辑长指令、添加规则、设置默认对话开场白、上传图标等。精心撰写这些字段十分重要，因为它们决定了 GPT 的定位与“第一印象”。

### 示例：Culinary Companion

- **Persona**：模仿传奇厨师 Julia Child，口吻亲切、充满仪式感。
- **目标**：根据用户现有食材提供易于操作的菜谱，顺带科普营养和成本。
- **核心指令**（Listing 3.1）：用温暖口吻安抚用户，鼓励实验；推荐简单步骤；适配饮食偏好。
- **规则**：
  1. 每次生成菜谱时都要附带成品图像。
  2. 估算每份卡路里与营养值。
  3. 列出购物清单并给出价格预估。
  4. 基于清单估算每份成本。

在预览窗口输入“我有一袋速冻鸡柳，想做一顿浪漫双人餐”，GPT 会产出可视化食谱、食材与购物单、营养估算以及总价/份价提醒。这些额外输出完全来自我们在指令中写下的规则。虽然价格或营养值只是估算，但快速验证了制作原型的能力。

---

## 3.2 构建能够做数据科学的 GPT

GPT Assistants 目前提供“知识（文件上传）”“记忆”“动作（Code Interpreter、自定义动作）”等组件。本节构建 Data Scout——一名仿 Nate Silver 风格、擅长 CSV 初步分析的“数据科学家”助手。实现思路：

1. **需求拆解**：让 GPT-4 先推荐一个适合单个 CSV 的有趣实验，再请它把实验流程写成正式指令，最后补上一位符合设定的公众人物作为 persona。
2. **最终 persona**：Nate Silver 式的数据讲述者，善于把复杂统计结果解释得浅显易懂。
3. **任务分解**（Listing 3.4）：
   - *Data Acquisition*：要求用户上传 CSV，使用 `pandas` 读取、`df.head()` 预览。
   - *EDA*：清洗（`isnull()` + 填补/类型转换）、可视化（`matplotlib`/`seaborn`）、描述统计（`df.describe()`）。
   - *Hypothesis Testing*：使用 `scipy.stats`（如 `ttest_ind`、`chi2`）验证假设。
   - *Predictive Modeling*：特征工程、模型选择（`RandomForestClassifier`、`LinearRegression` 等）、`train_test_split` 训测、`metrics` 评估。
   - *Insights*：总结重要特征、意义、建议。
   - *Presentation*：用图表和要点向非技术读者汇报。
4. **启用 Code Interpreter**：勾选后即可上传 `netflix_titles.csv`，让 GPT 自动写代码进行过滤、绘图、统计。示例把数据过滤为“加拿大”并绘制流派分布、年份趋势等。

Code Interpreter 本质上是“受控沙盒 + Python 工具链”。借助它，几乎可以把任何数据分析、计算或图表任务交给 GPT 完成，并随时迭代需求。

---

## 3.3 自定义 GPT 并添加自定义动作

### 3.3.1 用 GPT 帮你写 FastAPI 服务

自定义动作允许 GPT 调用你提供的 HTTP API。为避免手写繁琐的 OpenAPI 规范，本节先让 GPT 自己生成一个“FastAPI 服务生成器”助手：

- **目标**：根据用户描述的动作，输出一份带 FastAPI 代码 + OpenAPI 规范的服务模板。
- **指令要点**：
  1. 先澄清动作、HTTP 方法、路径与请求/响应结构。
  2. 使用 FastAPI + Pydantic 编写函数、装饰器、输入输出模型。
  3. 提示如何让 FastAPI 自动生成 OpenAPI，并可手动补充元数据/标签。
  4. 指导用户用 ngrok 暴露本地 8000 端口，便于 GPT 访问。
- **能力**：推荐启用 Code Interpreter，以便在对话中生成/修改代码片段。

借此，我们可以让 GPT 产出一个“待办任务服务”：返回当天任务、优先级和时间估算等信息。

### 3.3.2 把自定义动作接入助手

1. **运行 FastAPI 服务**：在本地启动生成的应用（默认 8000 端口）。
2. **开启外网访问**：运行 `ngrok http 8000`，复制生成的 HTTPS URL。
3. **新建助手 Task Organizer**：
   - Persona：借鉴 Tim Ferriss，强调效率与现实主义，用清晰直接的语言帮助用户分类任务并安排时间块。
   - 规则：完成整理后用 Code Interpreter 绘制任务时间表。
4. **添加自定义动作**：
   - 在 Configure 面板底部点击 **Create new Action**。
   - 将 FastAPI 生成的 OpenAPI 规范粘贴到窗口，并新增 `servers` 字段写入 ngrok URL。
   - 点击 **Test** 验证，成功后助手即可调用该 API。
5. **测试**：重新加载会话，输入 “how should I organize my tasks for today?”，GPT 会调用 API 获取任务、排序并输出图表。

> ⚠️ **安全提示**：一旦把含自定义动作的 GPT 发布到 GPT Store，任何使用者都能触发该 API。请勿暴露付费接口或敏感数据服务；若使用 ngrok，也要留意外部访问风险。

---

## 3.4 通过文件上传扩展知识

GPT Assistants 的“文件上传”能力，相当于内置了轻量 RAG。单个助手可上传最多 512 MB 的文档（PDF、TXT、MD 等），随后 GPT 可引用这些资料回答问题、对比、排序，甚至生成仿写内容。

### 3.4.1 Calculus Made Easy：书籍 + Persona 的教学助手

- **资料**：上传整本《Calculus Made Easy》。
- **Persona**：以数学家陶哲轩（Terence Tao）的语气教书。
- **规则**：
  1. 用教孩子的方式耐心说明。
  2. 必须画图展示函数或导数（需启用 Code Interpreter）。
  3. 每讲完一个概念就问学生是否要自己做题，并给出等价难度的练习。

在 GPT Store 搜索 “Calculus Made Easy” 即可体验：它会结合书本内容解释微积分，展示图像，最后抛出自测题，像定制家教一样伴学。

### 3.4.2 Classic Robot Reads：多文档检索与创作

- **资料**：上传 `gutenberg_robot_books` 目录下的多本经典机器人小说（Asimov 等）。
- **Persona**：化身 Isaac Asimov 本人，只引用知识库中的文本，永远提供 3 个例子，并在回答后询问用户是否需要更多帮助。
- **应用**：搜索特定段落、比较写作风格、找出差异、推荐阅读顺序、判断年代，甚至生成模仿原文笔调的短段落（表 3.1 给出了常见用法与示例提示）。

这种“知识助手”可以轻松应用到公司制度、团队文档或个人藏书中，大幅提升检索与学习效率。

---

## 3.5 发布 GPT

当你对 GPT 的体验满意后，可点击 **Share** 按钮选择分享方式：

- **Only me**：仅自己使用。
- **Share link**：持链接者可用（仍需 Plus 账号，费用计入使用者账户）。
- **Publish to GPT Store**：公开上架，供所有 ChatGPT Plus 用户搜索、体验。

### 3.5.1 控制资源消耗

OpenAI 会监控每个账号的资源使用（图像生成、Code Interpreter、Vision、文件上传等）。一旦超额，账号会暂时被封（通常几小时），影响体验。为避免用户在使用你的 GPT 时被封锁，可在指令里加入提醒，例如：

```
RULE: When generating images, remind the user that rapid multi-image requests may temporarily block their account.
```

也可以针对 Code Interpreter、Vision、批量文件上传等高消耗功能设置频率或先行确认，帮助用户合理使用。

### 3.5.2 GPT 的经济学

OpenAI 计划引入收益分享机制，具体比例尚未公布（社区推测 10%–20%）。即便暂未直接盈利，公开 GPT 仍有价值：

- **作品集 / 个人品牌**：展示提示工程、应用设计的能力。
- **知识产品**：把专业经验包装为顾问型助手。
- **商业引流**：作为产品/服务的对话入口，完成预筛选或售前沟通。
- **客户支持**：提供 7×24 小助手，降低自建聊天机器人的成本。

随着 GPT Store 逐渐开放给非 ChatGPT 用户，这些助手可能像早期网站一样成为企业的“标配入口”。

### 3.5.3 发布前清单

- **描述**：撰写清晰且富含关键词的介绍，必要时请 GPT 帮你做 SEO。
- **Logo**：设计辨识度高的图标，提升点击率。
- **类别**：确认分类准确；若无合适选项，可选择 “Other” 并自定义。
- **链接**：添加社交媒体、GitHub 或反馈渠道，让用户能与你取得联系。
- **后续维护**：保持监听用户反馈，及时更新指令、文件或自定义动作。

---

## 3.6 练习

1. **练习 1：构建你的第一个 GPT**
   - 订阅 ChatGPT Plus，打开 GPT Builder。
   - 复刻本章的 Culinary Companion，手动加入营养与成本规则。

2. **练习 2：数据分析助手**
   - 设计类似 Data Scout 的指令，启用 Code Interpreter。
   - 上传任意 CSV，完成清洗、可视化、假设检验，记录发现。

3. **练习 3：创建自定义动作**
   - 实现一个 FastAPI 服务（如返回待办列表），生成 OpenAPI 规范。
   - 用 ngrok 暴露端口，在 GPT 中注册该动作，测试任务组织流程。

4. **练习 4：文件知识助手**
   - 选取若干公开文档或电子书上传，定义 persona 与回答范围。
   - 设计测试提示，检验引用、总结、比较、创作等能力。

5. **练习 5：发布并分享**
   - 完成描述、Logo、分类与链接设置。
   - 发布到 GPT Store，邀请朋友体验，并根据反馈迭代。

---

## 本章小结

- GPT Assistants 平台让我们无需写代码即可设计、测试、共享 AI 助手；核心在于 persona、规则与对话体验的精细打磨。
- Code Interpreter 赋予 GPT 读写文件、运行 Python、绘制图表的能力，让它能胜任数据科学、公式计算、格式转换等任务。
- 自定义动作通过 OpenAPI 把 GPT 与任何 HTTP 服务打通，可与 FastAPI、ngrok 等工具结合快速原型。
- 文件上传即内置 RAG，可让 GPT 成为特定资料的“权威讲解员”，适用于教学、知识库、文档检索等场景。
- 发布到 GPT Store 前，需要关注资源消耗、用户体验、商业定位与推广策略，确保助手既易用又可持续。
- 通过章节尾的练习，你可以亲手完成 GPT 的设计—增强—发布全流程，为后续多代理系统打下基础。


---

# AI-Agents-in-Action-Codex中文翻译版-第4章

## 第4章 探索多代理系统

本章聚焦两大多代理平台：微软开源的 AutoGen 与近年来兴起的 CrewAI。前者强调“可对话”的代理协作，提供 AutoGen Studio 与 Python SDK 两种体验路径；后者面向企业场景，主打角色分工、顺序/层级流程与可观测性。章节中，你将动手安装 AutoGen Studio、为代理添加视觉技能、在代码层实践 UserProxy/ConversableAgent、让工程师与 Reviewer 协同、启用缓存与群聊；随后切换到 CrewAI，构建段子手小队、引入 AgentOps 观测、组建编码团队并比较顺序/层级流程；最后给出练习与要点总结。

---

## 4.1 AutoGen Studio：零代码体验多代理

### 4.1.1 安装与上手
1. 打开 `chapter_04` 目录，按附录 B 配好 Python 虚拟环境并安装 `requirements.txt`。
2. 在终端里设置 OpenAI Key 并启动 Studio（Listing 4.1）：
   ```bash
   export OPENAI_API_KEY="<你的 API Key>"
   autogenstudio ui --port 8081
   ```
   端口若冲突，可改成 8082 等。
3. 浏览器访问 `http://localhost:8081`。**Playground** 标签用于对话，**Build** 创建代理/技能，**Gallery** 回顾历史最佳输出。
4. 在输入框里给出复杂任务，例如 “Create a plot showing the popularity of the term GPT Agents in Google search.”，观察 UserProxy 如何分配子任务，Assistant 如何写代码，Proxy 再执行、评估并循环迭代（图 4.2、4.3、4.4）。
5. 若代码执行出错，可提示 Proxy 换方法；如需要更稳定的沙箱，官方推荐用 Docker 跑 Studio/AutoGen。

### 4.1.2 在 Studio 里添加技能
1. 切到 **Build → Skills**，点击 **New Skill**。
2. 把 `describe_image.py`（Listing 4.2）贴进去。该函数用 GPT-4 Turbo Vision 解析本地图像内容，可用于检查图片是否符合要求。
3. 在 **Build → Workflows** 中，选择默认的 `general` 工作流，编辑 `primary_assistant`，把 `describe_image` 技能加入。
4. 回到 Playground，输入（Listing 4.3）：
   > “Please create a cover for the book *GPT Agents in Action*, use the describe_image skill to ensure the title is spelled correctly.”
5. 助手会调用已有的 `generate_image` 技能生成封面，再用新建技能验证标题。图 4.6、4.7 展示了工作流配置与产出。

这种“写技能 → 加入工作流 → 通过语言触发”的模式，是 AutoGen Studio 最强的迭代路径之一。

---

## 4.2 AutoGen SDK：在代码层自定义代理

### 4.2.1 基础安装与 Hello World
1. 安装核心库：`pip install pyautogen`（Listing 4.4）。
2. 复制 `chapter_04/OAI_CONFIG_LIST.example` 为 `OAI_CONFIG_LIST`，填写模型/Key/Base URL 等配置（Listing 4.5）。可同时配置 OpenAI 与 Azure；凡是支持 OpenAI API 协议的服务（LM Studio、Groq 等）也可写入。
3. 查看 `autogen_start.py`（Listing 4.6）：
   - `ConversableAgent`：真正调用 LLM 的助手。
   - `UserProxyAgent`：代表人类，负责执行代码、提供反馈、判断何时 `TERMINATE`。
4. 运行脚本（F5），在终端输入简单的编程任务（Listing 4.7 如“一行写完 FizzBuzz”“写贪吃蛇”等）。Proxy 会自动执行生成的 Python 代码，并把源码写入 `working/` 目录以供复查。

### 4.2.2 引入 Reviewer 批改代码
- `autogen_coding_critic.py`（Listing 4.8）增加了第二个 `AssistantAgent`——Reviewer。
- 通过 `register_nested_chats`，当 Engineer 完成代码后自动触发 Reviewer 嵌套对话，调用 `review_code()` 读取最新代码并给出改进建议。
- 这种多角色结构让“写代码 + code review + 迭代”自动化完成。

### 4.2.3 理解缓存
- AutoGen 默认在工作目录创建 `.cache/`（SQLite）保存对话。
- 使用 `with Cache.disk(cache_seed=42)` 包裹 `initiate_chat`（Listing 4.9）可指定缓存文件，支持长任务暂停续跑、复现结果或分析历史对话。

---

## 4.3 群聊：让代理共享上下文

- 嵌套对话易造成“传话游戏”式失真。`autogen_coding_group.py`（Listing 4.10）展示 `GroupChat` + `GroupChatManager`：
  - `GroupChat` 持有多个代理与会话消息，像 Slack/Discord 频道。
  - Manager 负责指定谁在下一轮发言、避免重复。
  - 将 `human_input_mode` 设为 `NEVER`，实现完全自动协作。
- 运行后，工程师与 Reviewer 在群里同步讨论，Proxy 也能读全程记录。代价是 token 消耗更高，但协作质量显著提升。

---

## 4.4 CrewAI：面向企业的多代理框架

CrewAI 把多代理系统拆成“Agent + Task + Process + Memory/Tools”，默认不需要 UserProxy。它支持顺序（sequential）与层级（hierarchical）两种流程。

### 4.4.1 Jokester Crew：段子手小队
1. `crewai_introduction.py` 定义两个代理（Listing 4.11）：
   - **Senior Joke Researcher**：负责搜集题材笑点，可委派任务。
   - **Joke Writer**：根据研究成果写笑话。
2. 每个代理绑定 `Task`（Listing 4.12）：
   - `research_task`：输出 3 段报告 + 社会趋势分析。
   - `write_task`：写最终笑话，保存到 `the_best_joke.md`。
3. 用 `Crew(..., process=Process.sequential)` 组队（Listing 4.13），`crew.kickoff(inputs={"topic": "AI engineer jokes"})` 即可看到两位“段子手”在线合作，终端会输出多条机智回应。

### 4.4.2 加入 AgentOps 观测
1. 安装依赖：`pip install agentops` 或 `pip install crewai[agentops]`（Listing 4.14）。
2. 在 AgentOps 网站申请 API Key，写入 `.env`（Listing 4.15）。
3. 在脚本里 `import agentops` 并 `agentops.init()`（Listing 4.16）。
4. 运行 `crewai_agentops.py`，即可在仪表盘看到每次 GPT 调用的耗时、token、成本、日志、系统环境等（图 4.11）。

AgentOps 能同时接入 AutoGen/CrewAI 等多种框架，帮助追踪高成本或重复思考（Repeat Thoughts）等问题。

---

## 4.5 CrewAI 编码小队：顺序 vs 层级

### 4.5.1 顺序流程
1. `crewai_coding_crew.py` 定义三名代理（Listing 4.17）：
   - **Senior Engineer**：写代码。
   - **QA Engineer**：检查语法、逻辑、依赖。
   - **Chief QA Engineer**：最终审查，必要时可委派。
2. 任务（Listing 4.18）：
   - `code_task`：基于用户输入的游戏说明编写 Python 代码，并只输出最终代码。
   - `qa_task`：列出发现的问题。
   - `evaluate_task`：输出修正后的完整代码。
3. `Crew(..., process=Process.sequential)` 顺序执行（Listing 4.19）。运行脚本后输入想做的游戏（如贪吃蛇），观察三名角色如何串行协作。

### 4.5.2 层级流程
- `crewai_hierarchy.py` 把 `process` 换成 `Process.hierarchical`，并用 `manager_llm=ChatOpenAI(model="gpt-4", temperature=0)`（Listing 4.20）。
- 这时多了一个“Crew Manager”协调各 Agent，整体表现更像“项目经理 + 组员”结构。
- 搭配 AgentOps 的 Repeat Thoughts 图（图 4.13，可在原书看到完整页），能监控代理是否陷入重复尝试，必要时调整流程或提示。

层级调度适合复杂任务：Manager 负责拆解/调度，成员专注于执行；缺点是开销更高。

---

## 4.6 练习
1. **练习 1：AutoGen 基础通讯**——在 Studio 中搭建 UserProxy + 两个助手，让他们合写一段摘要。
2. **练习 2：扩展技能**——为 AutoGen 写一个可调用公开 API 的技能（例如天气/股价查询），让代理根据用户偏好返回实时信息。
3. **练习 3：CrewAI 角色分工**——设计“数据抓取→分析→报告”三段任务，观察信息如何在代理间传递。
4. **练习 4：AutoGen 群聊协作**——设定“出差行程规划”等复杂任务，启用 GroupChat 观察多代理讨论的过程与成果。
5. **练习 5：AgentOps 观测**——在 CrewAI 项目里集成 AgentOps，挑选一个耗时/高算力任务，分析性能、成本与潜在瓶颈。

---

## 本章小结
- **AutoGen**：微软推出的对话式多代理平台，提供 Studio GUI 与 Python SDK。UserProxy 负责执行/评估，Assistant 负责生成，可通过技能扩展图像/代码/数据等能力。
- **多种通讯模式**：AutoGen 支持代理链式/嵌套对话、群聊与层级代理；通过缓存和 Docker 隔离可提升稳定性。
- **CrewAI**：更偏企业级，强调角色/任务/流程配置，支持顺序或层级处理，易于把工具、记忆（RAG）、API 调用装配到各 Agent。
- **可观测性**：AgentOps 等平台可记录对话、成本、token、重复思考次数，是大规模部署代理时必备的“度量仪表”。
- **实践范式**：不论 AutoGen 还是 CrewAI，最佳体验都来自“明确定义 persona + 指令 + 工具 + 反馈”，并在必要时引入代码审查、群聊协作或层级调度。
- **成本意识**：多代理迭代能带来更高质量，也可能快速推高 token 花费。务必借助缓存/观测/流程优化控制成本。

下一章将把注意力转向“赋予代理行动能力”，继续完善你的 AI Agent 工程 toolbox。


---

# AI-Agents-in-Action-Codex中文翻译版-第5章

## 第5章 让代理拥有行动力

上一章我们学会用多代理协作完成复杂任务，本章则深入“行动”这一核心能力：如何让 LLM 通过函数、插件、技能、工具去操作外部世界。我们先复盘 ChatGPT 插件与 OpenAI 函数调用，再介绍微软的 Semantic Kernel（SK），学习用语义函数 + 本地代码（Native Function）来封装服务，最终把任意 API 包装成 GPT 接口，让聊天/代理系统可语义化调用。

### 本章内容
- `5.1` 代理动作的含义：插件、工具、技能之间的映射关系。
- `5.2` 在 OpenAI API 中定义函数（tools）并执行，含多函数并发示例。
- `5.3` Semantic Kernel 入门：安装、创建语义函数、使用上下文变量。
- `5.4` 语义函数与本地函数的协同，如何注册/复用插件。
- `5.5` 用 SK 把 TMDB API 封装成 GPT 接口，驱动聊天代理。
- `5.6` “语义式思维”：返回结构化 JSON 让 LLM 进一步筛选。
- `5.7` 练习与总结。

---

## 5.1 代理动作与插件
- 插件相当于“代理的代理”：ChatGPT 安装“电影推荐插件”后，LLM 会自动识别用户意图、抽取参数、调用插件去抓取数据，再把结果回传给用户（图 5.1）。
- 插件内部可包含多个动作，真正执行任务的是“函数/技能/工具”。不同框架术语不一，本章统一称之为 **Action**。
- 动作既可以触发 API（抓取网页、查询数据库），也可以调用其他 LLM 做进一步处理。Chevron 图标标记了“代理动作发生的位置”。
- ChatGPT 插件 + OpenAI 函数调用 = 让 LLM 系统拥有“外部臂膀”。

---

## 5.2 在 OpenAI API 中执行函数
### 5.2.1 在 API 请求里定义函数
- Listing 5.1 展示 `chat.completions.create` 如何通过 `tools=[{"type":"function", ...}]` 定义函数；这就是 ChatGPT 插件和 Functions API 的底层协议。
- 参数定义遵循 JSON Schema，可描述类型、枚举以及必填字段。LLM 会解析用户输入，将其映射到满足 Schema 的参数上（图 5.3）。
- 示例 `first_function.py`：
  - 请求 1：“推荐一部穿越电影” → 返回 `Function(name='recommend', arguments='{"topic": "time travel movie"}')`
  - 请求 2：增加“good”评级 → 参数中自动带上 `rating`。
- 注意：**LLM 只返回函数名和参数，不会执行函数**。开发者需在拿到函数名后调用本地实现。

### 5.2.2 触发并执行函数
- `parallel_functions.py` 演示更完整流程（图 5.4）：
  1. 用户一次性请求“穿越电影/菜谱/礼物”三种推荐。
  2. LLM 返回 3 组 `tool_calls`（同一函数多次调用）。
  3. 代码遍历每个 `tool_call`，调用本地 `recommend()`，将结果写入 `messages`。
  4. 再次调用 LLM，让它把多个函数结果转成自然语言回答。
- 该示例使用更便宜的 GPT-3.5 Turbo，表明“函数委派”可以由较小模型承担。

---

## 5.3 Semantic Kernel（SK）入门
SK 是微软开源的 AI 应用框架，核心用途：管理语义函数（Prompt）和本地函数（代码），并通过统一的插件系统对外暴露。支持 Python/Java/C# 等多语言。

### 5.3.1 安装与首次运行
1. 卸载旧版本、克隆仓库并安装可编辑包（Listing 5.8）。
2. 在 `SK_connecting.py` 中：
   - 创建 `Kernel()`。
   - 选择 OpenAI 或 Azure OpenAI 服务并加载 `.env` 中的 API Key。
   - 调用 `kernel.invoke_prompt("recommend a movie about time travel")`（Listing 5.9）。
3. 输出即为运行语义函数（prompt template）的结果。

### 5.3.2 语义函数 + 上下文变量
- `SK_context_variables.py` 使用模板变量（`{{$format}}`, `{{$subject}}` 等）构建“推荐器”提示（Listing 5.10）。
- 通过 `PromptTemplateConfig` 声明输入变量及描述，`kernel.create_function_from_prompt()` 将其注册为函数。
- 调用 `kernel.invoke` 时用 `KernelArguments` 提供变量值即可，输出示例推荐了一部“中世纪、穿越、喜剧电影”。

---

## 5.4 语义函数与本地函数的协同
### 5.4.1 创建并注册语义插件
- VS Code SK 插件可生成语义技能：
  1. 新建 Skill → 选目录 → 命名函数 → 撰写描述（图 5.6）。
  2. `config.json` 描述函数类型（`completion`）、参数、采样策略（Listing 5.11）。
  3. `skprompt.txt` 写实际 Prompt（Listing 5.12）。
- 运行 `SK_first_skill.py`：
  - `kernel.import_plugin_from_prompt_directory("plugins", "Recommender")` 将技能注册进 Kernel。
  - 调用 `recommend = recommender["Recommend_Movies"]` + `kernel.invoke` 即可完成推荐（Listing 5.13）。

### 5.4.2 原生函数（Native Function）
- 原生函数用 Python/JS/C# 实现任意逻辑，通过 `@kernel_function` 装饰器描述（Listing 5.14）。
- `SK_native_functions.py`：
  - `MySeenMoviesDatabase.load_seen_movies()` 读取文本文件返回观影列表。
  - `kernel.import_plugin_from_object(..., "SeenMoviesPlugin")` 注册该函数（Listing 5.15）。
  - 语义函数 `Recommend_Movies` 使用加载的观影列表生成新推荐。

### 5.4.3 在语义函数中嵌入原生函数
- `SK_semantic_native_functions.py` 直接在 Prompt 里引用 `{{MySeenMoviesDatabase.LoadSeenMovies}}`（Listing 5.16）。
- 调用前需先把原生函数作为插件导入；语义函数可以只用 `create_function_from_prompt` 创建而不注册。
- 运行后 LLM 会基于原生函数返回的清单给出新片建议（Listing 5.17）。

---

## 5.5 把 Semantic Kernel 作为 GPT 接口
### 5.5.1 构建 TMDB 语义服务
- TMDB 提供影视 API，无语义层。我们在 `skills/Movies/tmdb.py` 中封装 `TMDbService`：
  - `get_movie_genre_id`：根据名称获取 genre id。
  - `get_top_movies_by_genre`：按类型拉取当前热映电影（Listing 5.18-5.19）。
- 每个方法都用 `@kernel_function` 标注，使其自动成为插件。

### 5.5.2 在 Shell/Chat 中调用
- `SK_service.py`：示范在命令行直接调用 TMDB 插件（图 5.8）。
- `SK_service_chat.py`：
  - 实现一个简易聊天循环；用户输入自然语句，程序用 `kernel.invoke` 调度 TMDB 插件（Listing 5.23-5.24）。
  - 例如“列出动作和喜剧的当前热映影片” → 会顺序调用 `get_top_movies_by_genre` + `get_movie_genre_id`，最后返回两个类别的列表。

---

## 5.6 用“语义思维”编写服务
- 如果插件只返回片名，LLM 无法进一步筛选。应尽量返回结构化 JSON，留给 LLM 自己过滤、排序、摘要。
- `tmdb_v2.py` 将 `get_top_movies_by_genre` 改为 `json.dumps(filtered_movies)`（Listing 5.25），`SK_service_chat.py` 中切换到新服务（Listing 5.26）。
- 于是用户可以追加条件“只要太空题材的动作片”，LLM 会在本地过滤 JSON，并把匹配结果转成自然语言（Listing 5.27）。
- 这体现了“服务返回越富信息量，LLM 越能展现推理与转写能力”。

---

## 5.7 练习
1. **温度转换插件**：实现摄氏/华氏互转，接入 OpenAI Chat API。
2. **天气查询插件**：调用公开天气 API，支持城市参数。
3. **创作型语义函数**：写诗/儿童故事，支持用户主题输入。
4. **语义 + 原生函数**：例如语义函数生成菜单、原生函数查营养信息。
5. **用 SK 包装新闻 API**：把新闻接口暴露为聊天插件，支持按主题查询。

---

## 本章小结
- 代理的行动力来自“可调用的外部函数/插件/工具”。OpenAI 的 Functions API 与 ChatGPT 插件遵循同一 Schema。
- Semantic Kernel 统一管理语义函数（Prompt 模板）与本地函数（代码实现），并用插件机制让它们被聊天/代理系统调用。
- 语义函数可复用 Prompt 模板；原生函数可访问文件、数据库、API；两者可以相互嵌套，实现“代码 + Prompt”混合流水线。
- SK 插件既能消费外部 API，也能对外暴露自身，让任意 Web Service 摇身变成 GPT 接口。
- 编写语义服务时要“多返回数据”：尽可能输出完整 JSON，利用 LLM 自己过滤/排序/生成，而非只能回传字符串列表。
- 通过这些手段，代理可以精准地“执行动作”、调用服务、组合函数，为下一章的“自治行为树”铺平道路。


---

# AI-Agents-in-Action-Codex中文翻译版-第6章

## 第6章 构建自主助手

本章从“行为树（Behavior Tree, BT）”切入，讲解如何用树状控制结构协调多个助手（Assistants）完成目标；然后引入基于 Gradio 的 **GPT Assistants Playground**，通过 OpenAI Assistants API + 自定义 Actions 搭建交互式沙箱；最后利用 py_trees + Playground 实现“Agentic Behavior Trees（ABT）”，将不同助手以串行/并行/对话方式组合，甚至用“回溯链（Back Chaining）”逆向设计整个行为树。

---

## 6.1 行为树基础
- 行为树源自 1986 年 Rodney Brooks 的机器人控制论文，如今在游戏 NPC、机器人与智能体中广泛应用。节点类型包含 Selector（选择/回退）、Sequence（顺序）、Condition（条件）、Action（动作）、Decorator（装饰器/约束）、Parallel（并行）（图 6.1、表 6.1）。
- **执行逻辑**：树从根节点自上而下、从左到右 tick；每个节点都只返回 `SUCCESS` 或 `FAILURE`。Selector 在子节点成功时立即停止；Sequence 任一子节点失败就整体失败（图 6.2）。
- **适用范围**：可微观控制（机器人微动作）或宏观流程（游戏策略）。与有限状态机、Goal-Oriented Action Planning 等方法相比，行为树更模块化、易扩展（表 6.2）。
- **py_trees 示例**：Listing 6.1 展示如何用 Python + py_trees 实现“先吃苹果，没苹果再吃梨”的树。每个节点封装成类，加入 Sequence/Selector，再由 `BehaviourTree.tick()` 驱动；日志清晰显示执行序列。

---

## 6.2 GPT Assistants Playground
Gradio 开发、可本地运行的 OpenAI Assistants Playground，既能模拟官网 Playground，又提供更多自定义动作、日志、代码执行能力。

### 6.2.1 安装/启动
```bash
git clone https://github.com/cxbxmxcx/GPTAssistantsPlayground
cd GPTAssistantsPlayground
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
python main.py
```
浏览器打开后，与官方 Assistants Playground 类似：可创建助手、选择模型、勾选 Tools/Actions，查看输出文件（图 6.3）。

### 6.2.2 自定义 Actions
- Playground 自带多种 action，并支持在 `playground/assistant_actions/` 目录新增自定义函数。例如 Listing 6.4 的 `save_file()` 通过 `@agent_action` 装饰器注册，描述是助手机器理解动作的关键。
- 面板（图 6.4）可为助手勾选 `call_assistant`（调用其他助手）、`list_assistants` 等常用动作，实现“助手调助手”。
- Playground 还自带一个本地 **Code Runner**：选择 `run_code` + `run_shell_command`（图 6.5），助手即可在隔离虚拟环境中执行 Python，并可 `pip install` 依赖。相较 OpenAI Code Interpreter（昂贵、沙箱受限），本地执行更灵活。

### 6.2.3 管理助手数据库
- 通过 `create_manager_assistant` 动作快速安装“Manager Assistant”，再让它“列出并安装所有可用助手”“导出 assistants.json”等（步骤详见 6.3.1）。
- Manager Assistant 拥有全部权限，适合作为“助手管家”，但为安全起见建议专用、谨慎调用。

### 6.2.4 日志与可观测性
- Playground 集成 OpenAI Assistants 事件流，可在 **Logs** 标签查看每次工具调用/代码执行的详细日志（图 6.7）。对调试、理解内部流程非常有帮助。

---

## 6.3 构建 Agentic Behavior Trees（ABT）
ABT = 行为树 + Assistants API。借助 py_trees 组织节点，再通过 Playground 的辅助函数把每个节点映射为“调用某个助手完成行动或判定”。

### 6.3.1 用助手管理助手
- 步骤：创建任意助手 → 勾选 `create_manager_assistant` 动作 → 在聊天中输入“please create the manager assistant” → 刷新后选择该助手 → 命令它“列出/安装/导出”助手。
- 通过 Manager Assistant 可批量安装书中用到的 Python Coding Assistant、Coding Challenge Judge、YouTube Researcher 等。

### 6.3.2 Edabit 编程挑战 ABT
- 场景：Edabit“Plant the Grass”挑战（Listing 6.5）+ 对应测试（Listing 6.6）。
- 行为树：Sequence 根节点 → `Hack`（Python Coding Assistant）生成解并保存 → `Judge`（Coding Challenge Judge）运行测试，返回 `SUCCESS/FAILURE`（Listing 6.7）。
- Assistants 在 **同一线程** 对话，条件失败会自动重试。可扩展更多节点（多名 Hacker、分阶段分析等）。

### 6.3.3 对话 vs. 文件
- 让助手共享线程可激发“对话式推理/反馈”；让助手各自开启新线程并通过文件共享则更安静、更易定位问题。混合使用往往效果最佳。

### 6.3.4 YouTube → X（Twitter）发帖 ABT
- 行为：
  1. `YouTube Researcher v2` 搜索指定关键词、下载转录、摘要，输出 `youtube_transcripts.txt`。
  2. `Twitter Post Writer` 读取摘要，挑选亮点，写 280 字内推文，保存 `youtube_twitter_post.txt`。
  3. `Social Media Assistant` 读取文件，发布到 X（可选）。
- 所有节点用 Sequence 连接，且每个助手**使用独立线程**，便于排障（图 6.9）。
- 运行前须在 `.env` 中配置 `X_EMAIL/USERNAME/PASSWORD`（Listing 6.8）。未配置则最后一步失败但仍可阅读生成的文案。
- 示例输出如图 6.10。提醒：频繁自动发帖可能触发平台风控。

### 6.3.5 必备注意事项
- YouTube 存在大量垃圾视频，助手已尽量筛除，但仍需人工复检。
- 最终 ABT 展示了：搜索+抓取+摘要→内容创作→多 API 调用的协作流程。

---

## 6.4 构建可对话的多智能体
- Playground 支持 **Silo 模式**（每个助手独占线程）与 **Conversational 模式**（共享线程），也可混合（图 6.11）。
- `agentic_conversation_btree.py` 示例：
  - 共享线程 `thread = api.create_thread()`。
  - Sequence 节点包含 `Debug code`（Python Debugger）和 `Verify`（Python Coding Assistant），前者修复 bug，后者验证/保存（Listing 6.10）。
  - 只要任一节点失败，树就继续 tick，直到两者都 `SUCCESS`。
- 这种方式结合了“行为树的可控流程”与“线程对话的上下文共享”。

---

## 6.5 用 Back Chaining 设计 ABT
- Back chaining 步骤：1) 明确目标行为 2) 逆向列出所需动作 3) 标出条件 4) 选通信方式（共享线程？文件？） 5) 自底向上搭建树。
- 案例：目标“创建能帮我执行 {task} 的助手”：
  - 动作：编写指令→命名→测试→创建等；条件：验证。
  - 可先让 ChatGPT 生成树框架（Listing 6.11），再逐步细化每个动作与所需工具。
- 提示：宁可从少量助手起步，再按需要拆分；测试/验证最好由不同助手执行；存储可先用文件，未来也可接入更复杂的“黑板”系统。

---

## 6.6 练习
1. **旅行规划 ABT**：Travel Assistant 收集目标 → Itinerary Planner 制订行程 → 另一助手验证可行性。
2. **客服自动化 ABT**：Query Analyzer 分类 → Response Generator 草拟回复 → Customer Support 发送。
3. **库存管理 ABT**：Inventory Checker 检查库存 → Order Assistant 下单 → Condition 节点验证更新。
4. **私人健身教练 ABT**：Fitness Assessment 评估 → Training Plan Generator 制定方案 → Condition 验证安全性。
5. **金融顾问 ABT（Back Chaining）**：逆向设计“提供投资建议”的行为树。

---

## 本章小结
- 行为树以 Success/Failure 为核心信号，提供清晰、可扩展的 AI 控制结构；py_trees 等库让实现更简单。
- GPT Assistants Playground 结合 OpenAI Assistants API + 自定义 Actions + 本地代码执行，便于快速实验代理技能，并通过详尽日志掌握执行细节。
- Agentic Behavior Trees 让我们能把多个助手按照 Sequence/Selector/Parallel 等模式粘合，并根据场景选择“共享线程对话”或“独立线程+文件”通信策略。
- 通过 ABT 可实现从编程挑战评测到 YouTube→X 自动发帖的多步骤流程，示范了如何组合搜索、摘要、内容创作、发布等能力。
- Back chaining 为复杂目标提供系统化的树构建方法，强调从终点出发逐步拆解动作与条件。
- 这些方法为创建“自主助手”奠定基础，也为后续章节（控制、平台、评估等）做好准备。


---

# AI-Agents-in-Action-Codex中文翻译版-第7章

## 第7章 搭建并使用代理平台

本章围绕开源教育平台 **Nexus** 展开，讲解如何组合人格（persona）、工具、记忆与规划，构建可调试、可扩展的聊天代理。我们先介绍 Nexus 的安装与开发模式，再用 Streamlit 打造 ChatGPT 式界面；随后编写新的 agent profile、接入自定义动作与工具，最后用练习与总结梳理要点。

---

## 7.1 Nexus 平台简介

Nexus 结合 Streamlit + OpenAI API，提供一个“所见即所得”的代理实验环境。界面允许用户自由选择：
- **Persona/Profile**：系统提示、语气、角色定位。
- **Actions/Tools**：语义函数或本地代码函数，驱动代理执行外部操作。
- **Memory/Knowledge/Planning**：未来章节逐步开放，用于扩展上下文、反馈与评估能力。

### 7.1.1 快速运行 Nexus
1. 准备 Python 3.10 虚拟环境。
2. 运行：
   ```bash
   pip install git+https://github.com/cxbxmxcx/Nexus.git
   export OPENAI_API_KEY="<你的 API Key>"   # Linux/Mac
   # Windows PowerShell 用：$env:OPENAI_API_KEY="<key>"
   # 或写入 .env：echo 'OPENAI_API_KEY="<key>"' > .env
   nexus run
   ```
3. 浏览器自动打开登录页（图 7.2）。首次使用选择 “Create New User”，之后可直接用 cookies 自动登录。
4. 进入主界面（类似图 7.1），新建聊天即可体验默认代理。

### 7.1.2 开发模式
- 为了调试/二次开发，建议直接克隆仓库：
  ```bash
  git clone https://github.com/cxbxmxcx/Nexus.git
  pip install -e Nexus
  export OPENAI_API_KEY="<你的 API Key>"
  nexus run
  ```
- 可在 VS Code 中创建 `.vscode/launch.json`，以 `streamlit` 模式（module）调试 `Nexus/nexus/streamlit_ui.py`。
- Nexus 结构（图 7.4）：Streamlit 界面 ↔ Chat System ↔ Agent Manager / Profile Manager / Action Manager / 数据库。agent、profile、action 均通过插件机制动态发现。

---

## 7.2 Streamlit：快速打造聊天界面

### 7.2.1 构建 ChatGPT clone
- 文件 `chatgpt_clone_response.py` 展示最小可用的聊天应用：
  - `st.session_state` 存储模型名与对话历史。
  - `st.chat_message` 循环渲染历史消息。
  - `st.chat_input` 捕获用户输入；当用户提交时，追加到 `session_state` 并调用 `client.chat.completions.create(...)`。
  - `st.spinner` 提示“LLM 正在思考”。
- 调试方法：在 VS Code 中配置 `launch.json`，使用 `"module": "streamlit", "args": ["run", "${file}"]`，按 F5 即可。界面如图 7.5。

### 7.2.2 加入流式输出
- `chatgpt_clone_streaming.py` 将 `stream=True`，并用 `st.write_stream(stream)` 边接收边展示（图 7.6），无需再显示 spinner。
- 这个例子证明：Streamlit 允许开发者纯用 Python 构建现代化的聊天 UI，后续 Nexus 亦沿用这一模式。

---

## 7.3 在 Nexus 中定义 Profiles / Personas
- Profile 通过 `nexus/nexus_base/nexus_profiles/*.yaml` 描述，包含：名称、头像符号、persona 文案、可用动作等（图 7.7）。
- 示例 `fiona.yaml`：
  ```yaml
  agentProfile:
    name: "Finona"
    avatar: "?"
    persona: "你是一个健谈、用食人魔语言回答一切问题的 AI。"
    actions:
      - search_wikipedia
    knowledge: null
    memory: null
    evaluators: null
    planners: null
    feedback: null
  ```
- 保存后重启 Nexus，即可在界面选择新 persona（图 7.8）。profile 实际上就是系统提示 + 动作声明，决定代理如何开场、如何回应。

---

## 7.4 Agent Engine 的结构
- 所有代理引擎继承自 `BaseAgent`（位于 `nexus_base/agent_manager.py`），实现：加载 persona、拼接消息、调用底层 LLM、处理工具调用等。
- 目前示例为 `OpenAIAgent`，核心流程（节选自 `oai_agent.py`）：
  1. 将用户输入写入 `self.messages`。
  2. 若启用了工具，则在 `chat.completions.create` 中附上 `tools` 列表与 `tool_choice="auto"`。
  3. 拿到 `response_message.tool_calls` 后，遍历每个函数调用，反射执行实际 Python 函数，再把结果写回消息堆栈。
  4. 再次请求 LLM 生成最终回答。
- 由于采用插件机制，未来可轻松添加“基于 SK 的 agent”“Anthropic agent”等实现，只需放入 `nexus_agents/` 目录即可被发现。

---

## 7.5 为代理添加动作与工具
- 所有动作放在 `nexus/nexus_base/nexus_actions/`，以普通 Python 函数形式存在。
- 通过 `@agent_action` 装饰器注册：
  ```python
  from nexus.nexus_base.action_manager import agent_action

  @agent_action
  def get_current_weather(location, unit="fahrenheit"):
      """获取指定地点的天气"""
      return f"当前 {location} 的气温是 0 {unit}."

  @agent_action
  def recommend(topic):
      """
      System:
        Provide a recommendation for {{topic}} …
      User:
        please …
      """
      pass  # 语义函数只需写提示模板
  ```
- 装饰器负责生成符合 OpenAI Functions 规范的 `tool` 描述（Listing 7.12），包括参数类型、枚举、描述等。
- Nexus 的 OpenAI agent 支持 **并行** 函数调用：LLM 可一次返回多个 `tool_call`，引擎逐个执行并合并结果（Listing 7.13、7.14）。
- Demo：在 Nexus 中选中 persona “Olly”（冷淡语气），启用 `recommend` + `get_current_weather` 两个动作，即可看到代理在一次回复中串联两个工具（图 7.9）。

---

## 7.6 练习
1. **Streamlit 入门**：写一个最简单的输入框 + 按钮页面，点击后把文本显示出来。
2. **创建自定义 persona**：在 Nexus 中新增一个主题鲜明的 profile（如“历史学家”），编写符合 persona 的回答，并在界面实际对话测试。
3. **开发自定义 action**：新增一个动作（如 `fetch_current_news`），分别做成本地函数和语义函数两个版本，集成后在 Nexus 内调用验证。
4. **接入第三方 API**：挑选任意公开接口（天气/新闻等），实现含错误处理的 action，并在 Nexus 中测试其稳健性。

---

## 本章小结
- **Nexus**：本书配套的开源代理实验平台，以 Streamlit 提供聊天 UI，可扩展 profile、action、agent 引擎等。
- **Streamlit**：让 Python 开发者快速构建交互式聊天页面，支持状态管理、流式输出、云部署等特性。
- **Profiles/Personas**：通过 YAML 描述代理身份、语气与可用动作，是塑造代理行为的基础。
- **Actions/Tools**：Nexus 同时支持语义函数与本地函数，借助 OpenAI Function 规范在 LLM 中被调用，可并行执行。
- **可扩展性**：凭借插件架构，任何人都能轻松新增 agent、profile、action；未来还将覆盖 API、Discord Bot 等部署形态。

下一章将继续深化代理能力，探讨如何为代理加入检索式记忆与知识库。


---

# AI-Agents-in-Action-Codex中文翻译版-第8章

## 第8章 理解代理的记忆与知识

本章聚焦“检索增强生成（RAG）”如何为代理提供长期知识与记忆。我们先区分记忆/知识与提示工程策略的关系，再逐步实践：从 TF–IDF、余弦相似度到 OpenAI Embedding、Chroma DB、LangChain 文档加载/切分/检索，最后在 Nexus 中构建知识库与多种记忆库（对话、语义、情节、程序等），并讨论记忆/知识压缩的必要性。

---

## 8.1 记忆与检索在代理中的角色
- **知识**：外部文档（PDF、HTML、代码等）通过 RAG 提供上下文，帮助回答问题或引用资料。
- **记忆**：来自会话或交互日志的“事实与偏好”，可视为 RAG 机制在对话层面的应用。
- **提示工程映射**：
  - `Provide Reference Text` → 使用文档知识；
  - `Use External Tools` → 通过检索工具补充上下文；
  - `Memory` 策略 → 把历史对话或任务片段重新注入提示。

## 8.2 RAG 基础
1. **离线阶段**：加载文档 → 切分 chunk → 生成向量 → 存入向量库。
2. **在线阶段**：用户查询 → 同样嵌入为向量 → 语义相似度检索 → 将检索结果填入 Prompt → 调用 LLM 生成回答（图 8.2）。
3. **记忆版 RAG**：相同流程，只是数据源换成会话片段或提炼过的记忆（图 8.3）。

## 8.3 语义搜索与文档索引
### 8.3.1 TF–IDF + 余弦相似度
- 以“天空是蓝色而美丽”为例，计算 `TF=1/6`、`IDF=log10(8/4)`，得到 `TF–IDF≈0.05`。
- 使用 `TfidfVectorizer` + `cosine_similarity`（Listing 8.1–8.2）比较文档之间的向量距离，得分范围 -1~1（相似度）或 0~2（距离）（图 8.4、8.5）。
- 简易“向量数据库”示例（Listing 8.3）演示如何根据关键词/短语检索 TF–IDF 向量。

### 8.3.3 使用嵌入（Embeddings）
- OpenAI `text-embedding-ada-002` 生成 1536 维向量，后用 PCA 降至 3 维可视化（Listing 8.4、图 8.6）。
- 相较 TF–IDF，嵌入能够捕捉更丰富的语义关系。

### 8.3.4 引入 Chroma 向量库
- 示例（Listing 8.5）展示如何用 OpenAI Embedding + Chroma DB 存储文本，再通过余弦距离（越小越相关）查询相似片段。

## 8.4 使用 LangChain 构建 RAG
- LangChain 流程（图 8.7、8.8）：文档加载 → 切分 → 嵌入 → 存储 → 检索链。

### 8.4.1 文本切分
- `UnstructuredHTMLLoader` 读取 Mother Goose 童谣；
- `RecursiveCharacterTextSplitter` 以 100 字符 + 25 重叠切块；
- 嵌入后可语义查询（Listing 8.6）。

### 8.4.2 Token 级切分
- `CharacterTextSplitter.from_tiktoken_encoder(chunk_size=50, overlap=10)` 以 token 粒度切块；
- `Chroma.from_documents` + `OpenAIEmbeddings` 建立向量库；
- 查询“谁让女孩哭？”即可返回语义匹配的韵文，如 Georgy Porgy（Listing 8.7-8.8）。

## 8.5 在 Nexus 中搭建知识库
1. 安装/运行 Nexus（Listing 8.9）。
2. 在 “Knowledge Store Manager” 新建知识库，导入 `back_to_the_future.txt` 剧本（图 8.9）。
3. 等待切分/嵌入完成后，可在“Embeddings”界面查看 3D 分布并运行查询（图 8.10）。
4. 在 Chat 页面为代理启用 `time_travel` 知识库（图 8.11），便可围绕剧本提问。
5. “Configuration” 标签允许选择切分器、chunk size、overlap 等（图 8.12）。

## 8.6 构建代理记忆
### 8.6.1 基础记忆
- 代理记忆可映射到人类的感官记忆、短期记忆、长期记忆（图 8.13）。
- Nexus 记忆库流程（图 8.14）：
  1. 用户输入 → 通过记忆函数抽取事实/偏好 → 嵌入存储。
  2. 询问时再做语义检索，将“记得的事实”注入 Prompt。
- 操作步骤：
  - 在 Memory 页面创建 `my_memory`，选择 Agent Engine，添加若干个人偏好（图 8.15）。
  - 记忆函数（Listing 8.10）会将对话总结为 JSON 结构再入库。
  - 在 Chat 中启用该记忆库，测试代理是否能记住偏好（图 8.16）。

### 8.6.2 语义、情节、程序记忆
- 语义记忆（Semantic）、情节记忆（Episodic）、程序记忆（Procedural）需要额外的“语义增强”步骤：把输入转换成多条“针对该记忆类型的提问”，再分别检索（图 8.17）。
- Nexus 中可在 Memory 配置页选择 Memory Type = `SEMANTIC`，查看对应的记忆/增强/总结提示词（图 8.18）。
- 图 8.19 展示了同一批事实在“普通记忆”与“语义记忆”中的存储差异。

## 8.7 记忆与知识压缩
- 随时间积累，记忆与知识库会冗余；可通过 **k-means 聚类 + 总结** 来压缩（图 8.20）。
- Nexus 提供压缩工具（图 8.21）：
  - 3D 聚类可视化；
  - 指定 LLM（建议 GPT-4）对每个簇执行 summarization；
  - 适用于知识库（一次性）与记忆库（周期性）。
- 建议策略：
  - 大量冗余时压缩；
  - 视场景决定频率（记忆需定期压缩，知识库通常在导入时压缩即可）；
  - 可多重压缩形成不同粒度的“知识层级”；
  - 甚至可把压缩后的知识作为初始记忆灌入代理。

## 8.8 练习方向
1. **加载/切分新文档**：尝试不同的文本文档与切分参数，观察检索效果。
2. **语义搜索实验**：对比 TF–IDF、Word2Vec、BERT 等向量化方案的检索差异。
3. **定制 RAG 流程**：选定业务场景，用 LangChain 设计并测试专属 RAG pipeline。
4. **知识库 + 压缩实验**：构建知识库，尝试多种切分/压缩策略，观察检索性能变化。
5. **多记忆库构建**：动手创建对话、语义、情节、程序等不同记忆库，并测试压缩后的检索表现。

## 本章小结
- 记忆与知识都是对 RAG 的不同应用：前者关注个体交互，后者聚焦外部文档。
- TF–IDF/余弦相似度是理解语义检索的入门；嵌入 + 向量库（Chroma、OpenAI Embedding）提供更精确的语义匹配。
- LangChain 抽象了“加载→切分→嵌入→存储→检索”流程，便于快速搭建 RAG。
- Nexus 的知识库与记忆库实现了文档问答、偏好记忆、语义记忆等功能，并允许自定义切分、记忆函数、压缩策略。
- 记忆/知识压缩通过聚类+总结减少冗余，对提升检索效率和回答准确性至关重要。

掌握上述知识后，你即可为代理构建属于自己的“长期记忆”与“权威知识库”，并在后续章节中进一步叠加推理、评估与规划能力。


---

# AI-Agents-in-Action-Codex中文翻译版-第9章

## 第9章 使用 Prompt Flow 精通代理提示

本章聚焦 OpenAI “Test Changes Systematically” 策略，借助微软开源工具 **prompt flow** 实现“构建 → 评估 → 比较”提示迭代。我们将提示（prompt）视作代理 profile 的核心：它不仅包含 persona，还能扩展至工具、记忆、规划、反馈等组件。章内内容依次涵盖：迭代提示的重要性、profile 构成、prompt flow 的安装与运行、如何创建/部署/批量执行 prompt，以及用 **rubric + grounding** 自动评估不同提示版本。

---

## 9.1 为何需要系统化提示工程
1. **迭代提问示例**：直接问 “can you recommend something” → 需补充更多上下文；加入系统提示 `system: You are an expert on time travel movies.` 后，再提问即可得到更好回答。
2. **多轮对话 vs. 系统化流程**：手动在 ChatGPT 里反复提问虽然可行，但难以记录与评估。图 9.5 展示了结构化方法：编写提示 → 运行 → 评估 → 若输出符合预期则定版，否则继续修改。

## 9.2 代理 Profile 与 Persona
- Profile = 构成代理的全套提示：persona、规则、工具说明、记忆/知识指引、推理/规划/反馈要求等（图 9.6）。
- Persona 只是 Profile 的“语气 + 背景”部分；真正的 profile 还要对接 actions、memory 等组件。

## 9.3 Prompt Flow 实战入门
### 9.3.1 环境准备
- 需安装 VS Code、prompt flow 扩展、Python 虚拟环境，并 `pip install promptflow promptflow-tools`。
- 在 VS Code 的 prompt flow 面板创建 LLM 连接（图 9.7、图 9.8）。
- 打开 `chapter_09/promptflow/simpleflow/flow.dag.yaml`，使用 Visual Editor（图 9.9），设置 LLM block（图 9.10），点击 Run 即可看到基础推荐结果（图 9.11）。

### 9.3.2 基于 Jinja2 的 Profile 模板
- prompt flow 默认使用 **Jinja2** 生成 system/user prompt。修改 `recommended.jinja2` 即可改变 persona/提示文本（图 9.12）。

### 9.3.3 部署为本地应用
- 在 Flow Editor 中点 Build → Local App（图 9.13），即可生成网页（图 9.14），填写 `user_input` 后体验实时推荐。

## 9.4 Profiles 的变体与输入扩展
- 将 flow 改成 `recommender_with_variations`，新增输入 `subject/format/genre/custom`（图 9.15）。
- 输入可来自传统 UI（Option A）或代理对话（Option B）（图 9.16）。
- 在 Variants 中创建多个 Jinja2 模板；variant 0 把参数注入 user prompt；variant 1 注入 system prompt（图 9.17）。点击 “Run All” 可比较两个版本（图 9.18）。

## 9.5 Rubric 与 Grounding
- **Rubric** = 评价标准。构建步骤：明确目标 → 设定维度（subject/format/genre 等）→ 评分尺度（1~5）→ 描述每档标准（表 9.2）→ 应用、平均分、保持一致性 → 不断迭代。
- **Grounding** = 检查输出是否符合 Rubric/上下文要求。

## 9.6 用 LLM Prompt 做自动评分
- 在 `recommender_with_LLM_evaluation` flow 中添加 `evaluate_recommendation` block，模板内含 rubric 描述（图 9.19）。
- 运行后生成 JSON 文本，每条推荐都有 subject/format/genre 的 1-5 分（Listing 9.1）。

## 9.7 取得“完美提示”的方法
### 9.7.1 解析 LLM 评分输出
- 新增 `parsing_results` Python block（Listing 9.2），把字符串解析成字典列表，方便进一步处理（图 9.20）。

### 9.7.2 批量运行（Batch Processing）
1. 准备 JSONL 批量输入（示例见 Listing 9.3/9.4）。
2. 在 Flow Editor 中点击“Batch”（烧杯图标），选 JSONL 文件（图 9.21、9.22），prompt flow 会自动并发执行并记录日志。
3. 在 prompt flow 扩展的 Run History 中可查看每条运行，甚至查看 API 调用细节（图 9.23）。

### 9.7.3 评估与对比 Run
1. 使用 `evaluate_groundings` flow：`line_process.py` 计算每个推荐的平均分（Listing 9.3）；`aggregate.py` 聚合所有 run 的平均分并输出指标（Listing 9.4，图 9.24）。
2. 运行方法：在 flow 中选择 “Existing Run” 批量数据（图 9.25），执行后在 prompt flow 扩展里用 “Visualize Runs” 对比不同 Prompt 版本的指标（图 9.26）。示例显示：将参数注入 system prompt (variant 1) 获得更高评分。

## 9.7.4 练习建议
1. 为推荐场景创建新的 Prompt 变体，批量评估其效果。
2. 给 rubric 增添新指标并更新评估流程。
3. 设计全新用例 + Prompt + Rubric，比较不同场景下的表现。
4. 使用 LM Studio 托管本地 LLM，与 prompt flow 一起测试开源模型。
5. 应用“Write Clear Instructions”策略构建更多 prompt，并用 prompt flow 评估。

## 本章结论
- 代理 profile = 多个提示组件的集合，可扩展至工具/记忆/规划/反馈等维度。
- Prompt flow 提供“图形化编辑 + 模板管理 + 本地运行 + 批量评估 + 结果可视化”等全流程能力，非常适合系统化提示工程。
- LLM Prompt 可用作“评分器”，配合 rubric 在无人工介入下完成 grounding，易于量化不同 prompt 的表现。
- Batch Run + Evaluate Flow + Run Visualization 构成完整的“测试-比较-选择最佳 prompt”的闭环。

借助这些方法，你可以用 prompt flow 构建出高质量、可验证、易部署的代理 profile，为后续章节中的推理、规划与评估奠定基础。


---

