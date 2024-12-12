# Gunakan image Python yang sesuai
FROM python:3.10-slim

# Setel direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt ke dalam container
COPY requirements.txt .

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Instal protobuf versi yang kompatibel
RUN pip install protobuf==3.19.6

# Instal TensorFlow dan Keras versi kompatibel
RUN pip install tensorflow==2.10 keras==2.10

# Salin file model ke dalam container
COPY sleep_quality.pkl /app/
COPY sleep_duration.pkl /app/

# Salin seluruh aplikasi ke dalam container
COPY . .

# Tentukan port untuk aplikasi Flask
EXPOSE 8080

# Jalankan aplikasi Flask menggunakan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]