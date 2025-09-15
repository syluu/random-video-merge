# Video Tool - Công cụ xử lý video

Công cụ này cung cấp hai tính năng chính: **gộp video ngẫu nhiên** và **tách video** với giao diện đồ họa thân thiện.

## Tính năng chính

### 🎬 Gộp Video (Merge)
- **Nối video ngẫu nhiên**: Chọn ngẫu nhiên các video từ thư mục và nối chúng lại
- **Kiểm soát thời lượng**: Thiết lập thời lượng mong muốn cho video cuối
- **Chuẩn hóa tỷ lệ khung hình**: Hỗ trợ 16:9, 9:16, 4:3, 1:1
- **Tránh lặp lại**: Không có video nào xuất hiện liền nhau

### ✂️ Tách Video (Split)
- **Tách video thành đoạn**: Chia một video dài thành nhiều đoạn ngắn
- **Tùy chỉnh thời lượng**: Thiết lập độ dài mỗi đoạn video (ví dụ: 5 giây)
- **Đánh số tự động**: Tên file được tạo tự động theo thứ tự (video_001.mp4, video_002.mp4...)
- **Xử lý đoạn cuối**: Đoạn cuối được xử lý đúng cách nếu không đủ thời lượng

### 🖥️ Giao diện và Tiện ích
- **Giao diện tab**: Chuyển đổi dễ dàng giữa hai tính năng
- **Hỗ trợ nhiều định dạng**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Theo dõi tiến trình**: Thanh tiến trình và thông báo chi tiết
- **Log chi tiết**: Hiển thị quá trình xử lý từng bước

## Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11
- **Python**: Phiên bản 3.7 trở lên
- **Dung lượng**: Ít nhất 1GB trống cho việc xử lý video

## Hướng dẫn cài đặt

### Bước 1: Cài đặt Python

1. **Tải Python**:
   - Truy cập: https://www.python.org/downloads/
   - Tải phiên bản Python mới nhất cho Windows
   - Chọn file có tên dạng `python-3.x.x-amd64.exe`

2. **Cài đặt Python**:
   - Chạy file đã tải về
   - **QUAN TRỌNG**: Tích vào ô "Add Python to PATH" ở màn hình đầu tiên
   - Chọn "Install Now"
   - Đợi quá trình cài đặt hoàn tất

3. **Kiểm tra cài đặt**:
   - Mở Command Prompt (Cmd): Nhấn `Win + R`, gõ `cmd`, nhấn Enter
   - Gõ lệnh: `python --version`
   - Nếu hiển thị phiên bản Python thì cài đặt thành công

### Bước 2: Tải và chuẩn bị công cụ

