import os

VERSION = '0.1.0'

PRJ_FOLDER = '.x16prj'
EMU_FOLDER = os.path.join(PRJ_FOLDER, 'x16emu')
EMU_BIN = os.path.join(EMU_FOLDER, 'x16emu')
ROM_FOLDER = os.path.join(PRJ_FOLDER, 'x16rom')
ROM_BIN = os.path.join(ROM_FOLDER, 'build', 'x16', 'rom.bin')
CC65_FOLDER = os.path.join(PRJ_FOLDER, 'cc65')
CC65_BIN_FOLDER = os.path.join(CC65_FOLDER, 'bin')
CL65_BIN = os.path.join(CC65_BIN_FOLDER, 'cl65')

EMU_REPO = 'https://github.com/commanderx16/x16-emulator.git'
ROM_REPO = 'https://github.com/commanderx16/x16-rom.git'
CC65_REPO = 'https://github.com/cc65/cc65.git'

LAST_X16_RELEASE = 'r37'
LAST_CC65_RELEASE = 'cbf0c1d1dddc9d201ef3bf6ce9f3d5b54bc6e325'

HELLO_WORLD = """.org $080D
.segment "STARTUP"
.segment "INIT"
.segment "ONCE"
.segment "CODE"
    JMP start

start:
mainLoop:
    BRA mainLoop

"""
MAIN_NAME = 'main.asm'

CC65_CMDLINE = '{cl65} --cpu {cpu} --target {target} -u __EXEHDR__ -o {prg} {main} {modules}'
CC65_CPU = '65C02'
CC65_TARGET = 'cx16'

CFG_FILENAME = 'x16.toml'

DOCS_URL = 'https://github.com/commanderx16/x16-docs'
