import psycopg2
from menu_item import MenuItem


class MenuManager:
    @classmethod
    def connect(cls):
        """Create and return a database connection."""
        connection = psycopg2.connect(
            database="restaurant_db",
            user="postgres",
            password="your_password",  # Change this to your PostgreSQL password
            host="localhost",
            port="5432"
        )
        return connection

    @classmethod
    def get_by_name(cls, name):
        """Return a single MenuItem from the database by name, or None if not found."""
        connection = None
        try:
            connection = cls.connect()
            cursor = connection.cursor()
            query = "SELECT item_name, item_price FROM Menu_Items WHERE item_name = %s"
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return MenuItem(result[0], result[1])
            return None
        except Exception as e:
            print(f"Error getting item: {e}")
            return None
        finally:
            if connection:
                connection.close()

    @classmethod
    def all_items(cls):
        """Return a list of all MenuItems from the database."""
        connection = None
        try:
            connection = cls.connect()
            cursor = connection.cursor()
            query = "SELECT item_name, item_price FROM Menu_Items"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            items = []
            for row in results:
                item = MenuItem(row[0], row[1])
                items.append(item)
            return items
        except Exception as e:
            print(f"Error getting items: {e}")
            return []
        finally:
            if connection:
                connection.close()
