import requests
import click
import sqlite3
import datetime
import csv
from dataclasses import dataclass


CREATE_INVESTMENT_SQL = '''
    CREATE TABLE investments_full(
        coin_id TEXT NOT NULL,
        currency TEXT NOT NULL,
        amount REAL NOT NULL,
        sell BOOLEAN NOT NULL,
        time datetime NOT NULL
    );
'''


@dataclass
class Investment:
    coin_id: str
    currency: str
    amount: float
    sell: bool
    data: datetime.datatime

    def compute_value(self) -> float:
        return self.amount * get_coin_price(self.coin_id, self.currency)


def investment_row_factory(_, row):
    return Investment(
            coin_id=row[0],
            currency=row[1],
            amount=row[2],
            sell=bool(row[3]),
            date=datetime.datetime.strptime(
                row[4],
                '%Y-%m-%d %H:%M:%S.%f')
        )


def get_coin_price(coin_id, currency):
    url = (
        f'https://api.coingecko.com/api/v3/simple/'
        f'price?ids={coin_id}&vs_currencies={currency}'
    )
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price


@click.group()
def cli():
    pass


@click.command()
@click.option('--coin_id', default='bitcoin')
@click.option('--currency', default='usd')
def show_coin_price(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    print(f'The price of {coin_id} is {coin_price:.2f} {currency.upper()}')


@click.command()
@click.option('--coin_id', default='bitcoin')
@click.option('--currency', default='usd')
def get_investments_value(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    sql = """SELECT amount
    FROM investments_full
    WHERE coin_id=?
    AND currency=?
    AND sell=?;
    """
    print(coin_price)
    buy_result = cursor.execute(sql, (coin_id, currency, False)).fetchall()
    sell_result = cursor.execute(sql, (coin_id, currency, True)).fetchall()
    buy_amount = sum([row[0] for row in buy_result])
    sell_amount = sum([row[0] for row in sell_result])
    total = buy_amount - sell_amount
    total_price = total * coin_price

    print(
        f'You own a total of {total} {coin_id}'
        f'worth {total_price} {currency.upper()}'
    )


@click.command()
@click.option('--coin_id')
@click.option('--currency')
@click.option('--amount', type=float)
@click.option('--sell', is_flag=True)
def add_investment(coin_id, currency, amount, sell):
    print(coin_id)
    sql = 'INSERT INTO investments_full VALUES (?, ?, ?, ?, ?);'
    values = (coin_id, currency, amount, sell, datetime.datetime.now())
    cursor.execute(sql, values)
    database.commit()

    if sell:
        print(f'Added sell of {amount} {coin_id}')
    else:
        print(f'Added buy of {amount} {coin_id}')


@click.command()
@click.option('--csv_file')
def import_investments(csv_file):
    with open(csv_file, 'r') as f:
        rdr = csv.reader(f, delimiter=',')
        rows = list(rdr)
        sql = 'INSERT INTO investments_full VALUES(?, ?, ?, ?, ?);'

        cursor.executemany(sql, rows)
        database.commit()

        print(f'Imported {len(rows)} investments from {csv_file}')


cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investments_value)
cli.add_command(import_investments)


if __name__ == '__main__':
    database = sqlite3.connect('/home/radi/Projects/DataLab/data/data.db')
    database.row_factory = investement_row_factory
    cursor = database.cursor()
    # cursor.execute(CREATE_INVESTMENT_SQL)

    cli()

