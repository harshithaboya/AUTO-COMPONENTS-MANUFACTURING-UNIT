# AUTO-COMPONENTS-MANUFACTURING-UNIT

A GUI-based application developed using Python (Tkinter) that simulates operations within an auto components manufacturing unit. It handles user login, registration, department-wise product viewing, shopping cart, transaction generation, and admin-level functionalities like staff management and purchase tracking.

Project Structure
'layout.py': The core application file containing all the GUI logic (Tkinter-based).
'main.py': Sample Python starter script.
'background.jpg', 'userlogin.jpg', etc.: UI assets used in the application.
'ER diagram.png': Entity-Relationship diagram for the database schema.
'*.jpg': Images of parts like pistons, oil filters, engines used for product display.
Features
User Authentication:

Buyer registration, login, forgot password
Employee/admin login with role-based access
Database Operations:

Connected to MySQL ('ManufacturingUnit' database)
Handles buyers, workers, product inventory, raw material purchases, transactions
Admin Capabilities:

View feedback and messages
View department stats, shopping records, and supply logs
Bonus distribution to employees
Shopping & Billing:

View parts with image-based previews
Add items to cart, bill generation with printable receipts
Technologies Used
Python 3.x
Tkinter & Tix (GUI)
MySQL (backend database)
Pillow (image support)
tkcalendar (calendar widget)
ER Diagram
Setup Instructions
Clone the repository: '''bash git clone https://github.com/your-username/auto-components-manufacturing.git cd auto-components-manufacturing '''

Install dependencies: '''bash pip install mysql-connector-python tkcalendar Pillow '''

Create the 'ManufacturingUnit' database and tables using the ER diagram as a reference.

Update database credentials in 'layout.py': '''python mydb = mysql.connector.connect(user='root', password='yourpassword', host='127.0.0.1', database='ManufacturingUnit', autocommit=True) '''

Run the app: '''bash python layout.py '''
