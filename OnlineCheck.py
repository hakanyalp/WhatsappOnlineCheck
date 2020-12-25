from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time

def WriteToFile(text):
    with open("OnlineTimes.txt", "a") as f:
        f.write(text + "\n")
    # f = open("OnlineTimes.txt", "a")
    # print(text, file=f, flush=False)
    # print("--------------------------------")
    # f.close()

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')

d1 = datetime.now()
d2 = datetime.now()

time.sleep(10)
status = ""
name = ""
onlineTime = 0
onlineCheck = False
d1_ts = 0.0
d2_ts = 0.0
firstCheck = True  # For write the first log info
activeCheck = False
activeDate = datetime.now()
passiveDate = datetime.now()
while 1:
    # Whatsapp active control
    whatsappCheckText = ""
    whatsappCheckText2 = ""
    try:
        whatsappCheckText = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div').text
    except:
        pass
    try:
        whatsappCheckText2 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div').text
    except:
        pass

    if (whatsappCheckText == "WhatsApp'ı bilgisayarınızda kullanmak için" or whatsappCheckText2 == "WHATSAPP WEB"):
        # Giriş yapamamışsa değil de giriş yapmışsa kontrolü yapmak gerekiyor
        if (firstCheck or activeCheck):
            writeText = "Whatsapp Not Active: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            WriteToFile(writeText)
            print(writeText)
            firstCheck = False
            activeCheck = False
        else:
            print("Whatsapp Not Active")
        time.sleep(10)

    else:
        if (firstCheck or not activeCheck):
            writeText = "Whatsapp Active Time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            WriteToFile(writeText)
            print(writeText)
            firstCheck = False
            activeCheck = True
        status = ""
        name = ""
        onlineTime = 0
        try:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]').click()
            name = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text
            try:
                status = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span").text
            except:
                pass
                # print("ERROR 2")
        except:
            print("ERROR 1")

        if (status == "çevrimiçi"):
            if (not onlineCheck):
                d1 = datetime.now()
                d1_ts = time.mktime(d1.timetuple())
            onlineCheck = True

        elif (status == "" and onlineCheck):
            d2 = datetime.now()
            d2_ts = time.mktime(d2.timetuple())
            onlineTime = int(d2_ts-d1_ts)
            onlineCheck = False
            
            enterExitText = name + " EnterTime: " + d1.strftime("%Y-%m-%d %H:%M:%S") + " & ExitTime: " + d2.strftime("%Y-%m-%d %H:%M:%S") + " => " + str(onlineTime) + " seconds"
            print(enterExitText)

            WriteToFile(enterExitText)

        print(name + " state: " + status)
        time.sleep(3)

