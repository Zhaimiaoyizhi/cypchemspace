# cypchemspace 项目介绍视频录制文稿

本文档是单人项目介绍视频的录制脚本。推荐录制方式为：

```text
电脑端腾讯会议共享屏幕并录制
手机加入同一会议并负责语音解说
电脑麦克风关闭，手机麦克风打开
```

这个方案可行，而且适合本项目：电脑负责展示 GitHub、README、代码、命令行和结果图；手机负责稳定收音。正式录制前务必做 30 秒试录，确认画面能看清、手机声音被录进去、电脑端没有回声。

建议视频时长：8-10 分钟。最终文件建议命名为：

```text
cypchemspace_project_demo.mp4
```

## 一、录制前准备

### 1. 打开项目目录

PowerShell 进入项目目录：

```powershell
cd "D:\CLASSFILES\【项目】膜酶检索数据库\CYP_comparison\course_project_cypchemspace"
```

如果本机 Python 或 pandas 在 Windows 平台探测时卡住，先设置：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
```

### 2. 打开 GitHub 页面

浏览器打开：

```text
https://github.com/Zhaimiaoyizhi/cypchemspace
```

开场时展示这个页面，因为结题报告摘要中需要包含项目公开仓库链接。

### 3. 提前打开这些文件

建议在 VS Code 或资源管理器中提前打开：

```text
README.md
docs/final_report.md
src/cypchemspace/cli.py
src/cypchemspace/chem.py
src/cypchemspace/enrichment.py
examples/example_data/clean_rescued_substrates_2548.csv
results/demo_clean_2548_128bit_pca_perm19/summary.csv
results/demo_clean_2548_128bit_pca_perm19/cypchemspace_umap.png
results/full_clean_reference/combined_stats_results_perm5000.tsv
results/full_clean_reference/umap_mydb_vs_background_clean_rescued.png
```

### 4. 现场演示命令

正式录制时运行这一条：

```powershell
python -m cypchemspace.cli analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

这条命令使用：

- 输入表：`clean_rescued_substrates_2548.csv`，共 2,548 条清洗后底物记录
- fingerprint：Morgan radius 2，128 bit
- embedding：PCA
- kNN 参数：`k=15`
- permutation：19 次

本机实测运行约 15 秒，适合录屏现场跑。少量 RDKit warning 不影响输出，只要最后出现 `Wrote ... summary.csv`、`Wrote ... cypchemspace_umap.png` 即可。

### 5. 录制设置检查

- 电脑端腾讯会议：共享整个屏幕，开启录制，关闭麦克风。
- 手机端腾讯会议：打开麦克风，靠近自己，关闭摄像头或按课程要求打开。
- 电脑扬声器：调低音量，避免回声。
- 录制前试录 30 秒：检查画面、声音和鼠标移动是否清楚。

## 二、视频结构

| 时间 | 屏幕展示 | 说明重点 |
|---|---|---|
| 0:00-0:40 | GitHub 仓库首页 | 项目名称、公开链接、单人项目 |
| 0:40-1:30 | README | 生物问题和软件包目标 |
| 1:30-2:30 | 项目目录 | package 结构、API、CLI、tests、docs、results |
| 2:30-3:20 | 输入表 | 2548 条清洗底物、mydb 和 p450db 标签 |
| 3:20-4:40 | PowerShell | 现场运行 128-bit + PCA + 19 次置换 |
| 4:40-5:50 | 演示结果 | `summary.csv` 和 PCA 图 |
| 5:50-6:50 | 全量参考结果 | 5,000 次置换统计表和 UMAP 图 |
| 6:50-7:40 | pytest | 自动化测试通过 |
| 7:40-8:50 | final_report.md | 讨论、局限、提交材料 |
| 8:50-9:30 | GitHub README | 总结项目价值 |

## 三、详细讲稿

### 片段 1：开场与仓库链接

屏幕操作：

1. 打开 GitHub 仓库首页。
2. 让仓库标题、README 开头和文件结构出现在画面里。

建议解说：

> 大家好，我的项目是 cypchemspace。它是一个用于比较 CYP 底物化学空间的 Python package。项目已经上传到公开 GitHub 仓库，链接是 https://github.com/Zhaimiaoyizhi/cypchemspace。
>
> 这是一个单人项目。我的目标不是直接提交原始的大型研究仓库，而是把其中最适合课程展示的一条分析主线包装成一个结构规范、可以安装、可以运行、有测试、有文档、有结果输出的课程项目。

### 片段 2：项目背景和核心问题

屏幕操作：

1. 切到 README。
2. 展示 `Biological Question` 和流程列表。

建议解说：

> 项目的生物学背景是细胞色素 P450，也就是 CYP。CYP 参与很多小分子代谢、天然产物修饰和药物代谢过程。不同来源的 CYP 底物在化学结构空间中可能不是随机分布的。
>
> 这个项目关注的问题是：本地数据库中的膜相关 CYP 底物，也就是 mydb 这一组，是否在 P450DB 背景底物的化学结构空间中表现出局部富集。
>
> 为了把这个问题转化为可运行的软件流程，我设计了这样一条链路：读取底物表，解析标准化 SMILES，生成 Morgan fingerprint，做二维 embedding，然后用 kNN permutation test 判断 mydb 底物是否更倾向于互为近邻。

