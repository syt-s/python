import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="📈 分析看板", page_icon="📈", layout="wide")

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
    .insight-box.warning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left-color: #ff9800;
        color: #e65100;
    }
    .insight-box.danger {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left-color: #f44336;
        color: #c62828;
    }
    .filter-panel {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
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
    .metric-highlight {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="page-title">📈 分析看板</h1>', unsafe_allow_html=True)
st.markdown("<p style='color:#888; margin-bottom:1.5rem;'>六大维度深度分析 · 支持实时交互筛选</p>", unsafe_allow_html=True)

# 加载数据
df = pd.read_csv('data/movies.csv')
df['上映日期'] = pd.to_datetime(df['上映日期'])
df['年份'] = df['上映日期'].dt.year
df['票房(亿元)'] = df['票房(万元)'] / 10000

st.markdown("---")

# ========== 筛选面板 ==========
with st.container():
    st.markdown("""
    <div class="filter-panel">
        <h4 style="margin-top:0; color:#667eea;">🔍 筛选条件</h4>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        year_range = st.slider("📅 年份范围", int(df['年份'].min()), int(df['年份'].max()),
                                (int(df['年份'].min()), int(df['年份'].max())))
    with col_f2:
        seasons = st.multiselect("🎬 档期", options=df['档期'].unique(), default=list(df['档期'].unique()))
    with col_f3:
        genres = st.multiselect("🎭 类型", options=sorted(df['主类型'].unique()), default=list(df['主类型'].unique()))

# 应用筛选
df_f = df[(df['年份'] >= year_range[0]) & (df['年份'] <= year_range[1]) &
          (df['档期'].isin(seasons)) & (df['主类型'].isin(genres))]

st.markdown(f"""
<div style="text-align:center; margin:1rem 0;">
    <span style="background: linear-gradient(135deg, #667eea, #764ba2); color:white; padding:0.4rem 1.2rem; border-radius:20px; font-size:0.9rem;">
        📊 当前筛选结果：<b>{len(df_f)}</b> 部电影
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== 1. 档期效应 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">🎬 1. 档期效应分析</h3>
        <p style="color:#888; margin-bottom:1rem;">不同上映档期的票房表现差异分析</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) > 0:
        season_stats = df_f.groupby('档期').agg({'票房(亿元)': ['mean', 'sum', 'count']}).round(2)
        season_stats.columns = ['平均票房(亿)', '总票房(亿)', '电影数量']
        season_stats = season_stats.sort_values('平均票房(亿)', ascending=False)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<span class="chart-title">📊 档期统计表</span>', unsafe_allow_html=True)
            st.dataframe(season_stats, use_container_width=True, height=300)
            if len(season_stats) >= 2:
                max_s = season_stats['平均票房(亿)'].max()
                min_s = season_stats['平均票房(亿)'].min()
                st.markdown(f"""
                <div class="insight-box">
                    💡 最高档期平均票房是最低档期的 <b>{max_s/min_s:.1f}</b> 倍
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<span class="chart-title">📈 各档期平均票房对比</span>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(season_stats)))
            bars = ax.bar(range(len(season_stats)), season_stats['平均票房(亿)'], color=colors, edgecolor='white', linewidth=1.5)
            ax.set_xticks(range(len(season_stats)))
            ax.set_xticklabels(season_stats.index, rotation=45, ha='right')
            ax.set_ylabel('平均票房（亿元）', fontsize=11)
            ax.set_title('各档期平均票房对比', fontsize=13, fontweight='bold', pad=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            for bar, val in zip(bars, season_stats['平均票房(亿)']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
    else:
        st.warning("⚠️ 当前筛选条件下无数据")

st.markdown("---")

# ========== 2. 类型对决 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">🎭 2. 类型对决分析</h3>
        <p style="color:#888; margin-bottom:1rem;">各电影类型的市场竞争力对比</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) > 0:
        genre_stats = df_f.groupby('主类型').agg({'票房(亿元)': ['mean', 'sum', 'count']}).round(2)
        genre_stats.columns = ['平均票房(亿)', '总票房(亿)', '电影数量']
        genre_stats = genre_stats.sort_values('总票房(亿)', ascending=False)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<span class="chart-title">📊 类型统计表</span>', unsafe_allow_html=True)
            st.dataframe(genre_stats, use_container_width=True, height=300)
            max_c = genre_stats['电影数量'].idxmax()
            max_a = genre_stats['平均票房(亿)'].idxmax()
            st.markdown(f"""
            <div class="insight-box">
                💡 数量最多的类型：『{max_c}』({genre_stats.loc[max_c, '电影数量']}部)
            </div>
            <div class="insight-box warning">
                💡 平均票房最高的类型：『{max_a}』({genre_stats.loc[max_a, '平均票房(亿)']}亿)
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown('<span class="chart-title">📈 各类型总票房对比</span>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = plt.cm.Set2(np.linspace(0, 1, len(genre_stats)))
            bars = ax.bar(range(len(genre_stats)), genre_stats['总票房(亿)'], color=colors, edgecolor='white', linewidth=1.5)
            ax.set_xticks(range(len(genre_stats)))
            ax.set_xticklabels(genre_stats.index, rotation=45, ha='right')
            ax.set_ylabel('总票房（亿元）', fontsize=11)
            ax.set_title('各类型总票房对比', fontsize=13, fontweight='bold', pad=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            for bar, val in zip(bars, genre_stats['总票房(亿)']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{val:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")

# ========== 3. 头部效应 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">👑 3. 头部效应分析（帕累托法则）</h3>
        <p style="color:#888; margin-bottom:1rem;">验证"二八定律"在电影市场的存在</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) > 0:
        df_sorted = df_f.sort_values('票房(亿元)', ascending=False).reset_index(drop=True)
        df_sorted['累计票房'] = df_sorted['票房(亿元)'].cumsum()
        df_sorted['累计占比'] = df_sorted['累计票房'] / df_sorted['票房(亿元)'].sum() * 100

        top10_idx = int(len(df_sorted) * 0.1)
        top10_contrib = df_sorted.iloc[:top10_idx]['累计占比'].iloc[-1] if top10_idx > 0 else 0

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<span class="chart-title">📊 头部指标</span>', unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem; background:linear-gradient(135deg, #667eea, #764ba2); border-radius:12px; color:white;">
                    <div class="metric-highlight" style="color:white;">{top10_idx}</div>
                    <div class="metric-label" style="color:rgba(255,255,255,0.8);">TOP10%电影数量</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem; background:linear-gradient(135deg, #f093fb, #f5576c); border-radius:12px; color:white;">
                    <div class="metric-highlight" style="color:white;">{top10_contrib:.1f}%</div>
                    <div class="metric-label" style="color:rgba(255,255,255,0.8);">票房贡献占比</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="insight-box danger" style="margin-top:1rem;">
                🎯 TOP10%的电影贡献了 <b>{top10_contrib:.1f}%</b> 的票房
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<span class="chart-title" style="margin-top:1rem;">🏆 头部电影名单（前5部）</span>', unsafe_allow_html=True)
            top5 = df_sorted[['电影名称', '票房(亿元)', '档期', '主类型']].head(5)
            top5['票房(亿元)'] = top5['票房(亿元)'].round(2)
            st.dataframe(top5, use_container_width=True, hide_index=True, height=220)

        with col2:
            st.markdown('<span class="chart-title">📈 帕累托分析图</span>', unsafe_allow_html=True)
            fig, ax1 = plt.subplots(figsize=(8, 5))
            ax1.bar(range(len(df_sorted)), df_sorted['票房(亿元)'], color='steelblue', alpha=0.6, edgecolor='white', linewidth=0.5)
            ax1.set_xlabel('电影排名（按票房降序）', fontsize=11)
            ax1.set_ylabel('单部票房（亿元）', color='steelblue', fontsize=11)
            ax2 = ax1.twinx()
            ax2.plot(range(len(df_sorted)), df_sorted['累计占比'], color='red', linewidth=2.5)
            ax2.axhline(y=80, color='green', linestyle='--', alpha=0.7, linewidth=1.5)
            ax2.axvline(x=top10_idx, color='orange', linestyle='--', alpha=0.7, linewidth=1.5)
            ax2.set_ylabel('累计占比（%）', color='red', fontsize=11)
            ax1.set_title('帕累托分析：头部效应', fontsize=13, fontweight='bold', pad=15)
            ax1.spines['top'].set_visible(False)
            ax2.spines['top'].set_visible(False)
            ax1.grid(axis='y', alpha=0.3, linestyle='--')
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")

# ========== 4. 评分陷阱 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">🎯 4. 评分陷阱分析</h3>
        <p style="color:#888; margin-bottom:1rem;">识别"烂片高票房"与"叫好不叫座"现象</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) > 0:
        high_box_low = df_f[(df_f['票房(亿元)'] > 5) & (df_f['评分'] < 7.0)]
        low_box_high = df_f[(df_f['票房(亿元)'] < 1) & (df_f['评分'] > 8.0)]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<span class="chart-title" style="border-bottom-color:#e74c3c;">🔴 烂片高票房（票房>5亿 & 评分<7.0）</span>', unsafe_allow_html=True)
            if len(high_box_low) > 0:
                hbl = high_box_low[['电影名称', '票房(亿元)', '评分', '档期']].copy()
                hbl['票房(亿元)'] = hbl['票房(亿元)'].round(2)
                st.dataframe(hbl, use_container_width=True, hide_index=True, height=200)
            else:
                st.info("当前筛选下无符合条件的电影")

        with col2:
            st.markdown('<span class="chart-title" style="border-bottom-color:#27ae60;">🟢 叫好不叫座（票房<1亿 & 评分>8.0）</span>', unsafe_allow_html=True)
            if len(low_box_high) > 0:
                lbh = low_box_high[['电影名称', '票房(亿元)', '评分', '档期']].copy()
                lbh['票房(亿元)'] = lbh['票房(亿元)'].round(2)
                st.dataframe(lbh, use_container_width=True, hide_index=True, height=200)
            else:
                st.info("当前筛选下无符合条件的电影")

        st.markdown('<span class="chart-title">📈 票房 vs 评分散点图</span>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(12, 6))
        season_colors = {'春节档': '#e74c3c', '暑期档': '#3498db', '国庆档': '#f39c12',
                        '贺岁档': '#9b59b6', '普通档': '#95a5a6', '元旦档': '#1abc9c'}
        for season in df_f['档期'].unique():
            mask = df_f['档期'] == season
            ax.scatter(df_f[mask]['评分'], df_f[mask]['票房(亿元)'],
                      c=season_colors.get(season, '#666'), label=season, alpha=0.7, s=100, edgecolors='white', linewidth=0.5)
        ax.axhline(y=5, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax.axvline(x=7.0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax.axhline(y=1, color='green', linestyle='--', alpha=0.5, linewidth=1)
        ax.axvline(x=8.0, color='green', linestyle='--', alpha=0.5, linewidth=1)
        ax.set_xlabel('评分', fontsize=12)
        ax.set_ylabel('票房（亿元）', fontsize=12)
        ax.set_title('票房 vs 评分：识别"烂片高票房"与"叫好不叫座"', fontsize=13, fontweight='bold', pad=15)
        ax.legend(loc='upper left', fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(alpha=0.3, linestyle='--')
        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")

# ========== 5. 年份趋势 ==========
with st.container():
    st.markdown("""
    <div class="section-card">
        <h3 style="color:#667eea; margin-top:0;">📅 5. 年份趋势分析</h3>
        <p style="color:#888; margin-bottom:1rem;">年度票房变化趋势</p>
    </div>
    """, unsafe_allow_html=True)

    if len(df_f) > 0:
        year_s = df_f.groupby('年份').agg({'票房(亿元)': ['sum', 'mean', 'count']}).round(2)
        year_s.columns = ['总票房(亿)', '平均票房(亿)', '电影数量']
        year_s = year_s.reset_index()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown('<span class="chart-title">📊 年度统计表</span>', unsafe_allow_html=True)
            st.dataframe(year_s, use_container_width=True, hide_index=True, height=280)

        with col2:
            st.markdown('<span class="chart-title">📈 年度票房趋势</span>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(year_s['年份'], year_s['总票房(亿)'], marker='o', linewidth=3, markersize=10,
                   color='#667eea', markerfacecolor='white', markeredgewidth=2)
            ax.fill_between(year_s['年份'], year_s['总票房(亿)'], alpha=0.2, color='#667eea')
            ax.set_xlabel('年份', fontsize=12)
            ax.set_ylabel('年度总票房（亿元）', fontsize=12)
            ax.set_title('年度票房趋势', fontsize=13, fontweight='bold', pad=15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.3, linestyle='--')
            for x, y in zip(year_s['年份'], year_s['总票房(亿)']):
                ax.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0, 10),
                           ha='center', fontsize=9, fontweight='bold', color='#667eea')
            plt.tight_layout()
            st.pyplot(fig)

st.markdown("---")
st.caption("📊 分析工具：Python · Pandas · Matplotlib · Streamlit")