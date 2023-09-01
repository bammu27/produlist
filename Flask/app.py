import mysql.connector
from flask import  Flask ,render_template,request,redirect

app = Flask(__name__)


# Database configuration
db_config = {
    'user': 'root',
    'password': '236018br#',
    'host': 'localhost',
    'database': 'flask'
}

# Connect to the database
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()



@app.route('/',methods=['GET','POST'])
def index():
    cursor.execute('select * from products')
    data = cursor.fetchall()
    return  render_template('index.html',data =data)

@app.route('/form',methods=['GET','POST'])
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    pid = int(request.form['pid'])

    pname = request.form['pname']
    price = float(request.form['price'])  # Convert to float
    quantity = int(request.form['quantity'])  # Convert to integer

    try:
        cursor.execute('INSERT INTO products (prodid, pname, price, quantity) VALUES (%s, %s, %s, %s)',
                       (pid, pname, price, quantity))
        db_connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error:", e)

    return redirect('/')

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        cursor.execute('DELETE FROM products WHERE prodid = %s', (product_id,))
        db_connection.commit()
        print("Product deleted successfully")
    except Exception as e:
        print("Error:", e)

    return redirect('/')


@app.route('/update/<int:data>',methods=['GET','POST'])
def update(data):

    return render_template('uform.html',data =data)


@app.route('/change/<int:id>',methods=['POST'])
def change(id):
    print(id)
    pname = request.form['pname']
    price = float(request.form['price'])  # Convert to float
    quantity = int(request.form['quantity'])

    cursor.execute('update products set price=%s ,pname=%s ,quantity=%s where prodid=%s',(price,pname,quantity,id))
    db_connection.commit()
    return redirect('/')
