"""
Path and file operation tools.
"""

import platform
import os
import sys
import pathlib
import subprocess

PLATFORM = platform.system()
HOSTNAME = platform.node()

def set_paths(hostname=HOSTNAME):
    """ SETS SUBJECTS_DIR AND RAWDIR according to computer name. This function can be customized to fit various machines.

    Parameters
    ----------
    hostname: string
        Computer Name

    Returns
    -------
    Paths in native and WSL format.
    RAW_DATA
    RAW_DATA_NATIVE
    SUBJECTS_DIR
    SUBJECTS_DIR_NATIVE

    """

    # Default docker image setup
    RAW_DATA = r'/home/host/rawdata/'
    RAW_DATA_NATIVE = r'/home/host/rawdata/'
    SUBJECTS_DIR = r'/home/host/subjects/'
    SUBJECTS_DIR_NATIVE = r'/home/host/subjects/'

    # Override if necessary
    if hostname == 'ML':
        # Cristi's WSL setup
        RAW_DATA = r'/mnt/d/CloudSynology/rawdata/'
        RAW_DATA_NATIVE = r'd:\\CloudSynology\\rawdata\\'
        SUBJECTS_DIR = r'/mnt/d/CloudSynology/subjects/'  # as seen in WSL
        SUBJECTS_DIR_NATIVE = r'd:\\CloudSynology\\subjects\\'  # in native OS

    if hostname == 'osboxes':
        # Cristi's Virtual Box setup (fedora64_osboxes)
        RAW_DATA = r'/home/osboxes/host/CloudSynology/rawdata/'
        RAW_DATA_NATIVE = r'/home/osboxes/host/CloudSynology/rawdata/'
        SUBJECTS_DIR = r'/home/osboxes/subjects/'
        SUBJECTS_DIR_NATIVE = r'/home/osboxes/subjects/'  # in native OS

    if hostname == 'EPIFFB-SERVER':
        # Unibuc , Physics Dept. WSL setup
        RAW_DATA = r'/mnt/d/CloudEpi/SEEGRaw/'
        RAW_DATA_NATIVE = r'd:\\CloudEpi\\SEEGRaw\\'
        SUBJECTS_DIR = r'/mnt/d/CloudEpi/Subjects/'  # as seen in WSL
        SUBJECTS_DIR_NATIVE = r'd:\\CloudEpi\Subjects\\'  # in native OS

    return RAW_DATA, RAW_DATA_NATIVE, SUBJECTS_DIR, SUBJECTS_DIR_NATIVE


def wsl_tempfile(filename):
    """Creates a temporary filename in the current user's folder for native system and
    Windows Subsytem for Linux is native is Windows.

    Parameters
    ----------
    filename: string
        Name of temporary file

    Returns
    -------
    native_file: string
        Path to temporary file on native file system
    was_file: string
        Path to temporary file on WSL file system (ex: /mnt/c/Users/user/filename)
    """
    dir = str(pathlib.Path.home())
    native_file = os.path.join(dir, filename)
    wsl_file = None

    if sys.platform == 'win32':
        breakdown = native_file.replace(':', '').split(sep='\\')
        breakdown[0] = breakdown[0].lower()
        breakdown = ['mnt'] + breakdown
        wsl_file = '/' + '/'.join(breakdown)
    return native_file, wsl_file


def wsl2win(path):
    """Convert WSL path to Windows path

    Parameters
    ----------
    path: String
        Path in WSL format (/mnt/d/....)
    Returns
    -------
    win_path: String
        Path in Windows format

    """
    win_path = [wp for wp in path.replace('/mnt/', '')]
    win_path.insert(win_path.index('/'), ':\\')
    win_path.pop(win_path.index('/'))
    win_path = ''.join(win_path).replace('/', '\\')
    return win_path


def win2wsl(path):
    """Convert WIndows path tp WSL path

    Parameters
    ----------
    path: String
        Path in Windows format
    Returns
    -------
    win_path: String
        Path in WSL format (/mnt/d/....)

    """
    wsl_path = '//mnt//' + path.replace(':\\', '//').replace('\\', '//')
    return wsl_path


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


# def execute(cmd):
#     popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#     for stdout_line in iter(popen.stdout.readline, ''):
#         yield stdout_line.replace('\r', '').replace('\n', '')
#     popen.stdout.close()
#     return_code = popen.wait()
#     if return_code:
#         raise subprocess.CalledProcessError(return_code, cmd)


def execute(cmd):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines=True)
    # for stdout_line in iter(proc.stdout.readline, ''):
    #     yield stdout_line.replace('\r', '').replace('\n', '')
    while proc.poll() is None:
        line = proc.stdout.readline()
        if line != "":
            yield line.replace('\r', '').replace('\n', '')
    proc.stdout.close()
    return_code = proc.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
