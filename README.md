<div align="center">
  <h1>tiner</h1>
  <p><strong>Block-wise timer for Python</strong></p>
    <p>
    <img src="https://github.com/gusye1234/tiner/actions/workflows/main.yml/badge.svg">
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

### Design for loops, or pipeline

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
```

