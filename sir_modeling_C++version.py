from decimal import Decimal
import ctypes


#c++_file_import
import modeling

# constants and initial values
DT = 0.0001
λ = 0.03
γ = 0.5
END_TIME = 0
T = 0
S = 299
I = 1
R = 0


class SIR_MODELING:
    def __init__(self, DT: float, λ: float, γ: float, S: int, I: int=1, R: int=0, T: float=0, END_TIME: float=0):
        """
        make a SIR model and draw graphs with matplotlib, and save data to csv file

        :param DT: Time step
        :param λ: Infection rate
        :param γ: Recovery rate
        :param S: Initial susceptible
        :param I: Initial infected
        :param R: Initial recover
        :param T: Initial time
        :param END_TIME: End time
        """
        self.DT = DT
        self.λ = λ
        self.γ = γ
        self.END_TIME = END_TIME
        self.T = T
        self.S = S
        self.I = I
        self.R = R

    def modeling(self):
        """
        make SIR model with euler`s method
        """
        result = modeling.modeling(self.DT, self.λ, self.γ, self.T, self.S, self.I, self.R, self.END_TIME)
        self.t = result[0]
        self.s = result[1]
        self.i = result[2]
        self.r = result[3]
        self.dSdt_list = result[4]
        self.dIdt_list = result[5]
        self.dRdt_list = result[6]

    def render_graph(self):
        """
        render graph with matplotlib.pyplot
        """
        import matplotlib.pyplot as plt

        plt.figure(dpi=400)
        plt.title("SIR Model Graph")
        plt.plot(self.t, self.s, label='Susceptible')
        plt.plot(self.t, self.i, label='Infected')
        plt.plot(self.t, self.r, label='Recover')
        plt.legend()
        plt.show()

        del plt

    def save_data(self):
        """
        save datas into csv file named "data.csv"
        """
        import csv

        self.f = open('data.csv', 'w', encoding='utf-8', newline='')
        self.wr = csv.writer(self.f)
        self.wr.writerow(['Time', 'S', 'I', 'R', 'dSdt', 'dIdt', 'dRdt'])
        for i in range(len(self.t)):
            self.wr.writerow([self.t[i], self.s[i], self.i[i], self.r[i], self.dSdt_list[i], self.dIdt_list[i], self.dRdt_list[i]])
        self.f.close()

        del csv


if __name__ == '__main__':
    model = SIR_MODELING(DT=DT, λ=λ, γ=γ, S=S, I=I, R=R, T=T, END_TIME=END_TIME)
    model.modeling()
    model.render_graph()
    model.save_data()