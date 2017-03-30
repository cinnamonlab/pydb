import mysql
import mysql.connector


#Start a connection
connector = mysql.connector.connect(host="dbhost", user="dbuser", password="dbpass", database="dbname")

# Start-1
cursor = connector.cursor()
try:
 cursor.execute("Your SQL")
 cursor.execute("Another sql")
 connector.commit()
except:
 connector.rollback()
# End-1




# Start-2
connector.start_transaction()
cursor = connector.cursor()
if connector.in_transaction:
    try:
        cursor.execute("Your SQL")
        cursor.execute("Another sql")
        connector.commit()
    except:
        connector.rollback()
else:
    print("Are not in transaction")
# End-2


# Start-3
try:
    cursor = connector.cursor()
    # move some money from one person to the other
    cursor.execute("UPDATE money SET amt = amt - 6 WHERE name = 'Eve'")
    cursor.execute("UPDATE money SET amt = amt + 6 WHERE name = 'Ida'")
    cursor.close()
    connector.commit()
except mysql.connector.Error as error:
    print("Transaction failed, rolling back. Error was:", error.args)
    try:  # empty exception handler in case rollback fails
        connector.rollback()
    except:
        pass
# End-3

# Start-4
cursor = connector.cursor()
try:
    cursor.execute(...)
except mysql.connector.Error as error:
    cursor.rollback()
    #raise error
else:
    cursor.commit()
finally:
    cursor.close()


# http://stackoverflow.com/questions/12378227/mysqldb-with-multiple-transaction-per-connection