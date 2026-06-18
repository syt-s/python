import streamlit as st

# ========== 页面配置 ==========
st.set_page_config(
    page_title="🎬 中国电影票房数据分析",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 自定义CSS样式 ==========
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.5);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    .metric-card h3 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-card p {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.3rem 0 0 0;
    }
    .feature-tag {
        display: inline-block;
        background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    .feature-tag.green {
        background: linear-gradient(135deg, #51cf66, #40c057);
    }
    .feature-tag.blue {
        background: linear-gradient(135deg, #339af0, #228be6);
    }
    .feature-tag.orange {
        background: linear-gradient(135deg, #ff922b, #fd7e14);
    }
    .feature-tag.purple {
        background: linear-gradient(135deg, #9775fa, #845ef7);
    }
    hr.divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    .tech-badge {
        display: inline-block;
        background: #f0f0f0;
        color: #333;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin: 0.15rem;
        border: 1px solid #ddd;
    }
    .tip-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ========== 侧边栏美化 ==========
with st.sidebar:
    # 项目Logo区域
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">🎬</div>
        <div style="font-size:1.2rem; font-weight:700; color:#667eea;">电影票房分析</div>
        <div style="font-size:0.8rem; color:#888; margin-top:0.3rem;">Python课程设计</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 导航说明
    st.markdown("""
    <div style="padding:0.5rem 0;">
        <div style="font-size:0.9rem; font-weight:600; color:#444; margin-bottom:0.8rem;">
            📍 页面导航
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 页面导航卡片
    nav_items = [
        ("🏠", "main", "项目首页", "项目简介与核心指标"),
        ("📊", "Data Overview", "数据概览", "数据集介绍与统计"),
        ("📈", "Analysis Dashboard", "分析看板", "六大维度交互分析"),
        ("🔍", "Smart Insights", "智能洞察", "相关性+随机森林"),
    ]

    for icon, page, title, desc in nav_items:
        st.markdown(f"""
        <div style="background:#f8f9fa; border-radius:10px; padding:0.8rem; margin:0.4rem 0; 
                    border-left:3px solid #667eea; transition:all 0.2s;">
            <div style="display:flex; align-items:center;">
                <span style="font-size:1.3rem; margin-right:0.5rem;">{icon}</span>
                <div>
                    <div style="font-weight:600; color:#333; font-size:0.95rem;">{title}</div>
                    <div style="font-size:0.75rem; color:#888;">{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 快速统计
    st.markdown("""
    <div style="padding:0.5rem 0;">
        <div style="font-size:0.9rem; font-weight:600; color:#444; margin-bottom:0.8rem;">
            📊 快速统计
        </div>
    </div>
    """, unsafe_allow_html=True)

    import pandas as pd
    df = pd.read_csv('data/movies.csv')
    df['上映日期'] = pd.to_datetime(df['上映日期'])
    df['年份'] = df['上映日期'].dt.year
    df['票房(亿元)'] = df['票房(万元)'] / 10000

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style="text-align:center; background:linear-gradient(135deg,#667eea,#764ba2); 
                    border-radius:8px; padding:0.6rem; color:white;">
            <div style="font-size:1.2rem; font-weight:700;">{len(df)}</div>
            <div style="font-size:0.7rem; opacity:0.9;">电影总数</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="text-align:center; background:linear-gradient(135deg,#f093fb,#f5576c); 
                    border-radius:8px; padding:0.6rem; color:white;">
            <div style="font-size:1.2rem; font-weight:700;">{df['票房(亿元)'].sum():.0f}</div>
            <div style="font-size:0.7rem; opacity:0.9;">总票房(亿)</div>
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div style="text-align:center; background:linear-gradient(135deg,#4facfe,#00f2fe); 
                    border-radius:8px; padding:0.6rem; color:white;">
            <div style="font-size:1.2rem; font-weight:700;">{df['评分'].mean():.1f}</div>
            <div style="font-size:0.7rem; opacity:0.9;">平均评分</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div style="text-align:center; background:linear-gradient(135deg,#43e97b,#38f9d7); 
                    border-radius:8px; padding:0.6rem; color:white;">
            <div style="font-size:1.2rem; font-weight:700;">{int(df['年份'].min())}-{int(df['年份'].max())}</div>
            <div style="font-size:0.7rem; opacity:0.9;">时间跨度</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 技术栈
    st.markdown("""
    <div style="padding:0.5rem 0;">
        <div style="font-size:0.9rem; font-weight:600; color:#444; margin-bottom:0.5rem;">
            🛠️ 技术栈
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:0.3rem;">
            <span style="background:#e3f2fd; color:#1976d2; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Python</span>
            <span style="background:#e8f5e9; color:#388e3c; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Pandas</span>
            <span style="background:#fff3e0; color:#f57c00; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Matplotlib</span>
            <span style="background:#fce4ec; color:#c2185b; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Seaborn</span>
            <span style="background:#f3e5f5; color:#7b1fa2; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Scikit-learn</span>
            <span style="background:#e0f2f1; color:#00796b; padding:0.15rem 0.5rem; border-radius:4px; font-size:0.7rem;">Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 作者信息
    st.markdown("""
    <div style="text-align:center; padding:0.5rem 0;">
        <div style="font-size:0.8rem; color:#888;">
            🎓 Python程序设计课程设计<br>
            📅 2025-2026学年<br>
            📊 120部电影 · 2018-2024
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== 主标题区 ==========
st.markdown('<h1 class="main-title">🎬 中国电影票房数据分析与可视化</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">基于 Python 数据科学全栈技术 | 120部电影 · 2018-2024</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ========== 核心指标卡片 ==========
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(df)}</h3>
        <p>🎬 电影总数</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h3 style="color:white;">{df['票房(亿元)'].sum():.1f}</h3>
        <p style="color:rgba(255,255,255,0.8);">💰 总票房(亿)</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
        <h3 style="color:white;">{df['票房(亿元)'].mean():.2f}</h3>
        <p style="color:rgba(255,255,255,0.8);">📊 平均票房(亿)</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
        <h3 style="color:white;">{df['评分'].mean():.1f}</h3>
        <p style="color:rgba(255,255,255,0.8);">⭐ 平均评分</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
        <h3 style="color:white;">{int(df['年份'].min())}-{int(df['年份'].max())}</h3>
        <p style="color:rgba(255,255,255,0.8);">📅 时间跨度</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ========== 项目简介卡片 ==========
st.markdown("""
<div class="card">
    <h3 style="color:#667eea; margin-top:0;">📌 项目简介</h3>
    <p style="line-height:1.8; color:#444;">
    本项目基于 Python 数据科学全栈技术，对中国电影票房数据进行深度分析与可视化展示。
    通过数据清洗、探索性分析、机器学习建模和交互式可视化，揭示电影市场背后的规律与洞察。
    </p>
</div>
""", unsafe_allow_html=True)

# ========== 六大分析维度 ==========
st.markdown("""
<div class="card">
    <h3 style="color:#667eea; margin-top:0;">🔍 六大分析维度</h3>
    <p style="margin-bottom:1rem; color:#666;">点击下方标签查看各维度详细分析：</p>
    <span class="feature-tag">🎬 档期效应</span>
    <span class="feature-tag green">🎭 类型对决</span>
    <span class="feature-tag blue">👑 头部效应</span>
    <span class="feature-tag orange">🎯 评分陷阱</span>
    <span class="feature-tag purple">📊 相关性分析</span>
    <span class="feature-tag" style="background: linear-gradient(135deg, #ff6b6b, #feca57);">🤖 智能洞察</span>
</div>
""", unsafe_allow_html=True)

# ========== 技术栈展示 ==========
st.markdown("""
<div class="card">
    <h3 style="color:#667eea; margin-top:0;">🛠️ 技术栈</h3>
    <p style="margin-bottom:0.8rem;">
        <span class="tech-badge">Python 3.12</span>
        <span class="tech-badge">Pandas</span>
        <span class="tech-badge">NumPy</span>
        <span class="tech-badge">Matplotlib</span>
        <span class="tech-badge">Seaborn</span>
        <span class="tech-badge">Scikit-learn</span>
        <span class="tech-badge">Streamlit</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ========== 导航提示 ==========
st.markdown("""
<div class="tip-box">
    <b>💡 导航提示</b><br>
    👈 请点击左侧边栏切换页面，探索不同维度的数据分析：<br>
    &nbsp;&nbsp;• <b>📊 Data_Overview</b> — 数据集介绍与基础统计<br>
    &nbsp;&nbsp;• <b>📈 Analysis_Dashboard</b> — 六大维度交互式分析（支持实时筛选）<br>
    &nbsp;&nbsp;• <b>🔍 Smart_Insight</b> — 相关性热力图与随机森林特征重要性
</div>
""", unsafe_allow_html=True)

# ========== 页脚 ==========
st.markdown("""
<div class="footer">
    📊 数据来源：Kaggle / 和鲸社区公开数据集 | 120部电影 | 2018-2024年<br>
    🎓 《Python程序设计》课程设计作品
</div>
""", unsafe_allow_html=True)