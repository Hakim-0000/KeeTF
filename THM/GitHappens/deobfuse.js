const createLoginFunction = function () {
    let isFirstTime = true;
    
    return function (context, callback) {
        if ('CbRnH' === 'CbRnH') {
            const loginFunction = isFirstTime ? function () {
                if ('TEhxP' !== 'TEhxP') {
                    function showError() {
                        document.getElementById('error').innerHTML = 'INVALID USERNAME OR PASSWORD!';
                    }
                } else {
                    if (callback) {
                        const result = callback.apply(context, arguments);
                        return callback = null, result;
                    }
                }
            } : function () {};

            return isFirstTime = false, loginFunction;
        } else {
            function validateFunction() {
                const func = isFirstTime ? function () {
                    if (callback) {
                        const result = callback.apply(context, arguments);
                        return callback = null, result;
                    }
                } : function () {};
                return isFirstTime = false, func;
            }
        }
    };
}();

const isRegexValid = createLoginFunction(this, function () {
    const environment = typeof window !== 'undefined' ? window : typeof process === 'object' && typeof require === 'function' && typeof global === 'object' ? global : this,
        isRegexMatch = function () {
            const regexPattern = new environment.RegExp('^([^ ]' + '+( +[^ ]+)+)' + '+[^ ]}');
            return !regexPattern.test(isRegexValid);
        };
    return isRegexMatch();
});

isRegexValid();

async function login() {
    let loginForm = document.getElementById('login-form');
    console.log(loginForm.elements);
    let username = loginForm.elements.username.value,
        passwordHash = await digest(loginForm.elements.password.value);
    if (username === 'admin' && passwordHash === '4004c23a71fd6ba9b03ec9cb7eed08471197d84319a865c5442a9d6a7c7cbea070f3cb6aa5106ef80f679a88dbbaf89ff64cb351a151a5f29819a3c094ecebbb') {
        document.cookie = 'login=1';
        window.location.href = '/dashboard.html';
    } else {
        document.getElementById('error').innerHTML = 'INVALID USERNAME OR PASSWORD!';
    }
}

async function digest(password) {
    const encoder = new TextEncoder(),
        data = encoder.encode(password + 'SaltyBob'),
        hashBuffer = await crypto.subtle.digest('SHA-512', data),
        hashArray = Array.from(new Uint8Array(hashBuffer)),
        hashedPassword = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashedPassword;
}
