from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

app= Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")



try:
    db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
    print('Databse Connected')
    cursor = db.cursor(buffered=True)
except:
    print("connection failed")



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/products")
def products():
    cursor.execute("Select * from products")
    result= cursor.fetchall()
    return render_template("products.html", products=result)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        password= request.form['password']
        hashed_password= generate_password_hash(password)
        cursor.execute(
            "insert into users (username,email,user_password) values(%s,%s,%s)",
            (name,email,hashed_password)
            )    
        db.commit()
        return redirect("/")
    return render_template("register.html") 

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form['email']
        password= request.form['password']

        cursor.execute(
            "Select * from users where email=%s ",
            (email,)
        )
        user= cursor.fetchone()

        if user and user[6] == 1:
            return"Account Locked"
        
        if user and check_password_hash(user[3],password):
            cursor.execute("update users set failed_attempts =0 where user_id=%s",(user[0],))
            session['user_id']=user[0]
            return redirect("/")
        else:
            failed_attempt= user[5]+1
            if failed_attempt >=5:
                cursor.execute("update users set failed_attempts=%s, locked=1 where user_id=%s",(failed_attempt,user[0]))
                db.commit()
                return "Account is locked"
            else:
                cursor.execute('update users set failed_attempts=%s where user_id=%s',(failed_attempt,user[0]))
                db.commit()
                return "Invalid email or password"

    return render_template("login.html")

@app.route("/product/<int:product_id>")
def prodcut(product_id):
    cursor.execute(
        "Select * from products where product_id=%s",
        (product_id,)
    )
    result= cursor.fetchone()  
    return render_template("product.html", product=result)

cart={}
@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cursor.execute("select * from products where product_id=%s",(product_id,))
    prodcut= cursor.fetchone()
    if prodcut:
        stock= prodcut[4]
        if product_id in cart:
            if cart[product_id] < stock:
                cart[product_id]+=1
            else:
                print("Cannot add more items. Stock limit reached")
        else:
            cart[product_id]=1

    return redirect('/cart')

@app.route('/cart')
def view_cart():
    cart_items=[]
    total=0
    for product_id in cart:
        cursor.execute(' select * from products where product_id = %s', (product_id,))
        result= cursor.fetchone()
        if result:
            cart_items.append(result)
            total+= result[3]* cart[product_id]
    return render_template('cart.html',cart_items=cart_items,cart=cart, total=total)

@app.route("/increase-cart-items/<int:product_id>", methods=['POST'])
def increase_cart_items(product_id):
    cursor.execute('select * from products where product_id=%s',(product_id,))
    product=cursor.fetchone()
    if product:
        stock=product[4]
        if cart[product_id]<stock:
            cart[product_id]+=1
        else:
            print("Cannot add more items. Stock limit reached")
    return redirect('/cart')

@app.route("/decrease-cart-items/<int:product_id>", methods=["POST"])
def decrease_cart_items(product_id):
    if product_id in cart:
        cart[product_id]-=1

        if cart[product_id]<=0:
            del cart[product_id]
    return redirect('/cart')

@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    if product_id in cart:
        del cart[product_id]
    return redirect('/cart')

@app.route("/checkout", methods=['POST'])
def checkout():
    cart_items=[]
    total=0
    for product_id in cart:
            cursor.execute(' select * from products where product_id = %s', (product_id,))
            product= cursor.fetchone()

            if product:
                cart_items.append(product)
                total+= product[3]* cart[product_id]
    return render_template('checkout.html', cart_items=cart_items, cart=cart, total=total)

@app.route('/confirm-order', methods=['POST'])
def confirm_order():
    if "user_id" not in session:
        return redirect('/login')
    user_id= session['user_id']
    if not cart:
        return redirect('/cart')   
    cart_items=[]
    total=0
    for product_id in cart:
        cursor.execute("Select * from products where product_id=%s",(product_id,))
        product=cursor.fetchone()
        if product:
            cart_items.append(product)
            total+= product[3]*cart[product_id]
    cursor.execute("insert into orders (user_id,total,status,created_at) values(%s,%s,%s,NOW())",(user_id,total, 'pending'))
    db.commit()
    order_id=cursor.lastrowid
    return render_template('order.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user_id=session['user_id']
    
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)