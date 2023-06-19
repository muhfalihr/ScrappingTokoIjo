# Impor library yang diperlukan:
from bs4 import BeautifulSoup # Untuk melakukan parsing HTML.
from selenium import webdriver # Untuk mengendalikan browser secara otomatis.
from selenium.webdriver.support.ui import WebDriverWait # Untuk menunggu elemen muncul pada halaman web.
from selenium.webdriver import ActionChains # Untuk menggerakkan mouse pada halaman web.
from selenium.webdriver.chrome.options import Options # Untuk mengatur opsi Chrome.
import pandas as pd # untuk menganalisis, membersihkan, menjelajahi, dan memanipulasi data.
import time

def scrap(url, nama_file):
    # Mengatur opsi Chrome, termasuk pengaturan user-agent.
    option = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    option.add_argument('user-agent={0}'.format(user_agent))

    # Membuat contoh objek WebDriver dengan menggunakan ChromeDriver dan opsi yang telah diatur.
    driver = webdriver.Chrome(options=option)
    wait = WebDriverWait(driver, 20)
    action = ActionChains(driver)

    link_web = f'{url}'

    # Membuka URL halaman web menggunakan get() dan menunggu 5 detik untuk memastikan halaman sepenuhnya dimuat.
    driver.set_window_size(2560, 1440) # ukuran window website
    driver.get(link_web)
    time.sleep(5)

    # Melakukan scroll pada halaman web sebanyak 9 kali dengan jarak scroll sebesar 500 px dan jeda waktu 1 detik setiap kali scroll.
    scroll = 500
    for i in range(1, 10):
        akhir = scroll*i
        perintah = f"window.scrollTo(0, {str(akhir)})"
        driver.execute_script(perintah)
        print(f"Loading ke{str(i)}")
        time.sleep(1)

    # Mengambil screenshot halaman web menggunakan save_screenshot() dan menyimpannya sebagai file "display.png".
    driver.save_screenshot('display.png')

    # Mengambil konten halaman web menggunakan page_source.
    content = driver.page_source
    driver.quit() # Menutup browser

    # Menginisialisasi objek BeautifulSoup dengan konten halaman web dan menggunakan parser HTML.
    data = BeautifulSoup(content, 'html.parser')

    # Membuat list kosong dataAll untuk menyimpan semua data hasil scraping.
    dataAll = []


    # Melakukan iterasi melalui setiap area pada halaman web menggunakan find_all().
    for area in data.find_all('div', class_='css-bk6tzz e1nlzfl2'):
        
        # Mengambil data seperti name, image, price, address, dan link menggunakan metode find() dan atribut class yang sesuai.
        name = area.find('span', 'css-1bjwylw').get_text()
        try: image = area.find('img', class_='success fade')['src']
        except Exception:
            image = None
        price = area.find('span', class_='css-o5uqvq').get_text()
        address = area.find('span', class_='css-1kr22w3').get_text()
        link = area.find('a', class_='css-89jnbj')['href']

        # Menambahkan data ke dalam dataAll sebagai Dictionary.
        dataAll.append({
            "name": name,
            "image": image,
            "price": price,
            "address": address,
            "link": link
        })
    
    # Memisahkan data dari dataAll ke dalam list terpisah seperti listNm, listImg, listPrc, listAdrs, dan listLnk.
    listNm, listImg, listPrc, listAdrs, listLnk = [],[],[],[],[]

    for i in dataAll:
        listNm.append(i["name"])
        listImg.append(i["image"])
        listPrc.append(i["price"])
        listAdrs.append(i["address"])
        listLnk.append(i["link"])

    # Membuat DataFrame pandas menggunakan list yang telah dipisahkan.
    df = pd.DataFrame({"Name": listNm,
                    "Image": listImg,
                    "Price": listPrc,
                    "Address": listAdrs,
                    "Link": listLnk
                    })
    
    # Menyimpan DataFrame ke dalam file Excel menggunakan to_excel().
    with pd.ExcelWriter(f'result\{nama_file}.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer._save() # Menutup file Excel.