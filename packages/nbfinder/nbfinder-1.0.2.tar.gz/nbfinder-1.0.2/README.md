# `nbfinder` : Importing Jupyter Notebooks as Modules

[![build status](http://img.shields.io/travis/hadim/nbfinder/master.svg?style=flat)](https://travis-ci.org/hadim/nbfinder)
[![PyPI](https://img.shields.io/pypi/v/nbfinder.svg)](https://pypi.org/project/nbfinder)

`nbfinder` is a lightweight Python library to import Jupyter Notebook as module in Python file. This library is strongly inspired from the [Jupyter Notebook documentation](http://jupyter-notebook.readthedocs.io/en/latest/examples/Notebook/Importing%20Notebooks.html).

## Usage

Just import the `nbfinder` package and you're done.

```python
import nbfinder
import mynotebook  ## It will load `mynotebook.ipynb` in the current directoy.
```

## Install

```bash
pip install nbfinder
```

or

```bash
conda config --add channels conda-forge
conda install nbfinder
```

## License

MIT. See [LICENSE](LICENSE).

## Author

- Hadrien Mary <hadrien.mary@gmail.com>
