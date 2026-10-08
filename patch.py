import argparse
import re
import struct
from datetime import datetime
from pathlib import Path

_PATH_DATA = """
006A9004 mob/skins/Biome2/mushroom_tamer.png
006A907C mob/skins/Biome2/mushroom_archer_slim.png
006A9104 mob/skins/Biome2/mushroom_brawler_slim.png
006A9184 mob/skins/Biome2/mushroom_brewer.png
006A91E4 mob/skins/Biome2/mushroom_engineer.png
006A9268 mob/skins/Biome2/mushroom_explorer_slim.png
006A92E8 mob/skins/Biome2/mushroom_farmer_slim.png
006A9370 mob/skins/Biome2/mushroom_forager.png
006A93D0 mob/skins/Biome2/mushroom_griefer.png
006A944C mob/skins/Biome2/mushroom_hunter_slim.png
006A94C8 mob/skins/Biome2/mushroom_miner.png
006A9548 mob/skins/Biome2/mushroom_shroom_glutton.png
006A95A4 mob/skins/Biome2/nether_tamer_slim.png
006A95FC mob/skins/Biome2/nether_archer.png
006A9674 mob/skins/Biome2/nether_banished.png
006A96CC mob/skins/Biome2/nether_brawler.png
006A9740 mob/skins/Biome2/nether_brewer.png
006A97B8 mob/skins/Biome2/nether_engineer.png
006A9834 mob/skins/Biome2/nether_explorer.png
006A98BC mob/skins/Biome2/nether_extinguisher.png
006A993C mob/skins/Biome2/nether_farmer.png
006A9990 mob/skins/Biome2/nether_griefer_slim.png
006A9A0C mob/skins/Biome2/nether_hunter.png
006A9A7C mob/skins/Biome2/nether_miner.png
006A9B30 mob/skins/StoryMode/JesseF_T0.png
006A9B80 mob/skins/StoryMode/JesseF_T1.png
006A9BD0 mob/skins/StoryMode/JesseF_T2.png
006A9C38 mob/skins/StoryMode/JesseM_T0.png
006A9C88 mob/skins/StoryMode/JesseM_T1.png
006A9CD8 mob/skins/StoryMode/JesseM_T2.png
006A9D58 mob/skins/StoryMode/JesseF_T0_Armored.png
006A9DE0 mob/skins/StoryMode/JesseF_T1_Armored.png
006A9E68 mob/skins/StoryMode/JesseF_T2_Armored.png
006A9EF0 mob/skins/StoryMode/JesseM_T0_Armored.png
006A9F54 mob/skins/StoryMode/JesseM_T1_Armored.png
006A9FB8 mob/skins/StoryMode/JesseM_T2_Armored.png
006AA020 mob/skins/StoryMode/Axel.png
006AA094 mob/skins/StoryMode/Axel_Armored.png
006AA10C mob/skins/StoryMode/Ellegaard.png
006AA190 mob/skins/StoryMode/Ellie_armored.png
006AA200 mob/skins/StoryMode/Gabriel.png
006AA25C mob/skins/StoryMode/Ivor.png
006AA2C0 mob/skins/StoryMode/Lukas.png
006AA324 mob/skins/StoryMode/Magnus.png
006AA3A0 mob/skins/StoryMode/Magnus_armored.png
006AA40C mob/skins/StoryMode/olivia.png
006AA488 mob/skins/StoryMode/Olivia_Armored.png
006AA4F4 mob/skins/StoryMode/Petra.png
006AA568 mob/skins/StoryMode/Petra_armored.png
006AA5D4 mob/skins/StoryMode/Soren.png
006AA628 mob/skins/StoryMode/Soren_Armored.png
006AA6DC mob/skins/Redstone/Redstone_Artisan_Slim.png
006AA738 mob/skins/Redstone/Redstone_Composer.png
006AA7A8 mob/skins/Redstone/Redstone_Experimenter_Slim.png
006AA804 mob/skins/Redstone/Redstone_Electrician.png
006AA870 mob/skins/Redstone/Redstone_Chemist.png
006AA8DC mob/skins/Redstone/Redstone_Trapper.png
006AA944 mob/skins/Redstone/Redstone_Miner_Slim.png
006AA9B0 mob/skins/Redstone/Redstone_Programmer_Slim.png
006AAA20 mob/skins/Redstone/Redstone_Golem.png
006AAA90 mob/skins/Redstone/Redstone_Prospector_Slim.png
006AAB04 mob/skins/Redstone/Redstone_Architect_Slim.png
006AAB78 mob/skins/Redstone/Redstone_Rail_Rider_Slim.png
006AABD0 mob/skins/Redstone/Redstone_TNT_Technician.png
006AAC2C mob/skins/Redstone/Redstone_Hoarder.png
006AAC80 mob/skins/Redstone/Redstone_Tinkerer.png
006AAD24 mob/skins/JTTW/Red_Boy.png
006AAD80 mob/skins/JTTW/guanyin_slim.png
006AADE4 mob/skins/JTTW/blackwinddemon.png
006AAE5C mob/skins/JTTW/bull_demon_king.png
006AAECC mob/skins/JTTW/Jade_Emperor.png
006AAF38 mob/skins/JTTW/Baigujing_Slim.png
006AAFB4 mob/skins/JTTW/Many_Eyed_Demon_Lord.png
006AB034 mob/skins/JTTW/Scorpion_Demon_Slim.png
006AB0B0 mob/skins/JTTW/lady_earth_flow_slim.png
006AB120 mob/skins/JTTW/monkeyking.png
006AB198 mob/skins/JTTW/princess_iron_fan_slim.png
006AB20C mob/skins/JTTW/sha_wujing.png
006AB278 mob/skins/JTTW/spider_demon_slim.png
006AB2E4 mob/skins/JTTW/xuangzang_slim.png
006AB34C mob/skins/JTTW/zhu_bajie.png
006AB3E0 mob/skins/Festive/sweater_steve.png
006AB434 mob/skins/Festive/Festive_Sweater_Alex_Slim.png
006AB4A0 mob/skins/Festive/santa.png
006AB4E4 mob/skins/Festive/mrs_claus_slim.png
006AB550 mob/skins/Festive/rudolph.png
006AB5B4 mob/skins/Festive/greenelf.png
006AB624 mob/skins/Festive/father_christmas.png
006AB69C mob/skins/Festive/mother_christmas.png
006AB700 mob/skins/Festive/tomte.png
006AB760 mob/skins/Festive/Festive_Snow_Suit_Kid.png
006AB7DC mob/skins/Festive/Festive_Pajama_Kid_Slim.png
006AB83C mob/skins/Festive/Festive_Ski_Bibs_Slim.png
006AB894 mob/skins/Festive/parka_steve.png
006AB90C mob/skins/Festive/gingerbread.png
006AB96C mob/skins/Festive/gingerbread_creeperSlim.png
006AB9EC mob/skins/PVP_Warriors/tundra_tamer_slim.png
006ABA4C mob/skins/PVP_Warriors/tundra_archer.png
006ABAA8 mob/skins/PVP_Warriors/tundra_brawler.png
006ABB04 mob/skins/PVP_Warriors/tundra_brewer_slim.png
006ABB64 mob/skins/PVP_Warriors/tundra_engineer.png
006ABBC0 mob/skins/PVP_Warriors/tundra_griefer_slim.png
006ABC20 mob/skins/PVP_Warriors/tundra_hunter_slim.png
006ABC7C mob/skins/PVP_Warriors/tundra_stray.png
006ABCD4 mob/skins/PVP_Warriors/Forest_Griefer_Slim.png
006ABD34 mob/skins/PVP_Warriors/Forest_Archer.png
006ABD90 mob/skins/PVP_Warriors/Forest_Brawler.png
006ABDEC mob/skins/PVP_Warriors/Forest_Brewer.png
006ABE48 mob/skins/PVP_Warriors/Forest_Engineer_Slim.png
006ABEA8 mob/skins/PVP_Warriors/Forest_Hunter_Slim.png
006ABF04 mob/skins/PVP_Warriors/Forest_Tamer_Slim.png
006ABF68 mob/skins/PVP_Warriors/Forest_Woodbeast_Slim.png
006ABFC8 mob/skins/PVP_Warriors/Desert_Tamer_Slim.png
006AC028 mob/skins/PVP_Warriors/Desert_Archer_Slim.png
006AC088 mob/skins/PVP_Warriors/Desert_Brawler_Slim.png
006AC0E8 mob/skins/PVP_Warriors/Desert_Brewer.png
006AC144 mob/skins/PVP_Warriors/Desert_Engineer.png
006AC1A0 mob/skins/PVP_Warriors/Desert_Griefer.png
006AC1FC mob/skins/PVP_Warriors/Desert_Hunter.png
006AC250 mob/skins/PVP_Warriors/Desert_Husk_Slim.png
006AC2CC mob/skins/Halloween/zombie_costume.png
006AC328 mob/skins/Halloween/iron_golem_costume.png
006AC384 mob/skins/Halloween/creeper_costume.png
006AC3D4 mob/skins/Halloween/cow_costume.png
006AC428 mob/skins/Halloween/enderman_costume.png
006AC480 mob/skins/Halloween/ghast_costume.png
006AC4DC mob/skins/Halloween/mooshroom_costume.png
006AC538 mob/skins/Halloween/ocelot_costume.png
006AC588 mob/skins/Halloween/pig_costume.png
006AC5E0 mob/skins/Halloween/pink_sheep_costume.png
006AC644 mob/skins/Halloween/rainbow_sheep_costume.png
006AC6A4 mob/skins/Halloween/skeleton_costume.png
006AC704 mob/skins/Halloween/snow_golem_costume.png
006AC760 mob/skins/Halloween/spider_costume.png
006AC7C0 mob/skins/Halloween/zombie_pigman_costume.png
006AC810 mob/skins/CityFolk/Barmaid_slim.png
006AC854 mob/skins/CityFolk/Barman.png
006AC890 mob/skins/CityFolk/Baron.png
006AC8D4 mob/skins/CityFolk/Baroness.png
006AC91C mob/skins/CityFolk/Blacksmith.png
006AC95C mob/skins/CityFolk/Baker.png
006AC99C mob/skins/CityFolk/ButcherSkin.png
006AC9E4 mob/skins/CityFolk/Carpenter.png
006ACA24 mob/skins/CityFolk/Chef.png
006ACA60 mob/skins/CityFolk/HolyMan.png
006ACAA4 mob/skins/CityFolk/HolyWoman.png
006ACAE8 mob/skins/CityFolk/Jailer.png
006ACB24 mob/skins/CityFolk/King.png
006ACB5C mob/skins/CityFolk/Mage.png
006ACB98 mob/skins/CityFolk/Postman.png
006ACBD4 mob/skins/CityFolk/Queen.png
006ACC18 mob/skins/CityFolk/Shoemaker.png
006ACC60 mob/skins/CityFolk/Victorian.png
006ACCA8 mob/skins/CityFolk/Watchman.png
006ACCF0 mob/skins/CityFolk/WeaponSmith.png
006ACD58 mob/skins/TownFolk/Castaway.png
006ACD98 mob/skins/TownFolk/Bandit_slim.png
006ACDD8 mob/skins/TownFolk/Bard.png
006ACE14 mob/skins/TownFolk/FarmerSkin.png
006ACE5C mob/skins/TownFolk/Forester.png
006ACEA0 mob/skins/TownFolk/Gardener.png
006ACEDC mob/skins/TownFolk/Mime.png
006ACF14 mob/skins/TownFolk/Miner.png
006ACF50 mob/skins/TownFolk/Monk.png
006ACF8C mob/skins/TownFolk/OldLady.png
006ACFCC mob/skins/TownFolk/OldMan.png
006AD00C mob/skins/TownFolk/Peasant.png
006AD048 mob/skins/TownFolk/Rogue.png
006AD090 mob/skins/TownFolk/Shopkeeper_slim.png
006AD0DC mob/skins/TownFolk/StrongMan.png
006AD11C mob/skins/TownFolk/Thief.png
006AD160 mob/skins/TownFolk/TownCrier.png
006AD1AC mob/skins/TownFolk/Townswoman.png
006AD1F0 mob/skins/TownFolk/Vagrant.png
006AD22C mob/skins/TownFolk/Witch_slim.png
"""


