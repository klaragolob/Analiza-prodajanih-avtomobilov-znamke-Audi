import requests
import os
import re

#url of the main page of the audi listing
audi_frontpage_url = "https://www.avto.net/Ads/results.asp?znamka=Audi&model=&modelID=&tip=katerikoli%20tip" \
                     "&znamka2=&model2=&tip2=katerikoli%20tip&znamka3=&model3=&tip3=katerikoli%20tip&cenaMin=0&" \
                     "cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=0&ccmMin=0&ccmMax=99999" \
                     "&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=&motorvalji=&lokacija=0&sirina=" \
                     "&dolzina=&dolzinaMIN=&dolzinaMAX=&nosilnostMIN=&nosilnostMAX=&lezisc=&presek=&premer=&col=&vijakov=" \
                     "&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=1000000000&EQ5=" \
                     "1000000000&EQ6=1000000000&EQ7=1110100120&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PSLO=" \
                     "&akcija=&paketgarancije=&broker=&prikazkategorije=&kategorija=&zaloga=&arhiv=&presort=&tipsort=&stran="

#the directory to which we save out data
audi_directory = "audi_data"
#the file name we use to save the frontpage
frontpage_filename = "audi_data.html"
#the filename for the csv file for the extracted data
csv_filename = "audi_data.csv"


#getting data from the web

def download_url_to_string(url, i):
    '''This funtion takes a url as argument and tries to download
          it using requests. Upon success, it returns the page
          contents as string'''
    url += str(i)
    webpage = requests.get(url)
    if webpage.ok:
        webpage_text = webpage.text
    else:
        webpage_text = "Unable"
    return webpage_text

def save_string_to_file(text, directory, filename):
    '''This function writes "text" to file "filename" located in directory
       "directory". IF ""directory" is the empty string, use the
       current directory.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as file_out:
        file_out.write(text)
    return None







#processing data

def read_file_to_string(directory, filename):
    '''This function returns the contents of the file as string'''
    path =os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read

def split_text_to_prod(text):
    pattern = re.compile(
                        r'<a class="Adlink" href="../Ads/details.asp\?id=(?P<id>\d+)&display=(?P<name>.*?)">\r\n.*?'
                        r'<li>Letnik 1.registracije:(?P<registration>\d+)</li>.*?'
                        r'<li>(?P<driven_km>.*?)</li>'
                        r'<li>(?P<motor>.*?),.*?'
                        r'REDNA OBJAVA CENE.*?(?P<price>\d+\.\d+)'
                         , re.DOTALL)
    listt =[]
    for pat in re.finditer(pattern, text):
        listt += [[pat.group('id'),str(pat.group('name').encode('utf-8')), pat.group('registration'), pat.group('driven_km'), pat.group('motor'), pat.group('price')]]
    return listt



def all_data(url):
    data = []
    for i in range(1,31):
        text = download_url_to_string(url, 1)
        data += split_text_to_prod(text)
    return data



def convert_to_csv(info, head, name):
    with open(ime,'w') as csvFile:
        csvFile.write(head)
        for line in info:
            csvFile.write(','.join(line) + '\n')
    csvFile.close()


head = "Indeks,Ime,Prva registracija,Prevoženi km,Tip motorja,Cena"

#Klicanje funkcij
data = all_data(audi_frontpage_url)
convert_to_csv(data,head,csv_filename)






    

