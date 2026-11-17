# Kịch bản video demo tiếng Việt (6-8 phút)

> Video cuối phải dùng chính giọng của sinh viên và hiển thị JMeter cùng Activity Monitor trong một khung hình. Không dùng giọng tổng hợp. Điền link YouTube unlisted vào README/report sau khi upload.

## Chuẩn bị

1. Mở Activity Monitor, chọn CPU/Memory và tìm `java`/`node`.
2. Mở JMeter GUI để trình bày plan; chạy tải bằng non-GUI.
3. Mở HTML report và ảnh summary từng scenario.
4. Không hiển thị password, JWT, serial number hoặc Hardware UUID.
5. Kiểm tra microphone và quay toàn màn hình.

## 0:00-0:45 - Giới thiệu

“Em là Ngô Gia An, MSSV 23120205. Đây là HW05 Performance Testing trên EShop. Em dùng Apache JMeter 5.6.3 trên MacBook Air M2, 8 GB RAM. Video trình bày workflow, cách chạy, resource monitoring và kết quả Load, Stress, Spike, Soak.”

Hiển thị README, hardware spec, commit hiện tại và bốn JMX.

## 0:45-2:00 - Workflow

Trong JMeter, lần lượt chỉ vào CSV Data Set, Login/JWT extractor, Product Search/Detail, Cart, Checkout, assertions và random think time. Giải thích ba endpoint group và ba listener khác nhau: View Results Tree, Summary Report, Aggregate Report.

## 2:00-3:00 - Human review

“Run Load đầu có khoảng 15-16% lỗi. Em không kết luận SUT lỗi ngay mà kiểm tra raw JTL. Credential và product ID bị rỗng theo chu kỳ. Nguyên nhân cuối cùng là CSV có dòng rỗng cuối file. Em lưu run INVALID, xóa dòng, smoke 8 vòng được 40/40 sample pass rồi mới chạy full.”

Hiển thị các commit sửa CSV và phần Human review trong report.

## 3:00-4:30 - Load, Stress, Spike

- Load: 500 sample, 0 lỗi, 5.79 req/s, p95 19 ms.
- Stress: 4,000 sample, 0 lỗi, 22.06 req/s, p95 11 ms.
- Spike: 2,250 sample, 0 lỗi, 84.82 req/s, p95 15 ms.

Nói rõ Spike là burst throughput, không phải endurance threshold. Chỉ vào CPU/RSS backend và JMeter.

## 4:30-5:30 - Soak

- 12 phút, 13,701 sample, 0 lỗi;
- 19.08 req/s;
- p95 7 ms, p99 26 ms;
- backend RSS peak 51.53 MiB.

“Kết luận là phần cứng đã ổn định ít nhất ở 19.08 req/s trong 12 phút. Đây không phải maximum tuyệt đối vì test không tăng tải từng bước đến khi lỗi.”

## 5:30-6:30 - Bugs và CI

Trình bày hai reproduction: checkout lưu `total_amount=1` dù cart giá 25,000,000; account khóa sau hai lần sai và vẫn khóa sau 35 giây. Sau đó mở flow chart continuous testing: change filter → smoke → fixed runner → load gate → p95/error comparison → controlled rerun → nightly Stress/weekly Spike+Soak.

## 6:30-7:15 - Agent Skill và kết luận

Mở `agent-skill/jmeter-performance-evidence/SKILL.md`. Giải thích skill bắt buộc clean state, raw JTL, resource evidence, phân loại infrastructure failure và không bịa dữ liệu. Kết luận ưu tiên server-side total recalculation, sau đó sửa lockout.

## Sau khi quay

- [ ] Video dài ít nhất 6 phút.
- [ ] JMeter và Activity Monitor cùng khung.
- [ ] Giọng sinh viên nghe rõ; không lộ dữ liệu nhạy cảm.
- [ ] Upload YouTube Unlisted.
- [ ] Điền URL vào README/report, commit và đóng gói lại.
