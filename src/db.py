from typing import Dict, Generator
import pymongo


class Db:
    def __init__(self) -> None:
        client = pymongo.MongoClient("localhost", 27017)
        self.collection = client["keebo"]["keycounts"]

    def update_count(self, key: str) -> None:
        """ 
        Update the count for the given key.
        Create new entry if key doesn't exist.
        """
        self.collection.update_one(
            {"key_name": key}, {"$inc": {"count": 1}}, upsert=True
        )

    def get_stats(self) -> Generator[Dict[str, int], None, None]:
        all_keys = ({entry["key_name"]: entry["count"]} for entry in self.collection.find())
        return all_keys


