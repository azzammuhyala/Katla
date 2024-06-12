r"""
```
Anda menemukan karakter SUKI!
                                              .........                                             
                                   .-*%@%+:::::::::::::::::+%@%*-.                                  
                               :=*@@@@@@@@+:::::::::::::::+@@@@@@@@#=:                              
                           :+%@@@@@@@@@@@%---::::::--::----%@@@@@@@@@@@%+-                          
       -%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:     
        =#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+      
           =@@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@@@@@%%%%%%%%%%%%%%%%%%%%@@@@@-        
            @@@@*..:::::::::=+**#**=-:::::::---*@@@@@@%=====------+*+++==-::::::::::::%@@@#         
            *@@@@..::.   .=*##%%%@@%*=:.....::-@@@@@@@@+-----:   +@@%*++==--:....:::::@@@@:         
            :@@@@-:::    .+*#%%@@@@@#+=:....:-*@@@@@@@@@==---    .%%@%**++==-:......:*@@@%          
             %@@@*:::    =**#@@@@@@@@***:::::-@@@@@@@@@@*===-.  .#@%@@%#**++==:.....:@@@@+          
             +@@@@::::::***#@@@@@@@@@%##-::::#@@@@@@@@@@@=====+*@@@@@@@%#**+++-.....=@@@@.          
             :@@@@+:::::*%@@@@@@@@@@@@@#--::=@@@@@@@@@@@@#====*@@@@@@@@@%##**+::..:.#@@@%           
              #@@@@-::::-*@@@@@@@@@@@@%=----%@@@@@@@@@@@@@++++=#@@@@@@@@@%%#*-::::.+@@@@-           
              .%@@@@+-:::-=#@@@@@@@@%#==--=%@@@@@%%%%@@@@@@*++==*%@@@@@@@@#+-:::::*@@@@+            
                +@@@@@*=-::-=++***++=--=+#@@@@@@#****#@@@@@@%#+===+*####*=--::-+#@@@@@=             
                 +@@@@@@@@%###########%@@@@@@@#*++++++*#@@@@@@@@%###########%@@@@@@@=               
                 -=*%@@@@@@@@@@@@@@@@@@@@@@%#++++++++++++#%@@@@@@@@@@@@@@@@@@@@@@%*.                
                 :----+*%%%@@@@@@@@@@@%%#*+====+++++++=====+*#%%@@@@@@@@@@@@%%*+=--                 
                 .-----=+-------==---------=====+++++======---------====-=+-------:                 
                  ------=-----:-+*-:-------======++========--------=+----+*-------.                 
                  .--------------=--------=======+++=======--------**------------:                  
                   :----=++------------+%@@#*************#%@%#-------------------                   
                    --===++------------%@@@*=----------==+%@@@+-----------------.                   
                     :=======----------=#%@+:...........:=%%%*-----------+-----.                    
                      :=========--------==++.           .-+=========----------                      
                       .====================+++++++++++++++=============--==:                       
                         :===================++++++++++++++++=============-.                        
                           -+++++++========++++++++++++++++++++++++======.                          
                             -=+++++++++++++++++++++++++++++++++++++++-.                            
                               :-+++++++++++++++++++++************+=-.                              
                        ....::::--=++***************************++=--:::....                        
                     ....:::--==+++**####%################%%###***++==---:::...                     
                     ...::::--==++***###%%@@@@@@@@@@@@@@@@%%%###**++==---:::...                     
                        ....:::---==+++*****#############****+++===---:::....                       
                               .....::::::-----------------:::::......                              
-------++++++++============%%%#################%%~~%%#################%%%============++++++++-------
                                    ███████╗██╗   ██╗██╗  ██╗██╗                                    
                                    ██╔════╝██║   ██║██║ ██╔╝██║                                    
                                    ███████╗██║   ██║█████╔╝ ██║                                    
                                    ╚════██║██║   ██║██╔═██╗ ██║                                    
                                    ███████║╚██████╔╝██║  ██╗██║                                    
                                    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝                                    
-------++++++++============%%%#################%%~~%%#################%%%============++++++++-------
```

Modul yang di perlukan:
pip install:
  - asciiTUI
  - fernet
  - kbbi

"""

import components.module.jsonfl as jsonfl
import asciiTUI
import string
import kbbi
import os

