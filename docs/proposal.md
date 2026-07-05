# 开题报告：cypchemspace - CYP 底物化学空间比较课程项目

## 一、课题名称

**cypchemspace：面向课程项目的 CYP 底物化学空间比较 Python package**

## 二、课题背景与研究意义

细胞色素 P450（Cytochrome P450, CYP）是一类广泛参与小分子代谢、天然产物修饰、药物代谢和环境化合物转化的酶家族。不同来源的 CYP 底物在化学结构上具有明显差异：有些底物更偏脂溶性、萜类或甾体类，有些底物则更接近氨基酸、吲哚或其他亲水性小分子。理解这些底物在化学结构空间中的分布，有助于从计算角度认识 CYP 底物选择性、数据库覆盖范围和潜在研究空白。

原始 `CYP_comparison` 项目已经围绕本地数据库 `mydb` 与 P450DB 背景底物进行了较完整的探索，包括底物抽取、结构映射、RDKit fingerprint、UMAP 可视化、kNN permutation 局部富集检验、fingerprint sensitivity、unique-InChIKey 去重敏感性分析和 logP 补充解释等。但是，原始项目规模较大，包含大量历史脚本、全量数据、中间结果和科研探索分支，不适合直接作为课程项目提交。

因此，本课题拟将其中最适合课程展示的一条主线裁剪为一个独立、轻量、可安装、可测试、可复现的 Python package。该项目既保留真实生物信息学问题，又符合课程对软件工程、API 设计、CLI、测试、notebook 和文档的要求。

## 三、研究问题

本项目聚焦以下核心问题：

> 本地数据库中的膜相关 CYP 底物是否在 P450DB 背景底物的化学结构空间中表现出局部富集？

在课程包中，该问题被转化为一个可复现的计算流程：

1. 输入带有标准化 SMILES 和来源标签的小型底物表。
2. 使用 RDKit 将 SMILES 转换为分子对象。
3. 生成 Morgan molecular fingerprint。
4. 将 fingerprint 空间降维为二维坐标，用于可视化。
5. 使用 k-nearest-neighbor permutation test 检验 `mydb` 底物是否更倾向于互为近邻。
6. 输出 summary table 和核心化学空间图。

需要强调的是，本课程包不声称复现完整科研仓库的全部结论，而是构建一个可教学、可演示、可测试的最小闭环。

## 四、项目目标

### 4.1 生物信息学目标

- 将 CYP 底物比较问题抽象为结构化的小分子化学空间分析问题。
- 展示如何使用 molecular fingerprint 表示小分子结构。
- 通过 kNN permutation test 解释“局部富集”而不是只依赖 UMAP 图像直觉。
- 在报告中明确说明可视化、统计检验和生物学解释之间的边界。

### 4.2 软件工程目标

- 构建符合 `src-layout` 的 Python package。
- 提供 3-5 个可复用 API，包括数据读取、SMILES 解析、fingerprint 生成和富集检验。
- 提供一个命令行入口 `cypchemspace analyze`。
- 提供至少 5 个 pytest 单元测试。
- 提供 demo notebook、README、环境文件、课程报告和展示提纲。

### 4.3 课程提交目标

- 不提交完整大数据表和历史探索输出。
- 只提交小型教学样例数据与可复现演示流程。
- 保持项目边界清晰，使任课教师或助教可以快速安装、运行和评价。

## 五、技术路线

本项目的技术路线如下：

```text
example substrate table
  -> input validation
  -> RDKit Mol parsing
  -> Morgan fingerprint matrix
  -> UMAP / PCA 2D embedding
  -> kNN label enrichment with permutation test
  -> summary.csv + cypchemspace_umap.png
```

### 5.1 数据读取与校验

输入文件为 CSV 或 TSV 表格，至少包含：

- `compound_id`：底物名称或标识符。
- `std_smiles`：标准化 SMILES。
- `label`：来源标签，主要为 `mydb` 或 `p450db`。

程序会检查必要列是否存在，并对空值或无效行进行基础清理。

### 5.2 化学结构表示

