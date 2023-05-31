from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db_myhotel"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/guests", methods=["GET"])
def get_guest():
    data = data_fetch("""select * from guest""")
    return make_response(jsonify(data), 200)

@app.route("/guests/<int:id>", methods=["GET"])
def get_guest_byID(id):
    data = data_fetch("""select * from guest Where Guest_Id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/guests/<int:id>/booking", methods=["GET"])
def get_booking_ByGuest(id):
    data = data_fetch(
        """
        select Booking_Id,booking.Guest_Id,Check_In_Date,Check_Out_Date, FirstName,LastNAme,PhoneNumber
        from guest inner join booking on guest.Guest_Id=booking.Guest_Id 
        where guest.Guest_Id={}""".format(id))
    return make_response(jsonify({"Guest_Id": id, "count": len(data), "booking": data}), 200
    )
@app.route("/guests", methods=["POST"])
def add_guest():
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstName = info["FirstName"]
    LastName = info["LastName"]
    PhoneNumber = info["PhoneNumber"]
    Email = info["Email"]

    cur.execute(
        """ INSERT INTO guest (FirstName, LastName,PhoneNumber, Email) VALUE (%s, %s, %s, %s)""",(FirstName, LastName,PhoneNumber,Email))
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "guest added successfully", "rows_affected": rows_affected}),201)


@app.route("/guests/<int:id>", methods=["PUT"])
def update_guest(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    FirstName = info["FirstName"]
    LastName = info["LastName"]
    PhoneNumber = info["PhoneNumber"]
    
    cur.execute(
        """ UPDATE guest SET FirstName = %s, LastName = %s, PhoneNumber = %s WHERE Guest_Id = %s """,
        (FirstName, LastName,PhoneNumber, id))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "Guest updated successfully", "rows_affected": rows_affected}),200)


if __name__ == "__main__":
    app.run(debug=True)
