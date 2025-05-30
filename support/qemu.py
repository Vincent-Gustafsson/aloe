#! /usr/bin/env python

import sys
import subprocess
sys.dont_write_bytecode = True
import chariot_utils

CHARIOT_CACHE_PATH = "/home/vincent/projects/ember-cache"

OVMF_PATH = "/usr/share/ovmf/x64/OVMF.4m.fd"

chariot_recipes = [
    "source/ember",
    "custom/image"
]

qemu_args = [
    "-accel", "tcg",
    "-machine", "q35",
    "-cpu", "qemu64",
    "-smp", "cores=4",
    "-m", "1G",
    "-M", "smm=off",
    "-d", "int",
    "-D", "log.txt",
    "-monitor", "stdio",
    "-debugcon", "file:/dev/stdout",
    "-S",
    "-s",
    "-no-reboot",
    "-no-shutdown",
    "-display", "none",
    "-drive", f"format=raw,file={chariot_utils.path("custom/image", "--cache", CHARIOT_CACHE_PATH)}/ember.img",
    "-drive", f"if=pflash,unit=0,format=raw,file={OVMF_PATH},readonly=on"
]


chariot_utils.build(chariot_recipes, "--cache", CHARIOT_CACHE_PATH, check=True)

subprocess.run(["alacritty", "msg", "config", "font.size=10"])

try:
    subprocess.run(["qemu-system-x86_64"] + qemu_args, check=True)
except KeyboardInterrupt:
    pass

subprocess.run(["alacritty", "msg", "config", "font.size=13"])
