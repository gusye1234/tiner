<div align="center">
  <h1>tiner</h1>
  <p><strong>Block-wise timer for Python</strong></p>
    <p>
    <img src="https://github.com/gusye1234/tiner/actions/workflows/main.yml/badge.svg">
    <img src="https://img.shields.io/codecov/c/github/gusye1234/tiner">
    <img src="https://img.shields.io/pypi/v/tiner.svg">
  </p>
</div>


## Install

```shell
pip install tiner
```

## Usage

### Works like a context manager

```python
from tiner import tiner
from time import sleep

with tiner("see this block"):
  slezep(1)
# return the block running time
print(tiner.get('see this block'))
```

or as a python decorator

```python
@tiner('see this function')
def f():
  #do something
```

### Global mining and grouping

the timing is managed by `tiner`, not its instances

```python
# A.py
with tiner("In A"):
  #do something
...
# B.py
with tiner("In B"):
  #do something

tiner.table()
#-------------------------
╒═════════╤═══════════╕
│ Block   │   Time(s) │
╞═════════╪═══════════╡
│ In B    │  ...      │
├─────────┼───────────┤
│ In A    │  ...      │
╘═════════╧═══════════╛
```

`tiner` internally records the different locations for the same block name:

```python
for _ in range(loop_times):
  with tiner("test:loop"):
    sleep(duration)
# do something
with tiner("test:loop"):
  sleep(duration)
tiner.table(verbose=True)
#-------------------------
test:loop
╒═══════════════╤════════╤═══════════╕
│ File          │   Line │   Time(s) │
╞═══════════════╪════════╪═══════════╡
│ test_tiner.py │     29 │  0.516125 │
├───────────────┼────────┼───────────┤
│ test_tiner.py │     34 │  0.104061 │
╘═══════════════╧════════╧═══════════╛
```

### Design for loops

```python
from tiner import tiner
from time import sleep

for _ in range(10):
  #do something
  with tiner("see this loop"):
    sleep(0.1)
  #do something
  
# return the block running time over the loops
print(tiner.get('see this loop'))
```

### Easy to use

A timer should be clear and simple

```python
tiner.get(BLOCK_NAME) # return a certain block running time so far
tiner.table([BLOCK1, ...]) # print some blocks' time on a formatted table
tiner.zero([BLOCK1, ...]) # empty some blocks' time
tiner.disable() # disable time logging
```

---
> **NOTE**: `tiner`'s timing is relatively precise. You should only use it for comparison of the timings of different blocks in one run, not for different runs of your program.
