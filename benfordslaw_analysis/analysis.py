import matplotlib.pyplot as plt
from math import log10, sqrt, log
from matplotlib import style
from scipy.spatial import distance
from collections import Counter
from pandas import Series


class BenfordsLaw:
    """
    BenfordsLaw is a class to obtain benford properties:
    ----------
    first_benford_frequencies -> return the frequencies of benford's law for first significant digits
    second_benford_frequencies -> return the frequencies of benford's law for second significant digits
    third_benford_frequencies -> return the frequencies of benford's law for third significant digits
    ----------
    """

    @staticmethod
    def benford_formula(n: int):
        return log10(1 + 1 / n)

    @property
    def first_benford_frequencies(self):
        return {i: self.benford_formula(i) for i in range(1, 10)}

    @property
    def second_benford_frequencies(self):  # should be improved with formula
        return {0: 0.12, 1: 0.114, 2: 0.109, 3: 0.104, 4: 0.100, 5: 0.097, 6: 0.093, 7: 0.090, 8: 0.088, 9: 0.085}

    @property
    def third_benford_frequencies(self):  # should be improved with formula
        return {0: 0.102, 1: 0.101, 2: 0.101, 3: 0.101, 4: 0.100, 5: 0.100, 6: 0.099, 7: 0.099, 8: 0.099, 9: 0.098}


