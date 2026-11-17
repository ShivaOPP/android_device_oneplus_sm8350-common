#!/usr/bin/env python3
"""Export the selected kernel's real UAPI for calcite's kernel_headers modules."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
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
    os.environ["ANDROID_BUILD_TOP"] = str(ROOT)
    sys.path.insert(0, str(ROOT / "bionic/libc/kernel/tools"))
    import clean_header

    manifest = COMMON / "kernel-headers.json"
    prior = json.loads(manifest.read_text()) if manifest.exists() else {}
    previous = prior.get("files", {})
    active_prefixes = ("uapi/kernel-headers/", "kernel-headers/arm/", "kernel-headers/arm64/")
    # Keep the earlier raw snapshot and original source headers for comparison.
    # They are no longer exported. Never overwrite a manually edited snapshot.
    retained = {name for name in previous if not name.startswith(active_prefixes)}
    files: dict[str, bytes] = {}
    for name in retained:
        path = COMMON / name
        if not path.is_file() or digest(path.read_bytes()) != previous[name]:
            raise RuntimeError(f"Preserve missing/edited original snapshot: {path}")
        files[name] = path.read_bytes()

    exports: dict[str, dict[str, bytes]] = {}
    techpack_roots = {
        p.name for uapi in (KERNEL / "techpack").glob("*/include/uapi")
        for p in uapi.iterdir() if p.is_dir()
    }
    for arch in ("arm", "arm64"):
        build = gitdir / f"porsche-uapi-build-{arch}"
        install = gitdir / f"porsche-uapi-install-{arch}"
        build.mkdir(exist_ok=True)
        install.mkdir(exist_ok=True)
        subprocess.run(
            [
                "make", "-C", str(KERNEL), f"O={build}", f"ARCH={arch}",
                f"HOSTCC={clang}", f"CC={clang}", f"INSTALL_HDR_PATH={install}",
                "headers_install", "-j48",
            ],
            check=True,
        )
        exports[arch] = {}
        for header in sorted((install / "include").rglob("*.h")):
            relative = header.relative_to(install / "include")
            logical = f"asm-{arch}/{relative}" if relative.parts[0] == "asm" else str(relative)
            saved_statics = clean_header.kernel_known_generic_statics
            if relative.parts[0] in techpack_roots:
                # Bionic normally strips most inline functions; display/media
                # and audio UAPI contains userspace layout helpers we must keep.
                names = set(re.findall(r"\b([A-Za-z_]\w*)\s*\(", header.read_text()))
                clean_header.kernel_known_generic_statics = saved_statics | names
            try:
                cleaned = clean_header.cleanupFile(str(relative), str(header), logical)
            finally:
                clean_header.kernel_known_generic_statics = saved_statics
            if cleaned is None:
                raise RuntimeError(f"Failed to sanitize {arch} UAPI: {header}")
            exports[arch][str(relative)] = cleaned.encode()

    for name in sorted(set(exports["arm"]) | set(exports["arm64"])):
        arm = exports["arm"].get(name)
        arm64 = exports["arm64"].get(name)
        if arm is not None and arm == arm64:
            files[f"uapi/kernel-headers/{name}"] = arm
        else:
            for arch in ("arm", "arm64"):
                if name in exports[arch]:
                    files[f"kernel-headers/{arch}/{name}"] = exports[arch][name]

    files["kernel-headers.LICENSE"] = (KERNEL / "COPYING").read_bytes()
    originals = [KERNEL / "include/uapi", KERNEL / "arch/arm/include/uapi", KERNEL / "arch/arm64/include/uapi"]
    originals.extend(sorted((KERNEL / "techpack").glob("*/include/uapi")))
    for directory in originals:
        if not directory.is_dir():
            continue
        for header in sorted(directory.rglob("*.h")):
            relative = header.relative_to(KERNEL)
            files[str(Path("original-kernel-headers") / relative)] = header.read_bytes()

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
        "architectures": ["arm", "arm64"],
        "method": "make headers_install per architecture, Bionic cleanup preserving techpack inline helpers, shared/per-arch exports; raw snapshots retained",
        "bionic_cleaner_commit": git(ROOT / "bionic", "rev-parse", "HEAD"),
        "active_exports": ["uapi/kernel-headers", "kernel-headers/arm", "kernel-headers/arm64"],
        "retained_previous_exports": sorted(retained),
        "files": {relative: digest(data) for relative, data in sorted(files.items())},
    }, indent=2) + "\n")
    print(f"Exported {len(files)} kernel UAPI/original headers")


if __name__ == "__main__":
    main()
