#!/usr/bin/env python3
"""Export the selected kernel's real UAPI for calcite's kernel_headers modules."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


COMMON = Path(__file__).resolve().parent
ROOT = COMMON.parents[2]
KERNEL = ROOT / "kernel/oneplus/sm8350"


def git(directory: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(directory), *args], text=True).strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    version = re.search(
        r"^TARGET_KERNEL_CLANG_VERSION\s*:=\s*(\S+)",
        (COMMON / "BoardConfigCommon.mk").read_text(),
        re.M,
    ).group(1)
    clang = ROOT / f"prebuilts/clang/host/linux-x86/clang-{version}/bin/clang"
    gitdir = Path(git(COMMON, "rev-parse", "--absolute-git-dir"))
    build = gitdir / "porsche-uapi-build"
    install = gitdir / "porsche-uapi-install"
    build.mkdir(exist_ok=True)
    install.mkdir(exist_ok=True)
    subprocess.run(
        [
            "make", "-C", str(KERNEL), f"O={build}", "ARCH=arm64",
            f"HOSTCC={clang}", f"CC={clang}", f"INSTALL_HDR_PATH={install}",
            "headers_install", "-j48",
        ],
        check=True,
    )

    files: dict[str, bytes] = {}
    files["kernel-headers.LICENSE"] = (KERNEL / "COPYING").read_bytes()
    for header in sorted((install / "include").rglob("*.h")):
        relative = header.relative_to(install / "include")
        files[str(Path("kernel-headers") / relative)] = header.read_bytes()
    originals = [KERNEL / "include/uapi", KERNEL / "arch/arm64/include/uapi"]
    originals.extend(sorted((KERNEL / "techpack").glob("*/include/uapi")))
    for directory in originals:
        if not directory.is_dir():
            continue
        for header in sorted(directory.rglob("*.h")):
            relative = header.relative_to(KERNEL)
            files[str(Path("original-kernel-headers") / relative)] = header.read_bytes()

    manifest = COMMON / "kernel-headers.json"
    previous = json.loads(manifest.read_text()).get("files", {}) if manifest.exists() else {}
    # Preserve any manual edits before changing generated snapshots.
    for relative in set(files) | set(previous):
        path = COMMON / relative
        if not path.is_file():
            continue
        existing = path.read_bytes()
        if relative in previous and digest(existing) != previous[relative]:
            raise RuntimeError(f"Preserve manual header changes before regenerating: {path}")
        if relative not in previous and relative in files and existing != files[relative]:
            raise RuntimeError(f"Unmanaged header already exists: {path}")
    for relative, contents in files.items():
        path = COMMON / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.read_bytes() != contents:
            path.write_bytes(contents)
    for relative in set(previous) - set(files):
        path = COMMON / relative
        if path.is_file():
            path.unlink()
    manifest.write_text(json.dumps({
        "kernel": str(KERNEL.relative_to(ROOT)),
        "kernel_commit": git(KERNEL, "rev-parse", "HEAD"),
        "kernel_dirty": bool(git(KERNEL, "status", "--porcelain")),
        "clang": version,
        "architecture": "arm64",
        "method": "kernel make headers_install; originals retained separately",
        "files": {relative: digest(data) for relative, data in sorted(files.items())},
    }, indent=2) + "\n")
    print(f"Exported {len(files)} kernel UAPI/original headers")


if __name__ == "__main__":
    main()
