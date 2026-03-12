import streamlit as st
import random
import time

st.set_page_config(page_title="✨ 爆款标题工坊", page_icon="✍️", layout="centered")

# -------------------- 高级CSS（含移动端适配）--------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #f9f5ff 0%, #f0e7ff 100%);
    }
    
    h1 {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.2rem;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .subhead {
        text-align: center;
        color: #6B7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #E5E7EB;
        border-radius: 20px;
        padding: 16px 24px;
        font-size: 1.1rem;
        background: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        transition: all 0.3s;
        width: 100%;  /* 默认占满父容器 */
        color: #333 !important;  /* 确保文字可见 */
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8B5CF6;
        box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        border: none;
        border-radius: 40px;
        padding: 16px 32px;
        font-weight: 600;
        font-size: 1.2rem;
        color: white;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 35px rgba(139, 92, 246, 0.4);
    }
    
    .title-card {
        background: rgba(255,255,255,0.8);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 24px;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 20px 40px rgba(0,0,0,0.03);
        transition: all 0.3s;
    }
    
    .title-card:hover {
        background: white;
        box-shadow: 0 30px 60px rgba(139, 92, 246, 0.12);
    }
    
    .title-text {
        font-size: 1.4rem;
        font-weight: 600;
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .score-badge {
        background: linear-gradient(135deg, #F3E8FF 0%, #FFE1F0 100%);
        color: #8B5CF6;
        border-radius: 40px;
        padding: 6px 18px;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid #8B5CF6;
    }
    
    .footer {
        text-align: center;
        color: #9CA3AF;
        margin-top: 60px;
        font-size: 0.9rem;
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #8B5CF6, #EC4899, transparent);
        margin: 30px 0;
    }
    
    /* ========== 移动端优化 ========== */
    @media only screen and (max-width: 600px) {
        h1 {
            font-size: 2.2rem !important;
        }
        .subhead {
            font-size: 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        .stTextInput > div > div > input {
            font-size: 1rem !important;
            padding: 12px 16px !important;
        }
        .stButton > button {
            font-size: 1rem !important;
            padding: 12px 20px !important;
        }
        .title-card {
            padding: 16px !important;
        }
        .title-text {
            font-size: 1.2rem !important;
        }
        .score-badge {
            font-size: 0.8rem !important;
            padding: 4px 12px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -------------------- 标题模板 --------------------
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

EMOJIS = ["🔥", "✨", "💥", "🌟", "🎉", "💯", "😱", "🤫", "👀", "💪", "🌸", "🍦", "💰"]

def score_title(title):
    score = 0
    if any(char.isdigit() for char in title): score += 2
    if "!" in title or "！" in title: score += 1
    if any(emoji in title for emoji in ["🔥", "✨", "💥", "🌟", "🎉"]): score += 2
    if 8 <= len(title) <= 20: score += 2
    if "?" in title or "？" in title: score += 1
    if any(word in title for word in ["后悔", "千万别", "紧急"]): score += 2
    return min(score, 10)

def generate_titles(topic, num=8):
    results = []
    selected = random.sample(TEMPLATES, min(num, len(TEMPLATES)))
    for template in selected:
        title = template.replace("{topic}", topic)
        if random.random() > 0.3:
            emoji = random.choice(EMOJIS)
            title = f"{emoji} {title}" if random.random() > 0.5 else f"{title} {emoji}"
        results.append(title)
    while len(results) < num:
        title = f"{random.choice(EMOJIS)} {topic}的{random.randint(1,9)}个秘密"
        results.append(title)
    return results[:num]

# -------------------- 页面主体 --------------------
st.markdown("<h1>✨ 爆款标题工坊</h1>", unsafe_allow_html=True)
st.markdown('<p class="subhead">输入主题，3秒生成10个小红书爆款标题</p>', unsafe_allow_html=True)

# 布局优化：输入框和生成按钮并排（移动端自动换行）
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("", placeholder="例如：口红试色、周末探店", label_visibility="collapsed")
with col2:
    generate = st.button("🚀 生成", use_container_width=True)

if generate and topic:
    with st.spinner("AI 正在爆肝创作..."):
        time.sleep(1.2)
        titles = generate_titles(topic, num=10)
        st.session_state["generated_titles"] = titles
elif "generated_titles" not in st.session_state:
    st.session_state["generated_titles"] = []

if st.session_state["generated_titles"]:
    st.markdown("---")
    st.markdown(f"#### 为你生成的 {len(st.session_state['generated_titles'])} 个标题")
    
    for i, title in enumerate(st.session_state["generated_titles"]):
        score = score_title(title)
        stars = "⭐" * (score // 2) + "✨" * (score % 2)
        
        with st.container():
            st.markdown(f"""
            <div class="title-card">
                <div class="title-text">{title}</div>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <span class="score-badge">{stars} {score}/10 热度</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.code(title, language="text", line_numbers=False)
        
        if (i+1) % 2 == 0 and i < len(st.session_state["generated_titles"])-1:
            st.markdown("---")
    
    if st.button("🔄 换一批标题"):
        st.session_state["generated_titles"] = generate_titles(topic, num=10)
        st.rerun()
else:
    st.markdown("#### 🌟 试试这些爆款模板")
    examples = [
        "🔥 黄皮逆袭！这支口红显白到犯规！",
        "周末别再躺了！这3个宝藏地没人告诉你",
        "月入5位数的秘密，藏在我的手机相册里",
        "谁懂啊！这个早秋穿搭真的太减龄了"
    ]
    for ex in examples:
        st.info(ex)

st.markdown('<div class="footer">⚡ 完全免费 · 为小红书博主而生 · 代码开源</div>', unsafe_allow_html=True)
