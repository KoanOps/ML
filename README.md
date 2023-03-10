<h1>Machine Learning Model Environment with Backtesting</h1>
<h3>TL;DR</h3>
This is a work sample of an older model using a RL environment written in Python as a work reference to showcase a simplified Machine Learning model with applications in trading. This script in particular is designed to backtest the performance of the model based on historical exchange price data.

<h3>Prerequisites</h3>

<ul>
<li>Python 3</li>
<li>NumPy, a Python library that provides a multidimensional array object, various derived objects such as masked arrays and matrices, and an assortment of routines for fast operations on arrays, including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation, and more.</li>
<li>Pandas, a data analysis library built on top of NumPy that provides high-level data structures and operations for manipulating numerical tables, time series, vectorized methods, machine learning, data cleaning, data analysis, and more.</li>
</ul>

<h3>Configuration</h3>
This model backtesting script uses price data from a CSV file located at <code>data.csv</code>. This file should be placed in the same directory as the script. You may update the price data using raw data from price charts.

<h3>Usage</h3>

<p>You can install the required packages using <code>pip</code>:</p>

<pre><code>pip install numpy</code></pre>
<pre><code>pip install pandas</code></pre>

<p>To use, simply run the <code>bot.py</code> script:</p>

<pre><code>python bot.py</code></pre>

<p>The script will then read in the price data from the data.csv file, and use it to backtest the machine learning model. The results of the backtest will be output to the console.</p>

<h2>Disclaimer</h2>
<p>This script is intended only for work reference. It should not be used for actual trading purposes without extensive testing and modification. The performance of the machine learning model used by this bot may not be indicative of future results, and should not be relied upon for investment decisions.
The author is not liable for any losses.</p>
