# **Clay Printing Controller**

This a repository for the Clay Printing Controller.

## Requirements

- [TwinCAT 3]

## Development

- TwinCAT: `v3.1 build4022.24`
- [UV]: A blazingly fast Python package management (in Rust)

### Getting Started

#### TwinCAT setup

TBC..

#### Development environment

Create a virtual environment

``` bash
uv venv --python 3.12
source venv/bin/activate
uv pip install -e .

```

## Package Information
> [!NOTE]
> This is an initial repo structure, feel free to change. it
>
* `plc`: the TwinCAT project for the PLC controller.
* `robot`: the folder for the robot control.
* `script`: the example script for controlling Beckhoff controller via Python.


## Credits
Author: [Wei-Ting Chen]

This package was created by [Wei-Ting Chen] at [USI-FMAA](https://github.com/USI-FMAA).

<!-- link -->
[TwinCAT 3]: https://www.beckhoff.com/en-en/products/automation/twincat/texxxx-twincat-3-engineering/te1000.html
[UV]: https://docs.astral.sh/uv/
[Wei-Ting Chen]: https://github.com/WeiTing1991
