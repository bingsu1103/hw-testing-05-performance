# Kịch bản video demo tiếng Việt (6-8 phút)

> Video cuối phải dùng chính giọng của sinh viên và hiển thị JMeter cùng Activity Monitor trong một khung hình. Không dùng giọng tổng hợp. Điền link YouTube unlisted vào README/report sau khi upload.

## Chuẩn bị

1. Mở Activity Monitor, chọn CPU/Memory và tìm `java`/`node`.
2. Mở JMeter GUI để trình bày plan; nếu chạy lại tải thì dùng non-GUI.
3. Mở HTML report và ảnh summary của từng scenario.
4. Không hiển thị password, JWT, serial number hoặc Hardware UUID.
5. Kiểm tra microphone và quay toàn màn hình.

## 0:00-0:45 - Giới thiệu và phạm vi

“Em là Ngô Gia An, MSSV 23120205. Phần em phụ trách là Flow 2 - Tìm kiếm và Mã giảm giá: đăng ký, đăng nhập, tìm kiếm, xem chi tiết, thêm giỏ, áp mã giảm giá và thanh toán. Em dùng Apache JMeter 5.6.3 trên MacBook Air M2, 8 GB RAM.”

Hiển thị `docs/FLOW_ASSIGNMENT.md`, ảnh bảng phân công, commit hiện tại và bốn JMX. Nếu đã cập nhật bảng nhóm, hiển thị thêm ảnh có tên/MSSV.

## 0:45-2:00 - Workflow Flow 2

Trong JMeter, chỉ lần lượt tám sampler: Register, Login, Search Products, Product Detail, Add to Cart, Apply Coupon, Checkout và Record Coupon Usage. Giải thích:

- tài khoản duy nhất theo thread/iteration tránh trùng đăng ký;
- JWT, coupon ID, final amount và order ID được trích xuất để truyền giữa các bước;
- Checkout dùng đúng `final_amount` từ Apply Coupon;
- CSV dùng `BIGBUY` để kết quả đo ổn định;
- Load, Stress, Spike dùng ba listener khác nhau theo yêu cầu.

## 2:00-2:45 - Human review và smoke test

“Phiên bản cũ là flow mua hàng login-first nên thiếu đăng ký và áp mã. Em viết contract test yêu cầu đúng Flow 2, tạo lại bốn plan, rồi smoke một user một vòng. Smoke có đủ tám request và không lỗi trước khi chạy full.”

Hiển thị commit sửa scope, test `tests/test_flow2_scope.py` và kết quả validate.

## 2:45-4:15 - Load, Stress, Spike

- Load: 800 mẫu, 0 lỗi, 7.56 req/s, p95 8 ms.
- Stress: 6.400 mẫu, 0 lỗi, 28.84 req/s, p95 6 ms.
- Spike: 3.600 mẫu, 0 lỗi, 94.22 req/s, p95 39 ms.

Nói rõ checkout là label nhạy nhất trong Spike với p95 172 ms và max 449 ms. Spike là burst throughput, không phải endurance threshold. Chỉ vào raw JTL, HTML report và CPU/RSS của backend/JMeter.

## 4:15-5:15 - Soak

- 12 phút, 13.696 mẫu, 0 lỗi;
- 19.06 req/s;
- p95 7 ms, p99 22 ms;
- backend RSS peak 59.36 MiB.

“Có một excursion ngắn với max 2.285 ms khoảng phút 7-8, nhưng cửa sổ 30 giây kế tiếp trở lại khoảng 20 req/s, max 27-71 ms và vẫn 0 lỗi. Vì vậy kết luận an toàn là hệ thống ổn định ít nhất ở 19.06 req/s trong 12 phút, không phải maximum tuyệt đối.”

## 5:15-6:15 - Bug mã phần trăm và CI

Mở Issue #3 và evidence. Nói: “SAVE10 có type percent, discount value 10. Với giỏ 30 triệu, đúng ra còn 27 triệu. API lại trả final amount 300 triệu và discount âm 270 triệu, phù hợp với lỗi coi số 10 là hệ số thay vì 10 phần trăm.”

Sau đó mở flow chart continuous testing: change filter → smoke → fixed runner → Load gate → p95/error comparison → controlled rerun → nightly Stress/weekly Spike+Soak.

## 6:15-7:15 - Agent Skill và kết luận

Mở `agent-skill/jmeter-performance-evidence/SKILL.md`. Giải thích skill yêu cầu clean state, smoke trước measured run, lưu raw JTL/resource evidence, phân biệt infrastructure failure với SUT defect và không bịa dữ liệu. Kết luận ưu tiên sửa phép tính percentage coupon, bổ sung test cho cả fixed/percent, rồi chạy step-load để tìm capacity.

## Sau khi quay

- [ ] Video dài ít nhất 6 phút.
- [ ] JMeter và Activity Monitor cùng khung.
- [ ] Giọng sinh viên nghe rõ; không lộ dữ liệu nhạy cảm.
- [ ] Demo Agent Skill end-to-end.
- [ ] Upload YouTube Unlisted.
- [ ] Điền URL vào README/report, commit và đóng gói lại.
