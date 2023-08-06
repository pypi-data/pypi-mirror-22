# tmux-control

configure and control tmux

# setup

```Bash
sudo apt-get install cmus
sudo apt-get install elinks
sudo apt-get install htop
sudo apt-get install ranger
sudo apt-get install tmux

sudo pip install tmux_control
```

# configurations

## analysis mode

This mode is designed to be ergonomic for running an analysis. The bottom terminal runs the main analysis code while ranger allows for quick viewing of ongoing analysis output files.

```
-----------------------
|                     |
|       ranger        |
|                     |
|                     |
|---------------------|
|                     |
|      terminal       |
|                     |
|                     |
-----------------------
```

## badass mode

This mode is designed to be useful but also to show off the size of one's metaphorical terminal configuration cock. It opens arXiv so you can be a physics stunna, and cmus for acid dinner jazz.

```
-----------------------
| ranger   |          |
|----------|          |
| terminal |          |
|----------|          |
| htop     |  ranger  |
|----------|          |
| arXiv    |          |
|----------|          |
| cmus     |          |
-----------------------
```

## detail mode

This mode is designed to be a less fun version of badass mode.

```
-----------------------
|          |          |
| ranger   |          |
|----------|          |
| terminal |          |
|----------|  ranger  |
| htop     |          |
|----------|          |
| arXiv    |          |
|          |          |
-----------------------
```

## edit mode (default)

This mode is designed to be ergonomic for coding.

```
-----------------------
|          |          |
|          |          |
|          |          |
|          |          |
| terminal |  ranger  |
|          |          |
|          |          |
|          |          |
|          |          |
-----------------------
```

## Nvidia mode

This mode is designed to display system resource usage for a system featuring Nvidia  hardware.

```
-----------------------
|                     |
|        htop         |
|                     |
|                     |
|---------------------|
|                     |
|     nvidia-smi      |
|                     |
|                     |
-----------------------
```

## run mode

This mode launches all of the scripts at a specified directory in separate windows.

```
-----------------------
|                     |
|                     |
|                     |
|                     |
|      scripts        |
|                     |
|                     |
|                     |
|                     |
-----------------------
```

## work mode

This mode is designed to be a compromise between analysis, edit and badass modes.

```
-----------------------
|                     |
|       ranger        |
|---------------------|
|                     |
|      terminal       |
|---------------------|
|          |          |
|  ranger  |  cmus    |
|          |          |
-----------------------
```

# usage

```Bash
tmux-control.py --help
```
