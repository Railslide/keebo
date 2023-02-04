import collections
import json
import re

from typing import Dict, Optional

import keyboard


class KeyCounter:
    def __init__(self):
        self.positional_keys = KeyCounter._get_positional_keys_mapping()
        self._used_keys = collections.Counter()

    @classmethod
    def _get_positional_keys_mapping(cls) -> Dict[int, str]:
        """
        Returns a `key: scan_code` mapping of positional key for shift and ctrl.
        """
        mapping = {}
        with open("/usr/include/linux/input-event-codes.h") as fh:
            keycode_definitions = fh.read()

        pattern = "#define\s+KEY_((?:LEFT|RIGHT)(?:CTRL|SHIFT))\s+(\d+)"
        for key, scan_code in re.findall(pattern, keycode_definitions, re.MULTILINE):
            mapping[int(scan_code)] = key.lower()
        return mapping

    def register_key(self, key: keyboard.KeyboardEvent) -> None:
        # The keyboard library doesn't discern between left and right ctrl/shift
        if key.name in ("ctrl", "shift"):
            try:
                pressed_key = self.positional_keys[key.scan_code]
            except KeyError:
                print(f"Couldn't figure out if it was left or right {key.name}")
                pressed_key = key.name
            self._used_keys.update([pressed_key])
        else:
            self._used_keys.update([key.name])
        print(self._used_keys)

    @property
    def used_keys(self):
        return self._used_keys


def main() -> None:
    key_counter = KeyCounter()
    keyboard.on_press(key_counter.register_key)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Saving before exiting..")
        with open("key_stats.json", "w") as fh:
            fh.write(json.dumps(dict(key_counter.used_keys)))
        print("Done! Byeeee")
        exit()


if __name__ == "__main__":
    main()