使用 RDKit 将 `std_smiles` 解析为分子对象，并生成 Morgan fingerprint。默认参数为：

- radius = 2
- n_bits = 2048

CLI 中允许调整 bit 数和 radius，便于课程演示不同参数对结果的影响。

### 5.3 化学空间可视化

默认使用 UMAP 生成二维坐标。如果教学环境中 UMAP 不可用，程序提供 PCA fallback，以保证 demo 可以在受限环境中完成。

### 5.4 局部富集统计

核心统计量为：对于所有 `mydb` 底物，计算其 k 个最近邻中仍为 `mydb` 的比例，并与随机置换标签后的 null distribution 比较。输出包括：

- observed positive-neighbor fraction
- mean null positive-neighbor fraction
- delta
- empirical p-value

该统计检验用于支持“局部富集”判断，避免只凭二维图像下结论。

## 六、项目结构设计

项目目录为：

```text
course_project_cypchemspace/
  pyproject.toml
  README.md
  requirements.txt
  environment.yml
  src/cypchemspace/
    __init__.py
    io.py
    chem.py
    embedding.py
    enrichment.py
    visualize.py
    cli.py
  tests/
  examples/
    example_data/
    demo_cypchemspace.ipynb
  docs/
    requirements.html
    proposal.md
    tutorial.md
    report.md
    slides_outline.md
```

各模块职责如下：

| 模块 | 职责 |
|---|---|
| `io.py` | 读取并校验底物表 |
| `chem.py` | SMILES 解析、规范化和 Morgan fingerprint 生成 |
| `embedding.py` | UMAP/PCA 二维 embedding |
| `enrichment.py` | kNN permutation 局部富集检验 |
| `visualize.py` | 输出核心化学空间散点图 |
| `cli.py` | 提供命令行入口 |

## 七、可行性分析

### 7.1 数据可行性

课程包使用从原始项目输出中抽取的小型示例数据，不依赖完整原始大表，也不依赖在线 PubChem 查询。因此，数据体积小、可提交、可复制，适合课堂演示。

### 7.2 技术可行性

RDKit、pandas、numpy、scikit-learn、matplotlib 和 umap-learn 均为成熟 Python 科学生态工具。项目核心算法和数据规模较小，能够在普通个人电脑上完成。

### 7.3 课程可行性

项目覆盖课程项目指南中的多项要求：Python package、CLI、API、pytest、notebook、README、环境文件、结果图表和课程报告。同时，项目问题具有明确生物学背景，不只是纯编程练习。

## 八、测试与评价方案

计划使用 pytest 覆盖以下行为：

1. 示例数据读取和必要列检查。
2. 缺失必要列时抛出清晰错误。
3. 无效 SMILES 不导致整个流程崩溃。
4. 等价 SMILES 的规范化结果一致。
5. Morgan fingerprint 矩阵维度与输入分子数匹配。
6. toy fingerprint 数据中 kNN enrichment 能检测正类局部聚集。
7. CLI 能生成 `embedding.csv`、`summary.csv` 和 `cypchemspace_umap.png`。

项目评价主要参考：

- 软件结构是否清晰。
- 命令行和 API 是否可用。
- 测试是否覆盖关键行为。
- 结果解释是否把 UMAP 可视化与统计检验区分开。
- 文档是否说明数据来源、限制和复现方法。

## 九、预期成果

本项目预期交付：

- 一个可安装的 Python package：`cypchemspace`。
- 一个可运行的 CLI：`cypchemspace analyze`。
- 一份小型示例数据。
- 一个 demo notebook。
- 一张核心化学空间图。
- 一个 summary table。
- pytest 测试套件。
- README、tutorial、开题报告、课程报告和展示提纲。

预期通过该项目展示从真实生物学问题到可复现 Python package 的完整课程项目闭环。

## 十、进度安排

