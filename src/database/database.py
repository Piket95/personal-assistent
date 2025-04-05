import psycopg2

class PostgreSQLDatabase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                # Double-Checked Locking
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv()
        
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        
        self.connection = None
        self.connect()

    def connect(self):
        try:
            if not self.connection or self.connection.closed:
                self.connection = psycopg2.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    dbname=self.database
                )
                print("Datenbankverbindung hergestellt")
        except (Exception, psycopg2.Error) as error:
            print(f"Fehler bei Datenbankverbindung: {error}")
            raise

    def get_cursor(self):
        self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Datenbankverbindung geschlossen")
            self.connection = None

    def __del__(self):
        self.close()
