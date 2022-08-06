#include "Python.h"
#include "iostream"


using namespace std;

extern "C"{
    float dSdt(float λ, float s, float i) {
        return -λ * s * i;
    }
    float dIdt(float λ, float γ, float s, float i) {
        return λ * s * i - γ * i;
    }
    float dRdt(float γ, float i) {
        return γ * i;
    }

    float S_calc(float λ, float s, float i, float DT) {
        return s + dSdt(λ, s, i) * DT;
    }
    float I_calc(float λ, float γ, float s, float i, float DT) {
        return i + dIdt(λ, γ, s, i) * DT;
    }
    float R_calc(float γ, float i, float r, float DT) {
        return r + dRdt(γ, i) * DT;
    }

    PyObject* modeling(const float DT, const float λ, const float γ, const float T, const float S, const float I, const float R, const float END_TIME) {
        PyObject *t_list, *s_list, *i_list, *r_list, *dSdt_list, *dIdt_list, *dRdt_list, *result;
        cout << "1" << endl;
        t_list = PyList_New(10);
        cout << "0" << endl;
        s_list = PyList_New(0); i_list = PyList_New(0); r_list = PyList_New(0);
        cout << "2" << endl;
        dSdt_list = PyList_New(0); dIdt_list = PyList_New(0); dRdt_list = PyList_New(0);
        cout << "3" << endl;
        PyList_Append(t_list, Py_BuildValue("f", T)); PyList_Append(s_list, Py_BuildValue("f", S)); PyList_Append(i_list, Py_BuildValue("f", I)); PyList_Append(r_list, Py_BuildValue("f", R));
        PyList_Append(dSdt_list, Py_BuildValue("s", "N one")); PyList_Append(dIdt_list, Py_BuildValue("s", "None")); PyList_Append(dRdt_list, Py_BuildValue("s", "None"));
        while (true) {
            PyList_Append(t_list, PyFloat_FromDouble(PyFloat_AsDouble(PyList_GetItem(t_list, PyList_Size(t_list) - 1)) + DT));
            float s = PyFloat_AsDouble(PyList_GetItem(s_list, PyList_Size(s_list) - 1));
            float i = PyFloat_AsDouble(PyList_GetItem(i_list, PyList_Size(i_list) - 1));
            float r = PyFloat_AsDouble(PyList_GetItem(r_list, PyList_Size(r_list) - 1));
            PyList_Append(dSdt_list, Py_BuildValue("f", dSdt(λ, s, i)));
            PyList_Append(dIdt_list, Py_BuildValue("f", dIdt(λ, γ, s, i)));
            PyList_Append(dRdt_list, Py_BuildValue("f", dRdt(γ, i)));
            PyList_Append(s_list, Py_BuildValue("f", S_calc(λ, s, i, DT)));
            PyList_Append(i_list, Py_BuildValue("f", I_calc(λ, γ, s, i, DT)));
            PyList_Append(r_list, Py_BuildValue("f", R_calc(γ, i, r, DT)));
            if (END_TIME != 0) {
                if (PyFloat_AsDouble(PyList_GetItem(t_list, PyList_Size(t_list) - 1)) >= END_TIME) {
                    break;
                }
            }
            if (PyFloat_AsDouble(PyList_GetItem(r_list, PyList_Size(r_list) - 1)) >=
                    PyFloat_AsDouble(PyList_GetItem(s_list, 0)) + PyFloat_AsDouble(PyList_GetItem(i_list, 0)) +
                            PyFloat_AsDouble(PyList_GetItem(r_list, 0)) - 1) {
                break;
            }
        }
        result = PyList_New(0);
        PyList_Append(result, t_list); PyList_Append(result, s_list); PyList_Append(result, i_list); PyList_Append(result, r_list);
        PyList_Append(result, dSdt_list); PyList_Append(result, dIdt_list); PyList_Append(result, dRdt_list);
        return result;
    }
}

int main() {
    cout << modeling(0.1, 0.03, 0.5, 0, 299, 1, 0, 20) << endl;
    return 0;
}