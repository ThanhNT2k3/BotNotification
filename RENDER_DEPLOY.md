# Deploy Trading Bot to Render.com

## Ưu điểm của Render.com:
✅ **Hoàn toàn MIỄN PHÍ** - Không cần credit card  
✅ Deploy từ GitHub tự động  
✅ Auto-restart khi crash  
✅ SSL/HTTPS miễn phí  
✅ Logs và monitoring đầy đủ  

## Bước 1: Chuẩn bị GitHub Repository

### 1.1. Tạo file `.gitignore` (nếu chưa có)
```bash
echo "__pycache__/
*.pyc
.env
.DS_Store" > .gitignore
```

### 1.2. Push code lên GitHub

```bash
# Khởi tạo git (nếu chưa có)
git init

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit - Trading Bot"

# Tạo repo trên GitHub và push
# Truy cập: https://github.com/new
# Tạo repo mới (ví dụ: trading-bot)
# Sau đó chạy:
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git branch -M main
git push -u origin main
```

## Bước 2: Deploy trên Render.com

### 2.1. Đăng ký/Đăng nhập
1. Truy cập: **[render.com](https://render.com)**
2. Click **"Get Started"** hoặc **"Sign In"**
3. Đăng nhập bằng GitHub account

### 2.2. Tạo Web Service mới
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository của bạn
3. Chọn repository `trading-bot`

### 2.3. Cấu hình Service

Điền thông tin như sau:

**Name**: `trading-bot` (hoặc tên bạn muốn)

**Region**: `Singapore` (gần Vietnam nhất)

**Branch**: `main`

**Runtime**: `Docker`

**Instance Type**: `Free`

### 2.4. Environment Variables (Optional)

Nếu muốn ẩn Discord webhook URL:

Click **"Advanced"** → **"Add Environment Variable"**
- Key: `DISCORD_WEBHOOK_URL`
- Value: `your_webhook_url_here`

Sau đó update `trading_bot.py`:
```python
import os
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', 'YOUR_DISCORD_WEBHOOK_URL_HERE')
```

### 2.5. Deploy

Click **"Create Web Service"**

Render sẽ tự động:
- Clone repository
- Build Docker image
- Deploy và start bot
- Cung cấp URL (ví dụ: `https://trading-bot.onrender.com`)

## Bước 3: Verify

1. Đợi vài phút để build hoàn tất
2. Check logs trong Render dashboard
3. Bot sẽ tự động chạy và gửi notification đến Discord!

## Quản lý

### Xem Logs
Trong Render dashboard → Chọn service → Tab **"Logs"**

### Restart Service
Tab **"Manual Deploy"** → Click **"Clear build cache & deploy"**

### Update Code
Chỉ cần push code mới lên GitHub:
```bash
git add .
git commit -m "Update bot"
git push
```
Render sẽ tự động deploy lại!

## Lưu ý về Free Tier

⚠️ **Render Free Tier sẽ sleep sau 15 phút không hoạt động**

Để giữ bot chạy 24/7, dùng **UptimeRobot** (giống như Replit):

1. Đăng ký tại [uptimerobot.com](https://uptimerobot.com)
2. Tạo monitor:
   - Type: HTTP(s)
   - URL: URL Render của bạn (ví dụ: `https://trading-bot.onrender.com`)
   - Interval: 5 minutes
3. UptimeRobot sẽ ping mỗi 5 phút → Bot không bao giờ sleep!

## Troubleshooting

**Nếu build fail:**
- Check logs trong Render dashboard
- Verify `Dockerfile` và `requirements.txt` đúng
- Ensure `main.py` tồn tại

**Nếu bot không gửi notification:**
- Check logs xem có lỗi gì
- Verify Discord webhook URL đúng
- Check timezone settings

## Cost
**100% MIỄN PHÍ!** 🎉