class Analysis(BenfordsLaw):
    """
    Analysis is a class to analyse the first digits of your data.

    The following types of data can be inserted:
        ----------
        data (list): list of your data
        series (Series): panda series from your data
        ----------

    You can do the following things:
        * get the following properties in dictionary form:
        ----------
        first_digit_frequencies
        second_digit_frequencies
        third_digit_frequencies
        ----------

        * get the following measures:
        ----------
        first_euclidean_distance -> return the euclidean distance between your data's first significant data frequencies and benford frequencies
        second_euclidean_distance -> return the euclidean distance between your data's second significant data frequencies and benford frequencies
        third_euclidean_distance -> return the euclidean distance between your data's third significant data frequencies and benford frequencies
        ----------

        * plot the following:
        ----------
        plot_first_digit -> plot the first significant digit frequency versus benford's law with the euclidean distance in the title
        plot_second_digit ->  plot the second significant digit frequency versus benford's law with the euclidean distance in the title
        plot_third_digit -> plot the third significant digit frequency versus benford's law with the euclidean distance in the title
        ----------
    """

    def __init__(self, data: list = None, series: Series = None):
        self.data = data
        self.series = series

    @staticmethod
    def first_n_digits(num: float, n: int = 1):
        """
        Get the first n digits from a number.

        Parameters
        ----------
        num (float) : number
        n (int)     : number of first digits
        ----------
        """
        first_digits = int(abs(float(num)) // 10 ** (int(log(abs(float(num)), 10)) - n + 1))
        if n == 1:
            return first_digits
        elif n == 0:
            print('Cannot have input equal to 0')
        else:
            return int(str(first_digits)[-1])

    def _n_digit_frequencies(self, n):
        if self.series is not None:
            count = self.series.apply(lambda x: self.first_n_digits(x, n)).value_counts().to_dict()
        else:
            count = Counter([self.first_n_digits(d, n) for d in self.data])
        if n==1:
            for i in range(1, 10):
                if i not in count.keys():
                    count.update({i: 0})
            return dict(sorted({int(i): j / sum(count.values()) for i, j in count.items() if i != 0}.items()))

        else:
            for i in range(10):
                if i not in count.keys():
                    count.update({i: 0})
            return dict(sorted({int(i): j / sum(count.values()) for i, j in count.items()}.items()))

    @property
    def first_digit_frequencies(self):
        return self._n_digit_frequencies(1)

    @property
    def second_digit_frequencies(self):
        return self._n_digit_frequencies(2)

    @property
    def third_digit_frequencies(self):
        return self._n_digit_frequencies(3)

    def first_euclidean_distance(self, frequencies):
        return distance.euclidean(list(self.first_benford_frequencies.values()), frequencies) / distance.euclidean(
            list(self.first_benford_frequencies.values()), [0] * 8 + [1])

    def second_euclidean_distance(self, frequencies):
        return distance.euclidean(list(self.second_benford_frequencies.values()), frequencies) / distance.euclidean(
            list(self.second_benford_frequencies.values()), [0] * 9 + [1])

    def third_euclidean_distance(self, frequencies):
        return distance.euclidean(list(self.third_benford_frequencies.values()), frequencies) / distance.euclidean(
            list(self.third_benford_frequencies.values()), [0] * 9 + [1])

    def plot_first_digit(self, name: str = '', save_as: str = '', show: bool = True):
        """
        Plot the first significant digit frequency of your data versus benford's law.
        We use the Euclidean distance as measure and poisson error bars.

        Parameters
        ----------
        name (str): name of your data
        save_as (str): name for your image if you want to save
        show (bool): if you want to show on screen or not
        ----------
        """
        if self.series is not None:
            size = len(self.series)
        else:
            size = len(self.data)
        error_bar = 1 / sqrt(size)  # poisson error bars -> could be improved with other error bars
        style.use('ggplot')
        plt.scatter(self.first_benford_frequencies.keys(), self.first_benford_frequencies.values(), marker='s',
                    color='black')
        plt.scatter(self.first_digit_frequencies.keys(), self.first_digit_frequencies.values(), marker='o')
        plt.errorbar(self.first_digit_frequencies.keys(), self.first_digit_frequencies.values(), yerr=error_bar,
                     fmt='o')
        plt.legend(["Benford's law", "First significant digit frequency data"])
        plt.title(
            f"{name.title().replace('_', ' ')} has ED:\n{round(self.first_euclidean_distance(list(self.first_digit_frequencies.values())), 4)}",
            size=16)
        plt.xticks(size=16)
        plt.yticks(plt.yticks()[0], [int(round(p, 2) * 100) for p in plt.yticks()[0]], size=16)
        plt.xlabel('First significant digit', size=16)
        plt.ylabel('Frequency (%)', size=16)
        plt.tight_layout()
        if show:
            plt.show()
        if save_as:
            plt.savefig(f'{save_as}')
        return self

    def plot_second_digit(self, name: str = '', save_as: str = '', show: bool = True):
        """
        Plot the second significant digit frequency of your data versus benford's law.
        We use the Euclidean distance as measure and poisson error bars.

        Parameters
        ----------
        name (str): name of your data
        save_as (str): name for your image if you want to save
        show (bool): if you want to show on screen or not
        ----------
        """
        if self.series is not None:
            size = len(self.series)
        else:
            size = len(self.data)
        error_bar = 1 / sqrt(size)  # poisson error bars -> could be improved with other error bars
        style.use('ggplot')
        plt.scatter(self.second_benford_frequencies.keys(), self.second_benford_frequencies.values(), marker='s',
                    color='black')
        plt.scatter(self.second_digit_frequencies.keys(), self.second_digit_frequencies.values(), marker='o')
        plt.errorbar(self.second_digit_frequencies.keys(), self.second_digit_frequencies.values(), yerr=error_bar,
                     fmt='o')
        plt.legend(["Benford's law", "First significant digit frequency data"])
        plt.title(
            f"{name.title().replace('_', ' ')} has ED:\n{round(self.second_euclidean_distance(list(self.second_digit_frequencies.values())), 4)}",
            size=16)
        plt.xticks(size=16)
        plt.yticks(plt.yticks()[0], [int(round(p, 2) * 100) for p in plt.yticks()[0]], size=16)
        plt.xlabel('First significant digit', size=16)
        plt.ylabel('Frequency (%)', size=16)
        plt.tight_layout()
        if show:
            plt.show()
        if save_as:
            plt.savefig(f'{save_as}')
        return self

    def plot_third_digit(self, name: str = '', save_as: str = '', show: bool = True):
        """
        Plot the third significant digit frequency of your data versus benford's law.
        We use the Euclidean distance as measure and poisson error bars.

        Parameters
        ----------
        name (str): name of your data
        save_as (str): name for your image if you want to save
        show (bool): if you want to show on screen or not
        ----------
        """
        if self.series is not None:
            size = len(self.series)
        else:
            size = len(self.data)
        error_bar = 1 / sqrt(size)  # poisson error bars -> could be improved with other error bars
        style.use('ggplot')
        plt.scatter(self.third_benford_frequencies.keys(), self.third_benford_frequencies.values(), marker='s',
                    color='black')
        plt.scatter(self.third_digit_frequencies.keys(), self.third_digit_frequencies.values(), marker='o')
        plt.errorbar(self.third_digit_frequencies.keys(), self.third_digit_frequencies.values(), yerr=error_bar,
                     fmt='o')
        plt.legend(["Benford's law", "First significant digit frequency data"])
        plt.title(
            f"{name.title().replace('_', ' ')} has ED:\n{round(self.third_euclidean_distance(list(self.third_digit_frequencies.values())), 4)}",
            size=16)
        plt.xticks(size=16)
        plt.yticks(plt.yticks()[0], [int(round(p, 2) * 100) for p in plt.yticks()[0]], size=16)
        plt.xlabel('First significant digit', size=16)
        plt.ylabel('Frequency (%)', size=16)
        plt.tight_layout()
        if show:
            plt.show()
        if save_as:
            plt.savefig(f'{save_as}')
        return self


if __name__ == "__main__":
    # example:
    from random import uniform

    random_data = [uniform(-10, 10) for i in range(0, 1000)]
    bl = Analysis(data=random_data)
    bl.plot_first_digit('Random stuff')
    bl.plot_second_digit('Random stuff')
    bl.plot_third_digit('Random stuff')
