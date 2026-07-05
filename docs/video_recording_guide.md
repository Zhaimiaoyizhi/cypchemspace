# cypchemspace 项目介绍视频录制文稿与操作指南

本文档用于录制课程项目介绍视频。当前项目为单人项目，因此视频不需要体现小组分工；建议采用“电脑端腾讯会议共享屏幕录制 + 手机入会语音解说”的方式完成。这个方案可行，而且比较稳妥：电脑负责展示代码、README、命令行和结果图，手机负责收音，避免电脑麦克风或录屏软件音频设置出问题。

建议视频时长为 7-9 分钟。最终导出文件建议命名为：

```text
cypchemspace_project_demo.mp4
```

## 一、录制方式是否可行

你计划采用：

```text
电脑打开腾讯会议并共享屏幕
手机加入同一个会议并负责语音解说
腾讯会议录制电脑共享屏幕和手机声音
```

这是可行的，但录制前需要注意 5 件事：

1. 电脑端入会后关闭电脑麦克风，避免电脑和手机同时收音产生回声。
2. 手机端入会后打开麦克风，作为唯一收音设备。
3. 手机尽量靠近你，远离电脑扬声器。如果有耳机，可以手机接耳机麦克风。
4. 电脑端共享“整个屏幕”或共享包含 VS Code/浏览器/终端的窗口。
5. 录制前做 30 秒试录，确认视频中能看到屏幕、能听到手机声音。

推荐配置：

| 设备 | 操作 |
|---|---|
| 电脑腾讯会议 | 开启录制、共享屏幕、关闭麦克风 |
| 手机腾讯会议 | 打开麦克风、关闭摄像头或按课程要求开摄像头 |
| 电脑扬声器 | 音量调低，避免回声 |
| 浏览器 | 打开 GitHub 仓库、README 和结果图 |
| 终端 | 准备好项目目录和演示命令 |

## 二、录制前准备

### 1. 打开项目目录

电脑上打开项目目录：

```text
D:\CLASSFILES\【项目】膜酶检索数据库\CYP_comparison\course_project_cypchemspace
```

建议用 VS Code 或资源管理器打开。

### 2. 打开 GitHub 仓库

浏览器打开：

```text
https://github.com/Zhaimiaoyizhi/cypchemspace
```

录制时要展示这个页面，因为结题报告摘要中写了项目链接。

### 3. 打开本地文件

建议提前打开以下文件或页面：

```text
README.md
docs/final_report.md
examples/demo_cypchemspace.ipynb
results/demo_run/summary.csv
results/demo_run/cypchemspace_umap.png
```

### 4. 打开终端并进入项目目录

PowerShell 中运行：

```powershell
cd "D:\CLASSFILES\【项目】膜酶检索数据库\CYP_comparison\course_project_cypchemspace"
```

如果本机 Python 运行 pytest 或 pandas 时卡住，可以先设置：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
```

### 5. 预先跑一遍命令

录制前先确认以下命令可用：

```powershell
python -m cypchemspace.cli --help
python -m cypchemspace.cli analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-bits 128 --k 3 --n-permutations 99 --embedding-method pca
python -m pytest
```

如果都能运行，再开始正式录制。

## 三、视频整体结构

建议按以下顺序录制：

| 时间 | 屏幕展示 | 讲解重点 |
|---|---|---|
| 0:00-0:40 | GitHub 仓库首页 | 项目名称、项目目标、公开链接 |
| 0:40-1:40 | README | 背景问题和分析流程 |
| 1:40-2:50 | 项目目录和源码 | package 结构与模块职责 |
| 2:50-4:10 | 示例数据和命令行 | 输入数据、CLI 运行 |
| 4:10-5:20 | 输出结果 | summary.csv 和 UMAP 图 |
| 5:20-6:20 | pytest | 测试覆盖和测试通过 |
| 6:20-7:40 | final_report.md | 讨论、局限、未来工作 |
| 7:40-8:20 | GitHub / README | 总结和提交材料说明 |

不需要逐字背诵，但建议按下面文稿讲，录出来会比较完整。

## 四、详细录制文稿

### 片段 1：开场与项目链接

屏幕操作：

1. 浏览器打开 GitHub 仓库：`https://github.com/Zhaimiaoyizhi/cypchemspace`
2. 停留在仓库首页，让 README 标题和目录结构可见。

