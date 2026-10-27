### Deskripsi Program
Program mengimplementasikan Key Distribution Center (KDC) untuk mendistribusikan session key antara alice & bob. Komunikasi pesan dengan algoritma AES dengan pertukaran key dapat diperbarui tanpa restart program.

### Penjelasan Code
#### aes.py
Implementasi AES secara manual dengan fungsi mengenkripsi plaintext menjadi chipertext dan mendekripsi chipertext kembali menajdi plaintext menggunakan key.
#### kdc.py
Server KDC yang mengelola master key alice & bob dengan menerima session key, membuat key untuk komunikasi, mengirimkan tiket kepada alice dan menangani pembaruan master key.
#### alice.py
Sebagai client alice yang meminta session key kepada KDC lalu melakukan autentikasi dengan bob, menerima dan mengirim pesn yang dienkripsi menggunakan AES serta menerima pembaruan master key dari KDC.
#### bob.py
Sebagai client/server bob yang menerima koneksi dari alice, memverifikasi tiket dan autentikasi, serta melakukan komunikasi dua arah menggunakan session key AES. Bob juga mendukung pembaruan master key dari KDC.

### Konfigurasi Jaringan
#### KDC: 192.168.180.130
#### Port KDC: 5000
#### Port pembaruan key: 5001
#### Bob: 192.168.180.133
#### Port Bob: 6000
#### Alice: Windows
