# Bộ đăng YouTube (tiếng Việt): "Kỳ quan Trái Đất"

Video: `output/final-vi_film.mp4` (23:53, 16:9, 1280×720) · Phụ đề: `output/final-vi.srt` · Ngôn ngữ: tiếng Việt
Ảnh bìa: `publishing/thumbnail-vi.png` (1280×720)

## 1. Ảnh bìa
Dùng lại ảnh anh tạo theo Prompt A (nền Trái Đất "bùng nổ"), chỉ đổi dòng chữ sang tiếng Việt bằng font Patrick Hand (có đủ dấu tiếng Việt):
- Dòng trên: **TRÁI ĐẤT** (màu kem)
- Dòng dưới: **KHÔNG YÊN BÌNH** (màu cam)

Em đã xóa dấu sao watermark do máy tạo ảnh để lại, xem lại ở cỡ nhỏ 320×180 vẫn đọc rõ. Tạo lại bằng `python3 publishing/make_thumbnail_vi.py`.

Dòng chữ khác nếu anh muốn đổi (sửa trong file `make_thumbnail_vi.py`): "17 KỲ QUAN DỮ DỘI", "HÀNH TINH KHÔNG NGỪNG CHUYỂN ĐỘNG".

## 2. Tiêu đề (năm lựa chọn)
1. **Kỳ quan Trái Đất: 17 điều kỳ vĩ, từ đá rơi vũ trụ đến đáy đại dương sâu nhất** (em đề xuất)
2. Trái Đất không yên bình: núi lửa, sông băng, lốc xoáy và hơn thế nữa
3. 17 kỳ quan dữ dội nhất của hành tinh chúng ta
4. Từ quả cầu lửa đến cực lạnh: những nơi khắc nghiệt nhất Trái Đất
5. Vì sao Trái Đất chưa bao giờ đứng yên? 17 kỳ quan giải thích

## 3. Mô tả (dán sẵn)
Nhìn từ xa, Trái Đất có vẻ thật yên bình. Nhưng nhìn gần, hành tinh của chúng ta chưa bao giờ đứng yên.

Trong hành trình bằng tranh minh họa này, chúng ta đi qua 17 kỳ quan khắc nghiệt của Trái Đất: thiên thạch và sao chổi, Vành đai lửa, đỉnh Everest, siêu núi lửa và mạch phun nước nóng, động đất và sóng thần, dòng sông Amazon, Grand Canyon, sông băng và núi băng trôi, những hang động khổng lồ (có cả Sơn Đoòng), kho khoáng sản dưới lòng đất, đáy đại dương sâu nhất, lốc xoáy và bão, thời tiết kỳ quái, tuyết lở, hai cực Trái Đất và những sa mạc khô cằn nhất.

Mục lục
0:00 Mở đầu
0:19 Hành trình của chúng ta: mục lục
0:31 1. Vị khách từ vũ trụ
1:52 2. Trái Đất rạn nứt
3:22 3. Ngọn núi vĩ đại nhất
5:16 4. Núi lửa tột đỉnh
6:37 5. Những điểm nóng
7:57 6. Khi đất rung chuyển
9:22 7. Dòng sông vĩ đại nhất
10:35 8. Xói mòn cực độ
11:43 9. Dòng sông băng
13:05 10. Vào lòng vực thẳm
14:24 11. Kho báu dưới lòng đất
15:41 12. Lặn xuống biển sâu
17:08 13. Những cơn gió dữ
18:29 14. Thời tiết kỳ quái
19:56 15. Băng giá khắc nghiệt
21:11 16. Nơi tận cùng Trái Đất
22:19 17. Vùng đất khô cằn

Bạn ấn tượng nhất với kỳ quan nào? Hãy cho chúng mình biết ở phần bình luận nhé.

Hình ảnh là tranh minh họa đơn giản hóa để giải thích, không phải bản đồ hay sơ đồ khoa học chính xác. Giọng đọc do AI tạo.

#TráiĐất #KỳQuanThiênNhiên #KhoaHọcTráiĐất

## 4. Thẻ (tags)
trái đất, kỳ quan trái đất, kỳ quan thiên nhiên, khoa học trái đất, địa lý, núi lửa, siêu núi lửa, động đất, sóng thần, đỉnh everest, sông amazon, grand canyon, sông băng, núi băng, hang động, hang sơn đoòng, đại dương sâu, rãnh mariana, lốc xoáy, bão, thời tiết cực đoan, tuyết lở, nam cực, bắc cực, sa mạc sahara, thung lũng chết, phim tài liệu minh họa, video giáo dục

## 5. Bình luận ghim
Núi lửa, sông băng, hang động hay những cơn bão sa mạc: chương nào làm bạn bất ngờ nhất? Ghi số chương ở dưới nhé 👇

## 6. Danh sách kiểm tra trước khi đăng
| Mục | Tình trạng | Ghi chú |
|---|---|---|
| Mục lục (chapters) hợp lệ | ✅ | Bắt đầu từ 0:00, 19 mục, mỗi mục dài hơn 10 giây, mốc lấy từ bản render cuối |
| Tiêu đề, mô tả và mục lục khớp với video | ✅ | Mọi dữ kiện lấy từ lời dẫn đã duyệt, không thêm gì |
| Ảnh bìa | ✅ | `thumbnail-vi.png`; đủ dấu tiếng Việt; góc dưới bên phải (chỗ YouTube hiện thời lượng) chỉ có nền và đám mây |
| File phụ đề | ✅ | `output/final-vi.srt` (tải lên làm phụ đề tiếng Việt) |
| Nghe lại giọng đọc | ⚠️ anh nghe | Em chỉ kiểm tra bằng độ dài và khoảng lặng; anh nghe giúp các tên riêng (Eyjafjallajökull, Chomolungma, Sơn Đoòng…) |
| Gắn nhãn nội dung AI | ⚠️ anh quyết | Hình là tranh minh họa rõ ràng; giọng đọc do AI tạo, mô tả đã ghi rõ |
| Giấy phép giọng đọc, hình ảnh | ⚠️ anh kiểm tra | Giọng Gemini Algieba và ảnh tạo bằng Google: xem điều khoản thương mại hiện hành |
| Hiệu ứng âm thanh | ✅ | Tạo bằng ElevenLabs trên tài khoản của anh; xem điều khoản thương mại của gói |
| Phông chữ | ✅ | Patrick Hand và Noto Sans theo giấy phép SIL Open Font License |
| Content ID | ⚠️ không thể đảm bảo | Không dùng nhạc hay video của bên thứ ba |