需要强调：

- 图只是帮助观察分布。
- 最终统计判断来自 kNN permutation test。
- 这不是证明膜定位，而是比较底物化学结构空间。

### 片段 3：项目结构

屏幕操作：

1. 切到 VS Code 或资源管理器。
2. 展示目录：

```text
src/cypchemspace/
tests/
examples/
docs/
results/
```

建议解说：

> 这个项目采用标准 Python src-layout。核心代码放在 src/cypchemspace 下面，测试放在 tests，示例数据和 notebook 放在 examples，报告和视频文稿放在 docs，演示结果和参考结果放在 results。
>
> 这样的结构是为了让它像一个真正的 Python package，而不是一堆临时脚本。老师或助教可以通过 README 安装项目，通过 CLI 运行分析，也可以通过 pytest 检查核心功能。

可以逐个说明源代码：

| 文件 | 解说 |
|---|---|
| `io.py` | 读取 CSV/TSV，并检查 `compound_id`、`std_smiles`、`label` 等必要列 |
| `chem.py` | 用 RDKit 解析 SMILES，并生成 Morgan fingerprint |
| `embedding.py` | 支持 UMAP，也支持 PCA fallback |
| `enrichment.py` | 实现 kNN permutation 局部富集检验 |
| `visualize.py` | 输出二维散点图 |
| `cli.py` | 组织完整命令行流程 |

### 片段 4：输入数据

屏幕操作：

1. 打开 `examples/example_data/clean_rescued_substrates_2548.csv`。
2. 展示列名和前几行。

建议解说：

> 这里是本次录屏演示使用的数据表。它不是早期未处理的原始数据库导出，而是从原始项目 clean rescued 步骤复制进课程包的清洗后底物表。
>
> 这张表一共有 2,548 条可解析底物记录，其中 mydb 有 969 条，p450db 背景有 1,579 条。主要字段包括 compound_id、原始 SMILES、标准化 SMILES、InChIKey 和 label。
>
> 我把这张表放进仓库，是为了让演示命令不依赖外部路径，评阅者下载仓库后也可以直接复现。同时时，早期原始大表、PubChem 查询缓存和历史探索脚本没有放进课程包，避免仓库过大和流程边界不清。

### 片段 5：命令行现场演示

屏幕操作：

1. 切到 PowerShell。
2. 运行 help：

```powershell
python -m cypchemspace.cli --help
```

建议解说：

> 这个项目提供命令行入口，可以通过 python -m cypchemspace.cli 调用。这里可以看到主要子命令是 analyze，它负责从输入表一直跑到结果输出。

接着运行正式演示命令：

```powershell
python -m cypchemspace.cli analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

等待命令完成。成功时会看到：

```text
Wrote results\demo_clean_2548_128bit_pca_perm19\embedding.csv
Wrote results\demo_clean_2548_128bit_pca_perm19\summary.csv
Wrote results\demo_clean_2548_128bit_pca_perm19\cypchemspace_umap.png
```

建议解说：

> 这里为了保证现场演示速度，我采用 128-bit Morgan fingerprint、PCA embedding 和 19 次 label permutation。它不是最重的科研运行配置，而是一个适合录屏现场复现的演示配置。本机大约十几秒可以跑完。
>
> 输出有三个核心文件：embedding.csv 是每个底物的二维坐标，summary.csv 是 kNN permutation 统计结果，cypchemspace_umap.png 是二维化学空间图。文件名里虽然保留了 umap，这是历史命名，当前这次演示参数实际使用的是 PCA。

### 片段 6：解释现场演示结果

屏幕操作：

1. 打开 `results/demo_clean_2548_128bit_pca_perm19/summary.csv`。
2. 放大表格中的关键列。

建议解说：

> 这个 summary 是现场演示结果。n_rows 是 2548，表示进入分析的有效分子数；n_positive 是 969，也就是 mydb 记录数。
>
> observed_positive_neighbor_fraction 是真实标签下，mydb 底物附近邻居仍然是 mydb 的比例，这里约为 0.516。mean_null_positive_neighbor_fraction 是随机打乱标签后的平均比例，约为 0.378。两者差值 delta 约为 0.137。
>
> 这说明 mydb 底物在 fingerprint 近邻空间中比随机标签更倾向于互相靠近。p_value 是 0.05，但这里要注意，因为演示只做了 19 次置换，所以 p 值分辨率很粗。这个结果主要用于说明流程可以跑通。

屏幕操作：

1. 打开 `results/demo_clean_2548_128bit_pca_perm19/cypchemspace_umap.png`。

建议解说：

> 这张图是二维化学空间可视化。它帮助我们直观看 mydb 和 p450db 在二维空间中的分布。需要注意的是，二维图本身不是统计证明，因为 PCA 或 UMAP 都会压缩高维信息。真正的统计判断要结合刚才的 kNN permutation 表。

### 片段 7：展示项目实际全量参考结果

屏幕操作：

1. 打开 `results/full_clean_reference/combined_stats_results_perm5000.tsv`。
2. 再打开 `results/full_clean_reference/umap_mydb_vs_background_clean_rescued.png`。

建议解说：

> 接下来展示项目实际全量或参考运行结果。它放在 results/full_clean_reference 目录中，不是现场快速演示参数，而是从原始工作流复制过来的正式参考结果。
>
> 这里的 kNN enrichment 使用 5,000 次置换。以 k=15 为例，observed enrichment 约为 0.514，null mean 约为 0.380，delta 约为 0.134，单侧置换 p 值约为 0.0002。这个方向和刚才现场演示一致，但置换次数更多，因此更适合用于最终报告解释。
>
> 这张 UMAP 图对应 clean rescued 分析的最终可视化结果。我的展示逻辑是：现场跑一个快版本证明软件流程可复现，再展示这个 full reference 结果作为项目实际分析结论的支撑。

### 片段 8：pytest 测试

屏幕操作：

运行：

```powershell
python -m pytest
```

如果本机卡住或平台探测慢，就运行：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
python -m pytest
```

