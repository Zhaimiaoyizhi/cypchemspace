# 课程项目结题报告

## 摘要

本课程项目将原始 `CYP_comparison` 研究仓库中最适合教学展示的一条主线，裁剪并包装为一个独立的 Python package：`cypchemspace`。项目围绕“本地数据库中的膜相关 CYP 底物是否在 P450DB 背景底物的化学结构空间中表现出局部富集”这一问题，构建了从清洗后的底物表读取、RDKit 分子解析、Morgan fingerprint 生成、二维 embedding、kNN permutation 局部富集检验到核心图表输出的可复现流程。项目代码已整理为标准 `src-layout` 结构，包含命令行入口、可复用 API、pytest 测试、示例数据、demo notebook、README、环境文件、演示结果和课程文档。项目公开仓库链接为：<https://github.com/Zhaimiaoyizhi/cypchemspace>。

关键词：Cytochrome P450；Morgan fingerprint；RDKit；UMAP；kNN permutation；Python package

## 一、背景

细胞色素 P450（Cytochrome P450, CYP）是一类广泛参与小分子代谢、天然产物修饰、药物代谢和环境化合物转化的酶家族。不同来源的 CYP 底物在化学结构上可能具有不同的分布特征。例如，部分膜相关底物更偏疏水、脂溶或萜类/甾体类，而一些数据库背景底物可能更偏向氨基酸、吲哚或其他亲水性小分子。

原始 `CYP_comparison` 项目包含较完整的科研探索流程，包括底物抽取、结构映射、P450DB 背景整合、RDKit fingerprint、UMAP 可视化、kNN permutation 局部富集检验、fingerprint sensitivity、unique-InChIKey 去重敏感性分析和 logP 补充解释等。然而，原始项目包含大量全量数据、历史脚本和中间结果，不适合作为课程项目直接提交。

因此，本项目的目标不是提交完整科研仓库，而是将其中一条核心分析链路压缩为一个规范、轻量、可安装、可测试、可演示的 Python package。这样既保留真实生物信息学问题，又满足课程对软件工程规范和可复现分析流程的要求。

## 二、项目设计

### 2.1 总体目标

项目的核心问题为：

> 本地数据库中的膜相关 CYP 底物是否在 P450DB 背景底物的化学结构空间中表现出局部富集？

课程包将该问题抽象为以下计算流程：

```text
example substrate table
  -> input validation
  -> RDKit Mol parsing
  -> Morgan fingerprint matrix
  -> UMAP / PCA 2D embedding
  -> kNN label enrichment with permutation test
  -> summary.csv + cypchemspace_umap.png
```

### 2.2 项目结构

项目采用标准 `src-layout`：

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
```

主要模块如下：

| 模块 | 功能 |
|---|---|
| `io.py` | 读取 CSV/TSV 底物表并检查必要列 |
| `chem.py` | 使用 RDKit 解析 SMILES、规范化结构并生成 Morgan fingerprint |
| `embedding.py` | 使用 UMAP 或 PCA 生成二维化学空间坐标 |
| `enrichment.py` | 进行 kNN permutation 局部富集检验 |
| `visualize.py` | 输出核心二维散点图 |
| `cli.py` | 提供 `cypchemspace analyze` 命令行入口 |

### 2.3 数据设计

项目附带两类示例数据。第一类是很小的 toy table：`examples/example_data/cyp_substrates_demo.csv`，用于单元测试和快速理解数据格式。第二类是正式录屏演示使用的清洗表：`examples/example_data/clean_rescued_substrates_2548.csv`，该表从原始项目的 clean rescued 输出复制而来，包含 2,548 条可解析底物记录，其中 `mydb` 为 969 条，`p450db` 背景为 1,579 条。

出于课程提交和复现稳定性的考虑，本项目不直接包含更早阶段的原始数据库导出、历史中间结果或在线 PubChem 查询流程。课程包内的 `results/demo_clean_2548_128bit_pca_perm19/` 保存现场可复跑的快速演示结果；`results/full_clean_reference/` 保存原始项目中实际全量/参考运行结果，包括 5,000 次置换的 kNN enrichment 表和 clean rescued UMAP 图。

### 2.4 命令行与 API

命令行示例：

```bash
cypchemspace analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

主要输出：

- `embedding.csv`
- `summary.csv`
- `cypchemspace_umap.png`

API 示例：

```python
from cypchemspace import load_substrate_table, make_morgan_fingerprint_matrix, knn_label_enrichment

table = load_substrate_table("examples/example_data/clean_rescued_substrates_2548.csv")
fingerprints, valid_table = make_morgan_fingerprint_matrix(table, n_bits=128)
stats = knn_label_enrichment(fingerprints, valid_table["label"], positive_label="mydb", k=15, n_permutations=19)
```

## 三、测试结果

项目包含 pytest 测试套件，覆盖以下关键行为：

1. 示例数据读取和必要列检查。
2. 缺失必要列时抛出错误。
3. 无效 SMILES 不导致流程崩溃。
4. 等价 SMILES 可以得到一致的规范化结果。
5. Morgan fingerprint 矩阵维度与输入分子数匹配。
6. toy fingerprint 数据中 kNN enrichment 能检测正类局部聚集。
7. CLI 能生成 `embedding.csv`、`summary.csv` 和 `cypchemspace_umap.png`。

