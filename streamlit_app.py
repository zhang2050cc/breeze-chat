import streamlit as st
import random
import time

# -------------------- 页面配置 --------------------
st.set_page_config(
    page_title="小红书爆款标题生成器",
    page_icon="✍️",
    layout="centered"
)

# -------------------- 全局自定义CSS（高级版：莫兰迪紫+玻璃态）--------------------
st.markdown("""
<style>
/* 全局重置与背景 */
:root {
    --primary-color: #8B7E99;    /* 莫兰迪紫（主色） */
    --primary-hover: #7A6D8A;    /* 主色深色版 */
    --secondary-color: #E2BFBF;  /* 莫兰迪粉（辅助色） */
    --text-dark: #2D2D2D;
    --text-light: #6B6B6B;
    --border-radius: 16px;
    --shadow-light: 0 8px 32px rgba(139, 126, 153, 0.1);
    --shadow-card: 0 8px 32px rgba(139, 126, 153, 0.05);
}

/* 整体背景：极浅的灰紫，营造氛围 */
.stApp {
    background: linear-gradient(135deg, #f9f7fa 0%, #fcfafa 100%);
    color: var(--text-dark);
}

/* 容器内边距优化 */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 800px;
}

/* 标题样式：去色，强调留白 */
h1 {
    color: var(--primary-color) !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-bottom: 0.5rem !important;
    font-family: 'Helvetica Neue', sans-serif;
    letter-spacing: -0.5px;
}
.subhead {
    text-align: center;
    color: var(--text-light) !important;
    font-size: 1.2rem !important;
    margin-bottom: 3rem !important;
    font-weight: 300;
}

/* 输入框美化：玻璃态设计 */
.stTextInput > div > div > input {
    border-radius: var(--border-radius) !important;
    border: 1px solid #e0e0e0 !important;
    padding: 15px 20px !important;
    font-size: 1.1rem !important;
    background-color: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(10px) !important; /* 关键：毛玻璃效果 */
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.3s ease;
}
.stTextInput > div > div > input:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(139, 126, 153, 0.15) !important;
    transform: translateY(-1px);
}

/* 按钮样式：悬浮感 */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
    color: white;
    border: none;
    border-radius: var(--border-radius) !important;
    padding: 15px 30px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    box-shadow: var(--shadow-light);
    letter-spacing: 1px;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 24px rgba(139, 126, 153, 0.25) !important;
    background: linear-gradient(135deg, var(--primary-hover), #6B5F7C);
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* 卡片容器（玻璃态设计） */
.title-card {
    background: rgba(255, 255, 255, 0.7); /* 半透明白 */
    backdrop-filter: blur(10px); /* 毛玻璃核心 */
    border-radius: var(--border-radius);
    padding: 25px;
    margin: 15px 0;
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(255, 255, 255, 0.5);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    border-left: 4px solid var(--primary-color); /* 左侧强调条 */
}
.title-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(139, 126, 153, 0.15);
    background: rgba(255, 255, 255, 0.9);
}

/* 标题文本：优雅的排版 */
.title-text {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 15px;
    line-height: 1.5;
    word-wrap: break-word;
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 评分标签：精致胶囊 */
.score-badge {
    background-color: rgba(139, 126, 153, 0.1);
    color: var(--primary-color);
    border-radius: 30px;
    padding: 6px 14px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    border: 1px solid rgba(139, 126, 153, 0.2);
}
.stars {
    color: #FFD700; /* 金色星星 */
    margin-right: 4px;
}

/* 页脚 */
.footer {
    text-align: center;
    color: #aaa;
    margin-top: 50px;
    font-size: 0.9rem;
    opacity: 0.7;
}

/* 自定义复制按钮样式（更精致） */
.copy-btn {
    position: absolute;
    top: 12px;
    right: 12px;
    font-size: 0.8rem;
    padding: 6px 12px;
    border-radius: 12px;
    background-color: rgba(139, 126, 153, 0.1);
    border: 1px solid rgba(139, 126, 153, 0.3);
    color: var(--primary-color);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}
.copy-btn:hover {
    background-color: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
}

/* 示例卡片的样式优化 */
.stAlert {
    border-radius: var(--border-radius) !important;
    border: none !important;
    background: rgba(255, 255, 255, 0.5) !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: var(--shadow-card);
}
</style>
""", unsafe_allow_html=True)

