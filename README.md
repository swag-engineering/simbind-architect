# Simbind Architect

This project is a component of the [Simbind](https://github.com/swag-engineering/simbind-cli) tool, and it's primary
goals are following:

- Parse C code files that were generated
  by [Simulink Exporter](https://github.com/swag-engineering/simulink-exporter#Requirements) to extract variable names
  and types
- Build this C code with [SWIG](https://www.swig.org/)
- Compose thin Python Class wrapper for comprehensive and convenient usage

## Requirements

- Linux x86-64 machine, we didn't test under other OS's and architectures.
- Python 3.10+
- You also need gcc, cmake, make and swig. Under Debian-based distros you can install it with
  ```bash
  sudo apt-get install build-essential cmake swig
  ```

## Project structure

Project contains two major components:

- [Collector](https://github.com/swag-engineering/simbind-architect/blob/master/simbind_architect/Collector.py) that
  used to parse provided C code
- [SilDriver](https://github.com/swag-engineering/simbind-architect/blob/master/simbind_architect/sil/SiLDriver.py) that
  utilizes Collector to build C code and generate Python wrapper

You can check [here](https://github.com/swag-engineering/simbind-cli/blob/master/simbind/__main__.py) how you can make
use of these components. 
