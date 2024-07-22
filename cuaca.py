# Data Latihan
data_training_cuaca = [
    {'Suhu': 'Tinggi', 'Kelembaban': 'Rendah', 'Kecepatan_Angin': 'Sedang', 'Cuaca': 'Cerah'},
    { 'Suhu': 'Normal', 'Kelembaban': 'Tinggi', 'Kecepatan_Angin': 'Rendah', 'Cuaca': 'Berawan'},
    {'Suhu': 'Rendah', 'Kelembaban': 'Tinggi', 'Kecepatan_Angin': 'Tinggi', 'Cuaca': 'Hujan'},
    {'Suhu': 'Tinggi', 'Kelembaban': 'Rendah', 'Kecepatan_Angin': 'Rendah', 'Cuaca': 'Cerah'},
    {'Suhu': 'Normal', 'Kelembaban': 'Normal', 'Kecepatan_Angin': 'Sedang', 'Cuaca': 'Berawan'},
    { 'Suhu': 'Rendah', 'Kelembaban': 'Tinggi', 'Kecepatan_Angin': 'Tinggi', 'Cuaca': 'Hujan'},
    {'Suhu': 'Tinggi', 'Kelembaban': 'Tinggi', 'Kecepatan_Angin': 'Sedang', 'Cuaca': 'Hujan'},
    {'Suhu': 'Normal', 'Kelembaban': 'Rendah', 'Kecepatan_Angin': 'Rendah', 'Cuaca': 'Cerah'},
    {'Suhu': 'Tinggi', 'Kelembaban': 'Normal', 'Kecepatan_Angin': 'Tinggi', 'Cuaca': 'Berawan'},
    {'Suhu': 'Rendah', 'Kelembaban': 'Rendah', 'Kecepatan_Angin': 'Rendah', 'Cuaca': 'Cerah'},
]

def hitung_prioritas(data_training):
    total = len(data_training)
    count_cuaca = {'Cerah': 0, 'Berawan': 0, 'Hujan': 0}
    
    for data in data_training:
        count_cuaca[data['Cuaca']] += 1

    priors = {cuaca: (count + 1) / (total + 3) for cuaca, count in count_cuaca.items()}
    return priors


def hitung_likelihood(data_training, priors):
    likelihoods = {
        'Cerah': {'Suhu': {}, 'Kelembaban': {}, 'Kecepatan_Angin': {}},
        'Berawan': {'Suhu': {}, 'Kelembaban': {}, 'Kecepatan_Angin': {}},
        'Hujan': {'Suhu': {}, 'Kelembaban': {}, 'Kecepatan_Angin': {}}
    }
    feature_values = {'Suhu': [], 'Kelembaban': [], 'Kecepatan_Angin': []}

    for data in data_training:
        cuaca = data['Cuaca']
        for feature in ['Suhu', 'Kelembaban', 'Kecepatan_Angin']:
            value = data[feature]
            feature_values[feature].append(value)
            if value not in likelihoods[cuaca][feature]:
                likelihoods[cuaca][feature][value] = 0
            likelihoods[cuaca][feature][value] += 1
    
    for cuaca in likelihoods:
        for feature in likelihoods[cuaca]:
            total_values = sum(likelihoods[cuaca][feature].values())
            unique_values = len(set(feature_values[feature]))
            for value in likelihoods[cuaca][feature]:
                likelihoods[cuaca][feature][value] = (likelihoods[cuaca][feature][value] + 1) / (total_values + unique_values)
            # Menggunakan nilai prior yang lebih sesuai agar <UNK>
            likelihoods[cuaca][feature]['<UNK>'] = 1 / (total_values + unique_values)  # Disesuaikan agar tidak terlalu kecil
    
    return likelihoods

#klasifikasinya
def klasifikasi(suhu, kelembaban, kecepatan_angin, priors, likelihoods):
    probabilities = {cuaca: priors[cuaca] for cuaca in priors}
    
    for cuaca in probabilities:
        print(f"\nEvaluating for cuaca: {cuaca}")
        for feature, value in zip(['Suhu', 'Kelembaban', 'Kecepatan_Angin'], [suhu, kelembaban, kecepatan_angin]):
            if value in likelihoods[cuaca][feature]:
                probabilities[cuaca] *= likelihoods[cuaca][feature][value]
                print(f"  {feature} = {value}: {likelihoods[cuaca][feature][value]}")
            else:
                probabilities[cuaca] *= likelihoods[cuaca][feature]['<UNK>']
                print(f"  {feature} = {value} (UNK): {likelihoods[cuaca][feature]['<UNK>']}")
    
    print(f"Calculated probabilities: {probabilities}")
    return max(probabilities, key=probabilities.get)

#looping perhitungan
priors = hitung_prioritas(data_training_cuaca)
print("Priors:")
print(priors)

likelihoods = hitung_likelihood(data_training_cuaca, priors)
print("Likelihoods:")
for cuaca in likelihoods:
    print(f"Cuaca: {cuaca}")
    for feature in likelihoods[cuaca]:
        print(f"  Feature: {feature} - {likelihoods[cuaca][feature]}")

#testing nilainya
def prediksi_cuaca():
    hari = input("Masukkan hari: ")
    suhu = input("Masukkan kategori Suhu (Tinggi, Normal, Rendah): ").capitalize()
    kelembaban = input("Masukkan kategori Kelembaban (Tinggi, Normal, Rendah): ").capitalize()
    kecepatan_angin = input("Masukkan kategori Kecepatan Angin (Tinggi, Normal, Rendah): ").capitalize()

    cuaca = klasifikasi(suhu, kelembaban, kecepatan_angin, priors, likelihoods)
    print(" ")
    print(f"~ Prediksi Cuaca pada hari {hari} adalah: {cuaca}")
    print(" ")

prediksi_cuaca()
