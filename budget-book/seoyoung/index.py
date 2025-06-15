import tkinter as tk
import expenses, cal, deposit, budget, home
from datetime import datetime
from PIL import Image, ImageTk

def get_date():
    return datetime.now().strftime("%Y-%m-%d")

def openCal():
    cal.calendar(main_frame)

def openBudget():
    budget.budget(main_frame)

def openHome():
    home.home(main_frame)

def openHome_img():
    home.homeImg(main_frame)

w = tk.Tk()
w.title("티끌모아 태산")
w.geometry("900x600")
main_frame = tk.Frame(w)
main_frame.pack(fill="both", expand=True)

menubar = tk.Menu(w)

menubar.add_command(label="홈", command=openHome_img)
menubar.add_command(label="캘린더", command=openCal)
menubar.add_command(label="통계")
menubar.add_command(label="예산 관리", command=openBudget)
menubar.add_command(label="기부", command=openHome)

w.config(menu=menubar)
openHome_img()
w.mainloop()
