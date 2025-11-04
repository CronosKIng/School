from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(50))
    address = db.Column(db.String(200))
    level = db.Column(db.String(10), nullable=False)
    registration_number = db.Column(db.String(20), unique=True)
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(100))
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(100), default="2525")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(50))
    address = db.Column(db.String(200))
    level = db.Column(db.String(10), nullable=False)
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(100))
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Pending")
    control_number = db.Column(db.String(50))

class FeePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    amount = db.Column(db.Float)
    control_number = db.Column(db.String(50))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Pending")

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    target_level = db.Column(db.String(10), default="All")

# Initialize default users
def create_default_users():
    print("👤 Creating default users...")

    if not User.query.filter_by(username='ismailyussuf33@gmail.com').first():
        secretary = User(
            username='ismailyussuf33@gmail.com',
            password_hash=generate_password_hash('Mapinduzi@33'),
            role='secretary',
            email='ismailyussuf33@gmail.com'
        )
        db.session.add(secretary)
        print("✅ Secretary created")

    if not User.query.filter_by(username='headmaster').first():
        headmaster = User(
            username='headmaster',
            password_hash=generate_password_hash('Mapinduzi@33'),
            role='headmaster',
            email='headmaster@school.com'
        )
        db.session.add(headmaster)
        print("✅ Headmaster created")

    db.session.commit()
    print("🎉 Users setup completed!")

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply/nursery', methods=['GET', 'POST'])
def apply_nursery():
    if request.method == 'POST':
        student_name = request.form['student_name']
        birth_date = request.form['birth_date']
        address = request.form['address']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        parent_email = request.form['parent_email']

        new_application = Application(
            student_name=student_name,
            birth_date=birth_date,
            address=address,
            level="KG",
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_email=parent_email,
            control_number=f"KG{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        db.session.add(new_application)
        db.session.commit()

        flash('Maombi ya Nursery yamewasilishwa! Tafadhali maliza malipo ya TZS 30,000.', 'success')
        return redirect(url_for('payment', app_id=new_application.id))

    return render_template('apply_nursery.html')

@app.route('/apply/primary', methods=['GET', 'POST'])
def apply_primary():
    if request.method == 'POST':
        student_name = request.form['student_name']
        birth_date = request.form['birth_date']
        address = request.form['address']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        parent_email = request.form['parent_email']

        new_application = Application(
            student_name=student_name,
            birth_date=birth_date,
            address=address,
            level="PRIMARY",
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_email=parent_email,
            control_number=f"PL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        db.session.add(new_application)
        db.session.commit()

        flash('Maombi ya Primary yamewasilishwa! Tafadhali maliza malipo ya TZS 50,000.', 'success')
        return redirect(url_for('payment', app_id=new_application.id))

    return render_template('apply_primary.html')

@app.route('/apply/olevel', methods=['GET', 'POST'])
def apply_olevel():
    if request.method == 'POST':
        student_name = request.form['student_name']
        birth_date = request.form['birth_date']
        address = request.form['address']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        parent_email = request.form['parent_email']

        new_application = Application(
            student_name=student_name,
            birth_date=birth_date,
            address=address,
            level="OLEVEL",
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_email=parent_email,
            control_number=f"OL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        db.session.add(new_application)
        db.session.commit()

        flash('Maombi ya Secondary O-Level yamewasilishwa! Tafadhali maliza malipo ya TZS 70,000.', 'success')
        return redirect(url_for('payment', app_id=new_application.id))

    return render_template('apply_olevel.html')

@app.route('/apply/alevel', methods=['GET', 'POST'])
def apply_alevel():
    if request.method == 'POST':
        student_name = request.form['student_name']
        birth_date = request.form['birth_date']
        address = request.form['address']
        parent_name = request.form['parent_name']
        parent_phone = request.form['parent_phone']
        parent_email = request.form['parent_email']

        new_application = Application(
            student_name=student_name,
            birth_date=birth_date,
            address=address,
            level="ALEVEL",
            parent_name=parent_name,
            parent_phone=parent_phone,
            parent_email=parent_email,
            control_number=f"AL{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )

        db.session.add(new_application)
        db.session.commit()

        flash('Maombi ya Secondary A-Level yamewasilishwa! Tafadhali maliza malipo ya TZS 80,000.', 'success')
        return redirect(url_for('payment', app_id=new_application.id))

    return render_template('apply_alevel.html')

@app.route('/payment/<int:app_id>')
def payment(app_id):
    application = Application.query.get_or_404(app_id)

    amount = 0
    if application.level == "KG":
        amount = 30000
    elif application.level == "PRIMARY":
        amount = 50000
    elif application.level == "OLEVEL":
        amount = 70000
    elif application.level == "ALEVEL":
        amount = 80000

    payment_numbers = [
        {"bank": "NMB", "account": "0123456789", "name": "Zanzibar School"},
        {"bank": "CRDB", "account": "9876543210", "name": "Zanzibar School"},
        {"bank": "AIRTEL MONEY", "account": "0755123456", "name": "Zanzibar School"},
        {"bank": "TIGO PESA", "account": "0655123456", "name": "Zanzibar School"},
        {"bank": "MPESA", "account": "0744123456", "name": "Zanzibar School"}
    ]

    return render_template('payment.html',
                         application=application,
                         amount=amount,
                         payment_numbers=payment_numbers)

@app.route('/complete_application/<int:app_id>')
def complete_application(app_id):
    application = Application.query.get_or_404(app_id)
    application.status = "Completed"
    db.session.commit()

    flash('Maombi yamekamilika! Subiri majibu kutoka kwa Karani.', 'success')
    return redirect(url_for('home'))

@app.route('/secretary/login', methods=['GET', 'POST'])
def secretary_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"🔐 Login attempt: {username}")

        user = User.query.filter_by(username=username, role='secretary').first()

        if user:
            print(f"✅ User found: {user.username}")
            if check_password_hash(user.password_hash, password):
                print("🎉 Password correct! Logging in...")
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session['secretary_logged_in'] = True
                flash('Umefanikiwa kuingia kama Karani!', 'success')
                return redirect(url_for('secretary_dashboard'))
            else:
                print("❌ Password incorrect")
                flash('Nenosiri si sahihi!', 'error')
        else:
            print("❌ User not found")
            flash('Jina la mtumiaji halipo!', 'error')

    return render_template('secretary_login.html')

@app.route('/secretary/dashboard')
def secretary_dashboard():
    if not session.get('secretary_logged_in'):
        flash('Tafadhali ingia kwanza!', 'error')
        return redirect(url_for('secretary_login'))

    pending_applications = Application.query.filter_by(status='Pending').all()
    students = Student.query.all()

    print(f"📊 Dashboard loaded: {len(pending_applications)} pending applications")

    return render_template('secretary_dashboard.html',
                         applications=pending_applications,
                         students=students)

@app.route('/headmaster/login', methods=['GET', 'POST'])
def headmaster_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, role='headmaster').first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['headmaster_logged_in'] = True
            flash('Umefanikiwa kuingia kama Mkuu wa Shule!', 'success')
            return redirect(url_for('headmaster_dashboard'))
        else:
            flash('Umekosea jina la mtumiaji au nenosiri!', 'error')

    return render_template('headmaster_login.html')

@app.route('/headmaster/dashboard')
def headmaster_dashboard():
    if not session.get('headmaster_logged_in'):
        return redirect(url_for('headmaster_login'))

    total_students = Student.query.count()
    total_applications = Application.query.count()
    pending_applications = Application.query.filter_by(status='Pending').count()

    return render_template('headmaster_dashboard.html',
                         total_students=total_students,
                         total_applications=total_applications,
                         pending_applications=pending_applications)

@app.route('/approve_application/<int:app_id>')
def approve_application(app_id):
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))

    application = Application.query.get_or_404(app_id)

    year = datetime.now().year % 100
    level_prefix = ""

    if application.level.upper() == "KG":
        level_prefix = "KG"
    elif application.level.upper() == "PRIMARY":
        level_prefix = "PL"
    elif application.level.upper() == "OLEVEL":
        level_prefix = "OL"
    elif application.level.upper() == "ALEVEL":
        level_prefix = "AL"

    existing_count = Student.query.filter(Student.registration_number.like(f'{year}{level_prefix}%')).count()
    next_number = existing_count + 1
    registration_number = f"{year}{level_prefix}{next_number:03d}"

    new_student = Student(
        full_name=application.student_name,
        birth_date=application.birth_date,
        address=application.address,
        level=application.level,
        parent_name=application.parent_name,
        parent_phone=application.parent_phone,
        parent_email=application.parent_email,
        registration_number=registration_number
    )

    application.status = "Approved"

    db.session.add(new_student)
    db.session.commit()

    flash(f'Mwanafunzi amesajiliwa kikamilifu! Nambari ya usajili: {registration_number}', 'success')
    return redirect(url_for('secretary_dashboard'))

