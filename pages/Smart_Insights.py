import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="🔍 智能洞察", page_icon="🔍", layout="wide")

# ========== CSS样式 ==========
st.markdown("""
<style>
    .page-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    .insight-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 4px solid #4caf50;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #2e7d32;
    }
    .insight-box.highlight {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left-color: #2196f3;
        color: #1565c0;
    }
    .insight-box.gold {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        border-left-color: #ffc107;
        color: #e65100;
    }
    .chart-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #444;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #667eea;
        display: inline-block;
    }
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    .summary-card h4 {
        color: white;
        margin-top: 0;
        font-size: 1.2rem;
    }
    .summary-card p {
        color: rgba(255,255,255,0.9);
        line-height: 1.8;
        margin: 0.5rem 0;
    }
    .tag-pill {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        font-weight: 500;
    }
    .rank-badge {
        display: inline-block;
        width: 28px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.85rem;
        color: white;
        margin-right: 0.5rem;
    }
    .rank-1 { background: linear-gradient(135deg, #ffd700, #ffaa00); }
    .rank-2 { background: linear-gradient(135deg, #c0c0c0, #a0a0a0); }
    .rank-3 { background: linear-gradient(135deg, #cd7f32, #b87333); }
    .rank-other { background: linear-gradient(135deg, #667eea, #764ba2); }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">🔍 智能洞察</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#888; margin-bottom:1.5rem;'>相关性分析 · 随机森林特征重要性 · 核心洞察总结</p>", unsafe_allow_html=True)

# 加载数据
df = pd.read_csv('data/movies.csv')
df['上映日期'] = pd.to_datetime(df['上映日期'])
df['年份'] = df['上映日期'].dt.year
df['票房(亿元)'] = df['票房(万元)'] / 10000

st.markdown("---")

# 编码
df['档期编码'] = LabelEncoder().fit_transform(df['档期'])
df['主类型编码'] = LabelEncoder().fit_transform(df['主类型'])

# ========== 1. 相关性热力图 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📊 1. 票房影响因素相关性分析</h3>
        <p style="color:#888; margin-bottom:1rem;">Pearson相关系数热力图，揭示各因素与票房的关联程度</p>
    </div>
    """, unsafe_allow_html=True)

    corr_features = ['票房(亿元)', '评分', '想看人数', '片长(分钟)', '档期编码', '主类型编码', '年份']
    corr_matrix = df[corr_features].corr()

    feature_names = {
        '票房(亿元)': '票房',
        '评分': '评分',
        '想看人数': '想看人数',
        '片长(分钟)': '片长',
        '档期编码': '档期',
        '主类型编码': '电影类型',
        '年份': '上映年份'
    }
    corr_matrix_display = corr_matrix.rename(index=feature_names, columns=feature_names)

    corr_with_box = corr_matrix['票房(亿元)'].sort_values(ascending=False)
    corr_display = pd.DataFrame({
        '因素': [feature_names[k] for k in corr_with_box.index],
        '与票房相关系数': corr_with_box.values.round(3)
    })

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<span class="chart-title">📋 票房相关性排序</span>', unsafe_allow_html=True)
        st.dataframe(corr_display, use_container_width=True, hide_index=True, height=280)

        strongest = corr_display.iloc[1]
        st.markdown(f"""
        <div class="insight-box highlight">
            💡 与票房相关性最强的因素是『<b>{strongest['因素']}</b>』(r = {strongest['与票房相关系数']})
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="chart-title">🔥 相关性热力图</span>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        mask = np.triu(np.ones_like(corr_matrix_display, dtype=bool))
        sns.heatmap(corr_matrix_display, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r',
                    center=0, square=True, linewidths=1, ax=ax,
                    annot_kws={"size": 10, "weight": "bold"})
        ax.set_title('票房影响因素相关性热力图', fontsize=13, fontweight='bold', pad=15)
        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")

# ========== 2. 随机森林特征重要性 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">🤖 2. 随机森林特征重要性分析</h3>
        <p style="color:#888; margin-bottom:1rem;">基于100棵决策树的集成模型，量化各因素对票房预测的贡献度</p>
    </div>
    """, unsafe_allow_html=True)

    features = ['评分', '想看人数', '片长(分钟)', '档期编码', '主类型编码', '年份']
    X = df[features]
    y = df['票房(亿元)']

    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)

    feature_map = {
        '评分': '评分',
        '想看人数': '想看人数',
        '片长(分钟)': '片长',
        '档期编码': '档期',
        '主类型编码': '电影类型',
        '年份': '上映年份'
    }

    importance_df = pd.DataFrame({
        '特征': [feature_map[f] for f in features],
        '重要性': rf.feature_importances_
    }).sort_values('重要性', ascending=False)

    importance_df['重要性(%)'] = (importance_df['重要性'] * 100).round(1)
    importance_df = importance_df.reset_index(drop=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<span class="chart-title">📋 特征重要性排序</span>', unsafe_allow_html=True)

        # 带排名的表格
        for idx, row in importance_df.iterrows():
            rank_class = f"rank-{idx+1}" if idx < 3 else "rank-other"
            st.markdown(f"""
            <div style="display:flex; align-items:center; margin:0.4rem 0; padding:0.5rem; background:#f8f9fa; border-radius:8px;">
                <span class="rank-badge {rank_class}">{idx+1}</span>
                <span style="flex:1; font-weight:600;">{row['特征']}</span>
                <span style="color:#667eea; font-weight:700; font-size:1.1rem;">{row['重要性(%)']}%</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-box gold" style="margin-top:1rem;">
            🎯 关键发现：<br>
            影响票房的第一因素是『<b>{importance_df.iloc[0]['特征']}</b>』，占比 {importance_df.iloc[0]['重要性(%)']}%<br>
            第二因素是『<b>{importance_df.iloc[1]['特征']}</b>』，占比 {importance_df.iloc[1]['重要性(%)']}%<br>
            第三因素是『<b>{importance_df.iloc[2]['特征']}</b>』，占比 {importance_df.iloc[2]['重要性(%)']}%
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<span class="chart-title">📊 特征重要性可视化</span>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['#ffd700', '#c0c0c0', '#cd7f32', '#667eea', '#3498db', '#95a5a6']
        bars = ax.barh(importance_df['特征'], importance_df['重要性'], color=colors[:len(importance_df)],
                      edgecolor='white', linewidth=1.5, height=0.6)
        ax.set_xlabel('重要性', fontsize=12)
        ax.set_title('票房影响因素：随机森林特征重要性', fontsize=13, fontweight='bold', pad=15)
        ax.invert_yaxis()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='x', alpha=0.3, linestyle='--')

        for bar, val in zip(bars, importance_df['重要性']):
            ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                    f'{val*100:.1f}%', va='center', fontsize=11, fontweight='bold', color='#444')

        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")

# ========== 3. 核心洞察总结 ==========
with st.container():
    st.markdown("""
    <div class="summary-card">
        <h4>💡 核心洞察总结</h4>
        <p>基于对中国电影票房数据的多维度分析，我们得出以下核心结论：</p>
        <span class="tag-pill">📌 档期效应显著</span>
        <span class="tag-pill">📌 类型≠票房</span>
        <span class="tag-pill">📌 头部效应极端</span>
        <span class="tag-pill">📌 评分陷阱存在</span>
        <span class="tag-pill">📌 想看人数是关键</span>
        <span class="tag-pill">📌 随机森林量化</span>
    </div>
    """, unsafe_allow_html=True)

    insights = [
        ('🎬 档期效应显著', '春节档、暑期档、国庆档的平均票房远高于普通档。档期选择是票房成功的第一要素。', 'insight-box'),
        ('🎭 类型≠票房', '某些类型电影数量多（如喜剧），但平均票房未必最高。科幻、战争等类型虽然数量少，但单部平均票房表现突出。', 'insight-box highlight'),
        ('👑 头部效应极端', 'TOP10%的电影贡献了超过50%的票房。电影市场呈现明显的"赢家通吃"格局。', 'insight-box gold'),
        ('🎯 评分陷阱存在', '存在"烂片高票房"现象：低评分+高票房；也存在"叫好不叫座"现象：高评分+低票房。评分与票房并非简单线性关系。', 'insight-box'),
        ('📊 想看人数是关键先行指标', '想看人数与票房相关性最高。映前热度是预测票房的重要参考。', 'insight-box highlight'),
        ('🤖 随机森林量化洞察', '档期是影响票房的最重要因素，想看人数、电影类型、评分依次跟进，片长对票房影响相对较小。', 'insight-box gold'),
    ]

    for title, content, css_class in insights:
        st.markdown(f"""
        <div class="{css_class}">
            <b>{title}</b><br>{content}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption("📊 分析工具：Python · Pandas · Matplotlib · Seaborn · Scikit-learn · Streamlit")