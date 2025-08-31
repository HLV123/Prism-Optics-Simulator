# Mô Phỏng Lăng Kính Chính Xác
Một ứng dụng mô phỏng hiện tượng khúc xạ và tán sắc ánh sáng qua lăng kính với giao diện trực quan và tương tác.

## Tính năng chính
- **Mô phỏng chính xác**: Áp dụng định luật Snell để tính toán đường đi của tia sáng
- **Hai chế độ hiển thị**:
  - Chế độ đơn sắc: Hiển thị một tia sáng với thông số chi tiết
  - Chế độ tán sắc: Hiển thị hiệu ứng tán sắc thành quang phổ 7 màu
- **Giao diện tương tác**: Điều chỉnh các thông số vật lý trong thời gian thực
- **Thu phóng và di chuyển**: Hỗ trợ zoom và pan để quan sát chi tiết
- **Chụp ảnh**: Lưu hình ảnh mô phỏng với chất lượng cao
## Thông số có thể điều chỉnh
- Chỉ số khúc xạ môi trường (n₁)
- Chỉ số khúc xạ lăng kính (n₂)
- Góc tới của tia sáng (θ₁)
- Góc đỉnh của lăng kính (A)
## Cài đặt
1. Đảm bảo bạn đã cài đặt Python 3.7+
2. Cài đặt thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
## Sử dụng
Chạy chương trình bằng lệnh:
```bash
python hay.py
```
### Các nút chức năng
- **Reset**: Đặt lại tất cả thông số về giá trị mặc định
- **Tán sắc**: Chuyển sang chế độ hiển thị hiệu ứng tán sắc
- **Bình thường**: Chuyển về chế độ đơn sắc
- **Chụp ảnh**: Lưu hình ảnh mô phỏng vào file
### Điều khiển
- **Zoom**: Sử dụng scroll chuột để phóng to/thu nhỏ
- **Pan**: Nhấn và kéo chuột để di chuyển khung nhìn
## Giáo dục ứng dụng
Phần mềm này thích hợp cho:
- Giảng dạy vật lý quang học
- Học tập về hiện tượng khúc xạ và tán sắc
- Nghiên cứu ảnh hưởng của các thông số đến góc lệch

## Giấy phép

MIT License - xem file LICENSE để biết chi tiết.
