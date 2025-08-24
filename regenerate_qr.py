import qrcode
from pathlib import Path
import shutil

# 🟢 إعدادات
BASE_URL = "https://clientqrsystem.onrender.com"  # الرابط الجديد
CLIENTS = [f"C{str(i).zfill(3)}" for i in range(1, 51)]  # C001..C050
QRCODES_DIR = Path("static/qrcodes")  # المجلد اللي فيه الصور

# 🟢 مسح الصور القديمة
if QRCODES_DIR.exists():
    shutil.rmtree(QRCODES_DIR)  # حذف المجلد بالكامل
QRCODES_DIR.mkdir(parents=True, exist_ok=True)

# 🟢 توليد QR Codes جديدة
for cid in CLIENTS:
    url = f"{BASE_URL}/client/{cid}"
    img = qrcode.make(url)
    img_path = QRCODES_DIR / f"{cid}.png"
    img.save(img_path)
    print(f"✅ تم توليد QR Code للعميل {cid} -> {img_path}")

print("\n🎉 تم توليد جميع QR Codes الجديدة بنجاح!")
