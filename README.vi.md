<p align="center">
  <br>
  <img src="./npa-icon.png" style="width:26%;">
</p>
<br>

# NPA "HẠT ĐỘNG LỰC" Trình Phân Tích và Dịch Luận Văn

### 🌍 Ngôn Ngữ Tài Liệu

[**简体中文**](./README.zh-CN.md) | [**English**](./README.md) | [**Tiếng Việt**](./README.vi.md)

## 📖 Giới thiệu dự án

**NPA** (Tiếng Anh: _"Nuclear Powered" Paper Analyzer and Translator_; Tiếng Trung giản thể: _“核动力”论文解析与翻译器_; Tiếng Việt: _“Hạt Động Lực” – Trình Phân Tích và Dịch Luận Văn_) là một ứng dụng máy tính để bàn chạy cục bộ dựa trên Python Webview, được thiết kế nhằm giải quyết các khó khăn mà các nhà nghiên cứu khoa học không phải người bản ngữ tiếng Anh thường gặp khi đọc tài liệu học thuật tiếng Anh. Dự án này kết hợp công nghệ frontend hiện đại với các dịch vụ AI backend mạnh mẽ, hiện thực hóa việc phân tích tài liệu PDF sang Markdown với độ trung thực rất cao, đồng thời cung cấp chức năng dịch thuật học thuật chuyên nghiệp dựa trên các mô hình ngôn ngữ lớn. Hệ thống sử dụng **PyWebview** làm framework giao diện đồ họa (GUI), sử dụng **Flask** để xây dựng dịch vụ backend cục bộ, và được đóng gói thành tệp thực thi độc lập thông qua **Nuitka**, từ đó đạt được khả năng chạy đa nền tảng (Windows, macOS, Linux).

## ✨ Tính năng chính

