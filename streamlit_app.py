import streamlit as st
import random
import time

# -------------------- 页面配置 --------------------
st.set_page_config(
    page_title="小红书爆款标题生成器",
    page_icon="✍️",
    layout="centered"
)

# -------------------- 自定义CSS（优化版）--------------------
st.markdown("""
<style>
/* 整体背景 */
.stApp { background-color: #fdf2f2; }

/* 标题样式 */
h1 { color: #d14b4b; font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
.subhead { text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem; }

/* 输入框美化 */
.stTextInput > div > div > input { 
    border-radius: 30px; border: 1px solid #ffb7b7; padding: 12px 20px; 
    font-size: 1.1rem; background-color: white; box-shadow: 0 2px 8px rgba(255, 183, 183, 0.2); 
}
.stTextInput > div > div > input:focus { border-color: #ff6b6b; box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1); }

/* 按钮样式 */
.stButton > button { 
    background: linear-gradient(135deg, #ff6b6b, #ff8e8e); color: white; border: none; border-radius: 30px; 
    padding: 12px 30px; font-size: 1.1rem; font-weight: 600; width: 100%; transition: all 0.3s; 
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3); 
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 18px rgba(255, 107, 107, 0.4); }

/* 卡片容器（重点修改：增加内边距和阴影） */
.title-card { 
    background-color: white; border-radius: 20px; padding: 25px; margin: 15px 0; 
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); border-left: 5px solid #ffb7b7; 
    transition: 0.2s; position: relative; /* 为绝对定位按钮做准备 */ 
}
.title-card:hover { box-shadow: 0 8px 25px rgba(255, 183, 183, 0.3); }

/* 标题文本 */
.title-text { 
    font-size: 1.3rem; font-weight: 600; color: #333; margin-bottom: 15px; line-height: 1.4; 
    word-wrap: break-word; /* 防止长单词溢出 */
}

/* 评分标签 */
.score-badge { 
    background-color: #ffe8e8; color: #d14b4b; border-radius: 30px; padding: 5px 12px; 
    font-size: 0.8rem; font-weight: 600; display: inline-block; margin-right: 8px; 
}

/* 页脚 */
.footer { text-align: center; color: #aaa; margin-top: 50px; font-size: 0.9rem; }

/* 自定义复制按钮样式 */
.copy-btn {
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 15px;
    background-color: #ffdddd;
    border: none;
    color: #d14b4b;
    cursor: pointer;
    transition: 0.2s;
}
.copy-btn:hover {
    background-color: #d14b4b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------- 标题模板库（升级版：分类）--------------------
TEMPLATES = {
    "干货教程": [
        "新手必看！{topic}的{num}个核心技巧，建议收藏",
        "保姆级教程：{topic}从0到1的完整攻略",
        "这{num}个{topic}误区，{group}千万别踩！",
        "手把手教你{topic}，看完就会，{group}也能学会",
        "关于{topic}，这{num}件事你必须知道"
    ],
    "情绪共鸣": [
        "谁懂啊！{topic}真的太{adj}了",
        "我不允许还有人不知道{topic}，真的{adj}哭",
        "被问了{num}遍的{topic}，终于整理出来了",
        "真的后悔没早点{topic}，不然早就{result}",
        "救命！{topic}怎么可以这么{adj}！"
    ],
    "凡尔赛/炫耀": [
        "月薪{salary}，但我真的只花{price}买了{topic}",
        "坦白局：{topic}其实根本不需要花大钱",
        "这{topic}被我{action}后，朋友都说我赚翻了",
        "普通人也能拥有的{topic}，这质感绝了",
        "我不小心把{topic}做成了{result}，这也太值了"
    ],
    "避雷/测评": [
        "这{num}款{topic}真的别买！纯纯大冤种",
        "{topic}红黑榜：只有这款能打",
        "真实测评：{topic}到底值不值{price}？",
        "千万别{topic}！除非你想...",
        "避雷！{topic}的{num}个假象，看完省{price}"
    ]
}

# 所有风格列表
STYLE_OPTIONS = list(TEMPLATES.keys())

# 常用变量库
NUMBERS = ["3", "5", "8", "10", "15"]
GROUPS = ["小白", "新手", "打工人", "学生党", "宝妈"]
ADJECTIVES = ["绝", "香", "炸", "爽", "好用", "离谱", "惊艳"]
SALARY_RANGE = ["3k", "5k", "8k", "1w", "2w"]
PRICE_RANGE = ["一杯奶茶钱", "不到100块", "0成本", "9.9包邮", "一顿饭钱"]

# -------------------- 智能生成函数（核心逻辑）--------------------
def generate_titles(topic, style, num=8):
    results = []
    
    # 如果选择“全部风格”，则混合生成
    if style == "全部风格":
        all_templates = []
        for temp_list in TEMPLATES.values():
            all_templates.extend(temp_list)
    else:
        all_templates = TEMPLATES[style]
    
    # 确保生成数量
    while len(results) < num:
        # 1. 随机选择模板
        template = random.choice(all_templates)
        
        # 2. 智能替换占位符
        title = template
        
        # 替换 {topic}
        title = title.replace("{topic}", topic)
        
        # 替换 {num}
        if "{num}" in title:
            title = title.replace("{num}", random.choice(NUMBERS))
            
        # 替换 {group}
        if "{group}" in title:
            title = title.replace("{group}", random.choice(GROUPS))
            
        # 替换 {adj}
        if "{adj}" in title:
            title = title.replace("{adj}", random.choice(ADJECTIVES))
            
        # 替换 {salary}
        if "{salary}" in title:
            title = title.replace("{salary}", random.choice(SALARY_RANGE))
            
        # 替换 {price}
        if "{price}" in title:
            title = title.replace("{price}", random.choice(PRICE_RANGE))
            
        # 替换 {action}
        if "{action}" in title:
            actions = ["改造", "翻新", "复刻", "升级"]
            title = title.replace("{action}", random.choice(actions))
            
        # 替换 {result}
        if "{result}" in title:
            results_list = ["省下一个月工资", "被老板夸爆", "美到窒息", "效率翻倍"]
            title = title.replace("{result}", random.choice(results_list))
        
        # 3. 随机添加Emoji (60%概率)
        emojis = ["🔥", "✨", "💥", "🌟", "🎉", "💯", "😱", "🤫", "👀", "💪", "🌸"]
        if random.random() > 0.4:
            emoji = random.choice(emojis)
            # 50%概率加在开头，50%加在结尾
            if random.random() > 0.5:
                title = f"{emoji} {title}"
            else:
                title = f"{title} {emoji}"
        
        # 4. 去重
        if title not in results:
            results.append(title)
    
    return results[:num]

# -------------------- 评分函数（微调）--------------------
def score_title(title):
    score = 0
    if any(char.isdigit() for char in title):
        score += 2
    if "!" in title or "！" in title:
        score += 1
    if any(emoji in title for emoji in ["🔥", "✨", "💥", "🌟", "🎉"]):
        score += 2
    if 8 < len(title) < 20: # 修正长度判断
        score += 2
    if "?" in title or "？" in title:
        score += 1
    if any(word in title for word in ["后悔", "千万别", "避雷", "紧急", "绝了", "救命"]):
        score += 2
        
    return min(score, 10)

# -------------------- 页面主体 --------------------
st.markdown("<h1>✍️ 小红书爆款标题生成器</h1>", unsafe_allow_html=True)
st.markdown('<p class="subhead">输入你的笔记主题，选择风格，AI帮你一键生成高点击率标题</p>', unsafe_allow_html=True)

# --- 新增：风格选择器 ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("", placeholder="例如：口红试色、副业搞钱、租房改造", key="topic_input")
with col2:
    # 默认选项是“全部风格”
    style_choice = st.selectbox("选择风格", ["全部风格"] + STYLE_OPTIONS)

st.markdown("<br>", unsafe_allow_html=True) # 增加一点间距

# 生成按钮
if st.button("🚀 一键生成爆款标题", type="primary", use_container_width=True) and topic:
    with st.spinner("AI 正在为你构思..."):
        time.sleep(0.5) # 模拟思考
    titles = generate_titles(topic, style_choice, num=10)
    st.session_state["generated_titles"] = titles
    st.session_state["topic"] = topic
    st.session_state["style"] = style_choice
# 如果页面刷新但有缓存，或者已经生成过
elif "generated_titles" in st.session_state and st.session_state.get("topic") == topic and st.session_state.get("style") == style_choice:
    titles = st.session_state["generated_titles"]
else:
    titles = []
    st.session_state["generated_titles"] = []

# --- 展示结果 ---
if titles:
    st.markdown("---")
    st.markdown(f"#### 🎯 为你生成的 {len(titles)} 个标题：")
    
    # 使用自定义HTML和JS实现复制功能（Streamlit原生不支持直接复制文本到剪贴板，这里用一个小技巧）
    for i, title in enumerate(titles):
        score = score_title(title)
        stars = "⭐" * (score // 2) + "✨" * (score % 2)
        
        # 生成唯一的按钮ID
        button_id = f"copy_{i}"
        
        # 构建卡片HTML
        card_html = f"""
        <div class="title-card">
            <div class="title-text">{title}</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                <span> <span class="score-badge">{stars} {score}/10</span> <span style="color: #999; font-size:0.8rem;">爆款评分</span> </span>
                <button class="copy-btn" id="{button_id}" onclick="copyText('{title.replace("'", "\\'")}')">📋 复制</button>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
    # 注入JavaScript实现复制功能
    st.markdown("""
    <script>
    function copyText(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        // 简单的反馈（实际项目中可以用Toast）
        const button = event.target;
        const originalText = button.innerText;
        button.innerText = "✅ 已复制";
        setTimeout(() => { button.innerText = originalText; }, 2000);
    }
    </script>
    """, unsafe_allow_html=True)

    # 重新生成按钮
    if st.button("🔄 换一批标题", key="regenerate"):
        st.session_state["generated_titles"] = generate_titles(topic, style_choice, num=10)
        st.rerun()

else:
    # 首次打开或未输入时的示例
    if not topic:
        st.markdown("#### 🌟 热门示例（点击输入框开始）")
        example_pairs = [
            ("美妆", "黄皮逆袭！这支口红显白到犯规！🔥"),
            ("探店", "周末别再躺了！这3个宝藏地没人告诉你📍"),
            ("职场", "月入5位数的秘密，藏在我的手机相册里💼"),
            ("情感", "谁懂啊！这个早秋穿搭真的太减龄了👗")
        ]
        for cat, ex in example_pairs:
            st.markdown(f"**{cat}**")
            st.info(ex)

# -------------------- 页脚 --------------------
st.markdown('<div class="footer">💡 让创作更简单 | 基于智能算法生成</div>', unsafe_allow_html=True)
