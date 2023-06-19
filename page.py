# import library function scrap dari module scrap
from scrap import scrap

# Scraping akan dilakukan pada 10 halaman yang berbeda.
for i in range(1, 11):
    # Nilai i akan digunakan untuk mengganti bagian {i} dalam URL untuk mencapai halaman yang sesuai,
    # serta menambahkan angka pada nama file agar setiap file hasil scraping memiliki nama yang unik.
    scrap(f'https://www.tokopedia.com/p/komputer-laptop/komponen-komputer?page={i}', f'Komponen_Komputer-{i}')
    print(f"Scraping ke-{i} DONE!")