建议解说：

> 大家好，我的课程项目是 cypchemspace。这个项目是一个用于比较 CYP 底物化学空间的 Python package。项目已经上传到了公开 GitHub 仓库，链接是 https://github.com/Zhaimiaoyizhi/cypchemspace。  
>  
> 我做这个项目的目标，是把原来比较复杂的 CYP_comparison 分析仓库，裁剪成一个结构清楚、可以安装、可以运行、有测试、有 notebook 演示的小型课程项目。

需要强调：

- 这是单人项目。
- GitHub 仓库是最终代码提交位置。
- 项目不是把完整大仓库原样提交，而是包装成可复现 package。

### 片段 2：研究背景与问题

屏幕操作：

1. 滚动 README 到 `Biological Question`。
2. 指出核心问题文字。

建议解说：

> 项目的生物学背景是 CYP，也就是细胞色素 P450。CYP 参与很多小分子代谢、天然产物修饰和药物代谢。不同来源的 CYP 底物在化学结构空间里可能不是随机分布的。  
>  
> 这个项目关注的问题是：本地数据库中的膜相关 CYP 底物，也就是 mydb 这一组，是否在 P450DB 背景底物的化学结构空间中表现出局部富集。  
>  
> 为了把这个问题变成可以运行的程序，我设计了一个小型流程：读取底物表，解析 SMILES，生成 Morgan fingerprint，做二维 embedding，再用 kNN permutation test 判断 mydb 底物是不是更倾向于互为近邻。

需要强调：

- UMAP/PCA 图只是可视化。
- 真正用于判断局部富集的是 kNN permutation test。

### 片段 3：项目结构

屏幕操作：

1. 切换到 VS Code 或资源管理器。
2. 展示项目目录：

```text
src/cypchemspace/
tests/
examples/
docs/
results/
```

建议解说：

> 这个项目采用标准的 Python src-layout 结构。核心代码放在 src/cypchemspace 下面，测试放在 tests，示例数据和 notebook 放在 examples，报告和说明文档放在 docs，演示输出放在 results。  
>  
> 这样的结构是为了让项目既能作为普通 Python 包安装，也方便老师或助教直接检查代码、运行测试和复现实验。

逐个说明源码文件：

| 文件 | 解说内容 |
|---|---|
| `io.py` | 负责读取 CSV 或 TSV，并检查 `compound_id`、`std_smiles`、`label` 等必要列 |
| `chem.py` | 负责用 RDKit 解析 SMILES，生成 Morgan fingerprint |
| `embedding.py` | 负责生成二维坐标，默认支持 UMAP，也支持 PCA fallback |
| `enrichment.py` | 负责 kNN permutation 局部富集检验 |
| `visualize.py` | 负责输出二维散点图 |
| `cli.py` | 负责命令行入口 |

建议解说：

> 每个模块只负责一类任务，避免把所有逻辑写在一个脚本里。比如化学结构相关函数放在 chem.py，统计检验放在 enrichment.py，命令行解析放在 cli.py。这样代码比较容易测试和维护。

### 片段 4：示例数据

屏幕操作：

1. 打开 `examples/example_data/cyp_substrates_demo.csv`。
2. 展示列名和几行数据。

建议解说：

> 这里是项目自带的小型示例数据。它不是完整原始大数据，而是从原项目中抽取和整理出来的教学演示数据。  
>  
> 主要列包括 compound_id，也就是底物名称；std_smiles，也就是标准化 SMILES；label，也就是来源标签，分为 mydb 和 p450db。  
>  
> 我没有把完整原始大表放进课程包，因为那样会让提交包非常大，也不利于复现和评分。这个小数据集的作用是完整演示方法流程。

需要强调：

- 示例数据用于课程演示。
- 完整科研结论不只依赖这个小数据集。
- 这能解释为什么包小、结构清晰。

