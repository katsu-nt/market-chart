# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import pandas as pd
# import time

# # Khởi tạo trình duyệt headless
# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# url = "https://finance.yahoo.com/quote/VND=X/history/?period1=1451606400&period2=1753056000"
# driver.get(url)

# # Đợi trang tải
# time.sleep(5)

# soup = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()

# # Tìm bảng
# table = soup.find("table")
# if not table:
#     print("Không tìm thấy bảng.")
#     exit()

# # Header và rows
# headers = [th.text.strip() for th in table.find_all("th")]
# rows = []
# for tr in table.find("tbody").find_all("tr"):
#     cols = [td.text.strip().replace(',', '') for td in tr.find_all("td")]
#     if len(cols) == len(headers):
#         rows.append(cols)

# df = pd.DataFrame(rows, columns=headers)

# # Chuyển sang số nếu có thể
# for col in df.columns:
#     try:
#         df[col] = pd.to_numeric(df[col])
#     except:
#         pass

# df.to_excel("usd_vnd_2016_2025.xlsx", index=False)
# print("✅ Đã lưu vào: usd_vnd_2016_2025.xlsx")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Khởi tạo trình duyệt headless
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://finance.yahoo.com/quote/VND=X/history/?period1=1451606400&period2=1753056000"
driver.get(url)

# Đợi trang tải
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Tìm bảng
table = soup.find("table")
if not table:
    print("Không tìm thấy bảng.")
    exit()

# Header và rows
headers = [th.text.strip() for th in table.find_all("th")]
rows = []
for tr in table.find("tbody").find_all("tr"):
    cols = [td.text.strip().replace(',', '') for td in tr.find_all("td")]
    if len(cols) == len(headers):
        rows.append(cols)

df = pd.DataFrame(rows, columns=headers)

# Chuyển sang số nếu có thể
for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        pass

# 🔧 Tạo thư mục cùng cấp với file hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(current_dir, "csv-data")
os.makedirs(csv_dir, exist_ok=True)

# 🔽 Lưu file CSV
output_path = os.path.join(csv_dir, "usd_vnd_2016_2025.csv")
df.to_csv(output_path, index=False)

print(f"✅ Đã lưu vào: {output_path}")

