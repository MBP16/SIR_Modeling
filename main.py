from decimal import Decimal


# 상수

dt = Decimal('0.1') #시간 변화량
λ = Decimal('0.03') #감염률
γ = Decimal('0.5') #회복율
end_Time = 20 # 종료 시간(0이면 제한 없음)

# 요소들의 리스트(안에 있는건 초기값)

t = [Decimal('0')] #시간
S = [Decimal('299')] #Susceptible 감염 가능자
I = [Decimal('1')] #Infected 감염자
R = [Decimal('0')] #Recover 회복자

# 변화량 리스트

dSdt_list = ["None"]
dIdt_list = ["None"]
dRdt_list = ["None"]

# 변화량 계산 함수들

def dSdt(S, I):
    dSdt_list.append(-λ * S * I)
    return -λ * S * I
def dIdt(S, I):
    dIdt_list.append(λ * S * I - γ * I)
    return λ * S * I - γ * I
def dRdt(I):
    dRdt_list.append(γ * I)
    return γ * I

# S, I, R값 계산 함수들

def S_calc(S, I):
    return S + dSdt(S, I) * dt
def I_calc(S, I):
    return I + dIdt(S, I) * dt
def R_calc(I, R):
    return R + dRdt(I) * dt

# 파일 저장 함수
def save():
    import csv
    f = open('data.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(['시간', 'S', 'I', 'R', 'dSdt', 'dIdt', 'dRdt'])
    for i in range(len(t)):
        wr.writerow([t[i], S[i], I[i], R[i], dSdt_list[i], dIdt_list[i], dRdt_list[i]])
    del csv

# 그래프 그리기 함수
def plot():
    import matplotlib.pyplot as plt
    plt.figure(dpi=400)
    plt.title("SIR Model Graph")
    plt.plot(t, S, label='Susceptible')
    plt.plot(t, I, label='Infected')
    plt.plot(t, R, label='Recover')
    plt.legend()
    plt.show()
    del plt


if __name__ == '__main__':
    #S, I, R값 수치적분
    while True:
        t.append(t[-1] + dt) #시간 증가
        s = S_calc(S=S[-1], I=I[-1]) #S 계산
        i = I_calc(S=S[-1], I=I[-1]) #I 계산
        r = R_calc(I=I[-1], R=R[-1]) #R 계산
        S.append(s) #S 추가
        I.append(i) #I 추가
        R.append(r) #R 추가
        if end_Time:
            if t[-1] == end_Time: #끝나는 시간이 정해져 있다면
                break #종료
        elif R[-1] >= S[0] + I[0] + R[0] - Decimal(0.00001): #모두가 회복되면(총 인원으로 해야하지만 종료 안됨)
            break #종료
    #시간, S, I, R, dSdt, dIdt, dRdt 값 CSV파일로 저장
    save()
    #시간, S, I, R 값으로 그래프 그리기
    plot()