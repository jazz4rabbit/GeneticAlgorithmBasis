# GeneticAlgorithmBasis
This is a genetic algorithm experiment to investigate the influence of basis using `ga_pkg`.
`ga_pkg` requires [DEAP](https://github.com/DEAP/deap), an evolutionary computation framework.

## Introduction
- Experiments on bases affecting genetic algorithms.
- Experiments include onemax, variant-onemax, nk-landscape and graph partition.

### Implementation of problems
- [x] `onemax`
- [x] `v_onemax` (variant onemax)
- [ ] `good_basis`
- [ ] `nk-landscape`
- [ ] `graph partition`

## Getting Started

### Prerequisites
- `python 3.x`
- `deap`
- `numpy`

### Installing
How to install deap and numpy
```bash
pip install deap, numpy
```

## Example of `ga_pkg`
- onemax problem

```python
from ga_pkg import ga
from ga_pkg import problems

# default of cxpb=0.5, mutpb=0.2
# population size 20, individual size 10
model = problems.onemax.from_setting(n=20, IND_SIZE=10)

# search solution
runed_model, logbook = ga.run(model, ngen=100)

# get best instance
best_ind = runed_model.halloffame[0]

# save/load model as a file
ga.to_pkl(runed_model, "./onemax_model.pkl") # save
load_model = ga.from_pkl("./onemax_model.pkl") # load
```

## Details of `ga_pkg`
- `ga`
  - `run(model, ngen)`
  - `run_target(model, ngen, fit_val_target, nloop=10)`
  - `to_pkl(model, fname, logbook=None, with_rndstate=False)`
  - `from_pkl(fname)`
- `problems`
  - `onemax`
    - `from_setting(n, IND_SIZE, cxpb=0.5, mutpb=0.2)`
  - `v_onemax`
    - `from_setting(n, IND_SIZE, BASIS, cxpb=0.5, mutpb=0.2)`
    - `from_onemax(model_onemax, BASIS, cxpb=0.5, mutpb=0.2)`
  - `good_basis`
    - `from_setting(n, target_model, target_ngen, cxpb=0.5, mutpb=0.2)`
- `basislib`
  - `random.get_basis(ndim)`
  - `basis`
    - `basis.to_mat(ndim)`
    - `basis.to_inv_mat(ndim)`
    - `basis.applyBasis(model)`


## Example of Running Code
- onemax problem

```bash
git clone https://github.com/jazz4rabbit/GeneticAlgorithmBasis
cd GeneticAlgorithmBasis
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# or echo "export PYTHONPATH=\"\${PYTHONPATH}:$(pwd)\"" >> ~/.bashrc

python -O example/onemax_example.py
```

- onemax expriment

```bash
cd example
mkdir -p onemax/{pkl,logbook}
python -O experiment_onemax.py IND_SIZE # IND_SIZE is an individual size
```

- v_onemax problem

```bash
cd example
mkdir -p v_onemax/{pkl,logbook,basis}
python -O experiment_v_onemax.py IND_SIZE
```
