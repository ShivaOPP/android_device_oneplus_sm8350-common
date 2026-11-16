#!/usr/bin/env python3
"""Record the real selected kernel's complete module inventory for calcite.

Calcite parses image-module inputs before its legacy kernel task defines its
module archive. An explicit inventory avoids an empty vendor_dlkm image and
preserves the A17 modules.load ordering. Run after a successful kernel build.
"""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


COMMON = Path(__file__).resolve().parent
ROOT = COMMON.parents[2]
KERNEL = ROOT / "kernel/oneplus/sm8350"
ALIASES = {"wlan.ko": "qca_cld3_wlan.ko"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kernel_out", type=Path)
    args = parser.parse_args()
    output = args.kernel_out.resolve()
    sources = (output / "modules.order").read_text().splitlines()
    inventory = {}
    for source in sources:
        module = Path(source)
        if module.is_absolute():
            module = module.relative_to(output)
        path = output / module
        if path.suffix != ".ko" or not path.is_file():
            raise RuntimeError(f"Kernel module not built: {path}")
        name = ALIASES.get(path.name, path.name)
        if name in inventory:
            raise RuntimeError(f"Ambiguous module basename: {name}")
        inventory[name] = str(module)

    for filename in ("modules.load", "modules.include.recovery", "modules.load.recovery"):
        requested = set((COMMON / filename).read_text().split())
        missing = requested - inventory.keys()
        if missing:
            raise RuntimeError(f"{filename} references missing modules: {sorted(missing)}")

    (COMMON / "kernel-modules.list").write_text("\n".join(sorted(inventory)) + "\n")
    commit = subprocess.check_output(
        ["git", "-C", str(KERNEL), "rev-parse", "HEAD"], text=True
    ).strip()
    (COMMON / "kernel-modules.json").write_text(json.dumps({
        "kernel": str(KERNEL.relative_to(ROOT)),
        "commit": commit,
        "config_sha256": hashlib.sha256((output / ".config").read_bytes()).hexdigest(),
        "aliases": ALIASES,
        "modules": dict(sorted(inventory.items())),
    }, indent=2) + "\n")
    print(f"Recorded {len(inventory)} compiled modules; A17 load lists are complete")


if __name__ == "__main__":
    main()
