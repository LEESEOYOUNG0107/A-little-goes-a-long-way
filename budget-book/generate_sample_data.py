#  Test를 위해, 지출 파일을 임의로 생성 : 2025년 1월 ~ 5월까지만, 50 개 정도 생성
#  최초 1회만 실행
#  2025.06.14  -- ChatGPT로 생성

import random
import os
from datetime import datetime, timedelta

# 건강한 항목 설정
CATEGORIES = ["식비", "외식", "간식", "학원", "교육", "도서", "패션", "쇼핑", "뷰티", "여행", "문화", "기타"]

# 데이터 파일을 생성할 폴더
OUTPUT_DIR = "."

# 날짜 만들기: 2025-01-01 ~ 2025-05-31
start_date = datetime.strptime("2025-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-05-31", "%Y-%m-%d")

def generate_random_expense():
    items = random.randint(2, 6)
    lines = []
    total = 0
    for _ in range(items):
        cat = random.choice(CATEGORIES)
        amount = random.randint(5000, 50000)
        total += amount
        lines.append(f"{cat}: {amount:,}원")
    lines.append(f"총 지출: {total:,}원\n")
    return lines

def generate_sample_data(n_files=50):
    used_dates = set()
    attempts = 0
    while len(used_dates) < n_files and attempts < n_files * 5:
        rand_days = random.randint(0, (end_date - start_date).days)
        date = start_date + timedelta(days=rand_days)
        date_str = date.strftime("%Y-%m-%d")
        if date_str in used_dates:
            attempts += 1
            continue
        used_dates.add(date_str)
        content = generate_random_expense()
        file_path = os.path.join(OUTPUT_DIR, f"가계부_지출_{date_str}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
    print(f"총 {len(used_dates)}개의 샘플 지출 파일이 생성되었습니다.")

# 시험 버전
def main():
    generate_sample_data(50)

if __name__ == "__main__":
    main()
