import tkinter as tk
from datetime import datetime
import tkinter.messagebox as messagebox
import glob
import re

BUDGET_FILE = "budget.txt"

def load_budget():
    try:
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except:
        return None

def calculate_total_expenses():
    total = 0
    for filepath in glob.glob("가계부_지출_*.txt"):
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "총 수입" in line:
                    continue
                match = re.search(r":\s*([\d,]+)원", line)
                if match:
                    try:
                        amount = int(match.group(1).replace(",", ""))
                        total += amount
                    except:
                        continue
    return total


def expenses(frame, get_date):
    for widget in frame.winfo_children():  # 기존 프레임 위젯 삭제
        widget.destroy()

    def add():
        e_name = name_entry.get()  # 금액 가져오기
        e_amount = amount_entry.get()
        if e_name and e_amount:
            listbox.insert(tk.END, f"{e_name}: {e_amount}원")  # 마지막에 값 추가
            name_entry.delete(0, tk.END)  # 다음 풒목을 입략하기 위해 입력창에 적힌 내용을 처음부터 끝까지 지움
            amount_entry.delete(0, tk.END)
            update_total()

    def update_total():
        total = 0
        for item in listbox.get(0, tk.END):
            amount = int(item.split(":")[1].strip().replace("원", ""))  #:를 기준으로 list 만들고, 글자 원을 지운다
            total += amount
        total_label.config(text=f"총 지출: {total: }원")

    def remove():
        selected_index = listbox.curselection()  # 현재 선택된 항목을 selected_index 저장
        if selected_index:
            listbox.delete(selected_index)
            update_total()

    def save():
        # 1. 저장할 금액 합산 (현재 저장하려는 지출 총액)
        expenses = listbox.get(0, tk.END)
        current_total = 0
        for item in expenses:
            amount = int(item.split(":")[1].strip().replace("원", ""))
            current_total += amount

        budget = load_budget()
        if budget is not None:
            # 기존 파일에서 총 지출 불러오기 (현재 파일에 저장된 이전 총 지출)
            last_total = 0
            file_name = f"가계부_지출_{get_date()}.txt"
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in reversed(lines):
                        if line.startswith("총 지출: "):
                            last_total = int(line.split(":")[1].strip().replace("원", ""))
                            break
            except FileNotFoundError:
                pass

            total_expenses = calculate_total_expenses() - last_total + last_total + current_total
            # 남은 예산 계산
            remaining = budget - total_expenses

            # 예산의 10% 이하 남았고, 이번 지출이 남은 예산보다 클 경우 경고
            if remaining <= budget * 0.1 and current_total > remaining:
                confirm = messagebox.askyesno(
                    "예산 경고",
                    f"예산이 {remaining:,}원 남았습니다.\n"
                    f"{current_total:,}원 지출하려고 합니다.\n"
                    "정말 진행하시겠습니까?"
                )
                if not confirm:
                    return  # 취소하면 저장 중단

        # --- 기존 저장 로직 계속 ---
        selected_date = get_date()
        file_name = f"가계부_지출_{selected_date}.txt"

        # 기존 총 지출 불러오기
        lastTotal = 0
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in reversed(lines):
                    if line.startswith("총 지출: "):
                        lastTotal = int(line.split(":")[1].strip().replace("원", ""))
                        break
        except FileNotFoundError:
            pass

        newTotal = lastTotal + current_total

        with open(file_name, "a", encoding="utf-8") as file:
            for expen in expenses:
                file.write(expen + "\n")
            file.write(f"총 지출: {newTotal}원\n\n")

        savedLabel.config(text="저장되었습니다!")
        savedLabel.after(3000, lambda: savedLabel.config(text=""))

        listbox.delete(0, tk.END)
        total_label.config(text="총 지출: 0원")

    name_label = tk.Label(frame, text="품목")  # Label 위젯 설정
    name_label.grid(row=0, column=1)  # 창에 배치하기
    name_entry = tk.Entry(frame)  # 입력창
    name_entry.grid(row=0, column=2)

    amount_label = tk.Label(frame, text="금액")  # Label 위젯 설정
    amount_label.grid(row=1, column=1)
    amount_entry = tk.Entry(frame)  # 입력창
    amount_entry.grid(row=1, column=2)

    add_btn = tk.Button(frame, text="추가", command=add)  # 버튼
    add_btn.grid(row=2, column=1)
    remove_btn = tk.Button(frame, text="삭제", command=remove)
    remove_btn.grid(row=2, column=2)
    save_btn = tk.Button(frame, text="저장", command=save)
    save_btn.grid(row=2, column=3)

    savedLabel = tk.Label(frame, text="")  # 저장 완료 메시지
    savedLabel.grid(row=3, column=1)

    listbox = tk.Listbox(frame, selectmode=tk.SINGLE)  # 하나의 아이템씩
    listbox.grid(row=4, column=2)

    total_label = tk.Label(frame, text="총 지출: 0원")
    total_label.grid(row=5, column=2)