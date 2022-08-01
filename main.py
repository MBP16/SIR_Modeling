from decimal import Decimal
from typing import Union


# 고정소수점/부동소수점 결정 변수

FLOAT_TYPE = False # True/False 값에 따라 고정소수점/부동소수점 선택

# 상수

DT = 0.1 #시간 변화량
λ = 0.03 #감염률
γ = 0.5 #회복율
END_TIME = 20 # 종료 시간(0이면 제한 없음)

# 요소들의 리스트(안에 있는건 초기값)

t = [0] #시간
s = [299] #Susceptible 감염 가능자
i = [1] #Infected 감염자
r = [0] #Recover 회복자

# 변화량 리스트

dSdt_list = ["None"]
dIdt_list = ["None"]
dRdt_list = ["None"]

# 변화량 계산 함수들

def dSdt(S: Union[float, Decimal], I: Union[float, Decimal]) -> Union[float, Decimal]:
    dSdt_list.append(-λ * S * I)
    return -λ * S * I
def dIdt(S: Union[float, Decimal], I: Union[float, Decimal]) -> Union[float, Decimal]:
    dIdt_list.append(λ * S * I - γ * I)
    return λ * S * I - γ * I
def dRdt(I: Union[float, Decimal]) -> Union[float, Decimal]:
    dRdt_list.append(γ * I)
    return γ * I

# S, I, R값 계산 함수들

def S_calc(S: Union[float, Decimal], I: Union[float, Decimal]) -> Union[float, Decimal]:
    return S + dSdt(S, I) * DT
def I_calc(S: Union[float, Decimal], I: Union[float, Decimal]) -> Union[float, Decimal]:
    return I + dIdt(S, I) * DT
def R_calc(I: Union[float, Decimal], R: Union[float, Decimal]) -> Union[float, Decimal]:
    return R + dRdt(I) * DT

#변수들 고정소수화 하는 함수

def Decimalize(input: Union[list, int, float]) -> Union[list, Decimal]:
    if type(input) == list:
        output = input.copy()
        for i in range(len(input)):
            output[i] = Decimal(f'{input[i]}')
        return output
    elif type(input) == int or type(input) == float:
        output = Decimal(f'{input}')
        return output

# 파일 저장 함수
def save():
    import csv
    f = open('data.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['시간', 'S', 'I', 'R', 'dSdt', 'dIdt', 'dRdt'])
    for i in range(len(t)):
        wr.writerow([t[i], s[i], i[i], r[i], dSdt_list[i], dIdt_list[i], dRdt_list[i]])
    del csv

# 그래프 그리기 함수
def plot():
    import matplotlib.pyplot as plt
    plt.figure(dpi=400)
    plt.title("SIR Model Graph")
    plt.plot(t, s, label='Susceptible')
    plt.plot(t, i, label='Infected')
    plt.plot(t, r, label='Recover')
    plt.legend()
    plt.show()
    del plt


if __name__ == '__main__':
    if FLOAT_TYPE: #고정소수점을 선택한 경우
        t = Decimalize(t)
        s = Decimalize(s)
        i = Decimalize(i)
        r = Decimalize(r)
        DT = Decimalize(DT)
        λ = Decimalize(λ)
        γ = Decimalize(γ)
    #S, I, R값 수치적분
    while True:
        t.append(t[-1] + DT) #시간 증가
        s_output = S_calc(S=s[-1], I=i[-1]) #S 계산
        i_output = I_calc(S=s[-1], I=i[-1]) #I 계산
        r_output = R_calc(I=i[-1], R=r[-1]) #R 계산
        s.append(s_output) #S 추가
        i.append(i_output) #I 추가
        r.append(r_output) #R 추가
        if END_TIME:
            if t[-1] >= END_TIME: #끝나는 시간이 정해져 있다면
                break #종료
        if FLOAT_TYPE: #고정소수점을 선택한 경우
            if r[-1] >= s[0] + i[0] + r[0] - Decimal(0.00001): #모두가 회복되면(총 인원으로 해야하지만 종료 안됨)
                break #종료
        else: #부동소수점을 선택한 경우
            if r[-1] >= s[0] + i[0] + r[0] - 0.00001: #모두가 회복되면(총 인원으로 해야하지만 종료 안됨)
                break #종료
    #시간, S, I, R, dSdt, dIdt, dRdt 값 CSV파일로 저장
    save()
    #시간, S, I, R 값으로 그래프 그리기
    plot()