# 项目介绍视频录制指南

课程要求提交小组全员录制的项目介绍与演示视频，格式为 MP4。该视频需要由小组成员实际录制，我无法替你生成真实的小组出镜视频；下面提供推荐结构、分工和台词提纲。

## 一、建议时长

建议 6-10 分钟。

## 二、推荐分工

| 成员 | 建议负责内容 | 建议时长 |
|---|---|---:|
| 成员 1 | 项目背景、研究问题、数据来源 | 1.5-2 分钟 |
| 成员 2 | package 结构、核心模块、API/CLI 设计 | 2 分钟 |
| 成员 3 | 运行演示、测试结果、输出图表解释 | 2-3 分钟 |
| 成员 4 | 讨论、局限、未来改进 | 1-2 分钟 |

如果小组人数不同，可以合并或拆分上述内容。

## 三、视频内容结构

### 1. 开场

说明项目名称：

> 大家好，我们小组的 BIO2502 课程项目是 cypchemspace，一个用于比较 CYP 底物化学空间的 Python package。

### 2. 项目背景

说明 CYP 的生物学意义，以及为什么比较 `mydb` 与 P450DB 背景底物。

重点表达：

- CYP 参与多种小分子代谢。
- 不同来源底物可能在化学结构空间中分布不同。
- 本项目关注 `mydb` 底物在 P450DB 背景空间中的局部富集。

### 3. 项目设计

展示项目目录结构：

```text
src/cypchemspace/
tests/
examples/
docs/
```

说明核心流程：

```text
SMILES -> RDKit Mol -> Morgan fingerprint -> embedding -> kNN permutation -> figure + summary
```

### 4. 命令行演示

建议在视频中录屏运行：

```bash
python -m cypchemspace.cli analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-bits 128 --k 3 --n-permutations 99 --embedding-method pca
```

展示生成文件：

- `results/demo_run/embedding.csv`
- `results/demo_run/summary.csv`
- `results/demo_run/cypchemspace_umap.png`

### 5. 测试展示

运行：

```bash
python -m pytest
```

说明测试覆盖：

- 数据读取。
- SMILES 解析。
- fingerprint 矩阵。
- kNN enrichment。
- CLI 输出。

### 6. 结果解释

说明示例结果中：

- `observed_positive_neighbor_fraction = 1.0`
- `delta > 0`
- `p_value = 0.01`

解释为：在教学示例数据中，`mydb` 类底物表现出局部聚集。强调这是方法演示，完整科研结论需要全量数据支持。

### 7. 讨论与局限

必须提到：

- UMAP 图不是统计检验。
- 示例数据是教学子集，不是完整研究数据。
- 本 package 不包含在线 PubChem 查询、LLM rescue、全量 fingerprint sensitivity。
- 后续可扩展 unique-InChIKey 去重、logP 分析和 Snakemake workflow。

## 四、录制技术建议

- 使用 OBS Studio、PowerPoint 录屏、腾讯会议录制或系统自带录屏工具。
- 分辨率建议 1920x1080。
- 导出格式为 MP4。
- 视频文件名建议：`cypchemspace_project_demo.mp4`。
- 录制前先本地运行一遍 CLI 和 pytest，避免视频中临时出错。

## 五、提交前检查清单

- [ ] 每位小组成员至少有一次发言或署名说明。
- [ ] 视频中出现项目名称 `cypchemspace`。
- [ ] 视频中展示 GitHub/Gitee 仓库页面。
- [ ] 视频中展示 README。
- [ ] 视频中展示 CLI 运行。
- [ ] 视频中展示测试结果。
- [ ] 视频中展示核心图表。
- [ ] 视频格式为 MP4。
