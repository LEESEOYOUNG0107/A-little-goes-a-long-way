import os
import tkinter as tk
from tkinter.ttk import LabelFrame
from tkcalendar import Calendar
from expenses import expenses
from deposit import deposit

def calendar(frame):
    for widget in frame.winfo_children(): # 기존 프레임 위젯 초기화
        widget.destroy()

    canvas = tk.Canvas(frame, width=900, height=600)
    canvas.grid(row=0, column=0, columnspan=5, sticky="nsew")

    #스크롤바 생성 및 캔버스와 연결
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=4, sticky="ens")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 캔버스와 내부 프레임 생성
    scrLable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrLable_frame, anchor="nw")

    #캘린더, 지출, 수입 프레임을 캔버스 프레임에 추가
    calFrame = LabelFrame(scrLable_frame, text="캘린더")
    calFrame.grid(row=0, column=0, padx=20)

    cal = Calendar(calFrame, selectmode='day', date_pattern="yyyy-mm-dd")
    cal.grid(row=0, column=0)

    # 선택된 날짜를 추적
    selectedDate = cal.get_date()  # 초기 날짜 설정

    #날짜 선택 이벤트
    def updateSelectedDate(event):
        nonlocal selectedDate
        selectedDate = cal.get_date()  # 선택된 날짜 업데이트
        print(f"Selected date updated to: {selectedDate}")

    cal.bind("<<CalendarSelected>>", updateSelectedDate)



    expensesFrame = LabelFrame(scrLable_frame, text="지출") #지출 영역 생성
    expensesFrame.grid(row=0, column=2, padx=30)
    expenses(expensesFrame, lambda: selectedDate)

    depositFrame = LabelFrame(scrLable_frame, text="수입")
    depositFrame.grid(row=0, column=3, pady=30)
    deposit(depositFrame, lambda: selectedDate)

    dataFrame = LabelFrame(scrLable_frame, text="선택된 날짜의 수입/지출 내역")
    dataFrame.grid(row=1, column=0, columnspan=5, pady=30, sticky="nsew")

    def loadData(filepath): #파일에서 데이터를 읽어 리스트로 반환
        data = []
        if os.path.exists(filepath):
            with open(filepath, encoding="utf-8") as file:
                for line in file:
                    if line.strip():
                        data.append(line)
        else:
            print(f"File not found: {filepath}")  # 파일 없을 경우 디버그 메시지 출력
        return data


    #선택된 날짜의 데이터를 표시하는 함수
    def displayData():
        nonlocal selectedDate
        #사용자가 캘린더에서 날짜를 클릭할 때 호출. 선택된 날짜에 해당하는 내역을 dataFrame에 로드하여 표시.
        selectedDate = cal.get_date() #캘린더에서 현재 선택된 날짜 가져옴
        print(f"Selected date: {selectedDate}")

        expenses_file = f"가계부_지출_{selectedDate}.txt"
        deposit_file = f"가계부_수입_{selectedDate}.txt"

        # 지출 및 수입 파일에서 데이터 읽어오기
        expenses_data = loadData(expenses_file)
        deposit_data = loadData(deposit_file)

        for widget in dataFrame.winfo_children():
           widget.destroy()

        tk.Label(dataFrame, text="지출 내역: ").grid(row=0, column=0, padx=10)
        if expenses_data: #지출 데이터가 없는 경우
            for row_index, expense in enumerate(expenses_data, start=1):
                tk.Label(dataFrame, text=expense, anchor="w").grid(row=row_index, column=0, sticky="w", padx=5)
        else:
            tk.Label(dataFrame, text="지출 내역이 없습니다.", fg="gray").grid(row=2, column=0, sticky="w", padx=5)

        # 수입 내역 섹션
        row_offset = len(expenses_data) + 1  # 지출 섹션의 마지막 행 직후 (행 오프셋 설정)
        tk.Label(dataFrame, text="수입 내역:").grid(row=row_offset, column=0, sticky="w", padx=5, pady=5)

        if deposit_data: #수입 데이터가 없는 경우
            for row_index, deposit in enumerate(deposit_data, start=row_offset + 1):
                tk.Label(dataFrame, text=deposit, anchor="w").grid(row=row_index, column=0, sticky="w", padx=5)

        else:
            tk.Label(dataFrame, text="수입 내역이 없습니다.", fg="gray").grid(row=row_offset + 1, column=0, sticky="w", padx=5)

    # 캘린더 클릭 이벤트에 display_data 함수 연결
    cal.bind("<<CalendarSelected>>", lambda event: displayData())

    displayData()  #초기 내용 표시

    def scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrLable_frame.bind("<Configure>", scrollregion)