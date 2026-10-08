import importlib.util
from pathlib import Path

import ida_auto
import ida_bytes
import ida_kernwin
import ida_nalt


def load_patch():
    source = Path(__file__).with_name("patch.py")
    if not source.is_file():
        raise RuntimeError(f"Missing companion script: {source}")
    spec = importlib.util.spec_from_file_location("_skinprune_patch", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    ida_auto.auto_wait()
    if ida_nalt.get_imagebase() != 0:
        raise RuntimeError("Expected IDA image base 0")
    patch = load_patch()
    source = Path(ida_nalt.get_input_file_path()).read_bytes()
    patch.patch_library(source)  # Validate all on-disk sites before any IDA edit.
    segments = patch.load_segments(source)
    planned = []
    for address, old, new in patch.PATCHES:
        offset = patch.file_offset(segments, address, len(old), len(source))
        original = bytes(ida_bytes.get_original_byte(address + i) for i in range(len(old)))
        if original != source[offset:offset + len(old)]:
            raise RuntimeError(f"IDA and input SO differ at {address:#x}")
        patch.check_bytes(ida_bytes.get_bytes(address, len(old)), old, new, address)
        planned.append((address, new))

    for address, new in planned:
        ida_bytes.patch_bytes(address, new)
        if ida_bytes.get_bytes(address, len(new)) != new:
            raise RuntimeError(f"IDA patch failed at {address:#x}")
    ida_kernwin.msg("MCPE skin patch applied to IDA database: 175 paths + 1 branch.\n")
    ida_kernwin.msg("Use Edit > Patch program > Apply patches to input file on the copied SO.\n")


if __name__ == "__main__":
    run()
