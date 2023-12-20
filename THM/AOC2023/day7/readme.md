# Q1
Pada pertanyaan pertama, ditanyakan **berapa banyak IP address yang unik**. Untuk dapat menjawabnya kita dapat melakukannya dengan cara
```
cut -d ' ' -f2 access.log | sort | uniq | wc -l
```
dan nanti kita akan mendapat jawaban dari pertanyaan pertama.

# Q2
Selanjutnya untuk menjawab pertanyaan kedua, yaitu **berapa banyak domain unik yang diakses oleh semua workstation**, kita dapat melakukannya dengan cara
```
cut -d ' ' -f3 access.log | cut -d ':' -f1 | sort | uniq | wc -l
```
dan nanti kita akan mendapat jawaban dari pertanyaan kedua.

# Q3
Selanjutnya untuk menjawab pertanyaan ketiga, yaitu **status code yang muncul pada domain yang paling sedikit dikunjungi**, kita dapat melakukannya dengan cara yang hampir sama seperti dengan cara menjawab pertanyaan kedua
```
cut -d ' ' -f3 access.log | cut -d ':' -f1 | sort | uniq -c | sort -n
```
setelah melakukan command tersebut, kita bisa tahu domain yang paling sedikit dikunjungi, dan jika kita dapat menggunakan `grep`
```
cut -d ' ' -f3,6 access.log | grep "partnerservices.getmicrosoftkey.com" | sort | uniq
```
dan jawaban untuk pertanyaan ketiga akan didapatkan

# Q4
Untuk dapat menjawab pertanyaan keempat, yaitu **cari domain aneh berdasarkan high count of connection attempt**, dapat dilakukan dengan cara
```
cut -d ' ' -f3 access.log | cut -d ':' -f1 | sort | uniq -c | sort -n | grep -v "www" | grep -v ".com"
```
dan kita akan mendapat jawaban untuk pertanyaan keempat

# Q5
Untuk kita dapat menjawab pertanyaan kelima **IP source yang mengakses malicious domain**, kita dapat melakukannya dengan cara
```
paste <(cut -d ' ' -f2 access.log) <(cut -d ' ' -f3 access.log | cut -d ':' -f1) | sort | uniq | grep ".thm"
```
dan kita akan mendapat jawaban untuk pertanyaan kelima.

# Q6
Untuk dapat menjawab pertanyaan keenam **banyak requst yang dibuat untuk malicious domain**, kita dapat menggunakan cara dari pertanyaan keempat
```
cut -d ' ' -f3 access.log | cut -d ':' -f1 | sort | uniq -c | sort -n | grep -v "www" | grep -v ".com"
```

# Q7
Untuk dapat menjawab pertanyaan ketujuh **cari hidden flag setelah exfiltrate data**, kita dapat menyelesaikannya dengan cara
```
grep "frostlings.bigbadstash.thm" access.log | cut -d ' ' -f5 | cut -d '=' -f2 | base64 -d | grep -i THM\{
```