# -------------------- 标题模板库（升级版：分类）--------------------
# (这部分代码保持不变，为了节省篇幅，如果需要完整版请看上一轮回复)
# ... (保留你原来的 TEMPLATES, STYLE_OPTIONS, NUMBERS 等定义) ...
# 注意：这里为了阅读方便省略了中间的逻辑代码，实际使用时请保留原样
# -------------------- 智能生成函数（核心逻辑）--------------------
# ... (保留 generate_titles 和 score_title 函数) ...

# -------------------- 页面主体 --------------------
st.markdown("<h1>✍️ 爆款标题生成器</h1>", unsafe_allow_html=True)
st.markdown('<p class="subhead">输入主题，选择风格，AI一键生成高点击率标题</p>', unsafe_allow_html=True)

# --- 新增：风格选择器 ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("", placeholder="例如：口红试色、副业搞钱、租房改造", key="topic_input")
with col2:
    style_choice = st.selectbox("选择风格", ["全部风格"] + STYLE_OPTIONS)

st.markdown("<br>", unsafe_allow_html=True)

# 生成按钮逻辑 (保持不变)
if st.button("🚀 一键生成爆款标题", type="primary", use_container_width=True) and topic:
    with st.spinner("AI 正在为你构思..."):
        time.sleep(0.5)
        titles = generate_titles(topic, style_choice, num=10)
        st.session_state["generated_titles"] = titles
        st.session_state["topic"] = topic
        st.session_state["style"] = style_choice
elif "generated_titles" in st.session_state and st.session_state.get("topic") == topic and st.session_state.get("style") == style_choice:
    titles = st.session_state["generated_titles"]
else:
    titles = []
    st.session_state["generated_titles"] = []

# --- 展示结果 ---
if titles:
    st.markdown("---")
    st.markdown(f"#### 🎯 为你生成的 {len(titles)} 个标题：")

    for i, title in enumerate(titles):
        score = score_title(title)
        # 优化评分显示：使用金色星星
        stars = "".join(["⭐" for _ in range(score // 2)]) + ("✨" if score % 2 else "")
        
        button_id = f"copy_{i}"
        card_html = f"""
        <div class="title-card">
            <div class="title-text">{title}</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
                <span>
                    <span class="score-badge"><span class='stars'>{stars}</span> {score}/10</span>
                </span>
                <button class="copy-btn" id="{button_id}" onclick="copyText('{title.replace("'", "\\'")}')">📋 复制</button>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # 注入JavaScript (保持不变)
    st.markdown("""
    <script>
    function copyText(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        const button = event.target;
        const originalText = button.innerText;
        button.innerText = "✅ 已复制";
        setTimeout(() => { button.innerText = originalText; }, 2000);
    }
    </script>
    """, unsafe_allow_html=True)

    if st.button("🔄 换一批标题", key="regenerate"):
        st.session_state["generated_titles"] = generate_titles(topic, style_choice, num=10)
        st.rerun()

else:
    # 首次打开或未输入时的示例（样式微调）
    if not topic:
        st.markdown("#### 💡 热门示例")
        example_pairs = [
            ("美妆", "黄皮逆袭！这支口红显白到犯规！🔥"),
            ("探店", "周末别再躺了！这3个宝藏地没人告诉你📍"),
            ("职场", "月入5位数的秘密，藏在我的手机相册里💼"),
            ("情感", "谁懂啊！这个早秋穿搭真的太减龄了👗")
        ]
        for cat, ex in example_pairs:
            # 使用 st.markdown 并应用了上面的 .stAlert 样式优化
            st.markdown(f"**<span style='color: var(--primary-color);'>{cat}</span>**", unsafe_allow_html=True)
            st.info(ex)

# -------------------- 页脚 --------------------
st.markdown('<div class="footer">💡 让创作更简单 | 专业级排版设计</div>', unsafe_allow_html=True)
