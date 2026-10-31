# Campus Canteen Management System

Beginner-friendly DBMS mini project using Python Flask, MySQL, HTML and CSS.

## Setup in VS Code
1. Install Python and MySQL Server (or start MySQL in XAMPP).
2. Open this folder in VS Code.
3. Edit `config.py` with your MySQL username/password.
4. Run `database.sql` in phpMyAdmin or MySQL Workbench.
5. In the VS Code terminal run:

```powershell
python -m pip install -r requirements.txt
python app.py

## Pages
- `/` Home
- `/menu` Food menu
- `/order` Place order and generate bill
- `/admin` Add food, toggle availability, view recent orders

## Existing database warning
This project expects `orders` to have `order_id`, `customer_name`, `food_id`, `quantity`, `total_price`, `total`, `order_status`, and `order_time`. Back up your existing database before changing its schema. `CREATE TABLE IF NOT EXISTS` does not alter tables that already exist.

This is an academic demo. The admin page is not password-protected and should not be exposed publicly as-is.
