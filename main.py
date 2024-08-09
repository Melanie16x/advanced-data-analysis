import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Conexion a MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()

# Crear la base de datos
cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")
cursor.execute("USE CompanyData")

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS EmployeePerformance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    department VARCHAR(20),
    performance_score FLOAT,
    years_with_company INT,
    salary FLOAT
)
""")

# Extracción y análisis de datos
df = pd.read_sql("SELECT * FROM EmployeePerformance", con=db)

# Estadisticas por departamento
departament = df['department'].unique()

for dept in departament:
    dept_df = df[df['department'] == dept]

    # Calcular estadísticas
    mean_perf = dept_df['performance_score'].mean()
    median_perf = dept_df['performance_score'].median()
    std_perf = dept_df['performance_score'].std()

    mean_salary = dept_df['salary'].mean()
    median_salary = dept_df['salary'].median()
    std_salary = dept_df['salary'].std()

    total_employees = dept_df.shape[0]

    # verificar si hay suficientes datos para calcular la correlación
    if total_employees > 1:
        corr_years_perf = dept_df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
        corr_salary_perf = dept_df[['salary', 'performance_score']].corr().iloc[0, 1]
    else:
        corr_years_perf = "No suficiente data"
        corr_salary_perf = "No suficiente data"

    print(f"Estadísticas para el departamento '{dept}':")
    print(f"Media, mediana y desviación estándar de performance_score: {mean_perf}, {median_perf}, {std_perf}")
    print(f"Media, mediana y desviación estándar de salary: {mean_salary}, {median_salary}, {std_salary}")
    print(f"Número total de empleados: {total_employees}")
    print(f"Correlación entre years_with_company y performance_score: {corr_years_perf}")
    print(f"Correlación entre salary y performance_score: {corr_salary_perf}")
    print()
    
# Visualizacion de datos
for dept in departament:
    dept_df = df[df['department'] == dept]

    # Histograma
    plt.figure()
    plt.hist(dept_df['performance_score'], bins=10, edgecolor='black')
    plt.title(f"Histograma de performance_score - Departamento {dept}")
    plt.xlabel("Performance_Score")
    plt.ylabel("Frecuencia")
    plt.show()

# Gráfico de dispersión de years_with_company vs. performance_score
plt.figure()
plt.scatter(df['years_with_company'], df['performance_score'], c='blue')
plt.title("Years with Company vs. Performance Score")
plt.xlabel("Years with Company")
plt.ylabel("Performance Score")
plt.show()

# Gráfico de dispersion de salary vs. performance_score
plt.figure()
plt.scatter(df['salary'], df['performance_score'], c='green')
plt.title("Salary vs. Performance Score")
plt.xlabel("Salary")
plt.ylabel("Performance Score")
plt.show()

# Cerrar la conexión a la base de datos
cursor.close()
db.close()