@app.route('/reject_application/<int:app_id>')
def reject_application(app_id):
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))

    application = Application.query.get_or_404(app_id)
    application.status = "Rejected"
    db.session.commit()

    flash('Maombi yamekataliwa!', 'info')
    return redirect(url_for('secretary_dashboard'))

@app.route('/parent/login', methods=['GET', 'POST'])
def parent_login():
    if request.method == 'POST':
        registration_number = request.form['registration_number']
        password = request.form['password']

        student = Student.query.filter_by(registration_number=registration_number).first()

        if student and student.password == password:
            session['student_id'] = student.id
            session['registration_number'] = student.registration_number
            session['parent_logged_in'] = True
            return redirect(url_for('parent_dashboard'))
        else:
            flash('Nambari ya usajili au nenosiri si sahihi!', 'error')

    return render_template('parent_login.html')

@app.route('/parent/dashboard')
def parent_dashboard():
    if not session.get('parent_logged_in'):
        return redirect(url_for('parent_login'))

    student = Student.query.filter_by(registration_number=session['registration_number']).first()
    announcements = Announcement.query.filter(
        (Announcement.target_level == 'All') |
        (Announcement.target_level == student.level)
    ).order_by(Announcement.date_posted.desc()).limit(5).all()

    return render_template('parent_dashboard.html',
                         student=student,
                         announcements=announcements)

@app.route('/logout')
def logout():
    session.clear()
    flash('Umefanikiwa kutoka!', 'info')
    return redirect(url_for('home'))

# Initialize database
with app.app_context():
    print("=" * 50)
    print("🚀 STARTING SCHOOL MANAGEMENT SYSTEM")
    print("=" * 50)
    print("🔧 Creating database tables...")
    db.create_all()
    print("✅ Database tables created!")
    print("👥 Setting up default users...")
    create_default_users()
    print("🎉 System ready!")
    print("📧 Secretary: ismailyussuf33@gmail.com")
    print("🔑 Password: Mapinduzi@33")
    print("=" * 50)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
