import collections
import json
import re

import keyboard

used_keys: collections.Counter = collections.Counter()

def get_positional_keys_mapping():
    mapping = {}
    with open("/usr/include/linux/input-event-codes.h") as fh:
        keycode_definitions = fh.read()

    pattern = "#define\s+KEY_((?:LEFT|RIGHT)(?:CTRL|SHIFT))\s+(\d+)"
    for key, scan_code in re.findall(pattern, keycode_definitions, re.MULTILINE):
        mapping[scan_code] = key.lower()
    return mapping


def register_key(key: keyboard.KeyboardEvent) -> None:
    if key.name in ("ctrl", "shift"):
        used_keys.update([f"{key.name}_{key.scan_code}"])
    else:
        used_keys.update([key.name])
    print(used_keys)

def main() -> None:
    keyboard.on_press(register_key)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Saving before exiting..")
        with open("key_stats.json", "w") as fh:
            fh.write(json.dumps(dict(used_keys)))
        print("Done! Byeeee")
        exit()


if __name__ == "__main__":
    main()
