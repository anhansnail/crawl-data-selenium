import requests
from bs4 import BeautifulSoup
import re
import csv
import time

BASE_URL = "https://vieclamhanoi.net"
START_PAGE = 1
MAX_PAGES = 5  # 👉 Bạn có thể đổi số lượng trang muốn lấy

headers = {
    "User-Agent": "Mozilla/5.0"
}

data_list = []

for page in range(START_PAGE, START_PAGE + MAX_PAGES):
    list_url = f"{BASE_URL}/viec-tim-nguoi?page={page}"
    print(f"🔍 Đang xử lý trang {page}: {list_url}")
    try:
        res = requests.get(list_url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Không thể truy cập trang {page}: {e}")
        continue

    soup = BeautifulSoup(res.text, "html.parser")
    job_links = []
    for a in soup.select("a.job-title"):
        href = a.get("href")
        if href and href.startswith("/viec-lam/"):
            job_links.append(BASE_URL + href)

    print(f"👉 Tìm được {len(job_links)} tin tuyển dụng trong trang {page}")

    for url in job_links:
        try:
            job_res = requests.get(url, headers=headers, timeout=10)
            job_soup = BeautifulSoup(job_res.text, "html.parser")

            # Tên công ty
            ten_cty = job_soup.select_one(".job-details-info .company-info h2")
            ten_cty = ten_cty.get_text(strip=True) if ten_cty else ""

            # Mô tả công việc
            description = job_soup.select_one(".job-description")
            raw_text = description.get_text(separator=" ", strip=True) if description else ""

            # Tìm email và số điện thoại
            email_list = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", raw_text)
            sdt_list = re.findall(r"0\d{8,10}", raw_text)

            data_list.append({
                "url": url,
                "ten_cong_ty": ten_cty,
                "email": ", ".join(set(email_list)),
                "so_dien_thoai": ", ".join(set(sdt_list)),
            })

            print(f"✅ {ten_cty} | 📧 {email_list[:1]} | 📱 {sdt_list[:1]}")
            time.sleep(0.2)

        except Exception as e:
            print(f"⚠️ Lỗi xử lý tin: {url} - {e}")
            continue

# Lưu ra CSV
with open("nguoi_dang_tuyen.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["url", "ten_cong_ty", "email", "so_dien_thoai"])
    writer.writeheader()
    writer.writerows(data_list)

print("\n✅ Đã lưu dữ liệu vào file: nguoi_dang_tuyen.csv")
