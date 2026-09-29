# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: thay dòng `> *Câu trả lời của bạn*` bằng câu trả lời.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: ..........................  Mã học viên: ..........................

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

> Khi deploy, nếu quên set AGENT_API_KEY, Settings lập tức báo lỗi và container không nhận traffic. Nếu dùng mặc định changeme, app vẫn chạy và người khác có thể dùng khóa đó để gọi LLM, phát sinh chi phí trước khi tôi phát hiện.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

> Dòng log thu được: {"event":"ask_completed","level":"info","timestamp":"2026-09-29T03:46:04.286121+00:00","user_id":"sv-test","tokens_in":8,"tokens_out":31,"cost_usd":0.00002}. Tôi có thể lọc tất cả request của user_id sv-test và tính/tạo cảnh báo cho tổng cost_usd hoặc token; chuỗi print tự do không có field ổn định để làm hai việc này.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | 1.7 GB |
| Multi-stage | 271 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

> Tôi đo được bản 1-stage là 1.7 GB, còn bản multi-stage là 271 MB. Phần chênh lệch chủ yếu đến từ base image python:3.11 đầy đủ và các dependency/artifact chỉ phục vụ build. Runtime multi-stage chỉ giữ Python slim, dependency đã cài và source cần thiết.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

> Khi chỉ sửa app/main.py, các layer base image, COPY requirements.txt và pip install được dùng lại từ cache; layer COPY app/utils và layer sau nó build lại. Nếu COPY . . đứng trước pip install, thay đổi một ký tự trong source sẽ làm mất cache và cài lại toàn bộ dependency.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

> Một lỗ hổng có thể cho phép kẻ tấn công chạy lệnh trong process Python; nếu process là root, lệnh đó có quyền root trong container và có thể tận dụng mount, Docker socket hoặc cấu hình sai để mở rộng ảnh hưởng sang host. USER appuser hạ quyền của process, nên việc chiếm được app không tự động trở thành root.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

> Tối đa là 20 request trong khoảng 2 giây: 10 request ngay trước 10:01:00, rồi 10 request ngay sau 10:01:00. Cách đếm theo phút đồng hồ reset quota ở mốc phút, còn sliding window tính cả hai nhóm trong 60 giây nên chặn nhóm sau.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

> Rate limiter giới hạn tần suất request trong 60 giây, còn cost guard giới hạn số tiền đã dùng trong tháng. Một user gọi ít request nhưng prompt rất lớn có thể qua rate limit nhưng bị cost guard chặn khi vượt budget. Ngược lại, user đã dùng hết quota 10 request/phút nhưng mỗi request rất rẻ và vẫn còn dư budget sẽ bị rate limiter chặn.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

> *Câu trả lời của bạn*

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

> *Câu trả lời của bạn*

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

> *Câu trả lời của bạn*
