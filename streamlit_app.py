import streamlit as st
import random
import time

# -------------------- 页面配置 --------------------
st.set_page_config(
    page_title="小红书爆款标题生成器",
    page_icon="✍️",
    layout="centered"
)

# -------------------- 自定义CSS（让界面更小红书）--------------------
st.markdown("""
<style>
    /* 整体背景 */
    .stApp {
        background-color: #fdf2f2;  /* 柔光粉 */
    }
    /* 标题样式 */
    h1 {
        color: #d14b4b;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subhead {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    /* 输入框美化 */
    .stTextInput > div > div > input {
        border-radius: 30px;
        border: 1px solid #ffb7b7;
        padding: 12px 20px;
        font-size: 1.1rem;
        background-color: white;
        box-shadow: 0 2px 8px rgba(255, 183, 183, 0.2);
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff6b6b;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
    }
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(255, 107, 107, 0.4);
    }
    /* 卡片容器 */
    .title-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #ffb7b7;
        transition: 0.2s;
    }
    .title-card:hover {
        box-shadow: 0 8px 25px rgba(255, 183, 183, 0.3);
    }
    /* 标题文本 */
    .title-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 10px;
        line-height: 1.4;
    }
    /* 评分标签 */
    .score-badge {
        background-color: #ffe8e8;
        color: #d14b4b;
        border-radius: 30px;
        padding: 5px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 8px;
    }
    /* 复制代码块背景透明（融合卡片） */
    .stCodeBlock {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .stCodeBlock pre {
        background-color: #f9f9f9 !important;
        border-radius: 12px !important;
        border: 1px solid #ffdddd !important;
        font-size: 0.9rem !important;
    }
    /* 页脚 */
    .footer {
        text-align: center;
        color: #aaa;
        margin-top: 50px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- 标题模板库（小红书爆款结构）--------------------
TEMPLATES = [
    "千万别{topic}！否则你会……",
    "{topic}的3个秘诀，最后一个绝了！",
    "谁懂啊！{topic}真的太好用了",
    "抄作业！{topic}这样发pyq被赞爆",
    "后悔没早点知道！{topic}的隐藏玩法",
    "为了{topic}，我放弃了所有其他",
    "打工人必备{topic}，不到100块！",
    "{topic}翻车现场？其实是真香",
    "我不允许还有人不知道{topic}",
    "{topic}测评：到底哪个值得买？",
    "月入5位数的秘密，藏在{topic}里",
    "紧急通知！{topic}要这样才有效",
    "被问了800遍的{topic}，终于来了",
    "{topic}避雷指南，小白必看",
    "普通人也能学会的{topic}技巧",
    "为什么{topic}突然火了？",
    "{topic}这样搭，绝美！",
    "手把手教你{topic}，一看就会",
    "大数据没骗我！{topic}真的绝",
    "沉浸式体验{topic}，治愈了"
]

# 情绪词/emoji点缀
EMOJIS = ["🔥", "✨", "💥", "🌟", "🎉", "💯", "😱", "🤫", "👀", "💪", "🌸", "🍦", "💰"]

# -------------------- 标题评分函数（简单规则）--------------------
def score_title(title):
    score = 0
    if any(char.isdigit() for char in title):
        score += 2  # 包含数字
    if "!" in title or "！" in title:
        score += 1  # 感叹号
    if any(emoji in title for emoji in ["🔥", "✨", "💥", "🌟", "🎉"]):
        score += 2  # 热门emoji
    if len(title) >= 8 and len(title) <= 20:
        score += 2  # 长度适中
    if "?" in title or "？" in title:
        score += 1  # 提问式
    if "后悔" in title or "千万别" in title or "紧急" in title:
        score += 2  # 情绪词
    # 转化为星星（满分10分）
    stars = min(score, 10)
    return stars

# -------------------- 生成标题函数 --------------------
def generate_titles(topic, num=8):
    results = []
    # 随机选择模板
    selected = random.sample(TEMPLATES, min(num, len(TEMPLATES)))
    for template in selected:
        title = template.replace("{topic}", topic)
        # 随机添加emoji（50%概率）
        if random.random() > 0.3:
            emoji = random.choice(EMOJIS)
            # 随机位置：开头或结尾
            if random.random() > 0.5:
                title = f"{emoji} {title}"
            else:
                title = f"{title} {emoji}"
        results.append(title)
    # 如果不够数量，再随机补充一些变体
    while len(results) < num:
        title = f"{random.choice(EMOJIS)} {topic}的{random.randint(1,9)}个秘密"
        results.append(title)
    return results[:num]

# -------------------- 页面主体 --------------------
st.markdown("<h1>✍️ 小红书爆款标题生成器</h1>", unsafe_allow_html=True)
st.markdown('<p class="subhead">输入你的笔记主题，AI帮你一秒想出10个爆款标题</p>', unsafe_allow_html=True)

# 输入框
topic = st.text_input("", placeholder="例如：口红试色、周末探店、早秋穿搭", key="topic_input")

# 生成按钮
if st.button("🚀 一键生成爆款标题", type="primary") and topic:
    with st.spinner("AI正在绞尽脑汁生成中..."):
        time.sleep(1)  # 模拟思考
        titles = generate_titles(topic, num=10)
        st.session_state["generated_titles"] = titles  # 存到session，防止刷新消失
elif "generated_titles" not in st.session_state:
    st.session_state["generated_titles"] = []

# 如果已经生成过标题，展示出来
if st.session_state["generated_titles"]:
    st.markdown("---")
    st.markdown(f"#### 为你生成的 {len(st.session_state['generated_titles'])} 个标题：")
    
    for i, title in enumerate(st.session_state["generated_titles"]):
        score = score_title(title)
        stars = "⭐" * (score // 2) + "✨" * (score % 2)  # 简单可视化
        
        # 用卡片展示
        with st.container():
            st.markdown(f"""
            <div class="title-card">
                <div class="title-text">{title}</div>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span>
                        <span class="score-badge">{stars} {score}/10</span>
                        <span style="color: #999; font-size:0.8rem;">热度评分</span>
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 提供复制按钮（用st.code自带复制功能）
            st.code(title, language="text", line_numbers=False)
        
        # 每两个标题后加一个分隔线（可选）
        if (i+1) % 2 == 0 and i < len(st.session_state["generated_titles"])-1:
            st.markdown("---")

    # 提供重新生成按钮
    if st.button("🔄 换一批标题", key="regenerate"):
        st.session_state["generated_titles"] = generate_titles(topic, num=10)
        st.rerun()
else:
    # 首次打开时的示例
    if not topic:
        st.markdown("#### 🌟 示例标题（试试输入你的主题）")
        examples = [
            "🔥 黄皮逆袭！这支口红显白到犯规！",
            "周末别再躺了！这3个宝藏地没人告诉你",
            "月入5位数的秘密，藏在我的手机相册里",
            "谁懂啊！这个早秋穿搭真的太减龄了"
        ]
        for ex in examples:
            st.info(ex)

# -------------------- 页脚 --------------------
st.markdown('<div class="footer">Made with ❤️  for小红书博主 | 免费使用 | 代码开源</div>', unsafe_allow_html=True)