### 片段 5：命令行演示

屏幕操作：

1. 切换到 PowerShell。
2. 确认目录在项目根目录。
3. 先运行 help：

```powershell
python -m cypchemspace.cli --help
```

建议解说：

> 这个项目提供了命令行入口，可以直接用 python -m cypchemspace.cli 调用。先看 help，可以看到目前主要命令是 analyze。

接着运行分析命令：

```powershell
python -m cypchemspace.cli analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-bits 128 --k 3 --n-permutations 99 --embedding-method pca
```

建议解说：

> 这条命令读取 example_data 里的示例底物表，输出到 results/demo_run。这里为了演示速度，把 fingerprint bit 数设置成 128，把 k 设置成 3，置换次数设置成 99，并使用 PCA 作为二维 embedding 方法。实际项目中也可以用默认的 Morgan 2048 bits 和 UMAP。

命令成功后，屏幕应显示：

```text
Wrote results\demo_run\embedding.csv
Wrote results\demo_run\summary.csv
Wrote results\demo_run\cypchemspace_umap.png
```

建议解说：

> 程序生成了三个核心输出：embedding.csv 是每个底物的二维坐标，summary.csv 是 kNN permutation 的统计结果，cypchemspace_umap.png 是核心图表。

### 片段 6：结果文件解释

屏幕操作：

1. 打开 `results/demo_run/summary.csv`。
2. 放大显示关键列。

重点解释这些列：

| 列 | 解释 |
|---|---|
| `n_rows` | 进入分析的底物数量 |
| `n_positive` | mydb 底物数量 |
| `observed_positive_neighbor_fraction` | 真实标签下，mydb 近邻仍为 mydb 的比例 |
| `mean_null_positive_neighbor_fraction` | 随机置换标签后的平均近邻比例 |
| `delta` | observed 减去 null mean |
| `p_value` | 经验置换检验 p 值 |

建议解说：

> 这里最重要的是 observed、null mean、delta 和 p_value。observed 表示真实标签下 mydb 底物附近有多少近邻仍然是 mydb。null mean 是把标签随机打乱后得到的平均结果。  
>  
> 如果 observed 明显大于 null mean，delta 为正，并且 p 值比较低，就说明 mydb 底物在这个 fingerprint 空间里不是随机散开的，而是有局部聚集趋势。

屏幕操作：

1. 打开 `results/demo_run/cypchemspace_umap.png`。

建议解说：

> 这张图是二维化学空间可视化。蓝色点表示 mydb，灰色点表示 P450DB 背景。图可以帮助我们直观看到底物分布，但我不会只凭图下结论，因为二维 embedding 会压缩信息。最终解释要结合刚才的 kNN permutation 统计表。

### 片段 7：notebook 演示

屏幕操作：

1. 打开 `examples/demo_cypchemspace.ipynb`。
2. 展示前几个 cell，不一定现场全运行。

建议解说：

> 除了命令行，我还提供了 demo notebook。notebook 更适合老师或同学逐步查看每一步的输入和输出。它从读取数据开始，生成 fingerprint，再计算 embedding 和 enrichment，最后保存图表和 summary。

如果时间充足，可以运行第一个 cell 或展示已有输出路径。

### 片段 8：测试演示

屏幕操作：

1. 切换到 PowerShell。
2. 运行：

```powershell
python -m pytest
```

