from flask import Flask, render_template, url_for, request, redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship
from flask_mail import Mail, Message
from threading import Thread
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import UserMixin


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:feeltherain@1@127.0.0.1/nuda'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'engnrno1@gmail.com' 
app.config['MAIL_DEFAULT_SENDER'] = 'engnrno1@gmail.com' 
app.config['MAIL_PASSWORD'] = 'feeltherain@1'

db = SQLAlchemy(app)

mail = Mail(app)
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot1 = db.Column(db.Boolean, default=False, nullable=False)
    slot2 = db.Column(db.Boolean, default=False, nullable=False)
    slot3 = db.Column(db.Boolean, default=False, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    lastname = db.Column(db.String(15))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class darshanticket(db.Model):
    id = db.Column('tktid',db.Integer,nullable = False,primary_key = True)
    name = db.Column(db.String(200))
    typ = db.Column(db.String(200))
    no_of_adult = db.Column(db.Integer())
    no_of_child = db.Column(db.Integer())
    #price = db.Column(db.Integer())
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    date = db.Column(db.String(200))
    time = db.Column(db.String(200))
    TotalPrice = db.Column(db.Integer())
    def _init(self,name,typ,no_of_adult,no_of_child,price,email,phone,date,time):
        self.name = name
        self.typ = typ
        self.no_of_adult = no_of_adult
        self.no_of_child = no_of_child
        #self.price = price
        self.email = email
        self.phone = phone
        self.date = date
        self.time = time
        
class pujadetail(db.Model):
    id = db.Column('pujaid',db.Integer,nullable = False,primary_key = True)
    tktno = db.Column(db.String(200))
    typ = db.Column(db.String(200))
    price = db.Column(db.String(200))
    def _init(self,tktno,typ,price):
        self.tktno = tktno
        self.typ = typ
        self.price = price


class hallbook(db.Model):
    id = db.Column('hid',db.Integer,nullable = False,primary_key = True)
    fname = db.Column(db.String(200))
    lname = db.Column(db.String(200))
    hallname = db.Column(db.String(200))
    no_of_guests = db.Column(db.String(200))
    purpose = db.Column(db.String(200))
    email = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
    date = db.Column(db.String(200))
    TotalPrice = db.Column(db.Integer())
    capacity=db.Column(db.Integer())
    slotid=db.Column(db.String(20))
    def _init_(self,fname,lname,no_of_guests,email,moblie,date,starttime,endtime):
        self.fname = fname
        self.lname = lname
        self.hallname = hallname
        self.no_of_guests = no_of_guests
        self.purpose = purpose
        self.email = email
        self.mobile = mobile
        self.date = date
class prasadam(db.Model):
    id = db.Column('pid',db.Integer,nullable = False,primary_key = True)
    fname = db.Column(db.String(200))
    lname = db.Column(db.String(200))
    price = db.Column(db.String(200))
    email = db.Column(db.String(200))
    mobileno = db.Column(db.String(200))
    qty = db.Column(db.String(200))
    thalitype = db.Column(db.String(200))
    mod = db.Column(db.String(200))
    def _init_(self,fname,lname,price,email,mobileno,qty,thalitype,mod):
        self.fname = fname
        self.lname = lname
        self.price = price
        self.email = email
        self.mobileno = mobileno
        self.qty = qty
        self.thalitype = thalitype
        self.mod = mod
    

class onlinecustomer(db.Model):
    id = db.Column('oid',db.Integer,nullable = False,primary_key = True)
    name = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
    address = db.Column(db.String(200))
    proname = db.Column(db.String(200))
    price = db.Column(db.String(200))
    email = db.Column(db.String(200))
    def _init_(self,name,moblie,email,address,proname,price):
        self.name = name
        self.mobile = mobile
        self.address = address
        self.email = email
        self.proname = proname
        self.price = price

class FeedBack(db.Model):
    id = db.Column('feedid',db.Integer,nullable = False,primary_key = True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    msg = db.Column(db.String(10000))
    def _init_(self,name,email,msg):
        self.name = name
        self.email = email
        self.msg = msg

class Donor(db.Model):
    id = db.Column('doid',db.Integer,nullable = False,primary_key = True)
    fname = db.Column(db.String(200))
    lname = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    pin = db.Column(db.String(200))
    country = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    price = db.Column(db.String(200))
    def _init_(self,name,moblie,email,address,proname,price):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.city = city
        self.state = state
        self.pin = pin
        self.country = country
        self.email = email
        self.phone = phone
        self.price = price

class Complaint(db.Model):
    id = db.Column('compid',db.Integer,nullable = False,primary_key = True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    address = db.Column(db.String(1500))
    message = db.Column(db.String(10000))
    membertype = db.Column(db.String(200))
    def _init_(self,name,email,address,message):
        self.name = name
        self.email = email
        self.address = address
        self.message = message
        self.membertype = membertype


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=4, max=15)])
    lastname =  StringField('lastname', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', firstname=current_user.firstname,lastname=current_user.lastname)
@app.route('/logout')
@login_required
def logout():
    user=current_user
    logout_user()
    return redirect(url_for('index'))

@app.route('/aboutus', methods = ['GET','POST'])
def about_us():
    if request.method == 'GET':
        return render_template('about.html')
    return render_template('index2.html')

@app.route('/darshan',methods = ['GET', 'POST'])
def darshan():
    if request.method == 'POST':
        if request.form['darshan']:
            darshantype = request.form['darshan']
            if darshantype == "darshan1":
                darsh=["1","Special Morning Darshan", 1000]
            elif darshantype == "darshan2":
                darsh=["2","Morning Darshan", 700]
            elif darshantype == "darshan3":
                darsh=["3","Special Afternoon Darshan", 1000]
            elif darshantype == "darshan4":
                darsh=["4","Afternoon Darshan", 700]
            elif darshantype == "darshan5":
                darsh=["5","Special Evening Darshan", 1000]
            else:
                darsh=["6","Evening Darshan",1000]
            if not current_user.is_authenticated:
                return render_template('darshandetails.html',darshan = darsh)
            else:
                return render_template('darshandetails1.html',darshan=darsh, username=current_user.firstname+" "+current_user.lastname, email=current_user.email)
        else:
            return render_template('darshan.html',msg = 'Please select a darshan to proceed')
    return render_template('darshan.html')


@app.route('/darshandetails',methods = ['GET', 'POST'])
def darshandetail():
    if request.method == 'POST':
        dardetail = darshanticket(name = request.form['name'],
                                  typ = request.form['type'],
                                  no_of_adult = request.form['nadult'],
                                  no_of_child = request.form['nchild'],
                                  #price = request.form['price'],
                                  email = request.form['email'],
                                  phone = request.form['phone'],
                                  date = request.form['date'],
                                  time = request.form['time'],
                                  TotalPrice=request.form['RM'])
        dardetail.TotalPrice=int(dardetail.TotalPrice)*(int(dardetail.no_of_child)+int(dardetail.no_of_adult))
        db.session.add(dardetail)
        db.session.commit()
        return redirect(url_for('payment', dtid=dardetail.id))
    #return render_template('darshandetails.html',msg = 'tickets booked successfully!!!')
    return render_template('darshandetails.html')

def pay():
  return True

@app.route('/payment/<int:dtid>')
def payment(dtid):
  custmer=darshanticket.query.get(dtid)
  x=pay()
  if x is False:
    db.session.delete(custmer)
    db.session.commit()
  else:
    #msg = Message("Subject", recipients=['mohammadhamidreza7@gmail.com'])
    #msg.body="You are welcome"
    #mail.send(msg)
    send_mail("Darshan Ticket",custmer.email, 'confirmation.html', ticketid=dtid,name=custmer.name,typ=custmer.typ,no_of_child=custmer.no_of_child,no_of_adult=custmer.no_of_adult,email=custmer.email,phone=custmer.phone,date=custmer.date,time=custmer.time,TotalPrice=custmer.TotalPrice)
  return 'Your Ticket Is Booked Please Check Your Email' 

def pay1():
  return True

@app.route('/payment1/<int:htid>')
def payment1(htid):
  custmer1=hallbook.query.get(htid)
  y=pay1()
  if y is False:
    db.session.delete(custmer1)
    db.session.commit()
  else:
    #msg = Message("Subject", recipients=['mohammadhamidreza7@gmail.com'])
    #msg.body="You are welcome"
    #mail.send(msg)
    send_mail("Hall Ticket",custmer1.email, 'confirmation1.html', ticketid=htid,fname=custmer1.fname,lname=custmer1.lname,no_of_guests=custmer1.no_of_guests,hallname=custmer1.hallname,email=custmer1.email,mobile=custmer1.mobile,date=custmer1.date,purpose=custmer1.purpose,TotalPrice=custmer1.TotalPrice,slotid=custmer1.slotid)
  return 'Your Hall Ticket Is Booked Please Check Your Email' 


@app.route('/puja',methods = ['GET', 'POST'])
def epuja():
    if request.method == 'POST':
        if request.form['epuja']:
            halltype = request.form['epuja']
            return render_template('pujadetails.html',halltype = halltype)
        else:
            return render_template('epuja.html',msg = 'Please select a hall to proceed')
    return render_template('epuja.html')

@app.route('/pujadetails',methods = ['GET', 'POST'])
def pujadetails():
    if request.method == 'POST':
        puja_obj = pujadetail(tktno = request.form['tktno'],
                              typ = request.form['type'],
                              price = request.form['price'])
        db.session.add(puja_obj)
        db.session.commit()
        return render_template('pujadetails.html',msg = 'Puja booking done!!!!')
    return render_template('pujadetails.html')


@app.route('/eshop',methods = ['GET', 'POST'])
def eshop():
    if request.method == 'GET':
        return render_template('shopping.html')
    return render_template('shopping.html')

@app.route('/shopbooking',methods = ['GET', 'POST'])
def eshopping():
    if request.method == 'POST':
        eshop = onlinecustomer(name = request.form['name'],
                               address = request.form['address'],
                               email = request.form['email'],
                               mobile = request.form['phone'],
                               price = request.form['price'],
                               proname = request.form['proname'])
        db.session.add(eshop)
        db.session.commit()
        return render_template('shopbooking.html',msg = 'Order successfull!!!')
    return render_template('shopbooking.html')


@app.route('/checkout',methods = ['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['mobile'] or not request.form['address']:
            return render_template('checkout.html',msg = 'Please fill the necessary details') 
        else:
            check = onlinecustomer(fname = request.form['fname'],
                                   mobile = request.form['mobile'],
                                   address = request.form['address'])
            db.session.add(check)
            db.session.commit()
            return render_template('checkout.html',msg = 'You order successfull')
    return render_template('checkout.html')

@app.route('/hall',methods = ['GET', 'POST'])
def hall():
    if request.method == 'POST':
        if request.form['hall']:
            halltype = request.form['hall']
            if halltype == "hall1":
                h=["1","Hall 1", 3200,150,"Non AC Hall","Surround Speakers \n 2 AC Restrooms attached \n Power Back-up Facility"]
            elif halltype == "hall2":
                h=["2","Hall 2", 6000,300,"AC Hall","Surround Speakers \n 3 AC Restrooms attached \n Power Back-up Facility \n LED Projector available"]
            elif halltype == "hall3":
                h=["3","Hall 3", 10000,500,"AC Hall","Surround Speakers \n 3 AC Restrooms attached \n Power Back-up Facility \n LED Projector available \n Advanced Lighting System"]
            elif halltype == "hall4":
                h=["4","Hall 4", 13000,800,"AC Hall","Surround Speakers \n 3 AC Restrooms attached \n Power Back-up Facility \n LED Projector available \n Advanced Lighting System"]
            elif halltype == "hall5":
                h=["5","Hall 5", 15000,1000,"AC Hall","Surround Speakers \n 3 AC Restrooms attached \n Power Back-up Facility \n LED Projector available \n Advanced Lighting System"]
            else:
                h=["6","Hall 6",19000,1500,"AC Hall","Surround Speakers \n 3 AC Restrooms attached \n Power Back-up Facility \n LED Projector available \n Advanced Lighting System"]
            if not current_user.is_authenticated:
                return render_template('hallbooking.html',hall = h)
            else:
                return render_template('hallbooking1.html',hall=h, fname=current_user.firstname, lname=current_user.lastname, email=current_user.email)
        else:
            return render_template('hall.html')
    return render_template('hall.html')




@app.route('/hallbooks',methods = ['GET', 'POST'])
def hallbooks():
    if request.method == 'POST':
        hticket = hallbook(fname = request.form['fname'],
                               lname = request.form['lname'],
                               hallname = request.form['halltype'],
                               no_of_guests = request.form['nguest'],
                               purpose = request.form['purpose'],
                               email = request.form['email'],
                               mobile = request.form['mobileno'],
                               date = request.form['date'],
                               TotalPrice=request.form['HM'],
                               capacity=request.form['CP'])
        slotlist=request.form.getlist('slotid')
        hticket.slotid=slotlist
        s=hticket.date
        m=int(s[5:7])
        n=int(s[8:10])
        z=(m-1)*30+n
        c=Slot.query.get(z)
        if slotlist==['1']:
            if c.slot1==False:
                c.slot1=True
                hticket.TotalPrice=int(hticket.TotalPrice)
                db.session.add(hticket)
                db.session.commit()

                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['2']:
            if c.slot2==False:
                c.slot2=True
                hticket.TotalPrice=int(hticket.TotalPrice)
                db.session.add(hticket)
                db.session.commit()

                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['3']:
            if c.slot3==False:
                c.slot3=True
                hticket.TotalPrice=int(hticket.TotalPrice)
                db.session.add(hticket)
                db.session.commit()


                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['1','2']:
            if c.slot1==False and c.slot2==False:
                c.slot1=True
                c.slot2=True
                hticket.TotalPrice=int(hticket.TotalPrice)*2
                db.session.add(hticket)
                db.session.commit()

                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['1','3']:
            if c.slot1==False and c.slot3==False:
                c.slot1=True
                c.slot3=True
                hticket.TotalPrice=int(hticket.TotalPrice)*2
                db.session.add(hticket)
                db.session.commit()
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['2','3']:
            if c.slot2==False and c.slot3==False:
                c.slot2=True
                c.slot3=True
                hticket.TotalPrice=int(hticket.TotalPrice)*2
                db.session.add(hticket)
                db.session.commit()

                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        elif slotlist==['1','2','3']:
            if c.slot1==False and c.slot2==False and c.slot3==False:
                c.slot1=True
                c.slot2=True
                c.slot3=True
                hticket.TotalPrice=int(hticket.TotalPrice)*3
                db.session.add(hticket)
                db.session.commit()

                #return 'booked'
                return redirect(url_for('payment1', htid=hticket.id))
            else:
                return 'please choose another option'
        else:
            return redirect(url_for('hallbooks',msg="please select a slot"))
    #return render_template('darshandetails.html',msg = 'tickets booked successfully!!!')
    return render_template('hallbooking.html')

    
@app.route('/prasadam',methods = ['GET', 'POST'])
def prasad_seva():
    if request.method == 'POST':
        render_template('prasadbooking.html')
    return render_template('prasad.html')


@app.route('/prasadbook',methods = ['GET', 'POST'])
def prasad_book():
    if request.method == 'POST':
        probj = prasadam(fname = request.form['fname'],
                         lname = request.form['lname'],
                         price = request.form['price'],
                         email = request.form['email'],
                         mobileno = request.form['phone'],
                         qty = request.form['qty'],
                         thalitype = request.form['thalitype'],
                         mod = request.form['mode'])
        db.session.add(probj)
        db.session.commit()
        return render_template('prasadbooking.html',msg = 'Details filled successfuls!!!')
    return render_template('prasadbooking.html')

@app.route('/customthali',methods = ['GET', 'POST'])
def custom_thali():
    if request.method == 'GET':
        return render_template('customthali.html')
    return render_template('customthali.html')

'''
@app.route('/payment',methods = ['GET', 'POST'])
def payment():
    return render_template('payment.html')
'''


@app.route('/donation',methods = ['GET', 'POST'])
def donation():
    if request.method == 'GET':
        return render_template('donation.html')
    return render_template('donation.html')
        
@app.route('/donodetails',methods = ['GET','POST'])
def donordetails():
    if request.method == 'POST':
        don = Donor(fname = request.form['fname'],
                    lname = request.form['lname'],
                    address = request.form['address'],
                    city = request.form['city'],
                    state = request.form['state'],
                    pin = request.form['pin'],
                    country = request.form['country'],
                    email = request.form['email'],
                    phone = request.form['phone'],
                    price = request.form['price'])
        db.session.add(don)
        db.session.commit()
        return render_template('donationform.html',msg = 'Donation done successfull !!!')
    return render_template('donationform.html')



@app.route('/complaint', methods = ['GET', 'POST'])
def complaint():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['email'] or not request.form['address'] or not request.form['message']:
            return render_template('Complaint.html',msg = 'Please fill the necessary details')
        else:
            comp = Complaint(name = request.form['name'],
                             email = request.form['email'],
                             address = request.form['address'],
                             message = request.form['message'],
                             membertype = request.form['comp'])
            db.session.add(comp)
            db.session.commit()
            return render_template('Complaint.html',comments = 'Your Complaint has been recorded..!!!! Sorry for inconvinience!!!!!...')
    return render_template('Complaint.html')       
        
@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['email'] or not request.form['message']:
            return render_template('feedback.html',msg = 'Please fill the necessary details !!!!')
        else:
            feed = FeedBack(name = request.form['name'],
                            email = request.form['email'],
                            msg = request.form['message'])
            db.session.add(feed)
            db.session.commit()
            return render_template('feedback.html',comments = 'Thank You For Your Valuable Remarks !!!!')
    return render_template('feedback.html')       

if  __name__ == "__main__":
    db.create_all()
    for x in range(0,365):
        slt=Slot()
        db.session.add(slt)
        db.session.commit()
    
    
    app.run(port=7005,debug=False)
