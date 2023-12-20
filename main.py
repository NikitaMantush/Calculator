from decimal import Decimal
from tkinter import *
from tkinter import messagebox, ttk, Tk

def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

def Is_num(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def CalcOutputFormat(input_num):
    num_str = str(input_num)
    int_part_str = num_str
    fract_part_str = ""
    for i in range(len(num_str)):
        if num_str[i] == '.':
            int_part_str = num_str[:i]
            fract_part_str = num_str[i:i + 7].rstrip('0')
            if fract_part_str == ".":
                fract_part_str = ""
            break
    int_part_str = int_part_str[::-1]
    int_parts = [(int_part_str[i:i + 3]) for i in range(0, len(int_part_str), 3)]
    int_parts.reverse()
    for i in range(len(int_parts)):
        int_parts[i] = int_parts[i][::-1]
    result = ' '.join(int_parts) + fract_part_str
    return result

def FromStrToNumConvert(input_str):
    int_part_str = input_str
    negative = False
    fract_part_str = ""
    for i in range(len(input_str)):
        if input_str[i] == '.':
            int_part_str = input_str[:i]
            if int_part_str[0] == '-':
                negative = True
                int_part_str = int_part_str[1:]
            fract_part_str = input_str[i:len(input_str)].rstrip('0')
            if fract_part_str == ".":
                fract_part_str = ""
            break
    new_int_part_str = ""
    j = 0
    for i in range(len(int_part_str) - 1, -1, -1):
        j += 1
        if j % 4 == 0 and int_part_str[i] == ' ':
            continue
        new_int_part_str = int_part_str[i] + new_int_part_str
    result = new_int_part_str + fract_part_str
    if negative:
        result = '-' + result
    return result


def sum_function(FirstNum, SecondNum):
    Sum = Decimal(FirstNum + SecondNum)
    return Sum

def Diff_Function(FirstNum, SecondNum):
    Diff = Decimal(FirstNum - SecondNum)
    return Diff

def Mult_Function(FirstNum, SecondNum):
    Mult = Decimal(FirstNum * SecondNum)
    return Mult

def Div_Function(FirstNum, SecondNum):
    if SecondNum == 0:
        return "error"
    Div = round(FirstNum / SecondNum, 11)
    Div *= 10000000000
    Div = Decimal(int(Div + Decimal(0.5 if Div > 0 else -0.5)))
    Div /= 10000000000
    Div = Decimal(Div)
    return Div

def Math_Round(num):
    return str(int(num + (Decimal(0.5) if num > Decimal(0.0) else Decimal(-0.5))))

def Book_Round(num):
    return str(round(num))

def Trunct_round(num):
    return str(int(num))

def calculation_button_clicked():
    calculator_output.delete(1.0, "end")


    def get_and_convert_input(label):
        num_input = label.get().replace(',', '.')
        num_input = FromStrToNumConvert(num_input)
        return num_input

    def display_error(message):
        messagebox.showerror("Калькулятор", message)

    FirstNumInput = get_and_convert_input(FirstNum_Label)
    if not Is_num(FirstNumInput) or 'e' in FirstNumInput:
        display_error("Первое число введено некорректно")
        return

    FirstNum = Decimal(FirstNumInput)

    SecondNumInput = get_and_convert_input(SecondNum_Label)
    if not Is_num(SecondNumInput) or 'e' in SecondNumInput:
        display_error("Второе число введено некорректно")
        return

    SecondNum = Decimal(SecondNumInput)

    ThirdNumInput = get_and_convert_input(ThirdNum_Label)
    if not Is_num(ThirdNumInput) or 'e' in ThirdNumInput:
        display_error("Третье число введено некорректно")
        return

    ThirdNum = Decimal(ThirdNumInput)

    FourthNumInput = get_and_convert_input(FourthNum_Label)
    if not Is_num(FourthNumInput) or 'e' in FourthNumInput:
        display_error("Во четвёртом числе введена буква \"e\"")
        return

    FourthNum = Decimal(FourthNumInput)

    Result_Num = calculation_function(FirstNum, SecondNum, ThirdNum, FourthNum,
                                      FirstOperation_Info.get(), SecondOperation_Info.get(),
                                      ThirdOperation_Info.get())

    if isinstance(Result_Num, str):
        calculator_output.insert(INSERT, Result_Num + "\n")
    else:
        Result_Num_str = CalcOutputFormat(Result_Num)
        nums_str = [str(num) for num in [FirstNum, SecondNum, ThirdNum, FourthNum]]
        nums_str = [f"({num})" if Decimal(num) < 0 else str(num) for num in nums_str]
        expression = f"{nums_str[0]} {FirstOperation_Info.get()} ( {nums_str[1]} {SecondOperation_Info.get()} " \
                     f"{nums_str[2]} ) {ThirdOperation_Info.get()} {nums_str[3]}"
        calculator_output.insert(INSERT, f"{expression} = {Result_Num_str}\n")

        round_type = RoundType_Info.get()
        if round_type == "Математическое":
            calculator_output.insert(INSERT, f"Результат после математического округления: "
                                             f"{CalcOutputFormat(Math_Round(Result_Num))}\n")
        elif round_type == "Бухгалтерское":
            calculator_output.insert(INSERT, f"Результат после бухгалтерского округления: "
                                             f"{CalcOutputFormat(Book_Round(Result_Num))}\n")
        else:
            calculator_output.insert(INSERT, f"Результат после усечения {CalcOutputFormat(Trunct_round(Result_Num))}\n")


def calculation_function(A, B, C, D, OP1, OP2, OP3):
    if OP2 == "+":
        BC = sum_function(B, C)
    elif OP2 == "-":
        BC = Diff_Function(B, C)
    elif OP2 == "*":
        BC = Mult_Function(B, C)
    else:
        BC_str = Div_Function(B, C)
        if BC_str == "error":
            return "Произошла ошибка, деление на ноль невозможно"
        BC = Decimal(BC_str)
    if OP3 == "*" or OP3 == "/":
        if OP3 == "+":
            BCD = sum_function(BC, D)
        elif OP3 == "-":
            BCD = Diff_Function(BC, D)
        elif OP3 == "*":
            BCD = Mult_Function(BC, D)
        else:
            BCD_str = Div_Function(BC, D)
            if BCD_str == "error":
                return "Произошла ошибка, деление на ноль невозможно"
            BCD = Decimal(BCD_str)
        if OP1 == "+":
            A_BCD = sum_function(A, BCD)
        elif OP1 == "-":
            A_BCD = Diff_Function(A, BCD)
        elif OP1 == "*":
            A_BCD = Mult_Function(A, BCD)
        else:
            A_BCD_str = Div_Function(A, BCD)
            if A_BCD_str == "error":
                return "Произошла ошибка, деление на ноль невозможно"
            A_BCD = Decimal(A_BCD_str)
        return A_BCD
    else:
        if OP1 == "+":
            ABC = sum_function(A, BC)
        elif OP1 == "-":
            ABC = Diff_Function(A, BC)
        elif OP1 == "*":
            ABC = Mult_Function(A, BC)
        else:
            ABC_str = Div_Function(A, BC)
            if ABC_str == "error":
                return "Произошла ошибка, деление на ноль невозможно"
            ABC = Decimal(ABC_str)
        if OP3 == "+":
            ABC_D = sum_function(ABC, D)
        elif OP3 == "-":
            ABC_D = Diff_Function(ABC, D)
        elif OP3 == "*":
            ABC_D = Mult_Function(ABC, D)
        else:
            ABC_D_str = Div_Function(ABC, D)
            if ABC_D_str == "error":
                return "Произошла ошибка, деление на ноль невозможно"
            ABC_D = Decimal(ABC_D_str)
        return ABC_D


window_calculator: Tk = Tk()
window_calculator.withdraw()

FirstNum_Label = StringVar(window_calculator, value="0.0")
SecondNum_Label = StringVar(window_calculator, value="0.0")
ThirdNum_Label = StringVar(window_calculator, value="0.0")
FourthNum_Label = StringVar(window_calculator, value="0.0")

FirstOperation_Info = StringVar()
SecondOperation_Info = StringVar()
ThirdOperation_Info = StringVar()

RoundType_Info = StringVar()
calculator_output = Text(window_calculator, height=4.0, width=55, bd=5, font=("Times New Roman", 16), wrap=NONE)
calculator_output.place(relx=0.5, rely=0.86, anchor="c")
window_calculator.deiconify()
window_calculator.geometry('1500x800')
window_calculator.bind_all("<Key>", _onKeyRelease, "+")

window_calculator.resizable(width=False, height=False)
window_calculator["bg"] = "#7CCD7C"
window_calculator.title("Калькулятор")

student_info_label = Label(window_calculator, text="Мантуш Никита Сергеевич, 3 курс, 12 группа",
                           font=("Times New Roman", 14), bg="#7CCD7C")
student_info_label.place(relx=0, rely=0.015, anchor="w")

first_num_label = Label(window_calculator, text="Первое число", font=("Arial", 18), bg="#7CCD7C")
first_num_label.place(relx=0.5, rely=0.075, anchor="center")

first_num_txt = Entry(window_calculator, width=35, bd=1, font=("Times New Roman", 16), textvariable=FirstNum_Label)
first_num_txt.place(relx=0.5, rely=0.125, anchor="center")

first_operation_label = Label(window_calculator, text="Первая операция", font=("Arial", 18), bg="#7CCD7C")
first_operation_label.place(relx=0.2, rely=0.17, anchor="c")

first_operation_label = ttk.Combobox(window_calculator, values=["+", "-", "*", "/"], font=("Times New Roman", 16),
                                     width=2,
                                     state='readonly', textvariable=FirstOperation_Info)
first_operation_label.current(0)
first_operation_label.place(relx=0.29, rely=0.17, anchor="c")

second_num_label = Label(window_calculator, text="Второе число", font=("Arial", 18), bg="#7CCD7C")
second_num_label.place(relx=0.5, rely=0.215, anchor="c")

second_num_txt = Entry(window_calculator, width=35, bd=1, font=("Times New Roman", 16), textvariable=SecondNum_Label)
second_num_txt.setvar("0")
second_num_txt.place(relx=0.5, rely=0.265, anchor="center")

second_operation_label = Label(window_calculator, text="Вторая операция", font=("Arial Bold", 18), bg="#7CCD7C")
second_operation_label.place(relx=0.2, rely=0.305, anchor="c")

second_operation_label = ttk.Combobox(window_calculator, values=["+", "-", "*", "/"], font=("Times New Roman", 16),
                                      width=2,
                                      state='readonly', textvariable=SecondOperation_Info)
second_operation_label.current(0)
second_operation_label.place(relx=0.29, rely=0.305, anchor="c")

third_num_label = Label(window_calculator, text="Третье число", font=("Arial", 18), bg="#7CCD7C")
third_num_label.place(relx=0.5, rely=0.355, anchor="c")

third_num_txt = Entry(window_calculator, width=35, bd=1, font=("Times New Roman", 16), textvariable=ThirdNum_Label)
third_num_txt.place(relx=0.5, rely=0.395, anchor="c")

third_operation_label = Label(window_calculator, text="Третья операция", font=("Arial Bold", 18), bg="#7CCD7C")
third_operation_label.place(relx=0.2, rely=0.445, anchor="c")

third_operation_label = ttk.Combobox(window_calculator, values=["+", "-", "*", "/"], font=("Times New Roman", 16),
                                     width=2,
                                     state='readonly', textvariable=ThirdOperation_Info)
third_operation_label.current(0)
third_operation_label.place(relx=0.29, rely=0.445, anchor="c")

fourth_num_label = Label(window_calculator, text="Четвёртое число", font=("Arial", 18), bg="#7CCD7C")
fourth_num_label.place(relx=0.5, rely=0.495, anchor="c")

fourth_num_label = Entry(window_calculator, width=35, bd=1, font=("Times New Roman", 16), textvariable=FourthNum_Label)
fourth_num_label.place(relx=0.5, rely=0.535, anchor="c")

rounding_type_label = Label(window_calculator, text="Тип округления", font=("Arial", 18), bg="#7CCD7C")
rounding_type_label.place(relx=0.18, rely=0.72, anchor="c")

rounding_type = ttk.Combobox(window_calculator, values=["Математическое", "Бухгалтерское", "Усечение"],
                             font=("Times New Roman", 16), width=20, state='readonly', textvariable=RoundType_Info)
rounding_type.current(0)
rounding_type.place(relx=0.18, rely=0.76, anchor="c")

calculation_button = Button(window_calculator, text="Вычислить", font=("Arial", 18), bd=5,
                            background="#00FF00", command=calculation_button_clicked)
calculation_button.place(relx=0.5, rely=0.65, anchor="c")

window_calculator.mainloop()