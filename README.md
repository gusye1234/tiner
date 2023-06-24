<div align="center">
  <h1>tiner</h1>
  <p><strong>Block-wise, thread-safety timer for loops</strong></p>
    <p>
    <a href="https://github.com/gusye1234/tiner/actions?query=workflow%3Atest">
      <img src="https://github.com/gusye1234/tiner/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://codecov.io/gh/gusye1234/tiner">
      <img src="https://img.shields.io/codecov/c/github/gusye1234/tiner">
    </a>
    <a href="https://pypi.org/project/tiner/">
      <img src="https://img.shields.io/pypi/v/tiner.svg">
    </a>
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
  sleep(1)
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

the timing is managed by `tiner`, not its instances:

```python
# A.py
for _ in range(20):
  with tiner("t1"):
    #do something
...
# B.py
for _ in range(20):
  with tiner("t2"):
    #do something
...
# main.py
tiner.table()
#-------------------------
╒═════════╤═══════════╤════════╕
│ Block   │   Time(s) │   Hits │
╞═════════╪═══════════╪════════╡
│ t1      │ 0.026127  │     20 │
├─────────┼───────────┼────────┤
│ t2      │ 0.0131467 │     10 │
╘═════════╧═══════════╧════════╛
```

`tiner` internally records the different locations for the same block name and will merge their duration at report. Display the additional infomation with `tiner.table(verbose=True)`:

```python
for _ in range(10):
  with tiner("test:loop"):
    sleep(duration)
  ...
  with tiner("test:loop"):
    sleep(duration)
  
tiner.table(verbose=True)
#-------------------------
test:loop
╒═════════════════════╤════════╤═══════════╤════════╕
│ File                │   Line │   Time(s) │   Hits │
╞═════════════════════╪════════╪═══════════╪════════╡
│ tests/test_tiner.py │    107 │ 0.0128279 │     10 │
├─────────────────────┼────────┼───────────┼────────┤
│ tests/test_tiner.py │    112 │ 0.0132992 │     10 │
╘═════════════════════╧════════╧═══════════╧════════╛
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

### Handle asynchronous programs

```python
import os
from tiner import tiner

# tiner will call the synchronize function when the block is over
with tiner("loop", synchronize=torch.cuda.synchronize):
  # machine learning running
  
# return the block running time over the loops
print(tiner.get('loop'))
```

### Easy to use

A timer should be clear and simple

```python
tiner.get(BLOCK_NAME) # return a certain block running time so far
tiner.table([BLOCK1, ...]) # print some blocks' time on a formatted table
tiner.zero([BLOCK1, ...]) # empty some blocks' time
tiner.disable() # disable time logging
tiner.enable() # enable time logging
```
