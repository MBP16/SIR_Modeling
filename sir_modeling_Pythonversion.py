from decimal import Decimal


# constants and initial values
FLOAT_TYPE = False
DT = 0.01
λ = 0.03
γ = 0.5
END_TIME = 0
T = 0
S = 299
I = 1
R = 0


class SIR_MODELING:
    def __init__(self, DT: float, λ: float, γ: float, S: int, I: int=1, R: int=0, T: float=0, FLOAT_TYPE: bool=False, END_TIME: float=0):
        """
        make a SIR model and draw graphs with matplotlib, and save data to csv file

        :param DT: Time step
        :param λ: Infection rate
        :param γ: Recovery rate
        :param S: Initial susceptible
        :param I: Initial infected
        :param R: Initial recover
        :param T: Initial time
        :param FLOAT_TYPE: Select fixed/floating points True: fixed points/False: floating points
        :param END_TIME: End time
        """
        self.FLOAT_TYPE = FLOAT_TYPE
        self.DT = DT
        self.λ = λ
        self.γ = γ
        self.END_TIME = END_TIME
        self.t = [T]
        self.s = [S]
        self.i = [I]
        self.r = [R]
        self.dSdt_list = ["None"]
        self.dIdt_list = ["None"]
        self.dRdt_list = ["None"]
        if self.FLOAT_TYPE: # if fixed points
            self.decimalize()

    def modeling(self):
        """
        make SIR model with euler`s method
        """
        while True:
            self.t.append(self.t[-1] + self.DT)

            #get next S, I, R values
            self.s_output, self.dsdt_output = self.S_calc(λ=self.λ, s=self.s[-1], i=self.i[-1], DT=self.DT, dSdt_return=True)
            self.i_output, self.didt_output = self.I_calc(λ=self.λ, γ=self.γ, s=self.s[-1], i=self.i[-1], DT=self.DT, dIdt_return=True)
            self.r_output, self.drdt_output = self.R_calc(i=self.i[-1], γ=self.γ, r=self.r[-1], DT=self.DT, dRdt_return=True)

            #append S, I, R, dSdt, dIdt, and dRdt values to the list
            self.s.append(self.s_output)
            self.i.append(self.i_output)
            self.r.append(self.r_output)
            self.dSdt_list.append(self.dsdt_output)
            self.dIdt_list.append(self.didt_output)
            self.dRdt_list.append(self.drdt_output)

            # if end time is reached, break or if everyone is recovered, break
            if self.END_TIME:
                if self.t[-1] >= self.END_TIME:
                    break
            if self.FLOAT_TYPE:
                if self.r[-1] >= self.s[0] + self.i[0] + self.r[0] - Decimal(0.0001):
                    break
            else:
                if self.r[-1] >= self.s[0] + self.i[0] + self.r[0] - 0.0001:
                    break

    def render_graph(self, title: str="SIR Model Graph",
                     S_label: str="Susceptible", I_label: str="Infected", R_label: str="Recovered",
                     x_label: str="Time", y_label: str="Number of people",
                     export_to_image:bool = False, file_name: str="SIR_MODEL_GRAPH.png", file_dpi: int=300):
        """
        render graph with matplotlib.pyplot

        :param title: title of graph
        :param S_label: label of susceptible
        :param I_label: label of infected
        :param R_label: label of recovered
        :param x_label: label of x axis
        :param y_label: label of y axis
        :param export_to_image: if True, export graph to image file
        :param file_name: file name to export graph
        :param file_dpi: dpi of image file
        """
        import matplotlib.pyplot as plt

        plt.figure(dpi=400)
        plt.title(title)
        plt.plot(self.t, self.s, label=S_label)
        plt.plot(self.t, self.i, label=I_label)
        plt.plot(self.t, self.r, label=R_label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        if export_to_image:
            plt.savefig(file_name, dpi=file_dpi)
        plt.legend()
        plt.show()

        del plt

    def save_data(self, file_name: str="data.csv"):
        """
        save datas into csv file

        :param file_name: file name to save data
        """
        import csv

        self.f = open(file_name, 'w', encoding='utf-8', newline='')
        self.wr = csv.writer(self.f)
        self.wr.writerow(['Time', 'S', 'I', 'R', 'dSdt', 'dIdt', 'dRdt'])
        for i in range(len(self.t)):
            self.wr.writerow([self.t[i], self.s[i], self.i[i], self.r[i], self.dSdt_list[i], self.dIdt_list[i], self.dRdt_list[i]])
        self.f.close()

        del csv

    def decimalize(self):
        """
        make all varients to decimal type
        """
        self.t = self.Decimalize(self.t)
        self.s = self.Decimalize(self.s)
        self.i = self.Decimalize(self.i)
        self.r = self.Decimalize(self.r)
        self.DT = self.Decimalize(self.DT)
        self.λ = self.Decimalize(self.λ)
        self.γ = self.Decimalize(self.γ)

    @staticmethod
    def dSdt(λ: float | Decimal, s: float | Decimal, i: float | Decimal) -> float | Decimal:
        """
        calculate dSdt(delta Susceptible / delta time)

        :param λ: Infection rate
        :param s: previous Susceptible
        :param i: previous Infected
        :return: -λ(Infection rate) * s * i
        """
        return -λ * s * i
    @staticmethod
    def dIdt(λ: float | Decimal, γ: float | Decimal, s: float | Decimal, i: float | Decimal) -> float | Decimal:
        """
        calculate dIdt(delta Infected / delta time)

        :param λ: Infection rate
        :param γ: Recovery rate
        :param s: previous Susceptible
        :param i: previous Infected
        :return: -λ(Infection rate) * s * i - γ(Recovery rate) * i
        """
        return λ * s * i - γ * i
    @staticmethod
    def dRdt(γ: float | Decimal, i: float | Decimal) -> float | Decimal:
        """
        calculate dRdt(delta Recovery / delta time)

        :param γ: Recovery rate
        :param i: previous Infected
        :return: γ(Recover rate) * i
        """
        return γ * i

    @classmethod
    def S_calc(cls, λ: float | Decimal, s: float | Decimal, i: float | Decimal, DT: float | Decimal, dSdt_return=False) -> float | Decimal:
        """
        calculate next Susceptible

        :param λ: Infection rate
        :param s: previous Susceptible
        :param i: previous Infected
        :param DT: time step
        :param dSdt_return: If true, it returns current dSdt value
        :return: next Susceptible, current dSdt value(If dSdt_return = True)
        """
        if dSdt_return:
            return s + cls.dSdt(λ, s, i) * DT, cls.dSdt(λ, s, i)
        else:
            return s + cls.dSdt(λ, s, i) * DT
    @classmethod
    def I_calc(cls, λ: float | Decimal, γ: float | Decimal, s: float | Decimal, i: float | Decimal, DT: float | Decimal, dIdt_return=False) -> float | Decimal:
        """
        calculate next Infected

        :param λ: Infection rate
        :param γ: Recovery rate
        :param s: previous Susceptible
        :param i: previous Infected
        :param DT: time step
        :param dIdt_return: If true, it returns current dIdt value
        :return: next Infected, current dIdt value(If dIdt_return = True)
        """
        if dIdt_return:
            return i + cls.dIdt(λ, γ, s, i) * DT, cls.dIdt(λ, γ, s, i)
        else:
            return i + cls.dIdt(λ, γ, s, i) * DT
    @classmethod
    def R_calc(cls, γ: float | Decimal, i: float | Decimal, r: float | Decimal, DT: float | Decimal, dRdt_return=False) -> float | Decimal:
        """
        calculate next Recovery

        :param γ: Recovery rate
        :param i: previous Infected
        :param r: previous Recovery
        :param DT: time step
        :param dRdt_return: If true, it returns current dRdt value
        :return: next Recovery, current dRdt value(If dRdt_return = True)
        """
        if dRdt_return:
            return r + cls.dRdt(γ, i) * DT, cls.dRdt(γ, i)
        else:
            return r + cls.dRdt(γ, i) * DT

    @staticmethod
    def Decimalize(input: list | int | float) -> list | Decimal:
        """
        make input(number, list) into decimal.Decimal object

        :param input: number or list that is going to be Decimal object
        :return: If number, it becomes Decimal object and if list, its contents become all Decimal objects
        """
        if type(input) == list:
            output = input.copy()
            for i in range(len(input)):
                output[i] = Decimal(f'{input[i]}')
            return output
        elif type(input) == int or type(input) == float:
            output = Decimal(f'{input}')
            return output


if __name__ == '__main__':
    model = SIR_MODELING(DT=DT, λ=λ, γ=γ, S=S, I=I, R=R, T=T, FLOAT_TYPE=FLOAT_TYPE, END_TIME=END_TIME)
    model.modeling()
    model.render_graph()
    model.save_data()