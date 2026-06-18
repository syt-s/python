import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
import os
warnings.filterwarnings('ignore')

# ========== 美化 Matplotlib 样式 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['xtick.color'] = '#555555'
plt.rcParams['ytick.color'] = '#555555'
plt.rcParams['text.color'] = '#333333'

# 创建输出目录
os.makedirs('output', exist_ok=True)

# 加载数据
df = pd.read_csv('data/movies.csv')
df['上映日期'] = pd.to_datetime(df['上映日期'])
df['年份'] = df['上映日期'].dt.year
df['票房(亿元)'] = df['票房(万元)'] / 10000

print("=" * 60)
print("【数据清洗】")
print("=" * 60)
print(f"数据条数: {len(df)}")
print(f"时间范围: {df['年份'].min()} - {df['年份'].max()}")
print(f"票房范围: {df['票房(亿元)'].min():.2f}亿 - {df['票房(亿元)'].max():.2f}亿")
print(f"缺失值: {df.isnull().sum().sum()} 个")
print(f"平均评分: {df['评分'].mean():.2f}")
print(f"平均票房: {df['票房(亿元)'].mean():.2f}亿")

# ========== 1. 档期效应分析 ==========
print("\n" + "=" * 60)
print("【1. 档期效应分析】")
print("=" * 60)

season_stats = df.groupby('档期').agg({
    '票房(亿元)': ['mean', 'sum', 'count'],
    '评分': 'mean'
}).round(2)
season_stats.columns = ['平均票房(亿)', '总票房(亿)', '电影数量', '平均评分']
season_stats = season_stats.sort_values('平均票房(亿)', ascending=False)
print(season_stats)

