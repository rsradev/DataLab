from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, Session, relationship
from sqlalchemy import String, Numeric, create_engine, Text, ForeignKey
from typing import List


class Base(DeclarativeBase):
    pass


class Portfolio(Base):
    __tablename__ = 'portfolio'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())
    investment: Mapped[List['Investment']] = relationship(
        back_populates='portfolio'
    )

    def __repr__(self) -> str:
        return (
                f'<Portfolio name: {self.name}'
                f'Portfolio desription: {self.description}>'
            )


class Investment(Base):
    __tablename__ = 'investment'
    id: Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5, 2))
    portfolio_id: Mapped[int] = mapped_column(ForeignKey('portfolio.id'))
    portfolio: Mapped['Portfolio'] = relationship(back_populates='investment')

    def __repr__(self) -> str:
        return (
                f'<Investment coin: {self.coin},'
                f'currency: {self.currency}, amount {self.amount}>'
            )


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

portfolio_1 = Portfolio(name='Raddys Portfolio',
                        description='This is my portfolio')
portfolio_2 = Portfolio(name='Bobis Portfolio',
                        description='This is my portfolio')

bitcoin = Investment(coin='bitcoin', currency='USD', amount=3.0)
ethereum = Investment(coin='ethereum', currency='GBP', amount=10.0)
dogecoin = Investment(coin='dogecoin', currency='EUR', amount=213.0)

bitcoin.portfolio = portfolio_1
portfolio_2.investment.extend([ethereum, dogecoin])

with Session(engine) as session:
    # session.add(bitcoin)
    session.add(portfolio_2)
    session.commit()
