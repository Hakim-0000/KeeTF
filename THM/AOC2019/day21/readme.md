download file yang dibutuhkan.

extract file
```
unzip files.zip
...
|_ challenge1
|
|_ file1
```

materi pendukung dapat dilihat di [sini.](https://drive.google.com/file/d/1maTcdquyqnZCIcJO7jLtt4cNHuRQuK4x/view?usp=sharing)

ubah file permission pada 2 file hasil extract `chmod +x file`. Selanjutnya dapat coba untuk di run 
```
./file1
...
the value of a is 4, the value of b is 5 and the value of c is 9%


./challenge1

```

buka file challenge1 dengan r2 atau radare2 `r2 -d challenge1` atau `radare2 -d challenge`. Jika belum terinstall, dapat install dari [sini.](https://github.com/radareorg/radare2)

ketika sudah masuk, kita dapat masukkan inputan "aa"
```
[0x00400a30]>aa
...
[Invalid address from 0x004843acith sym. and entry0 (aa)
Invalid address from 0x0047b10d
Invalid address from 0x0047b181
Invalid address from 0x0044efc6
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00400a30]>
```

selanjutnya kita cari main function dengan cara

```
[0x00400a30]>afl | grep main
...
0x00400de0  114 1657         sym.__libc_start_main
0x0048fa40   16 247  -> 237  sym._nl_unload_domain
0x00403ae0  308 5366 -> 5301 sym._nl_load_domain
0x00470430    1 49           sym._IO_switch_to_main_wget_area
0x00403840   39 672  -> 640  sym._nl_find_domain
0x00400b4d    1 35           main
0x0048f9f0    7 73   -> 69   sym._nl_finddomain_subfreeres
0x0044ce10    1 8            sym._dl_get_dl_main_map
0x00415ef0    1 43           sym._IO_switch_to_main_get_area
[0x00400a30]>
```

untuk melihat main function, kita dapat melakukannya dengan cara
```
[0x00400a30]>pdf@main
            ; DATA XREF from entry0 @ 0x400a4d
┌ 35: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_ch @ rbp-0xc
│           ; var int64_t var_8h @ rbp-0x8
│           ; var int64_t var_4h @ rbp-0x4
│           0x00400b4d      55             push rbp
│           0x00400b4e      4889e5         mov rbp, rsp
│           0x00400b51      c745f4010000.  mov dword [var_ch], 1
│           0x00400b58      c745f8060000.  mov dword [var_8h], 6
│           0x00400b5f      8b45f4         mov eax, dword [var_ch]
│           0x00400b62      0faf45f8       imul eax, dword [var_8h]
│           0x00400b66      8945fc         mov dword [var_4h], eax
│           0x00400b69      b800000000     mov eax, 0
│           0x00400b6e      5d             pop rbp
└           0x00400b6f      c3             ret
[0x00400a30]>
```

selanjutnya kita akan membuat breakpoint pada beberapa instruksi sesuai dengan jumlah soal yang ada.

1. What is the value of local_ch when its corresponding movl instruction is called(first if multiple)?
2. What is the value of eax when the imull instruction is called?
3. What is the value of local_4h before eax is set to 0?

dari ketiga soal tersebut, kita akan membuat breakpoint pada bagian `local_ch`, `imull`, dan `mov eax`.

untuk membuat breakpoint pada 3 instruksi tersebut, kita dapat melakukannya dengan cara
```
[0x00400a30]> db 0x00400b51
[0x00400a30]> db 0x00400b62
[0x00400a30]> db 0x00400b69
[0x00400a30]> pdf@main
            ; DATA XREF from entry0 @ 0x400a4d
┌ 35: int main (int argc, char **argv, char **envp);
│           ; var int64_t var_ch @ rbp-0xc
│           ; var int64_t var_8h @ rbp-0x8
│           ; var int64_t var_4h @ rbp-0x4
│           0x00400b4d      55             push rbp
│           0x00400b4e      4889e5         mov rbp, rsp
│           0x00400b51 b    c745f4010000.  mov dword [var_ch], 1
│           0x00400b58      c745f8060000.  mov dword [var_8h], 6
│           0x00400b5f      8b45f4         mov eax, dword [var_ch]
│           0x00400b62 b    0faf45f8       imul eax, dword [var_8h]
│           0x00400b66      8945fc         mov dword [var_4h], eax
│           0x00400b69 b    b800000000     mov eax, 0
│           0x00400b6e      5d             pop rbp
└           0x00400b6f      c3             ret
[0x00400a30]>
```

selanjutnya kita dapat run programnya dengan command `dc`. dan jika kita `pdf@main` lagi, nantinya akan ada `rip` diatasnya dan `0x00400b51` akan di highlight berwarna hijau.
```
;-- rip:
│           0x00400b51 b    c745f4010000.  mov dword [var_ch], 1
```

selanjutnya kita akan navigasi ke `px @rbg-0xc`
```
[0x00400b51]> px@rbp-0xc
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x7ffccc5a9cf4  0000 0000 1890 6b00 0000 0000 4018 4000  ......k.....@.@.
0x7ffccc5a9d04  0000 0000 e910 4000 0000 0000 0000 0000  ......@.........
...
```

Karena kita mengatur breakpoint sebelum instruksi di run, lanjutkan dengan command `ds` lalu gunakan lagi `px @rbg-0xc`
```
[0x00400b51]> ds
[0x00400b51]> px@rbp-0xc
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x7ffccc5a9cf4  **** 0000 1890 6b00 0000 0000 4018 4000  ......k.....@.@.
0x7ffccc5a9d04  0000 0000 e910 4000 0000 0000 0000 0000  ......@.........
```

kita mendapat jawaban dari pertanyaan nomor 1 pada bagian yang bertanda `****`

kita lanjutkan program dengan command `dc`, dan kita akan berhenti di breakpoint kedua. Lanjutkan untuk maju satu line dengan `ds` tentunya, dan gunakan `dr` untuk menampilkan registri value
```
[0x00400b51]> dc
hit breakpoint at: 0x400b62
[0x00400b62]> ds
[0x00400b62]> dr
rax = 0x********
rbx = 0x00400400
...
```

dan kita mendapat jawaban dari pertanyaan kedua pada bagian yang bertanda `********`

lanjutkan lagi instruksi ke breakpoint terakhir dengan `dc`. selanjutnya kita dapat langsung query lokasi 4h dengan `px@rbp-0x4` (tidak perlu untuk maju 1 langkah).
```
[0x00400b69]> px@rbp-0x4
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x7ffccc5a9cfc  **** 0000 4018 4000 0000 0000 e910 4000  ....@.@.......@.
0x7ffccc5a9d0c  0000 0000 0000 0000 0000 0000 0000 0000  ................
```

dan kita dapatkan jawaban untuk pertanyaan terakhir pada bagian yang bertanda `****`.