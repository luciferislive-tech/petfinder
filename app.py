from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    adopted_pets = db.relationship('Pet', backref='adopter', lazy=True, foreign_keys='Pet.adopted_by_id')
    donated_pets = db.relationship('Pet', backref='donor', lazy=True, foreign_keys='Pet.donated_by_id')

    def set_password(self, password):
        self.password_hash = password  # Use bcrypt in production

    def check_password(self, password):
        return self.password_hash == password  # Use bcrypt in production

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80))
    age = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True)
    adopted_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    donated_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email or username already exists!', 'error')
            return redirect(url_for('register'))
        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    adopted_pets = Pet.query.filter_by(adopted_by_id=current_user.id).all()
    donated_pets = Pet.query.filter_by(donated_by_id=current_user.id).all()
    return render_template('dashboard.html', adopted_pets=adopted_pets, donated_pets=donated_pets)

@app.route('/adopt')
@login_required
def adopt_page():
    pets = Pet.query.filter_by(available=True).all()
    return render_template('adopt.html', pets=pets)

@app.route('/adopt_pet/<int:pet_id>', methods=['POST'])
@login_required
def adopt_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.available:
        pet.available = False
        pet.adopted_by_id = current_user.id
        db.session.commit()
        flash(f'You have adopted {pet.name}!', 'success')
    else:
        flash('This pet is no longer available!', 'error')
    return redirect(url_for('dashboard'))

@app.route('/donate_pet', methods=['POST'])
@login_required
def donate_pet():
    name = request.form['name']
    species = request.form['species']
    breed = request.form.get('breed')
    age = request.form.get('age')
    pet = Pet(name=name, species=species, breed=breed, age=age, donated_by_id=current_user.id)
    db.session.add(pet)
    db.session.commit()
    flash(f'{pet.name} has been donated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/donated_pets')
@login_required
def donated_pets():
    pets = Pet.query.all()  # Show all donated pets, not just user's
    return render_template('donated_pets.html', pets=pets)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admin access only!', 'error')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    pets = Pet.query.all()
    return render_template('admin.html', users=users, pets=pets)

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(email='admin@example.com', username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            user = User(email='user@example.com', username='user')
            user.set_password('user123')
            db.session.add(user)
            pets = [
                Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=2, donated_by_id=2),
                Pet(name="Whiskers", species="Cat", breed="Persian", age=1, donated_by_id=2),
                Pet(name="Max", species="Dog", breed="Labrador", age=3, donated_by_id=2)
            ]
            db.session.add_all(pets)
            db.session.commit()

init_db()

if __name__ == '__main__':
    app.run(debug=True)