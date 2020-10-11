import matplotlib.pyplot as plt
from math import log10, nan, sqrt
from matplotlib import style
from scipy.spatial import distance

"""This is a very simple script to test Benford's law 
on your data where we use Poisson error bars and calculate 
the normalized Euclidean Distance function.
The data has to be converted to a pandas dataframe."""

def bl_analysis(df, fields):
    def bl(n):
        return log10(1 + 1 / n)

    BL_frequencies = {i: bl(i) for i in range(1, 10)}

    def ed_bl(frequencies):
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
        error_bar = 1/sqrt(len(df[field].dropna()))
        print(error_bar)
        df_frequencies = {int(i):j for i,j in (df[field].apply(lambda x: above_one(x)).dropna().astype(str).str[
                              0].value_counts().sort_index() / len(df)).to_dict().items()}
        style.use('ggplot')
        plt.scatter(BL_frequencies.keys(), BL_frequencies.values(), marker='s', color='black')
        plt.scatter(df_frequencies.keys(), df_frequencies.values(), marker='o')
        plt.errorbar(df_frequencies.keys(), df_frequencies.values(), yerr=error_bar, fmt='o')
        plt.legend(["Benford's law", "First significant digit frequency data"])
        plt.title(f"{field.title().replace('_', ' ')} has ED:\n{ed_bl(list(df_frequencies.values()))}", size=16)
        plt.xticks(size=16)
        plt.yticks(plt.yticks()[0], [int(round(p, 2) * 100) for p in plt.yticks()[0]], size=16)
        plt.xlabel('First significant digit', size=16)
        plt.ylabel('Frequency (%)', size=16)
        plt.show()

if  __name__=="__main__":
    #example:
    from pandas import DataFrame
    from random import uniform
    random_dict = {i: uniform(0, 10) for i in range(1000)}
    df = DataFrame([random_dict]).transpose().rename(columns={0: 'example_field'})
    bl_analysis(df, ['example_field'])