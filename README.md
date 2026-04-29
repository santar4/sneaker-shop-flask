# Sneaker Shop — Flask Web Application

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF4D4D?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

A simple yet fully functional online sneaker store built with **Flask**. Users can browse sneakers by categories and add their own sneakers through a convenient form.

## ✨ Features

- Browse sneakers catalog with category filtering
- View detailed information about each sneaker
- Add new sneakers using WTForms with validation
- Admin-like functionality to manage sneakers and categories
- Responsive design with custom Jinja2 template filters
- Clean MVC-like architecture using Blueprints and SQLAlchemy ORM

## 🛠 Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLAlchemy ORM + SQLite
- **Forms**: WTForms
- **Frontend**: Jinja2 templates, HTML5, CSS3
- **Other**: Custom template filters, Blueprints architecture


**1. Home / Catalog page**  
![Home Page](app/static/media/homepage.png)

**2. Sneakers page**  
![Sneakers Page](app/static/media/sneakers_page.png)

**3. Add new sneaker form**  
![Add Sneaker Form](app/static/media/add_sneaker_page.png)

**4. Cart view**  
![Cart](app/static/media/cart_view.png)

## 🚀 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/santar4/Sneaker_shop.git
cd Sneaker_shop


python -m venv venv


# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


pip install -r requirements.txt


python app.py
