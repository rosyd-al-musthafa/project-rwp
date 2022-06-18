function salin_teks (teks) {
    navigator.clipboard.writeText(document.getElementById(teks).value);
}

function login (url) {
    location.assign(url);
}

function logout (url) {
    if (confirm('Apakah anda yakin ingin logout ?')) {
        location.assign(url);
    }
} 