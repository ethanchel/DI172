import psycopg2


class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def connect(self):
        """Create and return a database connection."""
        connection = psycopg2.connect(
            database="restaurant_db",
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432"
        )
        return connection

    def save(self):
        """Save the item to the Menu_Items table."""
        connection = None
        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = "INSERT INTO Menu_Items (item_name, item_price) VALUES (%s, %s)"
            cursor.execute(query, (self.name, self.price))
            connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error saving item: {e}")
            return False
        finally:
            if connection:
                connection.close()

    def delete(self):
        """Delete the item from the Menu_Items table by name."""
        connection = None
        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = "DELETE FROM Menu_Items WHERE item_name = %s"
            cursor.execute(query, (self.name,))
            rows_deleted = cursor.rowcount
            connection.commit()
            cursor.close()
            return rows_deleted > 0
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
        finally:
            if connection:
                connection.close()

    def update(self, new_name, new_price):
        """Update the item's name and price in the Menu_Items table."""
        connection = None
        try:
            connection = self.connect()
            cursor = connection.cursor()
            query = "UPDATE Menu_Items SET item_name = %s, item_price = %s WHERE item_name = %s"
            cursor.execute(query, (new_name, new_price, self.name))
            rows_updated = cursor.rowcount
            connection.commit()
            cursor.close()
            if rows_updated > 0:
                self.name = new_name
                self.price = new_price
                return True
            return False
        except Exception as e:
            print(f"Error updating item: {e}")
            return False
        finally:
            if connection:
                connection.close()
