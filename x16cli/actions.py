import os
import git
import glob
import toml
import click
import dotmap
import shutil
import webbrowser
import subprocess
import x16cli.config as cfg
from x16cli.checks import *

join = os.path.join


def create_folders(path):
    click.echo('Creating project hidden folder {}...'.format(cfg.PRJ_FOLDER))
    shutil.rmtree(join(path, cfg.PRJ_FOLDER), ignore_errors=True)
    os.makedirs(join(path, cfg.PRJ_FOLDER))


def create_config_file(path):
    if is_project_present(path):
        raise ProjectPresentError

    click.echo('Creating project config file {}...'.format(cfg.CFG_FILENAME))

    srcs = [os.path.relpath(src) for src in collect_src(path)]
    if cfg.MAIN_NAME in srcs:
        srcs.remove(cfg.MAIN_NAME)

    toml.dump({
        'version': cfg.VERSION,
        'rom': {
            'repository': cfg.ROM_REPO,
            'release': cfg.LAST_X16_RELEASE,
        },
        'emulator': {
            'repository': cfg.EMU_REPO,
            'release': cfg.LAST_X16_RELEASE,
        },
        'compiler': {
            'repository': cfg.CC65_REPO,
            'release': cfg.LAST_CC65_RELEASE,
            'command': cfg.CC65_CMDLINE,
            'cpu': cfg.CC65_CPU,
            'target': cfg.CC65_TARGET,
            'program':  os.path.basename(path) + '.prg',
            'source': {
                'main': cfg.MAIN_NAME,
                'modules': srcs,
            },
        },
    }, open(join(path, cfg.CFG_FILENAME), 'w+'))


def load_config_file(path):
    return dotmap.DotMap(toml.load(open(join(path, cfg.CFG_FILENAME), 'r')))


def clone_repos(path):
    c = load_config_file(path)
    cc65_folder = join(path, cfg.CC65_FOLDER)
    emu_folder = join(path, cfg.EMU_FOLDER)
    rom_folder = join(path, cfg.ROM_FOLDER)
    try:
        if not os.path.exists(cc65_folder):
            click.echo('Cloning cc65 repository...')
            git.Repo.clone_from(c.compiler.repository, to_path=cc65_folder)
        if not os.path.exists(emu_folder):
            click.echo('Cloning emulator repository...')
        git.Repo.clone_from(c.emulator.repository, to_path=emu_folder)
        if not os.path.exists(rom_folder):
            click.echo('Cloning rom repository...')
        git.Repo.clone_from(c.rom.repository, to_path=rom_folder)
    except:
        raise RepositoryCloneError


def checkout_release(path):
    c = load_config_file(path)
    cc65 = git.Git(join(path, cfg.CC65_FOLDER))
    emu = git.Git(join(path, cfg.EMU_FOLDER))
    rom = git.Git(join(path, cfg.ROM_FOLDER))
    try:
        click.echo('Setup release {} for cc65...'.format(c.compiler.release))
        cc65.checkout(c.compiler.release)
        click.echo('Setup release {} for emulator...'.format(
            c.emulator.release))
        emu.checkout(c.emulator.release)
        click.echo('Setup release {} for rom...'.format(c.rom.release))
        rom.checkout(c.rom.release)
    except git.GitCommandError:
        raise ReleaseNotFoundError


def compile_tools(path):
    cc65 = join(path, cfg.CC65_FOLDER)
    cc65_bin = join(path, cfg.CC65_BIN_FOLDER)
    emu = join(path, cfg.EMU_FOLDER)
    rom = join(path, cfg.ROM_FOLDER)

    click.echo('Compiling cc65...')
    make_cc65 = subprocess.Popen(
        'make', cwd=cc65, shell=True, stdout=subprocess.DEVNULL)
    make_cc65.wait()

    env = os.environ.copy()
    env['PATH'] = cc65_bin + ':' + env['PATH']

    click.echo('Compiling emulator...')
    make_emu = subprocess.Popen(
        'make', cwd=emu, stdout=subprocess.DEVNULL, env=env)
    click.echo('Compiling rom...')
    make_rom = subprocess.Popen(
        'make', cwd=rom, stdout=subprocess.DEVNULL, env=env)
    make_emu.wait()
    make_rom.wait()


def add_main_asm(path):
    if is_main_present(path):
        return
    open(join(path, cfg.MAIN_NAME), 'w+').write(cfg.HELLO_WORLD)


def collect_src(path):
    return glob.glob(join(path, '**', '*.asm'), recursive=True)


def collect_obj(path):
    return glob.glob(join(path, '*.o'))


def build(path):
    c = load_config_file(path)
    prj_folder = join(path, cfg.PRJ_FOLDER)
    cl65 = join(path, cfg.CL65_BIN)

    cc65 = join(path, cfg.CC65_FOLDER)
    emu = join(path, cfg.EMU_FOLDER)
    rom = join(path, cfg.ROM_FOLDER)
    if not is_correct_release(cc65, c.compiler.release) or not is_correct_release(emu, c.emulator.release) or not is_correct_release(rom, c.rom.release):
        checkout_release(path)
        compile_tools(path)

    click.echo('Building {}...'.format(c.compiler.program))
    cmdline = c.compiler.command
    cmdline = cmdline.replace('{cl65}', cl65)
    cmdline = cmdline.replace('{cpu}', c.compiler.cpu)
    cmdline = cmdline.replace('{target}', c.compiler.target)
    cmdline = cmdline.replace('{prg}', c.compiler.program)
    cmdline = cmdline.replace('{main}', c.compiler.source.main)
    if c.compiler.source.modules:
        cmdline = cmdline.replace(
            '{modules}', ' '.join(c.compiler.source.modules))
    else:
        cmdline = cmdline.replace(' {modules}', '')

    p = subprocess.Popen(cmdline.split(' '), stdout=subprocess.DEVNULL)
    p.wait()

    subprocess.Popen(['mv', *collect_obj(path), prj_folder])


def start_emu(path, debug):
    c = load_config_file(path)
    emu_bin = join(path, cfg.EMU_BIN)
    rom_bin = join(path, cfg.ROM_BIN)

    args = [emu_bin, '-rom', rom_bin, '-prg', c.compiler.program, '-run']
    if debug:
        args.append('-debug')

    click.echo('Launching emulator with {}...'.format(c.compiler.program))

    emu = subprocess.Popen(args, stdout=subprocess.DEVNULL)


def open_docs():
    webbrowser.open(cfg.DOCS_URL, new=2)
