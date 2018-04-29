import pymongo
from datetime import datetime


class MongoDataBase:
    def __init__(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        self.coins = self.client.db.coins
        self.transactions = self.client.db.transactions

    def check_coin(self, string):
        if self.coins.find_one({"string": {"$eq": string}}) is None:
            return True
        return False

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

    def check_coins(self, coin_status):
        return [(coin, self.check_coin(coin) and status) for coin, status in coin_status]

    def check_user_balance(self, user):
        try:
            return self.coins.find({"user": {"$eq": user}}).count()
        except Exception as err:
            print(">>> User balance error :", err)
            return 0

    def register_transaction(self, coin, user_from, user_to):
        self.transactions.insert_one(
            {
                "coin": coin,
                "from": user_from,
                "to": user_to,
                "time": datetime.utcnow()
            }
        )

    def send_coins(self, user_from, user_to, num_coins):
        coins_id = [c["_id"] for c in self.coins.find({"user": {"$eq": user_from}})[:num_coins]]
        for coin_id in coins_id:
            self.coins.update({"_id": coin_id}, {"$set": {"user": user_to}})
            self.register_transaction(coin_id, user_from, user_to)
