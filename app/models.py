from datetime import datetime, timezone

from sqlalchemy.dialects.mysql import DATETIME

from app import db
from flask_login import UserMixin
from sqlalchemy import String, Integer, Column, ForeignKey, Float, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
import sqlalchemy as sa
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(25))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[int] = mapped_column(String(50))
    carts = relationship('Cart', back_populates='user')

    def __repr__(self):
        return f"User: {self.nickname}"

    def __str__(self):
        return self.nickname.capitalize()


class Sneaker(db.Model):
    __tablename__ = "sneakers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(50), unique=True)
    prize: Mapped[float] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(25))

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', back_populates='sneakers')
    image: Mapped[bytes] = mapped_column(sa.LargeBinary)

    def __repr__(self):
        return f"<Sneaker(name={self.name})>"

class Category(db.Model):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    parent_id = Column(Integer, ForeignKey('categories.id'))

    parent = relationship('Category', remote_side=[id], back_populates='children')
    children = relationship('Category', back_populates='parent')
    sneakers = relationship('Sneaker', back_populates='category')

    def __repr__(self):
        return f"<Category(name={self.name})>"



class Cart(db.Model):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user = relationship('User', back_populates='carts')
    items = relationship('CartItem', back_populates='cart')

    def __repr__(self):
        return f"<Cart {self.id}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'), nullable=False)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey('sneakers.id'), nullable=False)

    size: Mapped[str] = mapped_column(String(5), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart = relationship('Cart', back_populates='items')
    sneaker = relationship('Sneaker')

    def __repr__(self):
        return f"<CartItem {self.id}>"

class Order(db.Model):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    total: Mapped[float] = mapped_column(Float, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    items = relationship('OrderItem', back_populates='order')

class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), nullable=False)
    sneaker_id: Mapped[int] = mapped_column(ForeignKey('sneakers.id'), nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order = relationship('Order', back_populates='items')
    sneaker = relationship('Sneaker')

def init_categories():
        categories = [
            "Літо",
            "Осінь",
            "Весна",
            "Зима",
            "Демісезон"
        ]
        for category_name in categories:
            category_exist = db.session.execute(
            db.select(Category).where(Category.name == category_name)
        ).scalar_one_or_none()
            if not category_exist:
                category = Category(name=category_name, parent_id=None)
                db.session.add(category)
                print(f'Додано категорію {category_name}')
            else:
                print(f'Категорія вже існує{category_name}')

        db.session.commit()