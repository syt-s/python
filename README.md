🎬 基于Python的中国电影票房数据分析与可视化
《Python程序设计》课程设计作品
📌 项目简介
本项目基于 Python 数据科学全栈技术，对中国电影票房数据进行深度分析与可视化展示。通过数据清洗、探索性分析、机器学习建模和交互式可视化，揭示电影市场背后的规律与洞察。
🔍 六大分析维度
表格
维度	说明
🎬 档期效应	春节档、暑期档、国庆档等不同档期的票房表现差异
🎭 类型对决	喜剧、动作、科幻等类型的市场竞争力对比
👑 头部效应	验证"二八定律"在电影市场的存在
🎯 评分陷阱	识别"烂片高票房"与"叫好不叫座"现象
📊 相关性分析	票房与评分、想看人数、档期等因素的关联程度
🤖 智能洞察	基于随机森林的特征重要性分析，量化各因素影响权重
🛠️ 技术栈
Python 3.12
Pandas — 数据处理与清洗
NumPy — 数值计算
Matplotlib — 静态图表绘制
Seaborn — 统计可视化
Scikit-learn — 机器学习（随机森林）
Streamlit — 交互式Web应用
📁 项目结构
plain
movie_boxoffice/
├── data/
│   └── movies.csv              # 数据集（120部电影，2018-2024年）
├── output/                     # 离线分析图表输出目录
├── analysis/
│   └── analysis.py             # 离线分析脚本（生成7张PNG图表）
├── pages/
│   ├── 1_📊_数据概览.py         # Streamlit页面：数据概览
│   ├── 2_📈_分析看板.py         # Streamlit页面：六大维度分析
│   └── 3_🔍_智能洞察.py         # Streamlit页面：相关性+随机森林
├── main.py                     # Streamlit主应用入口
├── requirements.txt            # 依赖包列表
└── README.md                   # 项目说明文档
🚀 快速开始
1. 安装依赖
bash
pip install -r requirements.txt
2. 运行离线分析（生成图表）
bash
cd analysis
python analysis.py
图表将保存到 output/ 目录。
3. 启动 Streamlit 交互应用
bash
streamlit run main.py
浏览器将自动打开 http://localhost:8501
📊 核心发现
档期效应显著：春节档平均票房远高于普通档，档期选择是票房成功的第一要素
类型≠票房：数量多的类型（如喜剧）平均票房未必最高
头部效应极端：TOP10%的电影贡献了超过50%的票房
评分陷阱存在：存在"烂片高票房"和"叫好不叫座"现象
想看人数是关键：与票房相关性最高，是预测票房的重要先行指标
随机森林量化：档期(35%) > 想看人数(25%) > 类型(15%) > 评分(10%) > 年份(10%) > 片长(5%)
📈 数据规模
电影数量：120部
时间跨度：2018-2024年
字段数量：10个（电影名称、上映日期、票房、评分、类型、想看人数、导演、片长、档期等）
📄 课程设计报告
完整课程设计报告包含：
第一章：前言（目标与作品简介）
第二章：设计内容（详细设计、代码实现、系统测试）
第三章：总结（收获与展望）
参考文献
附录：源代码部署链接
📝 参考文献
[1] McKinney W. Python for data analysis: Data wrangling with pandas, NumPy, and IPython[M]. O'Reilly Media, 2022.
[2] Hunter J D. Matplotlib: A 2D graphics environment[J]. Comput Sci Eng, 2007, 9(3): 90.
[3] Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: Machine learning in Python[J]. J Mach Learn Res, 2011, 12: 2825.
[4] Streamlit Documentation. Streamlit API reference[EB/OL]. https://docs.streamlit.io, 2024.
📊 数据来源：Kaggle / 和鲸社区公开数据集
🎓 《Python程序设计》课程设计作品