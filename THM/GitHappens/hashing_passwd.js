function digest(password) {
    const encoder = new TextEncoder(),
        data = encoder.encode(password + 'SaltyBob'),
        hashBuffer = await crypto.subtle.digest('SHA-512', data),
        hashArray = Array.from(new Uint8Array(hashBuffer)),
        hashedPassword = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashedPassword;
}

console.log(digest(admin))