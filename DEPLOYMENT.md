# Thông Tin Deploy — Checkpoint 5

> File này ghi lại thông tin và bằng chứng deploy thật. Chỉ ghi TÊN biến môi trường, tuyệt đối không dán giá trị API key vào đây.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Ha Anh Tuan |
| Mã học viên | 2A202602376 |
| Repo | K4-L3B-HaAnhTuan-2A202602376-Cloud-Service-And-Deployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://k4-l3b-haanhtuan-2a202602376-cloud-service-and-d-production.up.railway.app |
| Platform | Railway |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Cloud

Ghi tên biến và nguồn giá trị, không ghi giá trị secret:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | Railway tự gán |
| `AGENT_API_KEY` | ✅ | Đặt trong Railway Variables, không nằm trong repo |
| `REDIS_URL` | ✅ | Reference tới Railway Redis service |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |

## Lệnh Kiểm Tra

```bash
# 1. Liveness — mong đợi 200 {"status":"ok"}
curl -i https://k4-l3b-haanhtuan-2a202602376-cloud-service-and-d-production.up.railway.app/health

# 2. Readiness — mong đợi 200 {"status":"ready"} và Redis đã kết nối
curl -i https://k4-l3b-haanhtuan-2a202602376-cloud-service-and-d-production.up.railway.app/ready

# 3. Không có API key — mong đợi 401
curl -i -X POST https://k4-l3b-haanhtuan-2a202602376-cloud-service-and-d-production.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# 4. Có API key — mong đợi 200 kèm câu trả lời
curl -i -X POST https://k4-l3b-haanhtuan-2a202602376-cloud-service-and-d-production.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AGENT_API_KEY" \
  -H "X-User-Id: sv-test" \
  -d '{"question":"Deploy là gì?"}'
```

## Kết Quả Chạy Thật

```text
GET /health  -> 200 {"status":"ok","service":"day12-agent","version":"1.0.0"}
GET /ready   -> 200 {"status":"ready","redis":true}
POST /ask không có API key -> 401
```

## Ảnh Chụp Màn Hình

Đặt ảnh thật trong thư mục `screenshots/`:

- `screenshots/dashboard.png` — trang Railway hiển thị service deploy thành công.
- `screenshots/health.png` — kết quả gọi `/health` và/hoặc `/ready` từ trình duyệt hoặc terminal.

## Nếu Dùng Phương Án Dự Phòng

Không áp dụng: service đã được deploy công khai trên Railway, không dùng `LOCAL_FALLBACK=true`.
