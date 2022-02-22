from typing import Any
import pymongo.database
import pymongo.collection
from pymongo import MongoClient

class Collection:
    
    _collection: pymongo.collection.Collection

    def __init__(self, collection: pymongo.collection.Collection):
        self._collection = collection

    def get(self, search: object) -> Any:
        data = self._collection.find_one(search)
        return data

    def get_or_default(self, search: object, fetch: str, default: Any) -> Any:
        data = self.get(search)

        if not data or fetch not in data:
            result = default
        else:
            result = data[fetch]

        return result

    def update(self, search: object, update: object) -> None:
        data = self.get(search)

        if not data:
            self._collection.insert_one(update)
        else:
            self._collection.update_one(search, {
                "$set": update
            })

    def create(self, object: object) -> None:
        self._collection.insert_one(object)

    def delete(self, object: object) -> None:
        self._collection.find_one_and_delete(object)

    def increment(self, search: object, key: str, value: int):
        data = self.get_or_default(search, key, 0)

        self.update(search, {
            key: data + value   
        })

    def decrement(self, search: object, key: str, value: int):
        data = self.get_or_default(search, key, 0)

        self.update(search, {
            key: data - value
        })

    def push(self, search: object, key: str, value: Any):
        update = list(self.get_or_default(search, key, []))
        update.append(value)

        self.update(search, {
            key: update
        })

    def leaderboard(self, filter: object, sort: list[tuple], stop: int) -> list:
        if filter != {}:
            data: Any = self._collection.search(filter)
        else:
            data: Any = self._collection.search()

        data.sort(sort)

        data_list = list(data)

        if len(data_list) > stop:
            result = data_list[slice(stop)] 
        else:
            result = data_list

        return result

    def get_collection(self) -> pymongo.collection.Collection:
        return self._collection


class Database:

    _cluster: Any = None
    _database: Any = None

    def __init__(self, mongo_URI: str, database: str) -> None:
        self._cluster = MongoClient(mongo_URI)
        self._database = self._cluster[database]

    def load_collection(self, collection_name: str) -> Collection:
        collection = self._database[collection_name]
        return Collection(collection)
