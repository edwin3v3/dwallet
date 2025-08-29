from sqlalchemy import Integer, Float, String, DateTime, Text, create_engine, Column, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable= False)
    email = Column(String(50), nullable = False)
    wallets = relationship('Wallets', back_populates = 'users')



class Wallets(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    balance = Column(Float, nullable = False, default = 0.0)
    
    users = relationship('Users', back_populates = 'wallets')
    sent_transactions= relationship('Transactions',back_populates = 'sender_wallet', foreign_keys = "Transactions.sender_wallet_id")
    received_transactions = relationship('Transactions', back_populates = 'receiver_wallet', foreign_keys = "Transactions.receiver_wallet_id")



class Transactions(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key = True)
    sender_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False, index=True)
    receiver_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(Text)
    amount = Column(Float, nullable = False)

    sender_wallet = relationship("Wallets", foreign_keys=[sender_wallet_id], back_populates = "sent_transactions")
    receiver_wallet = relationship("Wallets", foreign_keys=[receiver_wallet_id], back_populates = "received_transactions")


engine = create_engine("sqlite:///dwallet.db")
Base.metadata.create_all(bind= engine)
Session = sessionmaker(bind=engine)
session = Session()