class Indonesia_KBBI(kbbi.KBBI):

    def __init__(self) -> None:
        self.kata_dari_input = []
        self.hasil_penulusuran = {
            "4": set(),
            "5": set(),
            "6": set(),
            "7": set(),
            "8": set(),
            "9": set()
        }
        self.hasil_penulusuran_tidak_valid = []
        self.hasil_penulusuran_gagal = []
        self.file_hasil = jsonfl.Json('hasil-penulusuran.json', self.hasil_penulusuran, indent=None)
        self.file_gagal = jsonfl.Json('hasil-penulusuran-gagal.json', [], indent=None)
        self.total_berhasil = 0
        self.progress = 0

    def mengandung_huruf_nonkapital(self, word) -> bool:
        for char in word:
            if char not in string.ascii_lowercase:
                return False
        return True

    def cetak_progress(self, msg, color='\033[31m') -> None:
        print('{}  {}{} / {}\033[0m | Total: \033[36m{}\033[0m'
            .format(
                asciiTUI.justify(msg, 60, 'left', wrap=False),
                color,
                self.progress,
                len(self.kata_dari_input),
                self.total_berhasil
            )
        )

    def ubah_tipe_set_ke_list(self) -> dict[str, list]:
        hasil = dict()
        for key, value in self.hasil_penulusuran.items():
            hasil[key] = list(value)
        return hasil

    def simpan_data(self) -> None:
        self.file_gagal.load_write(self.hasil_penulusuran_gagal)
        self.file_hasil.load_write(self.ubah_tipe_set_ke_list())

    def cek_semua(self) -> None:
        pb = asciiTUI.Init_progress_bar(width=60)
        panjang_kata_yang_diberi = len(self.kata_dari_input)

        for word in self.kata_dari_input:
            self.progress += 1

            if str(len(word)) not in self.hasil_penulusuran.keys():
                self.cetak_progress('[\033[31mX\033[0m] Panjang kata tidak valid: {}, {}'.format(word, len(word)))

            elif word in self.hasil_penulusuran[str(len(word))]:
                self.cetak_progress('[\033[31mX\033[0m] Kata sudah ada: {}'.format(word))

            elif word in self.hasil_penulusuran_tidak_valid:
               self.cetak_progress('[\033[31mX\033[0m] Kata sudah dan tidak valid: {}'.format(word)) 

            elif self.mengandung_huruf_nonkapital(word):
                selesai = False

                while not selesai:
                    try:

                        super().__init__(word)
                        self.serialisasi()
                        self.hasil_penulusuran[str(len(word))].add(word)
                        self.total_berhasil += 1
                        self.cetak_progress(pb.strbar((self.progress / panjang_kata_yang_diberi) * 100), color='\033[32m')
                        selesai = True

                    except Exception as e:
                        kelasEksepsi = type(e).__name__
                        if kelasEksepsi == 'TidakDitemukan':
                            self.hasil_penulusuran_tidak_valid.append(word)
                        elif kelasEksepsi == 'BatasSehari':
                            self.cetak_progress('[\033[33mPERINGATAN\033[0m] Pencarian telah mencapai batas dalam sehari.. Hentikan program segera mungkin!'.format(kelasEksepsi, str(e)))
                            continue
                        else:
                            self.hasil_penulusuran_gagal.append(word)
                        self.cetak_progress('[\033[31mX\033[0m] {}: {}'.format(kelasEksepsi, str(e)))
                        selesai = True

            else:
                self.cetak_progress('[\033[31mX\033[0m] Kata hanya mengandung huruf non-kapital: {}'.format(word))

        self.simpan_data()
        print("[\033[32mSELESAI\033[0m] Semua kamus yang diberikan selesai di filter!")

    def atur_ular_result(self) -> None:
        self.hasil_penulusuran = {
            "4": set(),
            "5": set(),
            "6": set(),
            "7": set(),
            "8": set(),
            "9": set()
        }

    def bantuan(self) -> None:
        print('[\033[36mBANTUAN\033[0m] "?": Bantuan (saat ini), "!": Kirim semua inputan, "$": Cek hasil akhir, "*": Hapus semua inputan, "#": Hapus semua penulusuran yang ada, "%": Bersihkan terminal\n[\033[33mPERHATIAN\033[0m] Modul KBBI python ini memiliki batasan penggunaan. Harap jangan terlalu sering menggunakan program ini ditakutkan sistem kbbi mengira melakukan spam!')

    def terminal(self) -> None:
        self.bantuan()

        while True:

            word = input('Masukan kata: ').lower().strip()

            if word == '!':
                try:
                    self.atur_ular_result()
                    self.cek_semua()
                    self.hasil_penulusuran_tidak_valid.clear()
                    self.hasil_penulusuran_gagal.clear()
                    self.kata_dari_input.clear()
                    self.progress = 0
                    self.total_berhasil = 0
                except KeyboardInterrupt:
                    self.simpan_data()
                    print("[\033[32mCTRL + C\033[0m] Pembatalan mendadak, kamus yang ada di simpan di \033[36m{}\033[0m!".format(self.file_hasil.file_path))
                    input("TEKAN ENTER UNTUK KELUAR . . .")
                    break
                except Exception as e:
                    print(type(e).__name__ + ':', e, '\n')
                    continue

            elif word == '%':
                os.system('cls' if os.name == 'nt' else 'clear')

            elif word == '$':
                print(self.hasil_penulusuran)

            elif word == '*':
                self.hasil_penulusuran_tidak_valid.clear()
                self.hasil_penulusuran_gagal.clear()
                self.kata_dari_input.clear()
                self.progress = 0
                self.total_berhasil = 0

            elif word == '#':
                self.atur_ular_result()

            elif word == '?':
                self.bantuan()

            else:
                self.kata_dari_input.append(word)

indo = Indonesia_KBBI()
indo.terminal()