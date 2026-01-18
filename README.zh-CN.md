<p align="center">
  <br>
  <img src="./npa-icon.png" style="width:22%;">
</p>
<br>

# NPA“核动力”论文解析与翻译器

### 🌍 文档语言

[**简体中文**](./README.zh-CN.md) | [**English**](./README.md) | [**Tiếng Việt**](./README.vi.md)

## 📖 项目简介

**NPA** (英语: _"Nuclear Powered" Paper Analyzer and Translator_; 简体中文: _“核动力”论文解析与翻译器_; 越南语: "Hạt Động Lực" - Trình Phân tích và Dịch Luận văn) 是一款基于 Python Webview 的本地桌面应用程序，能够在一定程度上解决非英语母语的学术科研人员阅读英文文献时的痛点。本项目结合了现代化的前端技术与强大的后端 AI 服务，实现了从 PDF 文档到 Markdown 的高保真解析，以及基于大语言模型的专业学术翻译。本系统采用 **Pywebview** 作为 GUI 框架，利用 **Flask** 搭建本地后端服务，并通过 **Nuitka** 打包为独立可执行文件，实现了跨平台（Windows, macOS, Linux）运行。

## ✨ 主要功能

**📄 高保真 PDF 解析**
* 集成 [**MinerU**](https://mineru.net/) API，支持将复杂的学术 PDF（包含双栏排版、公式、图表）精准解析为结构化的 Markdown 格式。
* 自动处理公式识别与排版，保留原始文档结构。

**🤖 专业学术翻译 (Zhipu AI)**
* 内置 [**智谱 AI GLM 大模型**](https://open.bigmodel.cn/) 接口调用逻辑，利用 LLM 进行专业的学术文本翻译。
* **流式输出**：实时渲染翻译结果，无需等待整段完成。
* **术语一致性**：维护全局术语表，确保全文专有名词翻译统一。
* **格式保留**：严格保留 Markdown 标题、粗体、列表、代码块及 LaTeX 公式，不破坏原文排版。

**🖥️ 本地化 GUI 界面**
* 基于 PyWebview 的轻量级桌面应用。基于 **marked.js** 和 **MathJax** 实现高质量的Markdown渲染与公式显示。
* 提供文件选择、API Key 管理、翻译对照预览等交互功能。

<img src="./demo.png" style="width:95%;"></img>

## 💡 使用方法说明

1. 您可以在本项目的Release页面下载预构建的可执行文件，当然您也可以选择自行构建或直接运行Python源代码。

2. **配置 API Key**：

* 请您登录 MinerU 官方网站 [**https://mineru.net/**](https://mineru.net/) 申请 MinerU API Key 以用于 PDF 解析。截至目前（2026年01月），申请 MinerU API Key 是 **完全免费** 的。每日限额多达 10000 份 PDF 解析请求，且前 2000 页为快速通道，第二日余量则可恢复，足以满足绝大部分用户的正常使用需求。

* 请您登录智谱 AI 开放平台 [**https://open.bigmodel.cn/**](https://open.bigmodel.cn/) 申请 Zhipu API Key，用于翻译服务。智谱 AI 提供多种大模型选择，部分模型是免费的，可以 **不限任何额度完全免费调用**，具体请参考官网说明。当然您也可以自行在智谱官网订阅付费额度，软件输入token为您的文档 Markdown 格式原文+软件内置指令（300汉字以内）+一定量的JSON格式术语表（文档越长、越专业，术语表随之越大），输出token为 Markdown 格式翻译结果（译文）+一定量的JSON格式术语表。

3. **解析 PDF 或 Markdown文档**：
点击“导入”并选择 PDF，程序会自动将其上传至 MinerU 进行解析，解析完成后会自动加载 Markdown 格式的解析结果内容到预览区，该过程将会消耗 MinerU 每日的额度。如果您导入Markdown文档，则会直接加载该文档内容到预览区，不消耗额度。

4. **翻译**：
您可以首先设置翻译参数（模型、源语言、目标语言）。然后点击“开始翻译”按钮，右侧将实时流式显示翻译结果。点击按钮后，可能会有十秒左右延时以初始化API连接，请耐心等待。

5. **导出**：
翻译完成后，可将结果导出为 Markdown 文件或 PDF 文件。其中 PDF 导出的功能基于 webview 内核的“打印”功能，这取决于您的操作系统。您设定好参数后，选择“保存为 PDF”即可。

## 📂 项目结构

以下是项目的核心文件结构及其功能说明：

```text
NPA-Paper-Analyzer-and-Translator/
├── main.py ........................... [核心入口] 程序的启动文件，初始化 GUI 窗口、API 桥接及基于术语一致性的LLM文档翻译逻辑
├── flask_server.py ................... [本地后端] Flask 服务器，负责向前端提供静态资源(HTML/JS/图片)及文件流
├── call_api.py ....................... [翻译服务] 封装智谱 AI 接口，处理流式请求、System Prompt 及 JSON 结果解析
├── analysis_pdf.py ................... [解析服务] 封装 MinerU API，处理 PDF 上传、轮询解析状态及结果下载解压
├── key_manager.py .................... [配置管理] 负责 API Key 的读取与持久化存储 (npa_api_config.ini)
├── split_text.py ..................... [文本处理] 用于将长文本按 Token 限制切分为小块，防止 API 超限
├── tempdir_manager.py ................ [临时文件] 管理解析过程中产生的临时目录及文件清理
├── close_splash.py ................... [UI工具] 用于关闭启动画面的辅助脚本
├── build_windows.bat ................. [构建脚本] Windows 平台打包脚本 (使用 Nuitka)
├── build_macos.sh .................... [构建脚本] macOS 平台打包脚本
├── build_linux.sh .................... [构建脚本] Linux 平台打包脚本
├── requirements.txt .................. [依赖清单] Python 依赖包列表
├── LICENSE ........................... [版权文件] 许可证文件
├── npa-icon.png ...................... 应用图标
└── static/ ........................... [前端资源] 存放 index.html, CSS, JS 及 MathJax 字体文件
    ├── index.html
    ├── js/
    │   ├── t-loading.js
    │   └── ...
    └── npa-icon.png

```

## 🛠️ 开发者部分：环境准备与开发

### 前置要求

* Python 3.10 或更高版本，建议使用 Python 3.13。
* [MinerU API Key](https://mineru.net/) (用于 PDF 解析)
* [ZhipuAI API Key](https://open.bigmodel.cn/) (用于翻译)

### 1. 克隆项目

```bash
git clone https://github.com/your-repo/NPA-Paper-Analyzer-and-Translator.git
cd NPA-Paper-Analyzer-and-Translator
```

### 2. 安装依赖

建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv
# 激活环境 (Windows)
venv\Scripts\activate
# 激活环境 (Mac/Linux)
source venv/bin/activate
# 注意，对于 Linux 系统，请你务必安装QT或GTK相关依赖，以确保 PyWebview 能够正常工作。

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行源码

```bash
python main.py
```

## 📦 自行构建

**构建硬性要求：必须使用下载自`python.org`的官方纯净版CPython，其余任何形式的Python解释器（如Anaconda、Miniconda、PyPy等）均不受支持。**

本项目使用 **Nuitka** 进行编译打包，以生成独立的、高性能的可执行文件。请根据你的操作系统运行相应的构建脚本，脚本中已尽可能写好了构建的所有步骤，若有报错，请您按脚本输出的提示解决。构建步骤细节不再此处赘述。

### Windows

双击运行或在命令行执行：

```bat
build_windows.bat
```

### Linux

赋予脚本执行权限并运行：

```bash
chmod +x build_linux.sh
./build_linux.sh
```

### macOS

赋予脚本执行权限并运行：

```bash
chmod +x build_macos.sh
./build_macos.sh
```

## ⚠️ 注意事项

**重点须知：由于本软件的解析功能和翻译功能均依赖API，所以请严禁上传包括但不限于涉密文件和隐私文件的任何类型的非公开文件。由此造成机密泄露、隐私泄露等信息安全问题，甚至是导致危害国家安全等的构成犯罪的行为，全部责任均由软件使用者（您）承担。本项目开发者和 API 提供方均不承担任何责任。另外，本软件解析 PDF 文档和文本翻译的功能均涉及 AI 能力，有造成错误的可能，本软件的一切输出仅供参考，不可将本软件的输出用于法律、公文、合同、专业内容用途等任何正式场合，由此造成的损失或法律责任均由使用者（您）承担，本软件项目开发者和 API 提供方均不承担任何责任。**

<details>

<summary>英文翻译版</summary>

**IMPORTANT NOTICE: DUE TO THE FACT THAT THE PARSING FUNCTIONS AND TRANSLATION FUNCTIONS OF THIS SOFTWARE RELY ON APIS, YOU ARE STRICTLY PROHIBITED FROM UPLOADING ANY TYPE OF NON-PUBLIC FILES, INCLUDING BUT NOT LIMITED TO CLASSIFIED FILES AND PRIVATE OR PERSONAL FILES. ANY INFORMATION SECURITY ISSUES CAUSED THEREBY, INCLUDING BUT NOT LIMITED TO THE LEAKAGE OF CONFIDENTIAL INFORMATION OR PERSONAL PRIVACY, OR EVEN ACTS THAT CONSTITUTE CRIMINAL OFFENSES SUCH AS ENDANGERING NATIONAL SECURITY, SHALL BE BORNE SOLELY AND IN FULL BY THE SOFTWARE USER (YOU). THE PROJECT DEVELOPER AND THE API PROVIDER SHALL BEAR NO RESPONSIBILITY OR LIABILITY WHATSOEVER. IN ADDITION, THE PDF DOCUMENT PARSING AND TEXT TRANSLATION FUNCTIONS OF THIS SOFTWARE INVOLVE AI CAPABILITIES AND MAY PRODUCE ERRORS. ALL OUTPUTS GENERATED BY THIS SOFTWARE ARE FOR REFERENCE PURPOSES ONLY AND MUST NOT BE USED IN ANY FORMAL CONTEXT, INCLUDING BUT NOT LIMITED TO LEGAL MATTERS, OFFICIAL DOCUMENTS, CONTRACTS, OR ANY PROFESSIONAL CONTENT. ANY LOSSES OR LEGAL LIABILITIES ARISING THEREFROM SHALL BE BORNE SOLELY BY THE USER (YOU), AND THE PROJECT DEVELOPER AND THE API PROVIDER SHALL BEAR NO RESPONSIBILITY OR LIABILITY WHATSOEVER.** _(The above notice was translated from the Chinese version by the GPT-5.2 model. In case of any dispute, the Chinese version shall prevail.)_

</details>

<details>

<summary>越南语翻译版</summary>

**THÔNG BÁO QUAN TRỌNG: DO CHỨC NĂNG PHÂN TÍCH VÀ CHỨC NĂNG DỊCH CỦA PHẦN MỀM NÀY ĐỀU PHỤ THUỘC VÀO API, DO ĐÓ NGHIÊM CẤM TUYỆT ĐỐI VIỆC TẢI LÊN, BAO GỒM NHƯNG KHÔNG GIỚI HẠN, BẤT KỲ LOẠI TỆP KHÔNG CÔNG KHAI NÀO CÓ CHỨA TÀI LIỆU MẬT VÀ/HOẶC THÔNG TIN RIÊNG TƯ. MỌI VẤN ĐỀ AN TOÀN THÔNG TIN PHÁT SINH TỪ ĐÓ, BAO GỒM NHƯNG KHÔNG GIỚI HẠN Ở VIỆC RÒ RỈ BÍ MẬT, RÒ RỈ QUYỀN RIÊNG TƯ, THẬM CHÍ CÁC HÀNH VI CẤU THÀNH TỘI PHẠM GÂY NGUY HẠI ĐẾN AN NINH QUỐC GIA, TOÀN BỘ TRÁCH NHIỆM ĐỀU DO NGƯỜI SỬ DỤNG PHẦN MỀM (BẠN) TỰ CHỊU. NHÀ PHÁT TRIỂN DỰ ÁN NÀY VÀ BÊN CUNG CẤP API KHÔNG CHỊU BẤT KỲ TRÁCH NHIỆM NÀO. NGOÀI RA, CÁC CHỨC NĂNG PHÂN TÍCH TÀI LIỆU PDF VÀ DỊCH VĂN BẢN CỦA PHẦN MỀM NÀY CÓ LIÊN QUAN ĐẾN NĂNG LỰC TRÍ TUỆ NHÂN TẠO (AI) VÀ CÓ KHẢ NĂNG PHÁT SINH SAI SÓT. MỌI ĐẦU RA CỦA PHẦN MỀM NÀY CHỈ ĐƯỢC CUNG CẤP VỚI MỤC ĐÍCH THAM KHẢO, TUYỆT ĐỐI KHÔNG ĐƯỢC SỬ DỤNG CHO CÁC VĂN BẢN PHÁP LÝ, VĂN KIỆN HÀNH CHÍNH, HỢP ĐỒNG, NỘI DUNG CHUYÊN MÔN HOẶC BẤT KỲ BỐI CẢNH CHÍNH THỨC NÀO. MỌI THIỆT HẠI HOẶC TRÁCH NHIỆM PHÁP LÝ PHÁT SINH TỪ ĐÓ ĐỀU DO NGƯỜI SỬ DỤNG PHẦN MỀM (BẠN) TỰ CHỊU; NHÀ PHÁT TRIỂN DỰ ÁN PHẦN MỀM NÀY VÀ BÊN CUNG CẤP API KHÔNG CHỊU BẤT KỲ TRÁCH NHIỆM NÀO.** _(Nội dung lưu ý nêu trên được dịch từ phiên bản tiếng Trung bởi mô hình GPT-5.2. Trong trường hợp có tranh chấp, phiên bản tiếng Trung sẽ được ưu tiên áp dụng.)_

</details>

## 👤 项目开发者

* **杜宇** (英语: _Du Yu_; 越南语: _Đỗ Vũ_)
* 电子邮箱: <qluduyu09@163.com> 或 <11250717@stu.lzjtu.edu.cn>
* 地址: 兰州交通大学电子与信息工程学院 (英语: _School of Electronic and Information Engineering, Lanzhou Jiaotong University_; 越南语: _Đại Học Giao thông Lan Châu, Học Viện Điện Tử Và Công Nghệ Thông Tin_)

<img src="./splash-screen-v1.0-small.png" style="width:35%;"></img>

## 📄 License

本项目遵循开源许可证，详情请查看 [LICENSE](./LICENSE) 文件。
