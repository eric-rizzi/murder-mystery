# Murder Mystery Debugging Exercise

```
                                                                                   .--.
                                                                               .-(    ).
                                                                               (___.__)__)
                                                                               ⚡   ⚡   ⚡
                                                                               '  '  '  '
                                                                             '  '  '  '  '  '
  __  __               _             __  __           _                         ':.
 |  \/  |             | |           |  \/  |         | |                           []_____
 | \  / |_   _ _ __ __| | ___ _ __  | \  / |_   _ ___| |_ ___ _ __ _   _          /\      \
 | |\/| | | | | '__/ _` |/ _ \ '__| | |\/| | | | / __| __/ _ \ '__| | | |     ___/  \__/\__\__
-| |  | | |_| | | | (_| |  __/ |----| |  | | |_| \__ \ ||  __/ |  | |_| |----/\___\ |''''''|__\
 |_|  |_|\__,_|_|  \__,_|\___|_|    |_|  |_|\__, |___/\__\___|_|   \__, |    ||'''| |''||''|''|
                                           __/ |                  __/ |     ``"""`"`""))""`""`
A debugger-based Mystery Solving game     |___/                  |___/
```

This folder contains a Python port of the "Murder Mystery" debugging exercise
developed at Rutgers (the original activity was in Java). It is intended to be
used with Microsoft's `vscode`, although it can be used with any Python IDE with
a debugger that's capable of handling multiple files.

Assignment based on [Nifty’s Murder Mystery](http://nifty.stanford.edu/) by
Colin Sullivan, Steven Chen, and Ana Paula Centeno.

## Activity Setup

1. Clone this repository to your local computer.
2. Open `vscode` and select `File` -> `Open Workspace from File`.
3. Select the `murder-mystery.code-workspace` file within this project folder.
4. Create a copy of this [GoogleDoc](https://docs.google.com/document/d/1raTq4IhXgCF_bPlXW3MFXrc_IMzhc5wMO3H0Bh9bFhw).
5. Start solving!

## Developer Setup

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
