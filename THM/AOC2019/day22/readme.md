Challenge kali ini kurang lebih sama dengan day21. Download file yang diperlukan dan extract file
```
unzip rechallenge.zip
|_ if1
|
|_ if2
|
|_ if.c
```

selanjutnya karena dari hint yang diberikan adalah `The questions below relate to the if2 binary.`, maka kita langsung saja fokus ke file `if2`.

buka file `if2` dengan `r2`
```
r2 -d if2 
...
[0x00400a30]> aaa
[Invalid address from 0x004843bcith sym. and entry0 (aa)
Invalid address from 0x0047b11d
Invalid address from 0x0047b191
...
[0x00400a30]>
```

selanjutnya cari main function dengan cara 
```
[0x00400a30]> afl | grep main
0x00400df0  114 1657         sym.__libc_start_main
0x0048fa50   16 247  -> 237  sym._nl_unload_domain
0x00403af0  308 5366 -> 5301 sym._nl_load_domain
0x00470440    1 49           sym._IO_switch_to_main_wget_area
0x00403850   39 672  -> 640  sym._nl_find_domain
0x00400b4d    4 43           main 
0x0048fa00    7 73   -> 69   sym._nl_finddomain_subfreeres
0x0044ce20    1 8            sym._dl_get_dl_main_map
0x00415f00    1 43           sym._IO_switch_to_main_get_area
[0x00400a30]>
```

pindah ke main function
```
[0x00400a30]> pdf@main                                                                                                               
            ; DATA XREF from entry0 @ 0x400a4d                                                                                       
┌ 43: int main (int argc, char **argv, char **envp);                                                                                 
│           ; var int64_t var_8h @ rbp-0x8                                                                                           
│           ; var int64_t var_4h @ rbp-0x4
│           0x00400b4d      55             push rbp
│           0x00400b4e      4889e5         mov rbp, rsp
│           0x00400b51      c745f8080000.  mov dword [var_8h], 8
│           0x00400b58      c745fc020000.  mov dword [var_4h], 2
│           0x00400b5f      8b45f8         mov eax, dword [var_8h]
│           0x00400b62      3b45fc         cmp eax, dword [var_4h]
│       ┌─< 0x00400b65      7e06           jle 0x400b6d
│       │   0x00400b67      8345f801       add dword [var_8h], 1
│      ┌──< 0x00400b6b      eb04           jmp 0x400b71
│      ││   ; CODE XREF from main @ 0x400b65
│      │└─> 0x00400b6d      8345fc07       add dword [var_4h], 7
│      │    ; CODE XREF from main @ 0x400b6b
│      └──> 0x00400b71      b800000000     mov eax, 0
│           0x00400b76      5d             pop rbp
└           0x00400b77      c3             ret
[0x00400a30]>
```

selanjutnya karena dari 2 pertanyaan berikut adalah mempertanyakan value sebelum akhir dari main function,

1. what is the value of local_8h before the end of the main function?
2. what is the value of local_4h before the end of the main function?

maka kita hanya perlu setting 1 breakpoint saja. kita pasang breakpoint pada `mov eax`
```
[0x00400a30]> db 0x00400b71                                               
[0x00400a30]> pdf@main
            ; DATA XREF from entry0 @ 0x400a4d
┌ 43: int main (int argc, char **argv, char **envp);                      
│           ; var int64_t var_8h @ rbp-0x8                                                                                           
│           ; var int64_t var_4h @ rbp-0x4                                                                                           
│           0x00400b4d      55             push rbp                                                                                  
│           0x00400b4e      4889e5         mov rbp, rsp                                                                              
│           0x00400b51      c745f8080000.  mov dword [var_8h], 8                                                                     
│           0x00400b58      c745fc020000.  mov dword [var_4h], 2                                                                     
│           0x00400b5f      8b45f8         mov eax, dword [var_8h]                                                                   
│           0x00400b62      3b45fc         cmp eax, dword [var_4h]                                                                   
│       ┌─< 0x00400b65      7e06           jle 0x400b6d                                                                              
│       │   0x00400b67      8345f801       add dword [var_8h], 1                                                                     
│      ┌──< 0x00400b6b      eb04           jmp 0x400b71                                                                              
│      ││   ; CODE XREF from main @ 0x400b65                                                                                         
│      │└─> 0x00400b6d      8345fc07       add dword [var_4h], 7                                                                     
│      │    ; CODE XREF from main @ 0x400b6b                                                                                         
│      └──> 0x00400b71 b    b800000000     mov eax, 0
│           0x00400b76      5d             pop rbp
└           0x00400b77      c3             ret
[0x00400a30]>
```

selanjutnya kita jalankan program dengan `dc`.
```
[0x00400a30]> dc
hit breakpoint at: 0x400b71
```

selanjutnya, kita akan cek value dari local_8h dengan cara
```
[0x00400b71]> px@rbp-0x8
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF 
0x7ffdf6ded898  **** 0000 0200 0000 5018 4000 0000 0000  ........P.@.....
0x7ffdf6ded8a8  f910 4000 0000 0000 0000 0000 0000 0000  ..@.............       
0x7ffdf6ded8b8  0000 0000 0100 0000 c8d9 def6 fd7f 0000  ................
```

kita daapat jawaban dari pertanyaan pertama pada bagian `****`.


selanjutnya melihat value dari local_4h dengan cara
```
[0x00400b71]> px@rbp-0x4
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x7ffdf6ded89c  0200 0000 5018 4000 0000 0000 f910 4000  ....P.@.......@.
0x7ffdf6ded8ac  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x7ffdf6ded8bc  0100 0000 c8d9 def6 fd7f 0000 4d0b 4000  ............M.@.
```