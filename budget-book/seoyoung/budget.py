import tkinter as tk
from tkinter import messagebox
import os
import glob
import re

# 전체 지출 합계를 계산하는 함수
def calculate_total_expenses():
    total = 0
    # "가계부_지출_*.txt" 형식의 파일을 모두 탐색
    for filepath in glob.glob("가계부_지출_*.txt"):
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 빈 줄이거나 "총 수입"이 포함된 줄은 무시
                if not line or "총 수입" in line:
                    continue
                # 정규표현식으로 금액 추출
                match = re.search(r":\s*([\d,]+)원", line)
                if match:
                    try:
                        # 쉼표 제거 후 정수형으로 변환하여 합산
                        amount = int(match.group(1).replace(",", ""))
                        total += amount
                    except:
                        continue  # 변환 실패 시 무시
    return total

# 예산 파일 경로 상수
BUDGET_FILE = "budget.txt"

# 지출 발생 시 예산에서 차감하는 함수
def deduct_from_budget(amount):
    current = load_budget()
    if current is not None:
        new_budget = current - amount
        if new_budget < 0:
            new_budget = 0
        save_budget_to_file(new_budget)

# 현재 예산을 파일에서 불러오는 함수
def load_budget():
    try:
        with open("budget.txt", "r", encoding="utf-8") as f:
            return int(f.read().strip())  # 문자열을 정수로 변환
    except FileNotFoundError:
        return None  # 파일이 없는 경우
    except ValueError:
        return None  # 변환 실패한 경우

# 예산 금액을 파일에 저장하는 함수
def save_budget_to_file(amount):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        f.write(str(amount))  # 정수를 문자열로 저장

# 메인 budget 화면을 그리는 함수
def budget(frame):
    # 기존 위젯 모두 삭제 (화면 전환 대비)
    for widget in frame.winfo_children():
        widget.destroy()

    # 화면 구성 요소: 제목, 입력 안내
    tk.Label(frame, text="월 예산 설정", font=("Arial", 18)).pack(pady=10)
    tk.Label(frame, text="예산 금액 입력 (원)").pack()

    # 예산 입력창 생성
    budget_entry = tk.Entry(frame)
    budget_entry.pack()

    # 현재 예산 상태를 표시할 라벨 변수
    current_budget_var = tk.StringVar()
    current_budget_label = tk.Label(frame, textvariable=current_budget_var, font=("Arial", 14))
    current_budget_label.pack(pady=10)

    # 현재 예산 정보 표시 및 예산 경고 처리 함수
    def update_current_budget_display():
        current = load_budget()
        total_expense = calculate_total_expenses()

        if current:
            remaining = current - total_expense
            current_budget_var.set(
                f"현재 월 예산: {current:,}원\n"
                f"총 지출: {total_expense:,}원\n"
                f"남은 예산: {remaining:,}원"
            )

            # 예산의 10% 이하로 남으면 경고 표시
            if remaining <= current * 0.1:
                messagebox.showwarning("예산 경고", f"⚠️ 남은 예산이 10% 이하입니다!\n({remaining:,}원 남음)")

        else:
            current_budget_var.set("현재 월 예산: 없음")

    # 입력된 예산을 저장하는 함수
    def save_budget():
        try:
            amount = int(budget_entry.get())  # 입력값을 정수로 변환
            if amount <= 0:
                raise ValueError  # 0 이하 예산은 오류 처리

            current = load_budget()

            # 기존 예산과 다른 경우 사용자에게 확인 요청
            if current is not None and current != amount:
                confirm = messagebox.askyesno("예산 변경 확인",
                                              f"현재 예산은 {current:,}원입니다.\n정말 {amount:,}원으로 변경하시겠습니까?")
                if not confirm:
                    return  # 사용자가 취소한 경우 저장하지 않음

            # 예산 저장 및 사용자 알림
            save_budget_to_file(amount)
            messagebox.showinfo("저장 완료", f"월 예산이 {amount:,}원으로 설정되었습니다.")
            update_current_budget_display()  # 변경된 예산 반영

        except ValueError:
            # 입력 오류 처리
            messagebox.showerror("입력 오류", "양의 정수를 입력하세요.")

    # 저장 버튼 추가
    tk.Button(frame, text="저장", command=save_budget).pack(pady=10)

    # 시작 시 예산 현황 표시
    update_current_budget_display()