本机验证命令：

```bash
python -m pytest
```

已验证结果：

```text
7 passed
```

CLI 演示命令：

```bash
python -m cypchemspace.cli analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

演示输出中，`summary.csv` 显示：

| 指标 | 数值 |
|---|---:|
| n_rows | 2548 |
| n_positive | 969 |
| observed_positive_neighbor_fraction | 0.5155142758857929 |
| mean_null_positive_neighbor_fraction | 0.3781869534517408 |
| delta | 0.1373273224340521 |
| p_value | 0.05 |

该演示使用 128-bit fingerprint、PCA 和 19 次置换，运行时间适合录屏现场复现。结果说明，在清洗后的 2,548 条底物记录中，`mydb` 类底物在 fingerprint 近邻空间中相对于随机标签置换表现出局部聚集。需要注意的是，19 次置换的经验 p 值分辨率较粗，因此它主要用于展示完整流程。

项目实际全量/参考结果保存在 `results/full_clean_reference/`。其中 `combined_stats_results_perm5000.tsv` 使用 5,000 次置换，结果如下：

| k | obs_knn_enrichment | null_mean | delta_vs_null | p_perm_one_sided_greater |
|---:|---:|---:|---:|---:|
| 10 | 0.5396284829721361 | 0.3800361197110423 | 0.15959236326109377 | 0.0001999600079984003 |
| 15 | 0.5137942896456829 | 0.37996250429996564 | 0.1338317853457172 | 0.0001999600079984003 |
| 30 | 0.47481940144478846 | 0.37996431372549017 | 0.09485508771929829 | 0.0001999600079984003 |

该参考结果与现场演示结果方向一致，但置换次数更高，因此更适合用于最终报告中的统计解释。

## 四、讨论

本项目的主要价值在于将一个复杂科研探索仓库整理为课程项目可评价的软件作品。相比直接提交原始 `CYP_comparison`，`cypchemspace` 具有更清晰的边界、更小的数据规模和更规范的软件结构。任课教师或助教可以通过 README、CLI、notebook 和 pytest 快速理解并复现项目。

从方法上看，Morgan fingerprint 提供了小分子结构的离散向量表示，UMAP/PCA 提供二维可视化，kNN permutation test 则提供局部富集的统计判断。报告中特别强调：UMAP 图不能单独作为统计结论，必须与 kNN permutation 结果结合解释。

本项目也存在限制。首先，现场演示为了录屏速度采用 128-bit fingerprint、PCA 和 19 次置换，因此 p 值只能作为流程演示，不应替代 5,000 次置换参考结果。其次，项目没有纳入在线 PubChem 结构映射、LLM rescue、八种 fingerprint sensitivity、unique-InChIKey 去重和 logP 分析等完整扩展流程。再次，logP 或化学空间聚集只能辅助解释底物性质，不能直接证明蛋白膜定位。

未来可扩展方向包括：加入多种 RDKit fingerprint 的敏感性分析、加入 unique-InChIKey 去重流程、加入 logP 统计模块、增加完整数据下载/复现脚本，以及用 Snakemake 或 Nextflow 管理全流程。

## 五、参考文献

[1] Guengerich F P. Cytochrome P450 and chemical toxicology[J]. *Chemical Research in Toxicology*, 2008, 21(1): 70-83. DOI: [10.1021/tx700079z](https://doi.org/10.1021/tx700079z).

[2] Zhang Y, Pan X, Shi T, et al. P450Rdb: A manually curated database of reactions catalyzed by cytochrome P450 enzymes[J]. *Journal of Advanced Research*, 2024, 63: 35-42. DOI: [10.1016/j.jare.2023.10.012](https://doi.org/10.1016/j.jare.2023.10.012).

[3] Preissner S, Kroll K, Dunkel M, et al. SuperCYP: a comprehensive database on Cytochrome P450 enzymes including a tool for analysis of CYP-drug interactions[J]. *Nucleic Acids Research*, 2010, 38(suppl_1): D237-D243. DOI: [10.1093/nar/gkp970](https://doi.org/10.1093/nar/gkp970).

[4] Rogers D, Hahn M. Extended-connectivity fingerprints[J]. *Journal of Chemical Information and Modeling*, 2010, 50(5): 742-754. DOI: [10.1021/ci100050t](https://doi.org/10.1021/ci100050t).

[5] Bajusz D, Racz A, Heberger K. Why is Tanimoto index an appropriate choice for fingerprint-based similarity calculations?[J]. *Journal of Cheminformatics*, 2015, 7: 20. DOI: [10.1186/s13321-015-0069-3](https://doi.org/10.1186/s13321-015-0069-3).

[6] Landrum G. RDKit: Open-source cheminformatics. Release 2014.03.1[EB/OL]. Zenodo, 2014. DOI: [10.5281/zenodo.10398](https://doi.org/10.5281/zenodo.10398).

[7] McInnes L, Healy J, Melville J. UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction[EB/OL]. arXiv, 2018. arXiv: [1802.03426](https://arxiv.org/abs/1802.03426).

[8] Healy J, McInnes L. Uniform manifold approximation and projection[J]. *Nature Reviews Methods Primers*, 2024, 4: 82. DOI: [10.1038/s43586-024-00363-x](https://doi.org/10.1038/s43586-024-00363-x).
