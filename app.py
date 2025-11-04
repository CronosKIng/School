from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    status = db.Column(db.String(20), default="Active")

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
    payment_proof = db.Column(db.String(300))
    notes = db.Column(db.Text)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(300), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    target_level = db.Column(db.String(10), default="All")
    announcement_type = db.Column(db.String(20), default="general")

class StudentMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_registration = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(300), nullable=True)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    sender_role = db.Column(db.String(20), default="secretary")

# Initialize default users
def create_default_users():
    print("👤 Creating default users...")
    
    # Check if users already exist
    existing_secretary = User.query.filter_by(username='ismailyussuf33@gmail.com').first()
    existing_headmaster = User.query.filter_by(username='headmaster').first()
    
    if not existing_secretary:
        secretary = User(
            username='ismailyussuf33@gmail.com',
            password_hash=generate_password_hash('Mapinduzi@33'),
            role='secretary',
            email='ismailyussuf33@gmail.com'
        )
        db.session.add(secretary)
        print("✅ Secretary user created")
    
    if not existing_headmaster:
        headmaster = User(
            username='headmaster',
            password_hash=generate_password_hash('Mapinduzi@33'),
            role='headmaster',
            email='headmaster@school.com'
        )
        db.session.add(headmaster)
        print("✅ Headmaster user created")
    
    db.session.commit()
    print("🎉 Users setup completed!")

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# Application Routes
@app.route('/apply/nursery', methods=['GET', 'POST'])
def apply_nursery():
    if request.method == 'POST':
        try:
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
                control_number=f"KG{datetime.now().strftime('%Y%m%d%H%M%S')}",
                status="Pending"
            )
            
            db.session.add(new_application)
            db.session.commit()
            
            flash('Maombi ya Nursery yamewasilishwa kikamilifu! Namba ya kudhibiti: ' + new_application.control_number, 'success')
            return redirect(url_for('payment', app_id=new_application.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Hitilafu imetokea wakati wa kuhifadhi maombi. Tafadhali jaribu tena.', 'error')
            print(f"Error in apply_nursery: {e}")
    
    return render_template('apply_nursery.html')

@app.route('/apply/primary', methods=['GET', 'POST'])
def apply_primary():
    if request.method == 'POST':
        try:
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
                control_number=f"PL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                status="Pending"
            )
            
            db.session.add(new_application)
            db.session.commit()
            
            flash('Maombi ya Primary yamewasilishwa kikamilifu! Namba ya kudhibiti: ' + new_application.control_number, 'success')
            return redirect(url_for('payment', app_id=new_application.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Hitilafu imetokea wakati wa kuhifadhi maombi. Tafadhali jaribu tena.', 'error')
            print(f"Error in apply_primary: {e}")
    
    return render_template('apply_primary.html')

@app.route('/apply/olevel', methods=['GET', 'POST'])
def apply_olevel():
    if request.method == 'POST':
        try:
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
                control_number=f"OL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                status="Pending"
            )
            
            db.session.add(new_application)
            db.session.commit()
            
            flash('Maombi ya O-Level yamewasilishwa kikamilifu! Namba ya kudhibiti: ' + new_application.control_number, 'success')
            return redirect(url_for('payment', app_id=new_application.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Hitilafu imetokea wakati wa kuhifadhi maombi. Tafadhali jaribu tena.', 'error')
            print(f"Error in apply_olevel: {e}")
    
    return render_template('apply_olevel.html')

@app.route('/apply/alevel', methods=['GET', 'POST'])
def apply_alevel():
    if request.method == 'POST':
        try:
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
                control_number=f"AL{datetime.now().strftime('%Y%m%d%H%M%S')}",
                status="Pending"
            )
            
            db.session.add(new_application)
            db.session.commit()
            
            flash('Maombi ya A-Level yamewasilishwa kikamilifu! Namba ya kudhibiti: ' + new_application.control_number, 'success')
            return redirect(url_for('payment', app_id=new_application.id))
        
        except Exception as e:
            db.session.rollback()
            flash('Hitilafu imetokea wakati wa kuhifadhi maombi. Tafadhali jaribu tena.', 'error')
            print(f"Error in apply_alevel: {e}")
    
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
    
    flash('Malipo yamekamilika! Maombi yako yamewasilishwa kikamilifu. Subiri mkuu wa shule aidhinisha.', 'success')
    return redirect(url_for('home'))

# Secretary Routes
@app.route('/secretary/login', methods=['GET', 'POST'])
def secretary_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, role='secretary').first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['secretary_logged_in'] = True
            flash('Umefanikiwa kuingia kama Karani!', 'success')
            return redirect(url_for('secretary_dashboard'))
        else:
            flash('Jina la mtumiaji au nenosiri si sahihi!', 'error')
    
    return render_template('secretary_login.html')

@app.route('/secretary/dashboard')
def secretary_dashboard():
    if not session.get('secretary_logged_in'):
        flash('Tafadhali ingia kwanza!', 'error')
        return redirect(url_for('secretary_login'))
    
    # Debug: Check all applications
    all_applications = Application.query.all()
    print(f"🔍 [DEBUG] Total applications in database: {len(all_applications)}")
    for app in all_applications:
        print(f"📄 [DEBUG] Application: {app.id} - {app.student_name} - {app.level} - {app.status}")
    
    # Load applications by level (ALL statuses)
    nursery_applications = Application.query.filter_by(level="KG").all()
    primary_applications = Application.query.filter_by(level="PRIMARY").all()
    olevel_applications = Application.query.filter_by(level="OLEVEL").all()
    alevel_applications = Application.query.filter_by(level="ALEVEL").all()
    
    print(f"👶 [DEBUG] Nursery apps: {len(nursery_applications)}")
    print(f"📚 [DEBUG] Primary apps: {len(primary_applications)}")
    print(f"🎓 [DEBUG] O-Level apps: {len(olevel_applications)}")
    print(f"🎓 [DEBUG] A-Level apps: {len(alevel_applications)}")
    
    students = Student.query.all()
    
    return render_template('secretary_dashboard.html',
                         nursery_applications=nursery_applications,
                         primary_applications=primary_applications,
                         olevel_applications=olevel_applications,
                         alevel_applications=alevel_applications,
                         students=students)

@app.route('/secretary/announcements')
def secretary_announcements():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    try:
        announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
        return render_template('secretary_announcements.html', announcements=announcements)
    except:
        return render_template('secretary_announcements.html', announcements=[])

@app.route('/secretary/results')
def secretary_results():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    try:
        results = Announcement.query.filter_by(announcement_type='results').order_by(Announcement.date_posted.desc()).all()
        return render_template('secretary_results.html', results=results)
    except:
        return render_template('secretary_results.html', results=[])

@app.route('/secretary/messages')
def secretary_messages():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    try:
        messages = StudentMessage.query.order_by(StudentMessage.date_sent.desc()).all()
        return render_template('secretary_messages.html', messages=messages)
    except:
        return render_template('secretary_messages.html', messages=[])

@app.route('/secretary/applications')
def secretary_applications():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    # Load all applications by level (ALL statuses)
    nursery_applications = Application.query.filter_by(level="KG").all()
    primary_applications = Application.query.filter_by(level="PRIMARY").all()
    olevel_applications = Application.query.filter_by(level="OLEVEL").all()
    alevel_applications = Application.query.filter_by(level="ALEVEL").all()
    
    print(f"📊 [DEBUG] Applications page - KG: {len(nursery_applications)}, PRIMARY: {len(primary_applications)}")
    
    return render_template('secretary_applications.html',
                         nursery_applications=nursery_applications,
                         primary_applications=primary_applications,
                         olevel_applications=olevel_applications,
                         alevel_applications=alevel_applications)

@app.route('/secretary/students')
def secretary_students():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    students = Student.query.all()
    return render_template('secretary_students.html', students=students)

@app.route('/secretary/reports')
def secretary_reports():
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    total_students = Student.query.count()
    total_applications = Application.query.count()
    pending_applications = Application.query.filter_by(status='Pending').count()
    completed_applications = Application.query.filter_by(status='Completed').count()
    approved_applications = Application.query.filter_by(status='Approved').count()
    rejected_applications = Application.query.filter_by(status='Rejected').count()
    
    return render_template('secretary_reports.html',
                         total_students=total_students,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         completed_applications=completed_applications,
                         approved_applications=approved_applications,
                         rejected_applications=rejected_applications)

# Application Review and Approval Routes
@app.route('/review_application/<int:app_id>')
def review_application(app_id):
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    try:
        application = Application.query.get_or_404(app_id)
        return render_template('review_application.html', application=application)
    except Exception as e:
        print(f"❌ Error in review_application: {e}")
        flash('Hitilafu imetokea wakati wa kukagua maombi.', 'error')
        return redirect(url_for('secretary_applications'))

@app.route('/approve_application/<int:app_id>', methods=['POST'])
def approve_application(app_id):
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    application = Application.query.get_or_404(app_id)
    
    try:
        # Generate registration number
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
        
        # Count existing students with same prefix
        existing_count = Student.query.filter(Student.registration_number.like(f'{year}{level_prefix}%')).count()
        next_number = existing_count + 1
        registration_number = f"{year}{level_prefix}{next_number:03d}"
        
        # Create new student
        new_student = Student(
            full_name=application.student_name,
            birth_date=application.birth_date,
            address=application.address,
            level=application.level,
            parent_name=application.parent_name,
            parent_phone=application.parent_phone,
            parent_email=application.parent_email,
            registration_number=registration_number,
            status="Active"
        )
        
        # Update application status
        application.status = "Approved"
        
        db.session.add(new_student)
        db.session.commit()
        
        flash(f'✅ Maombi yameidhinishwa! Mwanafunzi amesajiliwa kikamilifu.', 'success')
        flash(f'📝 Nambari ya usajili: {registration_number}', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash('❌ Hitilafu imetokea wakati wa kusajili mwanafunzi. Tafadhali jaribu tena.', 'error')
        print(f"Error in approve_application: {e}")
    
    return redirect(url_for('secretary_applications'))

@app.route('/reject_application/<int:app_id>', methods=['POST'])
def reject_application(app_id):
    if not session.get('secretary_logged_in'):
        return redirect(url_for('secretary_login'))
    
    application = Application.query.get_or_404(app_id)
    
    try:
        application.status = "Rejected"
        application.notes = request.form.get('rejection_reason', 'Maombi yamekataliwa bila maelezo')
        db.session.commit()
        
        flash('❌ Maombi yamekataliwa!', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash('Hitilafu imetokea wakati wa kukataa maombi.', 'error')
        print(f"Error in reject_application: {e}")
    
    return redirect(url_for('secretary_applications'))

# Headmaster Routes
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
    completed_applications = Application.query.filter_by(status='Completed').count()
    
    return render_template('headmaster_dashboard.html',
                         total_students=total_students,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         completed_applications=completed_applications)

# Parent Routes
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
            flash('Umefanikiwa kuingia!', 'success')
            return redirect(url_for('parent_dashboard'))
        else:
            flash('Nambari ya usajili au nenosiri si sahihi!', 'error')
    
    return render_template('parent_login.html')

@app.route('/parent/dashboard')
def parent_dashboard():
    if not session.get('parent_logged_in'):
        return redirect(url_for('parent_login'))
    
    student = Student.query.filter_by(registration_number=session['registration_number']).first()
    
    if not student:
        flash('Taarifa za mwanafunzi hazikupatikana!', 'error')
        return redirect(url_for('parent_login'))
    
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
    
    # Delete old database file to ensure clean start
    db_path = 'instance/school_management.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Old database deleted")
    
    print("🔧 Creating new database tables...")
    db.create_all()
    print("✅ Database tables created successfully!")
    
    print("👥 Setting up default users...")
    create_default_users()
    
    # Add sample completed application for testing
    sample_app = Application(
        student_name="Alih Test",
        birth_date="2015-01-01",
        address="Zanzibar",
        level="KG",
        parent_name="Mzazi Test",
        parent_phone="0755000000",
        parent_email="test@test.com",
        control_number="TEST001",
        status="Completed"
    )
    db.session.add(sample_app)
    db.session.commit()
    print("✅ Sample application added for testing")
    
    print("🎉 System initialization completed!")
    print("📧 Secretary Login: ismailyussuf33@gmail.com")
    print("🔑 Password: Mapinduzi@33")
    print("👨‍🏫 Headmaster Login: headmaster")
    print("🔑 Password: Mapinduzi@33")
    print("=" * 50)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
