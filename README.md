# X16 Command Line Interface

X16 Command Line Interface is a tool for assembly projects. Features:

- Downloading and building of compiler, emulator and rom
- Default configuration should just work
- Build and run with one command
- Easy to read configuration file

## Details

The first command you should use in your project folder is ```x16 init```. X16Cli downloads the compilation tools in a hidden folder and creates a `toml` configuration file.

The `hello world` project does nothing. You are free to start from the `main.asm` file.

If you want to change the *starting point* you just have to edit the config file under `compiler.source` section.

### Multiple Files

Every other `.asm` file (except the `main`) should be added to the config file in the `modules` list. The include files (`.inc`) shouldn't be added.

The modules compiled this way should *export* the right symbols (please look at cc65 documentation for that).

## Requirements

X16Cli is actively developed and tested on Linux Ubuntu. If you are a Mac or Windows user you may consider to help me supporting these platforms too. Thank you.

### Linux Ubuntu

- Python >= 3.6
- ```sudo apt install build-essential git```

If something is missing here, please reach out to me.

## Install

You should only need to do this in the right environment:

```pip install x16cli```

Or, something like that for user level:

```pip3 install x16cli --user```

You should have the `pip3` user binary folder in your system `PATH` to have easy access to `x16` script.

## Getting Started

```bash
mkdir myprj-folder
cd myprj-folder
x16 init
x16 run
```
