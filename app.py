from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import config

app = Flask(__name__)
app.secret_key = "canteen-demo-key"


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER,
        password=config.DB_PASSWORD, database=config.DB_NAME
    )


def get_food_items(available_only=False):
    con = get_connection()
    cur = con.cursor(dictionary=True)
    sql = "SELECT id, name, price, available FROM food_items"
    if available_only:
        sql += " WHERE available = 1"
    sql += " ORDER BY id"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    con.close()
    return rows


@app.route("/")
def home():
    try:
        return render_template("index.html", foods=get_food_items(True))
    except mysql.connector.Error:
        app.logger.exception("Database error on home")
        return render_template("error.html"), 500


@app.route("/menu")
def menu():
    try:
        return render_template("menu.html", foods=get_food_items(True))
    except mysql.connector.Error:
        app.logger.exception("Database error on menu")
        return render_template("error.html"), 500


@app.route("/order", methods=["GET", "POST"])
def order():
    try:
        foods = get_food_items(True)
        if request.method == "POST":
            name = request.form.get("customer_name", "").strip()
            try:
                food_id = int(request.form.get("food_id", "0"))
                quantity = int(request.form.get("quantity", "0"))
            except ValueError:
                flash("Choose a food and valid quantity.", "error")
                return render_template("order.html", foods=foods)
            if not name or len(name) > 100 or not 1 <= quantity <= 20:
                flash("Enter your name and quantity between 1 and 20.", "error")
                return render_template("order.html", foods=foods)

            con = get_connection()
            cur = con.cursor(dictionary=True)
            cur.execute("SELECT id, name, price FROM food_items WHERE id=%s AND available=1", (food_id,))
            food = cur.fetchone()
            cur.close()
            if not food:
                con.close()
                flash("That item is unavailable.", "error")
                return render_template("order.html", foods=foods)

            total_price = round(float(food["price"]) * quantity, 2)
            cur = con.cursor()
            # The existing project schema has both total_price and total.
            # Each column appears exactly once in this INSERT.
            cur.execute(
                "INSERT INTO orders (customer_name, food_id, quantity, total_price, total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (name, food_id, quantity, total_price, total_price)
            )
            con.commit()
            order_id = cur.lastrowid
            cur.close()
            con.close()
            return redirect(url_for("bill", order_id=order_id))
        return render_template("order.html", foods=foods)
    except mysql.connector.Error:
        app.logger.exception("Database error while placing order")
        return render_template("error.html"), 500


@app.route("/bill/<int:order_id>")
def bill(order_id):
    try:
        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT orders.order_id, orders.customer_name, food_items.name AS food_name, "
            "food_items.price, orders.quantity, orders.total_price, orders.order_status, orders.order_time "
            "FROM orders JOIN food_items ON orders.food_id=food_items.id "
            "WHERE orders.order_id=%s", (order_id,)
        )
        data = cur.fetchone()
        cur.close()
        con.close()
        if data is None:
            flash("Bill not found.", "error")
            return redirect(url_for("home"))
        return render_template("bill.html", bill=data)
    except mysql.connector.Error:
        app.logger.exception("Database error generating bill")
        return render_template("error.html"), 500


@app.route("/admin", methods=["GET", "POST"])
def admin():
    try:
        if request.method == "POST":
            action = request.form.get("action", "")
            con = get_connection()
            cur = con.cursor()
            if action == "add_food":
                name = request.form.get("name", "").strip()
                try:
                    price = float(request.form.get("price", "0"))
                except ValueError:
                    price = 0
                if not name or len(name) > 100 or price <= 0:
                    cur.close()
                    con.close()
                    flash("Enter a name and price greater than zero.", "error")
                    return redirect(url_for("admin"))
                cur.execute("INSERT INTO food_items (name, price, available) VALUES (%s, %s, 1)", (name, price))
                con.commit()
                flash("Food item added.", "success")
            elif action == "toggle_food":
                food_id = int(request.form.get("food_id", "0"))
                cur.execute("UPDATE food_items SET available=IF(available=1,0,1) WHERE id=%s", (food_id,))
                con.commit()
                flash("Food availability updated.", "success")
            cur.close()
            con.close()
            return redirect(url_for("admin"))

        con = get_connection()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT id, name, price, available FROM food_items ORDER BY id DESC")
        foods = cur.fetchall()
        cur.execute(
            "SELECT orders.order_id, orders.customer_name, food_items.name AS food_name, "
            "orders.quantity, orders.total_price, orders.order_status, orders.order_time "
            "FROM orders JOIN food_items ON orders.food_id=food_items.id "
            "ORDER BY orders.order_id DESC LIMIT 20"
        )
        orders = cur.fetchall()
        cur.close()
        con.close()
        return render_template("admin.html", foods=foods, orders=orders)
    except mysql.connector.Error:
        app.logger.exception("Database error on admin")
        return render_template("error.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
