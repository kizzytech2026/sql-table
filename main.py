
# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')


# STEP 1: Employees in Boston
df_boston = pd.read_sql("""
    SELECT employees.firstName,
           employees.lastName
    FROM employees
    INNER JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE offices.city = 'Boston'
    ORDER BY employees.firstName;
""", conn)


# STEP 2: Offices with zero employees
df_zero_emp = pd.read_sql("""
    SELECT offices.officeCode,
           offices.city
    FROM offices
    LEFT JOIN employees
        ON offices.officeCode = employees.officeCode
    WHERE employees.employeeNumber IS NULL;
""", conn)


# STEP 3: All employees and their office locations
df_employee = pd.read_sql("""
    SELECT employees.firstName,
           employees.lastName,
           offices.city,
           offices.state
    FROM employees
    LEFT JOIN offices
        ON employees.officeCode = offices.officeCode
    ORDER BY employees.firstName ASC,
             employees.lastName ASC;
""", conn)


# STEP 4: Customers who have never placed an order
df_contacts = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           customers.phone,
           customers.salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        ON customers.customerNumber = orders.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY customers.contactLastName ASC;
""", conn)


# STEP 5: Customer payments
df_payment = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           payments.paymentDate,
           payments.amount
    FROM customers
    INNER JOIN payments
        ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)


# STEP 6: Employees whose customers have an average credit limit above 90,000
df_credit = pd.read_sql("""
    SELECT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           COUNT(customers.customerNumber) AS num_customers
    FROM employees
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber,
             employees.firstName,
             employees.lastName
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY num_customers DESC;
""", conn)


# STEP 7: Product sales
df_product_sold = pd.read_sql("""
    SELECT products.productName,
           COUNT(orderdetails.orderNumber) AS numorders,
           SUM(orderdetails.quantityOrdered) AS totalunits
    FROM products
    INNER JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    GROUP BY products.productCode,
             products.productName
    ORDER BY totalunits DESC;
""", conn)


# STEP 8: Number of different customers who purchased each product
df_total_customers = pd.read_sql("""
    SELECT products.productName,
           products.productCode,
           COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    INNER JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    INNER JOIN orders
        ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode,
             products.productName
    ORDER BY numpurchasers DESC;
""", conn)


# STEP 9: Number of customers per office
df_customers = pd.read_sql("""
    SELECT offices.officeCode,
           offices.city,
           COUNT(customers.customerNumber) AS n_customers
    FROM offices
    INNER JOIN employees
        ON offices.officeCode = employees.officeCode
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode,
             offices.city
    ORDER BY offices.city ASC;
""", conn)


# STEP 10: Employees who sold products ordered by fewer than 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           offices.city,
           offices.officeCode
    FROM employees
    INNER JOIN offices
        ON employees.officeCode = offices.officeCode
    INNER JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    INNER JOIN orders
        ON customers.customerNumber = orders.customerNumber
    INNER JOIN orderdetails
        ON orders.orderNumber = orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT orderdetails.productCode
        FROM orderdetails
        INNER JOIN orders
            ON orderdetails.orderNumber = orders.orderNumber
        GROUP BY orderdetails.productCode
        HAVING COUNT(DISTINCT orders.customerNumber) < 20
    )
    ORDER BY employees.firstName ASC;
""", conn)


# Close the database connection
conn.close()
