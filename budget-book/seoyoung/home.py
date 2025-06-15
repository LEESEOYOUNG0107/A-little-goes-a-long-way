import tkinter as tk
from tkinter import messagebox, simpledialog
import budget  # budget 모듈에서 load_budget, calculate_total_expenses 함수 필요
import budget
from datetime import datetime
from PIL import Image, ImageTk

from seoyoung.deposit import log_donation_as_expense
from PIL import Image, ImageTk

def homeImg(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    image = Image.open("home_img.png")  # 이미지 경로 맞게 수정
    image = image.resize((900, 600))  # 필요시 크기 조절
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(frame, image=photo)
    label.image = photo  # 참조 유지
    label.pack(pady=20)


def openDonation(frame, selectedDate=None):
    # 예산에서 남은 금액 계산
    current_budget = budget.load_budget()
    if current_budget is None:
        messagebox.showwarning("예산 없음", "예산이 설정되어 있지 않습니다. 먼저 예산을 설정해주세요.")
        return

    # 현재 총 지출 계산
    total_expenses = budget.calculate_total_expenses()
    remaining = current_budget - total_expenses

    if remaining <= 0:
        messagebox.showinfo("예산 부족", "남은 예산이 없습니다. 기부가 불가능합니다.")
        return

    # 기부할 금액 입력 받기
    amount_str = simpledialog.askstring("기부 금액 입력", f"남은 예산은 {remaining:,}원입니다.\n얼마를 기부하시겠습니까?")
    if amount_str is None:
        return  # 취소 누름

    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError

        if amount > remaining:
            messagebox.showerror("금액 오류", "남은 예산보다 큰 금액을 기부할 수 없습니다.")
            return

        confirm = messagebox.askyesno("기부 확인", f"{amount:,}원을 기부하시겠습니까?")
        if confirm:
            log_donation_as_expense(amount, selectedDate)  # ✅ 지출 로그에 기부 내역 저장만 수행
            messagebox.showinfo("감사합니다", f"{amount:,}원이 성공적으로 기부되었습니다!")
            home(frame)  # 화면 갱신

        else:
            messagebox.showinfo("취소", "기부가 취소되었습니다.")

    except ValueError:
        messagebox.showerror("입력 오류", "올바른 숫자(양의 정수)를 입력해주세요.")

def home(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    welcome_label = tk.Label(frame, text="환영합니다! 티끌모아 태산에 오신 걸 환영합니다.", font=("Arial", 16))
    welcome_label.pack(pady=20)

    donate_btn = tk.Button(frame, text="기부하기", font=("Arial", 14), bg="orange", fg="white", padx=20, pady=10,
                           command=lambda: openDonation(frame))
    donate_btn.pack(pady=30)
