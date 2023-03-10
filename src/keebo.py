import logging
import re
from typing import Dict

import keyboard

import db


class KeyCounter:
    def __init__(self, database: db.Db) -> None:
        self.positional_keys = KeyCounter._get_positional_keys_mapping()
        self.db = database

    @classmethod
    def _get_positional_keys_mapping(cls) -> Dict[int, str]:
        """
        Returns a `key: scan_code` mapping of positional key for shift and ctrl.
        """
        mapping = {}
        with open("/usr/include/linux/input-event-codes.h") as fh:
            keycode_definitions = fh.read()

        pattern = r"#define\s+KEY_((?:LEFT|RIGHT)(?:CTRL|SHIFT))\s+(\d+)"
        for key, scan_code in re.findall(pattern, keycode_definitions, re.MULTILINE):
            mapping[int(scan_code)] = key.lower()
        return mapping

    def register_key(self, key: keyboard.KeyboardEvent) -> None:
        if not key.name:
            self.db.update_count("unknown")
        else:
            # The keyboard library doesn't discern between left and right ctrl/shift
            if key.name in ("ctrl", "shift"):
                try:
                    pressed_key = self.positional_keys[key.scan_code]
                except KeyError:
                    print(f"Couldn't figure out if it was left or right {key.name}")
                    pressed_key = key.name
                self.db.update_count(pressed_key)
            else:
                self.db.update_count(key.name)

    @property
    def key_stats(self) -> list[dict[str, int]]:
        return list(self.db.get_stats())


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Connecting to database...")
    database = db.Db()

    key_counter = KeyCounter(database)
    keyboard.on_press(key_counter.register_key)

    logging.info("Listening to key presses...")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        logging.info("Received exit signal")
        print(key_counter.key_stats)
        logging.info("Byeee!")
        exit()


if __name__ == "__main__":
    main()
