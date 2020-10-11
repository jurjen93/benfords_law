import pandas as pd
import matplotlib.pyplot as plt
from math import log10, nan
from matplotlib import style
from scipy.spatial import distance


def BL_analysis(df, fields):
    def BL(n):
        return log10(1 + 1 / n)

    BL_frequencies = {i: BL(i) for i in range(1, 10)}

    def ED_BL(frequencies):
        return round(distance.euclidean(list(BL_frequencies.values()), frequencies) / distance.euclidean(
            list(BL_frequencies.values()), [0] * 8 + [1]), 3)

    def above_one(inp):
        try:
            inp = float(inp)
            if inp == 0:
                return nan
            while inp < 1:
                inp *= 10
            return inp
        except TypeError:
            return nan

    for field in fields:
        df_frequencies = (df[field].apply(lambda x: above_one(x)).dropna().astype(str).str[
                              0].value_counts().sort_index() / len(df)).to_dict()

        style.use('ggplot')
        plt.scatter(BL_frequencies.keys(), BL_frequencies.values(), marker='+', color='black')
        plt.scatter([int(i) for i in df_frequencies.keys()], df_frequencies.values(), marker='^')
        plt.legend(["Benford's law", "First significant digit frequency data"])
        plt.title(f"{field.title().replace('_', ' ')} has ED:\n{ED_BL(list(df_frequencies.values()))}", size=16)
        plt.xticks(size=16)
        plt.yticks(plt.yticks()[0], [int(round(p, 2) * 100) for p in plt.yticks()[0]], size=16)
        plt.xlabel('First significant digit', size=16)
        plt.ylabel('Frequency (%)', size=16)
        plt.show()