1. **Tải mã nguồn**:
   - Tải toàn bộ thư mục chứa các file: `video_merger.py`, `requirements.txt`, `README.md`
   - Đặt vào một thư mục dễ nhớ (ví dụ: `C:\VideoMerger\`)

2. **Mở Command Prompt tại thư mục**:
   - Mở thư mục chứa file trong File Explorer
   - Giữ Shift + Click chuột phải trong thư mục
   - Chọn "Open PowerShell window here" hoặc "Open command window here"

### Bước 3: Cài đặt thư viện cần thiết

Chạy lệnh sau để cài đặt các thư viện:

```bash
pip install moviepy
```

**Lưu ý**: Quá trình này có thể mất 5-10 phút vì moviepy cần tải nhiều thành phần.

### Bước 4: Chạy công cụ

Trong Command Prompt/PowerShell, gõ lệnh:

```bash
python video_merger.py
```

Giao diện của công cụ sẽ xuất hiện.

## Hướng dẫn sử dụng

Ứng dụng có giao diện với hai tab: **"Gộp Video"** và **"Tách Video"**.

### 🎬 Tab Gộp Video (Video Merge)

#### Bước 1: Chuẩn bị video
- Tạo một thư mục chứa các file video bạn muốn gộp
- Các video nên có định dạng: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- Đảm bảo các video có thể phát được bình thường

#### Bước 2: Thực hiện gộp video
1. **Chọn thư mục video**:
   - Nhấn nút "Chọn thư mục"
   - Duyệt đến thư mục chứa video của bạn
   - Chọn thư mục và nhấn OK

2. **Cài đặt video**:
   - **Thời lượng**: Nhập thời lượng mong muốn (ví dụ: 25 giây)
   - **Tỷ lệ khung hình**: Chọn 16:9 (Ngang), 9:16 (Dọc), 4:3 hoặc 1:1 (Vuông)

3. **Chọn file đầu ra**:
   - Nhấn nút "Chọn vị trí"
   - Chọn nơi lưu file và đặt tên (ví dụ: `merged_video.mp4`)
   - Nhấn Save

4. **Bắt đầu xử lý**:
   - Nhấn nút "Bắt đầu nối video"
   - Theo dõi tiến trình qua thanh progress bar và log
   - Đợi thông báo hoàn thành

### ✂️ Tab Tách Video (Video Split)

#### Bước 1: Chuẩn bị video
- Chuẩn bị file video cần tách (MP4, AVI, MOV, MKV, WMV, FLV, WebM)
- Tạo thư mục để lưu các đoạn video được tách

#### Bước 2: Thực hiện tách video
1. **Chọn video cần tách**:
   - Nhấn nút "Chọn video"
   - Duyệt và chọn file video cần tách
   - Ứng dụng sẽ hiển thị thời lượng video

2. **Chọn thư mục lưu**:
   - Nhấn nút "Chọn thư mục"
   - Chọn thư mục để lưu các đoạn video được tách

3. **Cài đặt tách video**:
   - **Thời lượng mỗi đoạn**: Nhập số giây cho mỗi đoạn (ví dụ: 5 giây)
   - Ứng dụng sẽ tự động tính số đoạn cần tách

4. **Bắt đầu tách**:
   - Nhấn nút "Bắt đầu tách video"
   - Theo dõi tiến trình qua thanh progress bar và log
   - Các file sẽ được tạo với tên: `tên_gốc_001.mp4`, `tên_gốc_002.mp4`, ...

### 📋 Kết quả
- **Gộp video**: File video đã nối được lưu tại vị trí đã chọn
- **Tách video**: Các đoạn video được lưu trong thư mục đã chọn với tên được đánh số thứ tự

## Xử lý lỗi thường gặp

### Lỗi: "python is not recognized"
**Nguyên nhân**: Python chưa được thêm vào PATH
**Giải pháp**:
1. Gỡ cài đặt Python
2. Cài đặt lại và nhớ tích "Add Python to PATH"
3. Hoặc thêm Python vào PATH thủ công

### Lỗi: "No module named 'moviepy'"
**Nguyên nhân**: Chưa cài đặt thư viện moviepy
**Giải pháp**:
```bash
pip install moviepy
```

### Lỗi: "Permission denied" khi lưu file
**Nguyên nhân**: Không có quyền ghi vào thư mục đích
**Giải pháp**:
- Chọn thư mục khác (ví dụ: Desktop, Documents)
- Chạy Command Prompt với quyền Administrator

### Lỗi: "Codec not found" hoặc lỗi video
**Nguyên nhân**: File video bị lỗi hoặc định dạng không hỗ trợ
**Giải pháp**:
- Kiểm tra các file video có phát được không
- Chuyển đổi video sang định dạng MP4 trước khi sử dụng
- Loại bỏ các file video bị lỗi khỏi thư mục

### Lỗi: "Memory Error" hoặc máy bị treo
**Nguyên nhân**: Video quá lớn hoặc quá nhiều video
**Giải pháp**:
- Giảm số lượng video trong thư mục (gộp video)
- Sử dụng video có độ phân giải thấp hơn
- Đóng các ứng dụng khác để giải phóng RAM
- Với tách video: Thử tách thành đoạn ngắn hơn (ví dụ: 3 giây thay vì 10 giây)

### Lỗi: "'NoneType' object has no attribute 'stdout'" (Tách Video)
**Nguyên nhân**: Lỗi ffmpeg khi xử lý nhiều đoạn video liên tiếp
**Giải pháp**:
- Khởi động lại ứng dụng và thử lại
- Thử tách với thời lượng đoạn khác nhau
- Đảm bảo video gốc không bị hỏng
- Chọn thư mục đầu ra khác

### Lỗi: Video bị lỗi hoặc không phát được (Tách Video)
**Nguyên nhân**: Một số đoạn video có thể bị lỗi trong quá trình tách
**Giải pháp**:
- Kiểm tra video gốc có phát được đầy đủ không
- Thử tách với thời lượng ngắn hơn
- Sử dụng video có định dạng MP4 để đảm bảo tương thích tốt nhất


## Lưu ý quan trọng

### 🎬 Cho tính năng Gộp Video
1. **Hiệu suất**: Quá trình gộp video có thể mất từ vài phút đến vài chục phút tùy thuộc vào:
   - Số lượng video và thời lượng mục tiêu
   - Kích thước và độ phân giải video
   - Cấu hình máy tính

2. **Dung lượng**: 
   - File đầu ra có thể lớn hơn tổng dung lượng các video gốc
   - Cần thêm khoảng 20-30% dung lượng dự phòng

3. **Chất lượng**: 
   - Chất lượng video đầu ra phụ thuộc vào video gốc
   - Tất cả video sẽ được chuẩn hóa theo tỷ lệ khung hình đã chọn

### ✂️ Cho tính năng Tách Video
1. **Hiệu suất**: Quá trình tách video phụ thuộc vào:
   - Độ dài video gốc và thời lượng mỗi đoạn
   - Chất lượng video gốc
   - Số lượng đoạn cần tạo

2. **Dung lượng**: 
   - Tổng dung lượng các đoạn video sẽ lớn hơn video gốc
   - Cần có ít nhất 150% dung lượng của video gốc để tách

3. **Tên file**: 
   - File được đánh số tự động: `tên_gốc_001.mp4`, `tên_gốc_002.mp4`...
   - Đảm bảo thư mục đầu ra có quyền ghi

### 🔧 Chung
4. **Định dạng hỗ trợ**:
   - Đầu vào: MP4, AVI, MOV, MKV, WMV, FLV, WebM
   - Đầu ra: MP4 (khuyến nghị cho tính ổn định tốt nhất)

## Liên hệ và hỗ trợ

Nếu gặp vấn đề không thể giải quyết:
1. Kiểm tra lại các bước cài đặt
2. Đảm bảo tất cả file video đều hợp lệ
3. Thử với số lượng video ít hơn
4. Khởi động lại máy tính và thử lại

## Phiên bản

- **v1.0**: Phiên bản đầu tiên - Chỉ có tính năng gộp video
  - Hỗ trợ nối video ngẫu nhiên với kiểm soát thời lượng
  - Giao diện đồ họa cơ bản

- **v2.0**: Phiên bản hiện tại - Video Tool hoàn chỉnh
  - ✨ **TÍNH NĂNG MỚI**: Tách video thành các đoạn nhỏ
  - 🎨 Giao diện tab với hai tính năng chính
  - 🔧 Cải thiện độ ổn định và xử lý lỗi
  - 📏 Hỗ trợ nhiều tỷ lệ khung hình cho gộp video
  - 📝 Log chi tiết cho cả hai tính năng
  - 🛠️ Xử lý fallback tốt hơn khi gặp lỗi
