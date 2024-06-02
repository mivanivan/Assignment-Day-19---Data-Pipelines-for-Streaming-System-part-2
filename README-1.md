# Assignment 19 - Data Pipelines for Streaming

1. Awalnya coding aman ketika prosesnya hanya merubah dari json menjadi parsed data
   
`![Kafka-Streaming_1](https://github.com/mivanivan/Assignment-Day-19---Data-Pipelines-for-Streaming-System-part-2/assets/107350801/322fe969-ee32-49ee-8dc8-53e181577d64)

2. Namun coding menjadi selalu error ketika sudah memasuki proses aggregasi
   
![Kafka-Streaming_2](https://github.com/mivanivan/Assignment-Day-19---Data-Pipelines-for-Streaming-System-part-2/assets/107350801/1965bcca-ae8f-4640-9238-3b21fbc44b56)

setelah saya cek dari log, sepertinya kesalahan tersebut terjadi karena aplikasi tidak dapat membuat direktori di direktori /tmp karena masalah izin atau mungkin karena direktori yang ada dengan nama yang bertentangan. Hal ini menyebabkan pekerjaan Spark gagal ketika mencoba memeriksa atau menyimpan status.
Di titik ini saya tidak tau harus melakukan perubahan dimana.


