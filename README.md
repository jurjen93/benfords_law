# Benford's law analysis

Benford's law is a digit-law, which states that digits from numbers follow a specific frequency.
This specific frequency has been observed in many numerical datasets, 
as discovered by Simon Newcomb and Frank Benford.
You can find on [wikipedia] more information about this "mysterious" law.

Benford's law is a helpful tool to detect fraud, do science, or just to investigate the quality of data. 
You can also read my [blog] on Towards Data Science with a summary of Benford's law and [this paper], 
where I used Benford's law to study digit patterns of the distances between stars in our Milky Way.

#### Installation
With ```pip install benfordslaw-analysis``` you can install the package.

#### Usage
After installing, you can run in Python ```from benfordslaw_analysis.analysis import Analysis```.
This imports the class ```Analysis```.
With this class you can verify if Benford's law is hidden in your own data.

For example, make a plot with Benford's law versus random data with:
```
from benfordslaw_analysis.analysis import Analysis
from random import uniform
random_data = [uniform(-10, 10) for i in range(0,1000)]
bl = Analysis(random_data)
bl.plot_first_digit('Random stuff')
```
![Test Image 1](test/test.png)

Note that we use the [Euclidean distance] between the digit frequency from Benford's law and your own data as a measure
and that we use Poisson error bars (based on the number of data points).

#### Euclidean distance

The normalized Euclidean distance is a quick way to test whether your data follows Benford law.
This value is situated between 0 and 1, the closer to 0 the better.
However, it is not a formal statistic because it is sample size independent.
In the literature there are several other measures (Chi-square, Kolmogorov-Smirnov, ..) that are used. However, I noticed that 
size dependency is a limitation in bigger datasets and classifies all bigger datasets as non-Benford, even though they are Benford by eye.

[wikipedia]: https://en.wikipedia.org/wiki/Benford%27s_law
[blog]: https://towardsdatascience.com/benfords-law-in-the-gaia-universe-b5727db7a936
[Euclidean distance]: https://en.wikipedia.org/wiki/Euclidean_distance
[this paper]: https://www.aanda.org/articles/aa/pdf/2020/10/aa37256-19.pdf