| 阶段 | 任务 | 产出 |
|---|---|---|
| 第 1 阶段 | 明确课题边界与课程提交形式 | 总需求文档、模块需求文档、开题报告 |
| 第 2 阶段 | 构建 package 骨架与示例数据 | `pyproject.toml`、`src/`、`examples/` |
| 第 3 阶段 | 实现核心 API 与 CLI | `io.py`、`chem.py`、`embedding.py`、`enrichment.py`、`cli.py` |
| 第 4 阶段 | 编写测试与 demo notebook | `tests/`、`demo_cypchemspace.ipynb` |
| 第 5 阶段 | 完善报告和展示材料 | `report.md`、`slides_outline.md`、核心图表 |
| 第 6 阶段 | 运行验证并整理提交包 | pytest 结果、CLI 输出、最终课程目录 |

## 十一、风险与应对

| 风险 | 影响 | 应对策略 |
|---|---|---|
| 原始项目过大，课程包边界失控 | 难以评分和复现 | 只提交独立小包，不提交完整大数据 |
| UMAP 图被误读为统计证明 | 结论过度解释 | 报告中必须配套 kNN permutation statistic |
| RDKit 安装环境复杂 | 影响运行 | 提供 `environment.yml`，推荐 conda-forge 安装 |
| 在线数据请求失败 | demo 不稳定 | 不依赖远程 PubChem 查询 |
| 小样例不能代表完整研究结论 | 科研外推不足 | 明确说明 demo 是教学子集，完整分析作为背景说明 |

## 十二、创新点与课程价值

本项目的创新点不在于提出新的化学信息学算法，而在于把一个较复杂的真实科研探索过程压缩成课程可评价的软件工程作品。它同时训练：

- 生物学问题定义能力。
- 小分子结构表示能力。
- Python package 组织能力。
- 命令行工具设计能力。
- 统计检验与可视化解释能力。
- 可复现科研文档写作能力。

因此，该项目适合作为“统计组学/机器学习用于生物信息学”方向的综合课程项目。

## 十三、参考资料

[1] Guengerich F P. Cytochrome P450 and chemical toxicology[J]. *Chemical Research in Toxicology*, 2008, 21(1): 70-83. DOI: [10.1021/tx700079z](https://doi.org/10.1021/tx700079z).

[2] Zhang Y, Pan X, Shi T, et al. P450Rdb: A manually curated database of reactions catalyzed by cytochrome P450 enzymes[J]. *Journal of Advanced Research*, 2024, 63: 35-42. DOI: [10.1016/j.jare.2023.10.012](https://doi.org/10.1016/j.jare.2023.10.012).

[3] Preissner S, Kroll K, Dunkel M, et al. SuperCYP: a comprehensive database on Cytochrome P450 enzymes including a tool for analysis of CYP-drug interactions[J]. *Nucleic Acids Research*, 2010, 38(suppl_1): D237-D243. DOI: [10.1093/nar/gkp970](https://doi.org/10.1093/nar/gkp970).

[4] Rogers D, Hahn M. Extended-connectivity fingerprints[J]. *Journal of Chemical Information and Modeling*, 2010, 50(5): 742-754. DOI: [10.1021/ci100050t](https://doi.org/10.1021/ci100050t).

[5] Bajusz D, Racz A, Heberger K. Why is Tanimoto index an appropriate choice for fingerprint-based similarity calculations?[J]. *Journal of Cheminformatics*, 2015, 7: 20. DOI: [10.1186/s13321-015-0069-3](https://doi.org/10.1186/s13321-015-0069-3).

[6] Landrum G. RDKit: Open-source cheminformatics. Release 2014.03.1[EB/OL]. Zenodo, 2014. DOI: [10.5281/zenodo.10398](https://doi.org/10.5281/zenodo.10398).

[7] McInnes L, Healy J, Melville J. UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction[EB/OL]. arXiv, 2018. arXiv: [1802.03426](https://arxiv.org/abs/1802.03426).

[8] Healy J, McInnes L. Uniform manifold approximation and projection[J]. *Nature Reviews Methods Primers*, 2024, 4: 82. DOI: [10.1038/s43586-024-00363-x](https://doi.org/10.1038/s43586-024-00363-x).
