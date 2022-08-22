#c++_file_import
import modeling

# constants and initial values
DT = 0.01
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

    def save_data(self, file_name: str="datacpp.csv"):
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


if __name__ == '__main__':
    model = SIR_MODELING(DT=DT, λ=λ, γ=γ, S=S, I=I, R=R, T=T, END_TIME=END_TIME)
    model.modeling()
    model.render_graph()
    model.save_data()