建议解说：

> 课程项目不仅要有结果，也要体现软件工程规范。所以我写了 pytest 测试，覆盖输入表读取、必要列检查、SMILES 解析、fingerprint 维度、kNN enrichment 行为和 CLI smoke test。
>
> 这里可以看到测试结果是 7 passed，说明核心 API 和命令行流程都能正常工作。

### 片段 9：报告和文档

屏幕操作：

1. 打开 `docs/final_report.md`。
2. 展示摘要、项目设计、测试结果和讨论。
3. 回到 README 的 deliverables 列表。

建议解说：

> 结题报告按照摘要、背景、项目设计、测试结果、讨论和参考文献组织。摘要中包含公开 GitHub 链接。报告中也区分了现场演示结果和 full reference 结果，避免把 19 次置换的快速演示当作最终统计结论。
>
> README 中写了安装方法、快速开始、API 示例、数据来源、结果解释和局限。docs 目录中还包含开题报告、tutorial、slides outline 和当前这个视频录制文稿。

### 片段 10：总结

屏幕操作：

回到 GitHub 仓库首页或 README 顶部。

建议解说：

> 总结一下，cypchemspace 是一个围绕 CYP 底物化学空间比较的 Python package。它把原始复杂研究仓库中的核心分析主线整理成了可安装、可运行、可测试、可展示的课程项目。
>
> 录屏中我现场运行了 2548 条清洗底物的快速演示，也展示了 5,000 次置换的 full reference 结果。项目包括规范代码结构、命令行入口、可复用 API、示例数据、自动化测试、notebook、README、结题报告和结果图表。我的介绍到这里结束，谢谢大家。

## 四、常见问题处理

### 1. 现场运行太慢怎么办

本机实测 128-bit + PCA + 19 次置换约 15 秒。录制前先跑一遍，如果超过 1 分钟，可以：

1. 继续等待，不要中断，只要屏幕有输出即可。
2. 直接展示已经生成的 `results/demo_clean_2548_128bit_pca_perm19/`，并说明“这里是刚才命令生成的结果目录”。
3. 不要临时切换到 2048-bit 或 99 次置换，这会明显增加录制风险。

### 2. RDKit 出现 warning 怎么办

如果出现类似：

```text
WARNING: not removing hydrogen atom with dummy atom neighbors
```

不用慌，只要最后生成了 `summary.csv` 和图片即可。讲解时可以忽略这个 warning，或者简单说“这是 RDKit 对个别结构的 warning，不影响本次输出文件生成”。

### 3. 如果 pytest 卡住怎么办

先运行：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
python -m pytest
```

如果仍然慢，可以展示 README 中的测试命令和本地已有的通过记录，不建议在视频里长时间等待。

### 4. MP4 文件要不要上传 GitHub

不建议把 MP4 放进 GitHub 仓库。视频文件通常较大，适合单独提交到课程平台。如果必须放本地项目目录，可以放在：

```text
docs/cypchemspace_project_demo.mp4
```

但不建议提交到 GitHub。

## 五、录制前检查清单

- [ ] GitHub 仓库可打开：`https://github.com/Zhaimiaoyizhi/cypchemspace`
- [ ] PowerShell 已进入项目根目录。
- [ ] `python -m cypchemspace.cli --help` 可以运行。
- [ ] 现场演示命令可以生成 `results/demo_clean_2548_128bit_pca_perm19/summary.csv`。
- [ ] `results/full_clean_reference/combined_stats_results_perm5000.tsv` 可以打开。
- [ ] `results/full_clean_reference/umap_mydb_vs_background_clean_rescued.png` 可以打开。
- [ ] `python -m pytest` 或带 `PYTHONPATH` 的 pytest 可以显示 `7 passed`。
- [ ] 手机麦克风清楚，电脑麦克风关闭。
- [ ] 腾讯会议试录 30 秒，确认视频和声音正常。
