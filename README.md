# Particle Gibbs for Bayesian classification and structure learning in decomposable graphical models
A particle Gibbs sampler for Bayesian structure learning in discrete log-linear and Gaussian decomposable graphical models.

### Installation

```
$ pip install trilearn
```
If you don't have graphviz on you machine, you can install it from brew / aptitude / pacman for example
```
$ brew install graphviz
```

### Running the tests

```
$ make test
```

## Scripts
### Continuous data
To approximate the underlying decomposable graph posterior given the dataset centralized sample_data/dataset_p15.csv run
```
$ pgibbs_ggm_sample.py -N 50 -M 1000 -f sample_data/dataset_p15.csv
```
this will produce a file containing the Markov chain generated by the particle Gibbs algorithm. 
In order to analyze the chain run
```
$ pgibbs_ggm_analyze.py -N 50 -M 1000 -f sample_data/dataset_p15.csv
```
this will produce a bunch of files in the current directory to be analyzed.

### Discrete data
The dataset examples/data/czech_autoworkers.csv contains six variables, each taking values in {0,1}.
To estimate the underlying decomposable graph posterior run
```
$ pgibbs_loglinear_sample.py -N 50 -M 300 -f sample_data/czech_autoworkers.csv
```
and
```
$ pgibbs_loglinear_analyze.py -N 50 -M 300 -f sample_data/czech_autoworkers.csv
```
this will produce a number of files in the current directory.

### Estimate the number of decomposable graphs
To estimate the number of decomposable graphs with up to 15 nodes run for example
```
$ count_chordal_graphs.py -p 15 -N 20000
```
## Built With

* [NetworkX](https://networkx.github.io/documentation/stable/index.html)
* [NumPy](https://docs.scipy.org/doc/)
* [Scipy](https://docs.scipy.org/doc/)
* [Pandas](http://pandas.pydata.org/pandas-docs/stable/)
* [Seaborn](https://seaborn.pydata.org/api.html)
## Authors

* **Felix Rios**

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* **Jim Holmstrom**