def _path_patch(line):
    address, path = line.split(" ", 1)
    old = path.encode("ascii") + b"\0"
    new = b"mob/alex.png\0" if "slim" in path.lower() else b"mob/steve.png\0"
    return int(address, 16), old, new.ljust(len(old), b"\0")


PATCHES = tuple(_path_patch(line) for line in _PATH_DATA.strip().splitlines()) + (
    (0x316750, b"\x02\xd1", b"\x15\xe0"),
)


def load_segments(data):
    if data[:6] != b"\x7fELF\x01\x01" or len(data) < 52:
        raise ValueError("Expected a 32-bit little-endian ELF")
    header = struct.unpack_from("<16sHHIIIIIHHHHHH", data)
    if header[1:3] != (3, 40):  # ET_DYN, EM_ARM
        raise ValueError("Expected an ARM shared object")
    phoff, phentsize, phnum = header[5], header[9], header[10]
    if phentsize < 32 or phoff + phentsize * phnum > len(data):
        raise ValueError("Invalid ELF program headers")
    segments = [struct.unpack_from("<IIIIIIII", data, phoff + i * phentsize)
                for i in range(phnum)]
    if not any(segment[0] == 1 for segment in segments):
        raise ValueError("ELF has no LOAD segment")
    return segments


def file_offset(segments, address, size, total_size):
    for kind, offset, va, _pa, file_size, _mem_size, _flags, _align in segments:
        if kind == 1 and va <= address and address + size <= va + file_size:
            result = offset + address - va
            if result + size <= total_size:
                return result
    raise ValueError(f"Address {address:#x} is not file-backed")


