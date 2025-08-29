class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)

    sender_id = Column(Integer, ForeignKey("wallets.id"))
    receiver_id = Column(Integer, ForeignKey("wallets.id"))

    sender_wallet = relationship(
        "Wallets",
        back_populates="sent_transactions",
        foreign_keys=[sender_id]
    )

    receiver_wallet = relationship(
        "Wallets",
        back_populates="received_transactions",
        foreign_keys=[receiver_id]
    )
