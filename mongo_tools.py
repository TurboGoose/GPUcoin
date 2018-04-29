import pymongo
from datetime import datetime


class MongoDataBase:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.coins = self.client.db.coins

    def check_coin(self, string):
        if self.coins.find_one({"string": {"$eq": string}}) is None:
            return True
        return False

    def check_coins(self, coin_status):
        return [(coin, self.check_coin(coin) and status) for coin, status in coin_status]

    def register_coin(self, string, user):
        self.coins.insert_one(
            {
                "string": string,
                "time": datetime.utcnow(),
                "user": user,
            }
        )

    def register_coins(self, coins):
        for coin in coins:
            if self.check_coin(coin):
                user = coin.split("-", maxsplit=1)[0]
                self.register_coin(coin, user)