max_season = season_stats['平均票房(亿)'].max()
min_season = season_stats['平均票房(亿)'].min()
print(f"\n最高档期平均票房是最低档期的 {max_season/min_season:.1f} 倍")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(season_stats)))
bars1 = axes[0].bar(range(len(season_stats)), season_stats['平均票房(亿)'], color=colors, edgecolor='white', linewidth=1.5)
axes[0].set_xticks(range(len(season_stats)))
axes[0].set_xticklabels(season_stats.index, rotation=45, ha='right')
axes[0].set_ylabel('平均票房（亿元）', fontsize=12)
axes[0].set_title('各档期平均票房对比', fontsize=14, fontweight='bold', pad=15)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].grid(axis='y', alpha=0.3)
for bar, val in zip(bars1, season_stats['平均票房(亿)']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax1 = axes[1]
ax2 = ax1.twinx()
season_stats['电影数量'].plot(kind='bar', ax=ax1, color='lightcoral', alpha=0.7, edgecolor='white', linewidth=1.5)
season_stats['平均票房(亿)'].plot(kind='line', ax=ax2, color='darkgreen', marker='o', linewidth=2.5, markersize=8)
ax1.set_title('档期：数量 vs 平均票房', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('电影数量', color='lightcoral', fontsize=12)
ax2.set_ylabel('平均票房（亿元）', color='darkgreen', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('output/fig1_season_analysis.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图1已保存: output/fig1_season_analysis.png")

# ========== 2. 类型对决分析 ==========
print("\n" + "=" * 60)
print("【2. 类型对决分析】")
print("=" * 60)

genre_stats = df.groupby('主类型').agg({
    '票房(亿元)': ['mean', 'sum', 'count'],
    '评分': 'mean'
}).round(2)
genre_stats.columns = ['平均票房(亿)', '总票房(亿)', '电影数量', '平均评分']
genre_stats = genre_stats.sort_values('总票房(亿)', ascending=False)
print(genre_stats)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
top5_genre = genre_stats.head(5)
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(top5_genre)))
axes[0].pie(top5_genre['总票房(亿)'], labels=top5_genre.index, autopct='%1.1f%%',
            colors=colors_pie, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0].set_title('TOP5类型票房占比', fontsize=14, fontweight='bold', pad=15)

ax1 = axes[1]
ax2 = ax1.twinx()
genre_stats['电影数量'].plot(kind='bar', ax=ax1, color='lightskyblue', alpha=0.7, edgecolor='white', linewidth=1.5)
genre_stats['平均票房(亿)'].plot(kind='line', ax=ax2, color='crimson', marker='D', linewidth=2.5, markersize=8)
ax1.set_title('各类型：数量 vs 平均票房', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('电影数量', color='lightskyblue', fontsize=12)
ax2.set_ylabel('平均票房（亿元）', color='crimson', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('output/fig2_genre_analysis.png', dpi=200, bbox_inches='tight', facecolor='white')
print("图2已保存: output/fig2_genre_analysis.png")

max_count_genre = genre_stats['电影数量'].idxmax()
max_avg_genre = genre_stats['平均票房(亿)'].idxmax()
print(f"\n发现: 数量最多的类型是「{max_count_genre}」({genre_stats.loc[max_count_genre, '电影数量']}部)")
print(f"      平均票房最高的类型是「{max_avg_genre}」({genre_stats.loc[max_avg_genre, '平均票房(亿)']}亿)")
print(f"      -> 数量多不等于票房高！")

# ========== 3. 头部效应分析 ==========
print("\n" + "=" * 60)
print("【3. 头部效应分析 - 帕累托图】")
print("=" * 60)

df_sorted = df.sort_values('票房(亿元)', ascending=False).reset_index(drop=True)
df_sorted['累计票房'] = df_sorted['票房(亿元)'].cumsum()
df_sorted['累计占比'] = df_sorted['累计票房'] / df_sorted['票房(亿元)'].sum() * 100

top10_idx = int(len(df_sorted) * 0.1)
top10_contribution = df_sorted.iloc[:top10_idx]['累计占比'].iloc[-1]

print(f"TOP10%的电影（前{top10_idx}部）贡献了 {top10_contribution:.1f}% 的票房")
print(f"\n头部电影名单（前10部）：")
print(df_sorted[['电影名称', '票房(亿元)', '档期', '主类型']].head(10).to_string(index=False))

fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.bar(range(len(df_sorted)), df_sorted['票房(亿元)'], color='steelblue', alpha=0.6, edgecolor='white', linewidth=0.5)
ax1.set_xlabel('电影排名（按票房降序）', fontsize=12)
ax1.set_ylabel('单部电影票房（亿元）', color='steelblue', fontsize=12)
ax2 = ax1.twinx()
ax2.plot(range(len(df_sorted)), df_sorted['累计占比'], color='red', linewidth=2.5, marker='o', markersize=3)
ax2.axhline(y=80, color='green', linestyle='--', alpha=0.7, linewidth=1.5, label='80%线')
ax2.axvline(x=top10_idx, color='orange', linestyle='--', alpha=0.7, linewidth=1.5, label=f'TOP10% ({top10_idx}部)')
ax2.set_ylabel('累计票房占比（%）', color='red', fontsize=12)
ax2.set_ylim(0, 105)
ax1.set_title('电影市场头部效应：帕累托分析', fontsize=14, fontweight='bold', pad=15)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.3)
ax2.legend(loc='center right', fontsize=11)

plt.tight_layout()
plt.savefig('output/fig3_pareto.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图3已保存: output/fig3_pareto.png")

# ========== 4. 评分陷阱分析 ==========
print("\n" + "=" * 60)
print("【4. 评分陷阱分析】")
print("=" * 60)

high_box_low_rating = df[(df['票房(亿元)'] > 5) & (df['评分'] < 7.0)]
low_box_high_rating = df[(df['票房(亿元)'] < 1) & (df['评分'] > 8.0)]

print(f"\n「烂片高票房」案例（票房>5亿 & 评分<7.0）：{len(high_box_low_rating)} 部")
if len(high_box_low_rating) > 0:
    print(high_box_low_rating[['电影名称', '票房(亿元)', '评分', '档期']].to_string(index=False))

print(f"\n「叫好不叫座」案例（票房<1亿 & 评分>8.0）：{len(low_box_high_rating)} 部")
if len(low_box_high_rating) > 0:
    print(low_box_high_rating[['电影名称', '票房(亿元)', '评分', '档期']].to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 8))
season_colors = {'春节档': '#e74c3c', '暑期档': '#3498db', '国庆档': '#f39c12',
                '贺岁档': '#9b59b6', '普通档': '#95a5a6', '元旦档': '#1abc9c'}
for season in df['档期'].unique():
    mask = df['档期'] == season
    ax.scatter(df[mask]['评分'], df[mask]['票房(亿元)'],
              c=season_colors.get(season, '#666'), label=season, alpha=0.7, s=120,
              edgecolors='white', linewidth=0.5)

for _, row in high_box_low_rating.iterrows():
    ax.annotate(row['电影名称'], (row['评分'], row['票房(亿元)']),
                xytext=(5, 5), textcoords='offset points', fontsize=10, color='red', fontweight='bold')

for _, row in low_box_high_rating.iterrows():
    ax.annotate(row['电影名称'], (row['评分'], row['票房(亿元)']),
                xytext=(5, 5), textcoords='offset points', fontsize=10, color='green', fontweight='bold')

ax.axhline(y=5, color='red', linestyle='--', alpha=0.5, linewidth=1, label='高票房线(5亿)')
ax.axvline(x=7.0, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax.axhline(y=1, color='green', linestyle='--', alpha=0.5, linewidth=1, label='低票房线(1亿)')
ax.axvline(x=8.0, color='green', linestyle='--', alpha=0.5, linewidth=1)
ax.set_xlabel('评分', fontsize=13)
ax.set_ylabel('票房（亿元）', fontsize=13)
ax.set_title('票房 vs 评分：识别"烂片高票房"与"叫好不叫座"', fontsize=14, fontweight='bold', pad=15)
ax.legend(loc='upper left', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('output/fig4_rating_trap.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图4已保存: output/fig4_rating_trap.png")

# ========== 5. 相关性分析 ==========
print("\n" + "=" * 60)
print("【5. 相关性分析】")
print("=" * 60)

df['档期编码'] = LabelEncoder().fit_transform(df['档期'])
df['主类型编码'] = LabelEncoder().fit_transform(df['主类型'])

corr_features = ['票房(亿元)', '评分', '想看人数', '片长(分钟)', '档期编码', '主类型编码', '年份']
corr_matrix = df[corr_features].corr()

print("\n票房与其他因素的相关性：")
corr_with_box = corr_matrix['票房(亿元)'].sort_values(ascending=False)
print(corr_with_box.round(3).to_string())

fig, ax = plt.subplots(figsize=(11, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r',
            center=0, square=True, linewidths=1, ax=ax,
            annot_kws={"size": 11, "weight": "bold"})
ax.set_title('票房影响因素相关性热力图', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('output/fig5_correlation.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图5已保存: output/fig5_correlation.png")

# ========== 6. 随机森林特征重要性 ==========
print("\n" + "=" * 60)
print("【6. 随机森林特征重要性分析】")
print("=" * 60)

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

print("\n特征重要性排序：")
for idx, row in importance_df.iterrows():
    medal = "[1]" if idx == 0 else "[2]" if idx == 1 else "[3]" if idx == 2 else "   "
    print(f"   {medal} {row['特征']}: {row['重要性']*100:.1f}%")

print(f"\n关键发现：")
print(f"   影响票房的第一因素是「{importance_df.iloc[0]['特征']}」，重要性占比 {importance_df.iloc[0]['重要性']*100:.1f}%")
print(f"   第二因素是「{importance_df.iloc[1]['特征']}」，重要性占比 {importance_df.iloc[1]['重要性']*100:.1f}%")

fig, ax = plt.subplots(figsize=(11, 7))
colors = ['#ffd700', '#c0c0c0', '#cd7f32', '#667eea', '#3498db', '#95a5a6']
bars = ax.barh(importance_df['特征'], importance_df['重要性'], color=colors[:len(importance_df)],
              edgecolor='white', linewidth=1.5, height=0.6)
ax.set_xlabel('重要性', fontsize=13)
ax.set_title('票房影响因素：随机森林特征重要性分析', fontsize=14, fontweight='bold', pad=15)
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)

for bar, val in zip(bars, importance_df['重要性']):
    ax.text(val + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val*100:.1f}%', va='center', fontsize=12, fontweight='bold', color='#444')

plt.tight_layout()
plt.savefig('output/fig6_feature_importance.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图6已保存: output/fig6_feature_importance.png")

# ========== 7. 年份趋势 ==========
print("\n" + "=" * 60)
print("【7. 年份趋势分析】")
print("=" * 60)

year_stats = df.groupby('年份').agg({
    '票房(亿元)': ['sum', 'mean', 'count']
}).round(2)
year_stats.columns = ['总票房(亿)', '平均票房(亿)', '电影数量']
print(year_stats)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(year_stats.index, year_stats['总票房(亿)'], marker='o', linewidth=3, markersize=10,
       color='#667eea', markerfacecolor='white', markeredgewidth=2.5)
ax.fill_between(year_stats.index, year_stats['总票房(亿)'], alpha=0.2, color='#667eea')
ax.set_xlabel('年份', fontsize=13)
ax.set_ylabel('年度总票房（亿元）', fontsize=13)
ax.set_title('中国电影市场年度票房趋势', fontsize=14, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3)
for x, y in zip(year_stats.index, year_stats['总票房(亿)']):
    ax.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0, 12),
               ha='center', fontsize=11, fontweight='bold', color='#667eea')

plt.tight_layout()
plt.savefig('output/fig7_year_trend.png', dpi=200, bbox_inches='tight', facecolor='white')
print("\n图7已保存: output/fig7_year_trend.png")

print("\n" + "=" * 60)
print("全部分析完成！7张高清图表已保存至 output/ 目录")
print("=" * 60)