def check_bytes(current, old, new, address):
    if current is None or len(current) != len(old) or any(
        value not in (before, after) for value, before, after in zip(current, old, new)
    ):
        raise ValueError(f"Unexpected bytes at {address:#x}; analyze this SO before patching")


def patch_library(source):
    segments = load_segments(source)
    patched = bytearray(source)
    changed = 0
    for address, old, new in PATCHES:
        offset = file_offset(segments, address, len(old), len(source))
        current = source[offset:offset + len(old)]
        check_bytes(current, old, new, address)
        changed += sum(a != b for a, b in zip(current, new))
        patched[offset:offset + len(old)] = new
    if re.search(rb"mob/skins/[^\x00]+\.png\x00", patched):
        raise ValueError("An unlisted skin PNG path remains; analyze this SO before removing PNGs")
    return bytes(patched), changed


def build(source):
    if source.name != "libminecraftpe.so":
        raise ValueError("Input must be named libminecraftpe.so")
    patched, changed = patch_library(source.read_bytes())
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = source.parent / f"SkinPrune_{stamp}_libminecraftpe.so"
    try:
        with destination.open("xb") as stream:
            stream.write(patched)
    except FileExistsError:
        raise FileExistsError(f"Output already exists: {destination}; run again after one second") from None
    print(f"Output: {destination}\nChanged bytes: {changed}")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to libminecraftpe.so")
    args = parser.parse_args()
    try:
        build(args.source)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
