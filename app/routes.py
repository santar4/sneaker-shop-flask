import os
from io import BytesIO

from flask import render_template, flash, redirect, url_for, request, send_file, session
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app import app, User, db, models
from app.models import Sneaker, Category, Cart, CartItem, Order, OrderItem
from app.forms import SignUpForm, LoginForm, SneakerForm


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/add-sneaker', methods=['GET', 'POST'])
def add_sneaker():
    form = SneakerForm()

    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        prize = form.prize.data
        gender = form.gender.data
        category_id = form.category_id.data
        image_file = form.image.data

        if image_file:
            filename = secure_filename(image_file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            image_path = os.path.join(upload_folder, filename)

            if os.path.exists(image_path):
                flash('File already exists. Please choose a different file.', 'danger')
                return redirect(url_for('add_sneaker'))
            try:
                image_file.save(image_path)
            except Exception as e:
                flash(f'An error occurred while saving the file: {str(e)}', 'danger')
                return redirect(url_for('add_sneaker'))

            with open(image_path, 'rb') as f:
                image_data = f.read()

            new_sneaker = Sneaker(
                name=name,
                description=description,
                prize=prize,
                gender=gender,
                category_id=category_id,
                image=image_data
            )
            db.session.add(new_sneaker)
            db.session.commit()

            os.remove(image_path)
            flash('Sneaker added successfully!', 'success')
            if gender.lower() == "male":
                return redirect(url_for('male'))
            else:
                return redirect(url_for('female'))

    return render_template('add_sneaker.html', form=form)


@app.route('/category/<int:category_id>')
def sneakers_by_category(category_id):
    sneakers = Sneaker.query.filter_by(category_id=category_id).all()
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    return render_template('sneakers_by_category.html', sneakers=sneakers, category=category, categories=categories)

@app.route('/all_genders')
def all_genders():
    all_shoes = db.session.execute(
        db.select(models.Sneaker).filter(models.Sneaker.gender.in_(["Male", "Female"]))
    ).scalars().all()
    categories = Category.query.all()
    return render_template("all_shoes_.html", all_sh=all_shoes, categories=categories)

@app.route('/male')
def male():
    all_shoes = db.session.execute(
        db.select(models.Sneaker).filter(models.Sneaker.gender == "Male")
    ).scalars().all()
    categories = Category.query.all()
    return render_template("all_shoes_.html", all_sh=all_shoes, categories=categories)


@app.route('/female')
def female():
    all_shoes = db.session.execute(
        db.select(models.Sneaker).filter(models.Sneaker.gender == "Female")
    ).scalars().all()
    categories = Category.query.all()
    return render_template("all_shoes_.html", all_sh=all_shoes, categories=categories)


@app.route('/details/<int:id_shoes>', methods=['GET', 'POST'])
def details_shoes(id_shoes):
    sneaker = db.get_or_404(Sneaker, id_shoes)
    categories = Category.query.all()
    sizes = ['36', '37', '38', '39', '40', '41', '42', '43', '44', '45']

    if request.method == 'POST':
        selected_size = request.form.get('size')
        quantity = int(request.form.get('quantity', 1))

        if current_user.is_authenticated:
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if cart is None:
                cart = Cart(user_id=current_user.id)
                db.session.add(cart)
                db.session.commit()

            cart_item = CartItem.query.filter_by(cart_id=cart.id, sneaker_id=sneaker.id, size=selected_size).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(cart_id=cart.id, sneaker_id=sneaker.id, size=selected_size, quantity=quantity)
                db.session.add(cart_item)
            db.session.commit()
            flash(f'Добавлена {quantity} пара кросівок за розміром {selected_size} до Кошика!', 'success')
        else:
            flash('You need to log in to add items to your cart.', 'danger')

        return redirect(url_for('details_shoes', id_shoes=sneaker.id))

    return render_template("details_shoes.html", sneaker=sneaker, categories=categories, sizes=sizes)


@app.route('/cart/')
@login_required
def view_cart():
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        total = sum(item.quantity * float(item.sneaker.prize) for item in cart_items)

    flash('Замовлення створено', 'success')
    return render_template('cart.html', cart=cart, items=cart_items, total=total)


@app.route('/create_order', methods=['POST'])
@login_required
def create_order():
    cart = Cart.query.filter_by(user_id=current_user.id).first()

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()

        total = sum(item.quantity * float(item.sneaker.prize) for item in cart_items)

        order = Order(user_id=current_user.id, total=total)
        db.session.add(order)
        db.session.commit()

        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                sneaker_id=item.sneaker.id,
                quantity=item.quantity,
                price=float(item.sneaker.prize)
            )
            db.session.add(order_item)

        db.session.commit()

        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

    flash('Замовлення створено', 'success')
    return redirect(url_for('view_cart'))


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user:
            flash("User currently exists")
            return redirect(url_for("login"))
        new_user = User(
            nickname=form.nickname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("user/signup.html", form=form, title="Signup")


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.query(User).where(User.nickname == form.nickname.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash("Invalid nickname or password")

    return render_template("user/login.html", form=form, title="Login")


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
