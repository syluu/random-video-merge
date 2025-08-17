# Random Video Merger - Công cụ nối video ngẫu nhiên

Công cụ này giúp bạn nối các file video trong một thư mục một cách ngẫu nhiên để tạo ra một video có thời lượng nằm trong khoảng thời gian mong muốn.

## Tính năng chính

- **Nối video ngẫu nhiên**: Chọn ngẫu nhiên các video từ thư mục và nối chúng lại
- **Kiểm soát thời lượng**: Thiết lập khoảng thời gian mong muốn (ví dụ: 24-26 giây)
- **Giao diện đơn giản**: Sử dụng giao diện đồ họa dễ sử dụng
- **Hỗ trợ nhiều định dạng**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Theo dõi tiến trình**: Thanh tiến trình và thông báo chi tiết

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

### Bước 1: Chuẩn bị video
- Tạo một thư mục chứa các file video bạn muốn nối
- Các video nên có định dạng: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- Đảm bảo các video có thể phát được bình thường

### Bước 2: Sử dụng công cụ

1. **Chọn thư mục video**:
   - Nhấn nút "Chọn thư mục"
   - Duyệt đến thư mục chứa video của bạn
   - Chọn thư mục và nhấn OK

2. **Thiết lập thời lượng**:
   - Nhập thời lượng tối thiểu (ví dụ: 24)
   - Nhập thời lượng tối đa (ví dụ: 26)
   - Đơn vị tính: giây

3. **Chọn file đầu ra**:
   - Nhấn nút "Chọn vị trí"
   - Chọn nơi lưu file và đặt tên (ví dụ: `output.mp4`)
   - Nhấn Save

4. **Bắt đầu xử lý**:
   - Nhấn nút "Bắt đầu nối video"
   - Theo dõi tiến trình qua thanh progress bar
   - Đợi thông báo hoàn thành

### Bước 3: Kết quả
- File video đã nối sẽ được lưu tại vị trí bạn đã chọn
- Thời lượng video sẽ nằm trong khoảng bạn đã thiết lập
- Các video được chọn ngẫu nhiên từ thư mục gốc

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
- Giảm số lượng video trong thư mục
- Sử dụng video có độ phân giải thấp hơn
- Đóng các ứng dụng khác để giải phóng RAM


## Lưu ý quan trọng

1. **Hiệu suất**: Quá trình nối video có thể mất từ vài phút đến vài chục phút tùy thuộc vào:
   - Số lượng video
   - Kích thước và độ phân giải video
   - Cấu hình máy tính

2. **Dung lượng**: Đảm bảo có đủ dung lượng ổ cứng:
   - File đầu ra có thể lớn hơn tổng dung lượng các video gốc
   - Cần thêm khoảng 20-30% dung lượng dự phòng

3. **Chất lượng**: 
   - Chất lượng video đầu ra phụ thuộc vào video gốc
   - Các video có độ phân giải khác nhau sẽ được chuẩn hóa

4. **Định dạng hỗ trợ**:
   - Đầu vào: MP4, AVI, MOV, MKV, WMV, FLV, WebM
   - Đầu ra: MP4 (khuyến nghị)

## Liên hệ và hỗ trợ

Nếu gặp vấn đề không thể giải quyết:
1. Kiểm tra lại các bước cài đặt
2. Đảm bảo tất cả file video đều hợp lệ
3. Thử với số lượng video ít hơn
4. Khởi động lại máy tính và thử lại

## Phiên bản

- **v1.0**: Phiên bản đầu tiên với đầy đủ tính năng cơ bản
- Hỗ trợ nối video ngẫu nhiên với kiểm soát thời lượng
- Giao diện đồ họa thân thiện với người dùng
