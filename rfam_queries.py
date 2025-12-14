import mysql.connector

conn = mysql.connector.connect(
    host="mysql-rfam-public.ebi.ac.uk",
    port=4497,
    user="rfamro",
    database="Rfam"
)

cursor = conn.cursor()

queries = [
    # Q2a
    "SELECT COUNT(DISTINCT species) FROM taxonomy WHERE species LIKE 'Panthera tigris%'",
    "SELECT ncbi_id, species FROM taxonomy WHERE species LIKE '%sumatra%'",
    # Q2b
    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='Rfam' AND COLUMN_NAME IN ('rfam_acc','rfamseq_acc','ncbi_id')",
    # Q2c
    "SELECT t.species, MAX(r.length) FROM taxonomy t JOIN rfamseq r ON t.ncbi_id=r.ncbi_id WHERE t.species LIKE '%Oryza%' GROUP BY t.species ORDER BY MAX(r.length) DESC LIMIT 1",
    # Q2d
    "SELECT COUNT(*) FROM (SELECT f.rfam_acc FROM family f JOIN full_region fr ON f.rfam_acc=fr.rfam_acc JOIN rfamseq r ON fr.rfamseq_acc=r.rfamseq_acc GROUP BY f.rfam_acc HAVING MAX(r.length)>1000000) AS large_families"
]

for i, query in enumerate(queries):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Query {i+1} results: {results[:3]}")  # Show first 3 results
    except Exception as e:
        print(f"Query {i+1} error: {e}")

cursor.close()
conn.close()