如果本机卡在 Windows 平台探测，先运行：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
python -m pytest
```

建议解说：

> 下面展示测试。测试套件覆盖了数据读取、缺失列报错、SMILES 解析、fingerprint 矩阵维度、kNN enrichment 和 CLI 输出。  
>  
> 可以看到 pytest 结果是 7 passed，说明这些核心功能都通过了自动化测试。

屏幕上看到：

```text
7 passed
```

### 片段 9：README 与提交材料

屏幕操作：

1. 回到 GitHub README。
2. 展示 `Course Deliverables` 或 README 中的安装、Quick Start、API 示例。

建议解说：

> README 里写了项目背景、安装方法、快速开始、API 示例、数据来源、结果解释和局限。课程相关材料也都放在 docs 目录下，包括结题报告、开题报告、tutorial、展示提纲和视频录制指南。

需要展示：

- `docs/final_report.md`
- `docs/proposal.md`
- `docs/tutorial.md`
- `docs/slides_outline.md`
- `docs/video_recording_guide.md`

### 片段 10：讨论和局限

屏幕操作：

1. 打开 `docs/final_report.md`。
2. 滚动到“讨论”部分。

建议解说：

> 这个项目的主要价值，是把一个复杂的科研探索仓库整理为可提交、可运行、可测试的课程项目。  
>  
> 但它也有局限。第一，示例数据是教学子集，不能替代完整研究数据。第二，UMAP 或 PCA 图只是可视化，不是统计证明。第三，这个课程包没有包含在线 PubChem 查询、LLM rescue、全量 fingerprint sensitivity 和 unique-InChIKey 去重分析。  
>  
> 后续如果继续扩展，可以加入多种 fingerprint 的敏感性分析、结构级去重、logP 分析，以及 Snakemake workflow。

### 片段 11：结尾

屏幕操作：

1. 回到 GitHub 仓库首页。
2. 停留在项目标题和 README。

建议解说：

> 总结一下，cypchemspace 是一个围绕 CYP 底物化学空间比较的 Python package。它包含规范的项目结构、可复用 API、命令行工具、示例数据、notebook、测试套件和课程报告。  
>  
> 项目已经上传到公开 GitHub 仓库，老师和同学可以通过 README 里的命令复现实验流程。我的介绍到这里结束，谢谢大家。

## 五、腾讯会议录制操作步骤

### 1. 创建会议

1. 电脑打开腾讯会议。
2. 创建快速会议。
3. 手机扫码或输入会议号加入。

### 2. 设置音频

电脑端：

- 关闭麦克风。
- 保留扬声器低音量或静音。

手机端：

- 打开麦克风。
- 摄像头可按课程要求打开或关闭。
- 手机靠近你，用它收音。

### 3. 共享屏幕

电脑端点击共享屏幕，建议共享整个屏幕。正式录制前确认能看到：

- 浏览器 GitHub 页面。
- VS Code 或资源管理器。
- PowerShell。
- 结果图。

### 4. 开始录制

电脑端点击录制。如果腾讯会议提示选择本地录制或云录制，建议选择本地录制，方便导出 MP4。

### 5. 结束录制

录制结束后等待腾讯会议转换视频。确认文件为 MP4。如果不是 MP4，可以用格式转换工具转换。

## 六、录制前检查清单

- [ ] GitHub 页面可以打开：`https://github.com/Zhaimiaoyizhi/cypchemspace`
- [ ] README 可以看到安装和 Quick Start。
- [ ] PowerShell 已进入项目目录。
- [ ] `python -m cypchemspace.cli --help` 可以运行。
- [ ] `python -m cypchemspace.cli analyze ...` 可以生成结果。
- [ ] `python -m pytest` 显示 `7 passed`。
- [ ] `summary.csv` 和 `cypchemspace_umap.png` 可以打开。
- [ ] 手机麦克风收音清楚。
- [ ] 电脑麦克风已关闭，避免回声。
- [ ] 试录 30 秒并确认画面和声音正常。

## 七、如果现场命令出错怎么办

如果录制时命令突然报错，不要慌，可以这样处理：

1. 停止录制，重新开始一遍最简单。
2. 如果只是 pytest 卡住，先设置：

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
```

3. 如果 CLI 输出目录已存在，不影响演示，可以直接覆盖运行。
4. 如果不想现场冒险，可以提前生成好 `results/demo_run/`，录制时只展示命令和已有结果，并说明“这里是运行后生成的结果文件”。

## 八、最终提交文件建议

最终视频文件建议放在课程提交包外或单独提交平台中，命名为：

```text
cypchemspace_project_demo.mp4
```

如果需要放进本地项目目录，可放在：

```text
course_project_cypchemspace/docs/cypchemspace_project_demo.mp4
```

但不建议把视频提交到 GitHub 仓库，因为 MP4 文件通常较大，容易影响仓库体积。
