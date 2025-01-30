import click
import requests
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from sqlalchemy import String, Numeric, create_engine, select, Text, ForeignKey
from typing import List

def get_coin_price(coins, currencies):
    coin_csv = ','.join(coins)
    currency_csv = ','.join(currencies)

    url = (
        f'https://api.coingecko.com/api/v3/simple/'
        f'price?ids={coin_csv}&vs_currencies={currency_csv}'
    )

    data = requests.get(url).json()

    return data

class Base(DeclarativeBase):
    pass

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())
    investment: Mapped[List['Investment']] = relationship(back_populates='portfolio')

    def __repr__(self) -> str:
        return f'<Portfolio name: {self.name} Portfolio desription: {self.description}>'


class Investment(Base):
    __tablename__='investment'
    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5,2))
    portfolio_id: Mapped[int] = mapped_column(ForeignKey('portfolio.id'))
    portfolio: Mapped['Portfolio'] = relationship(back_populates='investment')

    def __repr__(self) -> str:
         return f'<Investment coin: {self.coin}, currency: {self.currency}, amount {self.amount}>' # no qa
    
#postger connection engine = create_enging('postgresql://user:password@server/db')
# N.B. create db
engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

@click.group()
def cli():
    pass

@click.command(help='View the investments in a porfolio')
def view_portfolio():
    with Session(engine) as session:
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()

        for index, portfolio in enumerate(all_portfolios):
            print(f'{index + 1}: {portfolio.name}')

        portfolio_id = int(input('Select a portfolio: ')) - 1
        portfolio = all_portfolios[portfolio_id]
        investments = portfolio.investment

        coins = set([investment.coin for investment in investments])
        currencies = set([investment.currency for investment in investments])

        coin_prices = get_coin_price(coins, currencies)
        print(f'Investments in {portfolio.name}')
        for index, investment in enumerate(investments):
            coin_price = coin_prices[investment.coin][investment.currency.lower()]
            total_price = float(investment.amount) * coin_price
            print(
                f'{index+ 1}: {investment.coin} {total_price:.2f} {investment.currency}'
            )
        print('Prices provide by CoinGecko')


@click.command(help='Create a new investment ad add it to a portfolio')
@click.option('--coin', prompt=True)
@click.option('--currency', prompt=True)
@click.option('--amount', prompt=True)
def add_investment(coin, currency, amount):
    with Session(engine) as session:
        stmt = select(Portfolio)
        all_portfolios = session.execute(stmt).scalars().all()

        for index, portfolio in enumerate(all_portfolios):
            print(f'{index + 1}: {portfolio.name}')

        portfolio_index = int(input('Select a porfolio: ')) -1
        portfolio = all_portfolios[portfolio_index]

        investment = Investment(coin=coin, currency=currency, amount=amount)
        portfolio.investment.append(investment)

        session.add(portfolio)
        session.commit()
        print(f'Added new {coin} investment to {portfolio.name}')
        
@click.command(help='Create a new portfolio')
@click.option('--name', prompt=True)
@click.option('--description', prompt=True)
def add_portfolio(name, description):
    portfolio = Portfolio(name=name, description=description)
    with Session(engine) as session:
        session.add(portfolio)
        session.commit()
    print(f'Added portfolio: {name}')


@click.command(help='Drop all tables in the database')
def clear_database():
    Base.metadata.drop_all(engine)
    print('Database cleared!')


cli.add_command(clear_database)
cli.add_command(add_portfolio)
cli.add_command(add_investment)
cli.add_command(view_portfolio)

if __name__ == '__main__':
    cli()
