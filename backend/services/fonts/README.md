# 中文 PDF 字体

NotoSansSC-Regular.ttf 基于 Google Fonts 的 Noto Sans SC 可变 TrueType 字体，使用 SIL Open Font License 1.1；授权全文见 OFL.txt。保留原版权声明，字体未使用保留名称 Source。

来源：https://github.com/google/fonts/tree/main/ofl/notosanssc

通过 GitHub 官方 API 下载原始 blob，以 FontTools 固定 wght=400 并更新名称表，生成常规字重实例。生成命令：`fonttools varLib.instancer 'NotoSansSC[wght].ttf' wght=400 --update-name-table --output NotoSansSC-Regular.ttf`。报告生成时由 ReportLab 按所用字符嵌入子集，使无中文语言包的阅读器和 Linux 容器也能显示中文。