**📄 Phân tích PDF độ trung thực cao**
* Tích hợp API [**MinerU**](https://mineru.net/), hỗ trợ phân tích chính xác các tài liệu PDF học thuật phức tạp (bao gồm bố cục hai cột, công thức, hình ảnh và bảng biểu) và chuyển đổi chúng sang định dạng Markdown có cấu trúc.
* Tự động xử lý việc nhận dạng và dàn trang công thức, bảo toàn tối đa cấu trúc của tài liệu gốc.

**🤖 Dịch thuật học thuật chuyên nghiệp**
* Tích hợp sẵn logic gọi giao diện của [**Zhipu (Tiếng Trung: _智谱_; Tiếng Việt: _Trí Phổ_) AI GLM – mô hình ngôn ngữ lớn**](https://open.bigmodel.cn/), sử dụng LLM để thực hiện dịch thuật chuyên sâu đối với văn bản học thuật.
* **Xuất kết quả dạng luồng**: hiển thị kết quả dịch theo thời gian thực, không cần chờ toàn bộ đoạn văn hoàn tất mới hiển thị.
* **Tính nhất quán thuật ngữ**: duy trì bảng thuật ngữ toàn cục, đảm bảo các danh từ và thuật ngữ chuyên ngành được dịch thống nhất xuyên suốt toàn bộ văn bản.
* **Giữ nguyên định dạng**: bảo toàn nghiêm ngặt tiêu đề Markdown, chữ in đậm, danh sách, khối mã và công thức LaTeX, tuyệt đối không làm hỏng bố cục và cấu trúc của văn bản gốc.

**🖥️ Giao diện GUI cục bộ**
* Ứng dụng máy tính để bàn nhẹ, chạy cục bộ, dựa trên PyWebview. Sử dụng **marked.js** và **MathJax** để hiển thị Markdown và công thức toán học với chất lượng cao.
* Cung cấp các chức năng tương tác như lựa chọn tệp, quản lý API Key, và xem trước song song văn bản gốc cùng bản dịch.

## 💡 Hướng dẫn sử dụng

1. Bạn có thể tải các tệp thực thi đã được xây dựng sẵn từ trang Release của dự án. Ngoài ra, bạn cũng có thể tự xây dựng chương trình hoặc chạy trực tiếp mã nguồn Python.

2. **Cấu hình API Key**：

* Vui lòng truy cập trang web chính thức của MinerU tại [**https://mineru.net/**](https://mineru.net/) để đăng ký MinerU API Key phục vụ cho việc phân tích PDF. Tính đến thời điểm hiện tại (tháng 01 năm 2026), việc đăng ký MinerU API Key là **hoàn toàn miễn phí**. Hạn mức hằng ngày lên đến 10.000 yêu cầu phân tích PDF, trong đó 2.000 trang đầu tiên được xử lý qua kênh nhanh, phần hạn mức còn lại sẽ được khôi phục vào ngày hôm sau, đủ để đáp ứng nhu cầu sử dụng thông thường của đại đa số người dùng.

* Vui lòng truy cập nền tảng mở của Zhipu (_Trí Phổ_) AI tại [**https://open.bigmodel.cn/**](https://open.bigmodel.cn/) để đăng ký Zhipu API Key cho dịch vụ dịch thuật. Zhipu (_Trí Phổ_) AI cung cấp nhiều mô hình ngôn ngữ lớn khác nhau, trong đó một số mô hình là miễn phí và có thể **được gọi không giới hạn hoàn toàn miễn phí**. Chi tiết cụ thể vui lòng tham khảo thông tin trên trang web chính thức. Ngoài ra, bạn cũng có thể mua thêm hạn mức trả phí nếu có nhu cầu.
  Token đầu vào của phần mềm bao gồm: nội dung Markdown gốc của tài liệu + chỉ dẫn nội bộ của phần mềm (dưới 300 ký tự tiếng Trung giản thể) + một lượng nhất định bảng thuật ngữ ở định dạng JSON (tài liệu càng dài và càng mang tính chuyên môn cao thì bảng thuật ngữ tương ứng sẽ càng lớn).
  Token đầu ra bao gồm: nội dung Markdown đã được dịch (văn bản dịch) + một lượng nhất định bảng thuật ngữ ở định dạng JSON.

3. **Phân tích tài liệu PDF hoặc Markdown**：
Nhấn nút “Import” và chọn tệp PDF, chương trình sẽ tự động tải tệp đó lên MinerU để tiến hành phân tích. Sau khi hoàn tất, nội dung Markdown đã được phân tích sẽ tự động được tải vào khu vực xem trước. Quá trình này sẽ tiêu tốn hạn mức MinerU hằng ngày.  
Nếu bạn nhập tệp Markdown, nội dung của tệp sẽ được tải trực tiếp vào khu vực xem trước mà không tiêu tốn bất kỳ hạn mức nào.

4. **Dịch thuật**：
Trước tiên, hãy thiết lập các tham số dịch (mô hình, ngôn ngữ nguồn, ngôn ngữ đích). Sau đó nhấn nút “Bắt đầu dịch”, kết quả dịch sẽ được hiển thị theo dạng luồng thời gian thực ở khu vực bên phải. Sau khi nhấn nút, có thể cần khoảng mười giây để khởi tạo kết nối API, vui lòng kiên nhẫn chờ đợi.

5. **Xuất kết quả**：
Sau khi hoàn tất dịch, bạn có thể xuất kết quả ra tệp Markdown hoặc tệp PDF. Chức năng xuất PDF dựa trên tính năng “In” của nhân webview và phụ thuộc vào hệ điều hành mà bạn đang sử dụng. Sau khi thiết lập các tham số cần thiết, chỉ cần chọn “Lưu dưới dạng PDF”.

## 📂 Cấu trúc dự án

Dưới đây là cấu trúc các tệp lõi của dự án cùng với mô tả chức năng tương ứng:

```text
NPA-Paper-Analyzer-and-Translator/
├── main.py ........................... [Điểm khởi chạy cốt lõi] Tệp khởi động chính của chương trình, dùng để khởi tạo cửa sổ GUI, cầu nối API và logic dịch tài liệu bằng mô hình ngôn ngữ lớn với cơ chế đảm bảo tính nhất quán thuật ngữ
├── flask_server.py ................... [Hậu phương cục bộ] Máy chủ Flask chạy trên máy người dùng, chịu trách nhiệm cung cấp tài nguyên tĩnh (HTML, JS, hình ảnh) và luồng dữ liệu tệp cho giao diện
├── call_api.py ....................... [Dịch vụ dịch thuật] Đóng gói giao diện Zhipu (_Trí Phổ_) AI, xử lý các yêu cầu dạng luồng, System Prompt và phân tích kết quả ở định dạng JSON
├── analysis_pdf.py ................... [Dịch vụ phân tích] Đóng gói API MinerU, xử lý việc tải lên PDF, thăm dò trạng thái phân tích và tải xuống cũng như giải nén kết quả
├── key_manager.py .................... [Quản lý cấu hình] Phụ trách đọc và lưu trữ lâu dài API Key trong tệp cấu hình (npa_api_config.ini)
├── split_text.py ..................... [Xử lý văn bản] Dùng để chia nhỏ văn bản dài theo giới hạn số lượng token nhằm tránh vượt quá hạn mức cho phép của API
├── tempdir_manager.py ................ [Tệp tạm thời] Quản lý các thư mục tạm được tạo ra trong quá trình xử lý và thực hiện dọn dẹp tệp sau khi hoàn tất
├── close_splash.py ................... [Công cụ giao diện] Tệp hỗ trợ dùng để đóng màn hình chào khi chương trình khởi động
├── build_windows.bat ................. [Tập lệnh đóng gói] Tập lệnh dùng để biên dịch và đóng gói chương trình trên hệ điều hành Windows (sử dụng Nuitka)
├── build_macos.sh .................... [Tập lệnh đóng gói] Tập lệnh dùng để biên dịch và đóng gói chương trình trên hệ điều hành macOS
├── build_linux.sh .................... [Tập lệnh đóng gói] Tập lệnh dùng để biên dịch và đóng gói chương trình trên hệ điều hành Linux
├── requirements.txt .................. [Danh sách phụ thuộc] Danh sách các thư viện Python mà dự án cần cài đặt
├── LICENSE ........................... [Giấy phép] Tệp chứa thông tin giấy phép của dự án
├── npa-icon.png ...................... Biểu tượng của ứng dụng
└── static/ ........................... [Tài nguyên giao diện] Thư mục lưu trữ tệp index.html, các tệp CSS, tệp JavaScript và phông chữ MathJax
    ├── index.html
    ├── js/
    │   ├── t-loading.js
    │   └── ...
    └── npa-icon.png
```

## 🛠️ Dành cho nhà phát triển: Chuẩn bị môi trường và phát triển

### Yêu cầu trước

* Python 3.10 hoặc phiên bản cao hơn, khuyến nghị sử dụng Python 3.13.
* [MinerU API Key](https://mineru.net/) (dùng cho phân tích PDF)
* [ZhipuAI API Key](https://open.bigmodel.cn/) (dùng cho dịch thuật)

### 1. Sao chép dự án

```bash
git clone https://github.com/your-repo/NPA-Paper-Analyzer-and-Translator.git
cd NPA-Paper-Analyzer-and-Translator
```

### 2. Cài đặt phụ thuộc

Khuyến nghị sử dụng môi trường ảo:

```bash
# Tạo môi trường ảo
python -m venv venv
# Kích hoạt môi trường (Windows)
venv\Scripts\activate
# Kích hoạt môi trường (Mac/Linux)
source venv/bin/activate
# Lưu ý: Đối với hệ điều hành Linux, bạn bắt buộc phải cài đặt các phụ thuộc QT hoặc GTK để PyWebview có thể hoạt động bình thường.

# Cài đặt phụ thuộc
pip install -r requirements.txt
```

### 3. Chạy mã nguồn

```bash
python main.py
```

## 📦 Tự xây dựng

**Yêu cầu bắt buộc khi xây dựng: phải sử dụng CPython chính thức được tải từ `python.org`. Mọi hình thức trình thông dịch Python khác (ví dụ như Anaconda, Miniconda, PyPy, v.v.) đều không được hỗ trợ.**

Dự án này sử dụng **Nuitka** để biên dịch và đóng gói, tạo ra các tệp thực thi độc lập với hiệu năng cao. Vui lòng chạy tập lệnh xây dựng tương ứng với hệ điều hành của bạn. Các tập lệnh này đã bao gồm hầu hết các bước cần thiết; nếu xảy ra lỗi, hãy làm theo các hướng dẫn được hiển thị trong quá trình xây dựng. Chi tiết cụ thể của quá trình xây dựng sẽ không được trình bày thêm tại đây.

### Windows

Chạy bằng cách nhấp đúp chuột hoặc thông qua dòng lệnh:

```bat
build_windows.bat
```

### Linux

Cấp quyền thực thi và chạy:

```bash
chmod +x build_linux.sh
./build_linux.sh
```

### macOS

Cấp quyền thực thi và chạy:

```bash
chmod +x build_macos.sh
./build_macos.sh
```

## ⚠️ THÔNG BÁO QUAN TRỌNG

**THÔNG BÁO QUAN TRỌNG: DO CHỨC NĂNG PHÂN TÍCH VÀ CHỨC NĂNG DỊCH CỦA PHẦN MỀM NÀY ĐỀU PHỤ THUỘC VÀO API, DO ĐÓ NGHIÊM CẤM TUYỆT ĐỐI VIỆC TẢI LÊN, BAO GỒM NHƯNG KHÔNG GIỚI HẠN, BẤT KỲ LOẠI TỆP KHÔNG CÔNG KHAI NÀO CÓ CHỨA TÀI LIỆU MẬT VÀ/HOẶC THÔNG TIN RIÊNG TƯ. MỌI VẤN ĐỀ AN TOÀN THÔNG TIN PHÁT SINH TỪ ĐÓ, BAO GỒM NHƯNG KHÔNG GIỚI HẠN Ở VIỆC RÒ RỈ BÍ MẬT, RÒ RỈ QUYỀN RIÊNG TƯ, THẬM CHÍ CÁC HÀNH VI CẤU THÀNH TỘI PHẠM GÂY NGUY HẠI ĐẾN AN NINH QUỐC GIA, TOÀN BỘ TRÁCH NHIỆM ĐỀU DO NGƯỜI SỬ DỤNG PHẦN MỀM (BẠN) TỰ CHỊU. NHÀ PHÁT TRIỂN DỰ ÁN NÀY VÀ BÊN CUNG CẤP API KHÔNG CHỊU BẤT KỲ TRÁCH NHIỆM NÀO. NGOÀI RA, CÁC CHỨC NĂNG PHÂN TÍCH TÀI LIỆU PDF VÀ DỊCH VĂN BẢN CỦA PHẦN MỀM NÀY CÓ LIÊN QUAN ĐẾN NĂNG LỰC TRÍ TUỆ NHÂN TẠO (AI) VÀ CÓ KHẢ NĂNG PHÁT SINH SAI SÓT. MỌI ĐẦU RA CỦA PHẦN MỀM NÀY CHỈ ĐƯỢC CUNG CẤP VỚI MỤC ĐÍCH THAM KHẢO, TUYỆT ĐỐI KHÔNG ĐƯỢC SỬ DỤNG CHO CÁC VĂN BẢN PHÁP LÝ, VĂN KIỆN HÀNH CHÍNH, HỢP ĐỒNG, NỘI DUNG CHUYÊN MÔN HOẶC BẤT KỲ BỐI CẢNH CHÍNH THỨC NÀO. MỌI THIỆT HẠI HOẶC TRÁCH NHIỆM PHÁP LÝ PHÁT SINH TỪ ĐÓ ĐỀU DO NGƯỜI SỬ DỤNG PHẦN MỀM (BẠN) TỰ CHỊU; NHÀ PHÁT TRIỂN DỰ ÁN PHẦN MỀM NÀY VÀ BÊN CUNG CẤP API KHÔNG CHỊU BẤT KỲ TRÁCH NHIỆM NÀO.** _(Nội dung lưu ý nêu trên được dịch từ phiên bản tiếng Trung bởi mô hình GPT-5.2. Trong trường hợp có tranh chấp, phiên bản tiếng Trung sẽ được ưu tiên áp dụng.)_

<details>

<summary>Phiên bản Tiếng Trung</summary>

**重点须知：由于本软件的解析功能和翻译功能均依赖API，所以请严禁上传包括但不限于涉密文件和隐私文件的任何类型的非公开文件。由此造成机密泄露、隐私泄露等信息安全问题，甚至是导致危害国家安全等的构成犯罪的行为，全部责任均由软件使用者（您）承担。本项目开发者和 API 提供方均不承担任何责任。另外，本软件解析 PDF 文档和文本翻译的功能均涉及 AI 能力，有造成错误的可能，本软件的一切输出仅供参考，不可将本软件的输出用于法律、公文、合同、专业内容用途等任何正式场合，由此造成的损失或法律责任均由使用者（您）承担，本软件项目开发者和 API 提供方均不承担任何责任。**

</details>

<details>

<summary>Phiên bản Tiếng Anh</summary>

**IMPORTANT NOTICE: DUE TO THE FACT THAT THE PARSING FUNCTIONS AND TRANSLATION FUNCTIONS OF THIS SOFTWARE RELY ON APIS, YOU ARE STRICTLY PROHIBITED FROM UPLOADING ANY TYPE OF NON-PUBLIC FILES, INCLUDING BUT NOT LIMITED TO CLASSIFIED FILES AND PRIVATE OR PERSONAL FILES. ANY INFORMATION SECURITY ISSUES CAUSED THEREBY, INCLUDING BUT NOT LIMITED TO THE LEAKAGE OF CONFIDENTIAL INFORMATION OR PERSONAL PRIVACY, OR EVEN ACTS THAT CONSTITUTE CRIMINAL OFFENSES SUCH AS ENDANGERING NATIONAL SECURITY, SHALL BE BORNE SOLELY AND IN FULL BY THE SOFTWARE USER (YOU). THE PROJECT DEVELOPER AND THE API PROVIDER SHALL BEAR NO RESPONSIBILITY OR LIABILITY WHATSOEVER. IN ADDITION, THE PDF DOCUMENT PARSING AND TEXT TRANSLATION FUNCTIONS OF THIS SOFTWARE INVOLVE AI CAPABILITIES AND MAY PRODUCE ERRORS. ALL OUTPUTS GENERATED BY THIS SOFTWARE ARE FOR REFERENCE PURPOSES ONLY AND MUST NOT BE USED IN ANY FORMAL CONTEXT, INCLUDING BUT NOT LIMITED TO LEGAL MATTERS, OFFICIAL DOCUMENTS, CONTRACTS, OR ANY PROFESSIONAL CONTENT. ANY LOSSES OR LEGAL LIABILITIES ARISING THEREFROM SHALL BE BORNE SOLELY BY THE USER (YOU), AND THE PROJECT DEVELOPER AND THE API PROVIDER SHALL BEAR NO RESPONSIBILITY OR LIABILITY WHATSOEVER.** _(The above notice was translated from the Chinese version by the GPT-5.2 model. In case of any dispute, the Chinese version shall prevail.)_

</details>

## 👤 Nhà phát triển dự án

* **Đỗ Vũ** (Tiếng Trung: _杜宇_; Tiếng Anh: _Du Yu_)  
* Thư điện tử: <qluduyu09@163.com> hoặc <11250717@stu.lzjtu.edu.cn>  
* Địa chỉ: Học viện Điện tử và Công nghệ Thông tin, Đại học Giao thông Lan Châu  
  (Tiếng Trung: _兰州交通大学电子与信息工程学院_; Tiếng Anh: _School of Electronic and Information Engineering, Lanzhou Jiaotong University_)

<img src="./splash-screen-v1.0-small.png" style="width:35%;"></img>

## 📄 Giấy phép

Dự án này tuân theo giấy phép mã nguồn mở. Vui lòng xem tệp [LICENSE](./LICENSE) để biết chi tiết.


