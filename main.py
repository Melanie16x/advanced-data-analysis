import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Clase para manejar la conexión a la base de datos
class DatabaseConnection:
    def __init__(self, host, user, password):
        # Inicializa los atributos
        self.host = host
        self.user = user
        self.password = password
        self.db = None
        self.cursor = None
    
    # Realiza la coneccion
    def connect(self, database_name):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.cursor = self.db.cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        self.cursor.execute(f"USE {database_name}")
    
    # Ejecuta la consulta sql
    def execute_query(self, query):
        self.cursor.execute(query)
    
    # Recupera datos de la base de dats
    def fetch_data(self, query):
        return pd.read_sql(query, con=self.db)
    
    # cierra la coneccion con la base de datos
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

# Clase para manejar los datos de rendimiento de empleados
class EmployeePerformanceData:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.df = None
    
    def create_table(self):
        self.db_connection.execute_query("""
        CREATE TABLE IF NOT EXISTS EmployeePerformance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            department VARCHAR(20),
            performance_score FLOAT,
            years_with_company INT,
            salary FLOAT
        )
        """)
    
    
    # Carga los datos de la tabla EmployeePerformance en un DataFrame
    def load_data(self):
        self.df = self.db_connection.fetch_data("SELECT * FROM EmployeePerformance")
    
    # Obtiene una lista de departamentos unicos de los datos
    def get_departments(self):
        return self.df['department'].unique()
    
    # Filtra los datos para un departamento especifico
    def get_department_data(self, department):
        return self.df[self.df['department'] == department]

# Clase para realizar analisis de datos
class DataAnalysis:
    
    # Calcula estadisticas basicas y correlaciones para un departamento
    def calculate_statistics(department_data):
        stats = {
            'mean_perf': department_data['performance_score'].mean(),
            'median_perf': department_data['performance_score'].median(),
            'std_perf': department_data['performance_score'].std(),
            'mean_salary': department_data['salary'].mean(),
            'median_salary': department_data['salary'].median(),
            'std_salary': department_data['salary'].std(),
            'total_employees': department_data.shape[0]
        }
        if stats['total_employees'] > 1:
            stats['corr_years_perf'] = department_data[['years_with_company', 'performance_score']].corr().iloc[0, 1]
            stats['corr_salary_perf'] = department_data[['salary', 'performance_score']].corr().iloc[0, 1]
        else:
            stats['corr_years_perf'] = "No hay suficiente datos"
            stats['corr_salary_perf'] = "No hay suficiente datos"
        return stats
    

    # Imprime las estadisticas calculadas
    def print_statistics(department, stats):
        print(f"Estadísticas para el departamento '{department}':")
        print(f"Media, mediana y desviación estándar de performance_score: {stats['mean_perf']}, {stats['median_perf']}, {stats['std_perf']}")
        print(f"Media, mediana y desviación estándar de salary: {stats['mean_salary']}, {stats['median_salary']}, {stats['std_salary']}")
        print(f"Número total de empleados: {stats['total_employees']}")
        print(f"Correlación entre years_with_company y performance_score: {stats['corr_years_perf']}")
        print(f"Correlación entre salary y performance_score: {stats['corr_salary_perf']}")
        print()

# Clase para visualización de datos
class DataVisualization:
    # Genera un histograma de las puntuaciones de rendimiento por departamento
    def plot_histogram(department, department_data):
        plt.figure()
        plt.hist(department_data['performance_score'], bins=10, edgecolor='black')
        plt.title(f"Histograma de performance_score - Departamento {department}")
        plt.xlabel("Performance_Score")
        plt.ylabel("Frecuencia")
        plt.show()
    
    # Genera un grafico de dispersion
    def plot_scatter(x, y, x_label, y_label, title, color='blue'):
        plt.figure()
        plt.scatter(x, y, c=color)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

# Clase principsl para ejecutar el analisis de rendimiento de empleados
class EmployeePerformanceAnalysis:
    
    # Inicializa la conexion y el manejo de datos
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.performance_data = EmployeePerformanceData(db_connection)
    
    # Ejecuta el analisis completo
    def run_analysis(self):
        self.performance_data.create_table()
        self.performance_data.load_data()
        departments = self.performance_data.get_departments()
        
        for dept in departments:
            dept_data = self.performance_data.get_department_data(dept)
            stats = DataAnalysis.calculate_statistics(dept_data)
            DataAnalysis.print_statistics(dept, stats)
            DataVisualization.plot_histogram(dept, dept_data)
        
        # Graficos de dispersion generales
        DataVisualization.plot_scatter(
            self.performance_data.df['years_with_company'],
            self.performance_data.df['performance_score'],
            "Years with Company",
            "Performance Score",
            "Years with Company vs. Performance Score"
        )
        
        DataVisualization.plot_scatter(
            self.performance_data.df['salary'],
            self.performance_data.df['performance_score'],
            "Salary",
            "Performance Score",
            "Salary vs. Performance Score",
            color='green'
        )
        
# Crear conexion, ejecutar analisis y cerrar la conexion
db_conn = DatabaseConnection(host="localhost", user="root", password="")
db_conn.connect(database_name="CompanyData")

analysis = EmployeePerformanceAnalysis(db_connection=db_conn)
analysis.run_analysis()

db_conn.close()
