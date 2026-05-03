import mysql.connector
from mysql.connector import Error
import os

class Database:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "db") # Default to 'db' for docker-compose
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "root")
        self.database = os.getenv("MYSQL_DATABASE", "reviews_db")
        self.connection = None
        self.connect_db()

    def connect_db(self):
        """Connects to the MySQL database and creates table if not exists."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL Database")
                self._create_table_if_not_exists()
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def _create_table_if_not_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            review_text TEXT,
            prediction VARCHAR(10),
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error creating table: {e}")

    def insert_review(self, text, prediction, confidence):
        """Inserts a new review into the database."""
        if not self.connection or not self.connection.is_connected():
            self.connect_db()
            
        query = """
        INSERT INTO reviews (review_text, prediction, confidence)
        VALUES (%s, %s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (text, prediction, float(confidence)))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error inserting review: {e}")
            return False

    def fetch_stats(self):
        """Fetches aggregated statistics for the dashboard."""
        if not self.connection or not self.connection.is_connected():
            self.connect_db()
            
        query_total = "SELECT COUNT(*) FROM reviews"
        query_genuine = "SELECT COUNT(*) FROM reviews WHERE prediction = 'Genuine'"
        query_fake = "SELECT COUNT(*) FROM reviews WHERE prediction = 'Fake'"
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(query_total)
            total = cursor.fetchone()[0]
            
            cursor.execute(query_genuine)
            genuine = cursor.fetchone()[0]
            
            cursor.execute(query_fake)
            fake = cursor.fetchone()[0]
            
            cursor.close()
            
            genuine_pct = round((genuine / total * 100), 2) if total > 0 else 0
            fake_pct = round((fake / total * 100), 2) if total > 0 else 0
            
            return {
                "total_reviews": total,
                "genuine_count": genuine,
                "fake_count": fake,
                "genuine_percentage": genuine_pct,
                "fake_percentage": fake_pct
            }
        except Error as e:
            print(f"Error fetching stats: {e}")
            return {
                "total_reviews": 0,
                "genuine_count": 0,
                "fake_count": 0,
                "genuine_percentage": 0,
                "fake_percentage": 0
            }
