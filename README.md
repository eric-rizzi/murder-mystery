# Murder Mystery Debugging Exercise

This folder contains a Python port of the "Murder Mystery" debugging exercise
developed at Rutgers (the original activity was in Java). It is intended to be
used with Microsoft's `vscode`, although it can be used with any Python IDE with
a debugger that's capable of handling multiple files.

Assignment based on [Nifty’s Murder Mystery](http://nifty.stanford.edu/) by
Colin Sullivan, Steven Chen, and Ana Paula Centeno.

## Setup

There are three basic steps you need in order to get this project up and
running with type checking, linting, and unit testing enabled.

#### 0. Open the project's workspace

Open `vscode` and select `File` -> `Open Workspace from File`. Then, select the
`murder-mystery.code-workspace` file within this project folder.

#### 1. Install necessary extensions

On the left-most side of the `vscode` window, select the extensions tab (four
small squares making a larger square) and install the following extensions:

- `Python`
- `Pylance` (auto installed with `Python` extension)
- `Black Formatter`
- `isort`

> Note: be careful to select only the "Microsoft approved" extensions.

#### 2. Install necessary Python modules

Open the terminal window by selecting `Terminal` -> `New Terminal`. Then,
install `pytest` by typing `pip3 install pytest`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
