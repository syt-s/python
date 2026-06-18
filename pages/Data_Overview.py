import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="📊 数据概览", page_icon="📊", layout="wide")

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
    .stat-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid #667eea;
    }
    .stat-card h4 {
        color: #667eea;
        font-size: 1.5rem;
        margin: 0;
    }
    .stat-card p {
        color: #666;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }
    .data-table {
        border-radius: 12px;
        overflow: hidden;
    }
    .highlight {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border-left: 4px solid #f39c12;
        margin: 0.5rem 0;
    }
    .tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== 标题 ==========
st.markdown('<h1 class="page-title">📊 数据概览</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#888; margin-bottom:2rem;'>数据集介绍、字段说明与基础统计分析</p>", unsafe_allow_html=True)

# 加载数据
df = pd.read_csv('data/movies.csv')
df['上映日期'] = pd.to_datetime(df['上映日期'])
df['年份'] = df['上映日期'].dt.year
df['票房(亿元)'] = df['票房(万元)'] / 10000

st.markdown("---")

# ========== 数据来源卡片 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📌 数据来源</h3>
        <p style="line-height:1.8; color:#444;">
        本分析使用的数据集来源于公开权威数据平台（Kaggle / 和鲸社区），包含 <b>2018-2024年</b> 中国电影市场票房数据。
        数据经过清洗与预处理，确保分析的准确性与可靠性。
        </p>
        <div style="margin-top:1rem;">
            <span class="tag">120部电影</span>
            <span class="tag">7年跨度</span>
            <span class="tag">10个字段</span>
            <span class="tag">6大档期</span>
            <span class="tag">10+类型</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== 字段说明表格 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📋 数据集字段说明</h3>
    </div>
    """, unsafe_allow_html=True)

    field_data = {
        '字段名': ['电影名称', '上映日期', '票房(万元)', '评分', '类型', '主类型', '想看人数', '导演', '片长(分钟)', '档期'],
        '数据类型': ['字符串', '日期', '浮点数', '浮点数', '字符串', '字符串', '整数', '字符串', '整数', '字符串'],
        '说明': [
            '影片中文名称',
            '首映日期（YYYY-MM-DD）',
            '累计票房金额（万元）',
            '猫眼/豆瓣综合评分（1-10分）',
            '影片类型标签（可多选）',
            '影片主类型分类',
            '平台预约观看人数',
            '导演姓名',
            '影片时长（分钟）',
            '上映档期分类'
        ],
        '示例': ['流浪地球', '2019-02-05', '468700.00', '8.5', '科幻/冒险', '科幻', '350000', '郭帆', '125', '春节档']
    }
    field_df = pd.DataFrame(field_data)
    st.dataframe(field_df, use_container_width=True, hide_index=True, height=420)

st.markdown("---")

# ========== 核心统计指标 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📈 核心统计指标</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <h4>{len(df)}部</h4>
            <p>电影总数</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#e74c3c;">
            <h4 style="color:#e74c3c;">{df['票房(亿元)'].sum():.1f}亿</h4>
            <p>总票房</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#27ae60;">
            <h4 style="color:#27ae60;">{df['票房(亿元)'].mean():.2f}亿</h4>
            <p>平均票房</p>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#f39c12;">
            <h4 style="color:#f39c12;">{df['评分'].mean():.1f}分</h4>
            <p>平均评分</p>
        </div>
        """, unsafe_allow_html=True)

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#9b59b6;">
            <h4 style="color:#9b59b6;">{df['票房(亿元)'].median():.2f}亿</h4>
            <p>票房中位数</p>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#1abc9c;">
            <h4 style="color:#1abc9c;">{df['票房(亿元)'].max():.1f}亿</h4>
            <p>最高票房</p>
        </div>
        """, unsafe_allow_html=True)
    with c7:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#34495e;">
            <h4 style="color:#34495e;">{df['票房(亿元)'].min():.2f}亿</h4>
            <p>最低票房</p>
        </div>
        """, unsafe_allow_html=True)
    with c8:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color:#e67e22;">
            <h4 style="color:#e67e22;">{df['评分'].min():.1f} - {df['评分'].max():.1f}</h4>
            <p>评分范围</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ========== 档期分布 ==========
with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <div class="section-card">
            <h3 style="color:#667eea; margin-top:0;">🎬 档期分布</h3>
        </div>
        """, unsafe_allow_html=True)
        season_dist = df['档期'].value_counts().reset_index()
        season_dist.columns = ['档期', '电影数量']
        season_dist['占比'] = (season_dist['电影数量'] / len(df) * 100).round(1).astype(str) + '%'
        st.dataframe(season_dist, use_container_width=True, hide_index=True, height=280)

    with col2:
        st.markdown("""
        <div class="section-card">
            <h3 style="color:#667eea; margin-top:0;">📅 年度统计</h3>
        </div>
        """, unsafe_allow_html=True)
        year_stats = df.groupby('年份').agg({
            '电影名称': 'count',
            '票房(亿元)': 'sum'
        }).round(1)
        year_stats.columns = ['电影数量', '年度总票房(亿)']
        year_stats = year_stats.reset_index()
        st.dataframe(year_stats, use_container_width=True, hide_index=True, height=280)

st.markdown("---")

# ========== 数据样本 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📋 数据样本（前10条）</h3>
    </div>
    """, unsafe_allow_html=True)

    df_display = df[['电影名称', '上映日期', '票房(亿元)', '评分', '类型', '想看人数', '导演', '档期']].head(10)
    df_display['上映日期'] = df_display['上映日期'].dt.strftime('%Y-%m-%d')
    df_display['票房(亿元)'] = df_display['票房(亿元)'].round(2)
    st.dataframe(df_display, use_container_width=True, hide_index=True, height=400)

st.markdown("---")
st.caption("📊 数据来源于Kaggle/和鲸社区公开数据集 | 120部电影 | 2018-2024年")