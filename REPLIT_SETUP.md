# Replit Keep-Alive Setup Guide

## Bước 1: Deploy lên Replit

1. Truy cập [Replit.com](https://replit.com) và đăng nhập
2. Tạo một Repl mới:
   - Click **"+ Create Repl"**
   - Chọn **"Import from GitHub"** hoặc upload files
   - Hoặc tạo **Python Repl** và copy các files sau vào:
     - `main.py`
     - `trading_bot.py`
     - `keep_alive.py`
     - `requirements.txt`

3. Trong Replit, click **"Run"** - bot sẽ chạy và web server sẽ start ở port 8080

## Bước 2: Setup UptimeRobot để Keep Alive

Replit free sẽ sleep sau một thời gian không hoạt động. Để giữ bot chạy 24/7, dùng **UptimeRobot**:

1. Truy cập [UptimeRobot.com](https://uptimerobot.com) và đăng ký tài khoản miễn phí

2. Sau khi đăng nhập, click **"+ Add New Monitor"**

3. Điền thông tin:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Trading Bot Keep Alive
   - **URL**: Copy URL từ Replit của bạn (ví dụ: `https://your-repl-name.your-username.repl.co`)
   - **Monitoring Interval**: 5 minutes (miễn phí)

4. Click **"Create Monitor"**

## Bước 3: Verify

- UptimeRobot sẽ ping URL của bạn mỗi 5 phút
- Điều này sẽ giữ cho Repl không bị sleep
- Bot sẽ chạy liên tục 24/7

## Lưu ý quan trọng:

⚠️ **Replit Free Tier có giới hạn:**
- Mỗi tháng có giới hạn về compute time
- Nếu vượt quá, Repl sẽ bị tạm dừng
- Nên nâng cấp lên **Replit Hacker Plan** ($7/tháng) để unlimited uptime

## Alternative: Sử dụng Cron-Job.org

Nếu không muốn dùng UptimeRobot, có thể dùng [Cron-Job.org](https://cron-job.org):

1. Đăng ký tài khoản
2. Tạo cronjob mới
3. URL: URL Replit của bạn
4. Interval: Mỗi 5 phút
5. Save

## Kiểm tra Bot đang chạy

Truy cập URL Replit của bạn trong browser, bạn sẽ thấy: **"Bot is running!"**

Logs trong Replit Console sẽ hiển thị hoạt động của bot.
