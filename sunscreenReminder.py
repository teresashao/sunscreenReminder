import schedule
import smtplib
import requests
import getpass
from bs4 import BeautifulSoup
from datetime import date

from tkinter import *
global recieverEmail 
global reminderTime 

def fiveDayForcast():
    # creating url and requests instance
    url = "https://www.uvindextoday.com/usa/california/santa-clara-county/mountain-view-uv-index"
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    accordian = soup.find('div', class_='accordion')
    card1 = accordian.find('div', class_ = 'card')


    #create list of uv indicies for next five days
    alluvList = []
    forcast_allcards = accordian.find_all('div', class_ = 'card')
    for card in forcast_allcards:
        day_alluv = card.find_all('td', class_="align-middle text-center text-md-left")
        for num in day_alluv:
            alluvList.append(num.text)

    print(alluvList)

def dailyForcast():
    # creating url and requests instance
    state_url = state_field.get().replace(" ", "-")
    county_url = county_field.get().replace(" ", "-")
    city_url = city_field.get().replace(" ", "-")
    url = "https://www.uvindextoday.com/usa/" + state_url + "/"+ county_url + "/" + city_url + "-uv-index"
    print(url)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    accordian = soup.find('div', class_='accordion')
    card1 = accordian.find('div', class_ = 'card')
    day_alluv = card1.find_all('td', class_="align-middle text-center text-md-left")
    day_alltimes = card1.find_all('td', class_="align-middle")
    date_num = date.today()
    #create list of uv indicies for the day
    alluvList = []
    alltimesList = []
    count1 = 0

    need_sunscreen = False
    for num in day_alluv:
        if float(num.text) > 5:
             #CHECK GREATER THAN 5 CONDITION 
             need_sunscreen = True 
             alluvList.append(num.text)
             alltimesList.append(count1)
        count1 = count1 + 1
    
    #finds the first time you need sunscreen
    count2 = 0
    firstTime = ''
    stillfirst = True
    for t in day_alltimes:
        for index in alltimesList:
            if (index == count2 and stillfirst):
                firstTime = t.text
                stillfirst=False
        count2 = count2+1


    if need_sunscreen:
        sender_email = "teresashao068@gmail.com"
        rec_email = recEmail_field.get() 
        password = "jgsulbjjymkbgomh " 
        message = """Subject: PUT ON SUNSCREEN TODAY:""" + str(date_num) + """\n\n
        
        At """ + str(firstTime) + """, the UV Index will be """ + str(alluvList[0]) + """ out of 11. Make sure to apply sunscreen every 2 hours."""


        server = smtplib.SMTP('smtp.gmail.com', 587)
        status_code, response = server.ehlo()
        print(f"Echoing the server: " + str(status_code) + str(response))

        status_code, response = server.starttls()
        print(f"Post tls: echoing the server: " + str(status_code) + str(response))

        #PASSWORD: jgsulbjjymkbgomh 
        status_code, response = server.login(sender_email, password)
        print(f"Post log in: echoing the server: " + str(status_code) + str(response))
        
        print("Login success")
        server.sendmail(sender_email, rec_email, message)
        server.quit()

def scheduleReminder():
    reminder_time = time_field.get()
    print(reminder_time)
    schedule.every().day.at(reminder_time).do(dailyForcast)
  
    while True:
        schedule.run_pending()

    print("reminderScheduled")
#tkinter interface 
if __name__ == "__main__" :
    gui = Tk()
    gui.configure(bg = 'white')
    gui.geometry("500x400")
    gui.title("Sunscreen Reminder")
    
    labelIntro = Label(gui, text = "SUNSCREEN REMINDER", font = ("calibri", 30), fg = 'white', bg = 'black')
    labelIntro.grid(row = 1, column = 0, columnspan = 2, padx = 10, pady = 10)

    label1 = Label(gui, text = "State: ", fg = 'white', bg = 'black')
    label1.grid(row = 2, column = 0, padx = 10, pady = 10) 

    label2 = Label(gui, text = "County: ", fg = 'white', bg = 'black')
    label2.grid(row = 3, column = 0, padx = 10, pady = 10) 

    label3 = Label(gui, text = "City: ", fg = 'white', bg = 'black')
    label3.grid(row = 4, column = 0, padx = 10, pady = 10) 
    
    label4 = Label(gui, text = "Set time (HH: MM): ", fg = 'white', bg = 'black')
    label4.grid(row = 5, column = 0, padx = 10, pady = 10) 

    label4 = Label(gui, text = "Your email: ", fg = 'white', bg = 'black')
    label4.grid(row = 6, column = 0, padx = 10, pady = 10) 

    state_field = Entry(gui)
    county_field = Entry(gui)
    city_field = Entry(gui)
    time_field = Entry(gui)
    recEmail_field = Entry(gui)
    
    state_field.grid(row = 2, column = 1, padx = 10, pady = 10) 
    county_field.grid(row = 3, column = 1, padx = 10, pady = 10) 
    city_field.grid(row = 4, column = 1, padx = 10, pady = 10) 
    time_field.grid(row = 5, column = 1, padx = 10, pady= 10)
    recEmail_field.grid(row = 6, column = 1, padx = 10, pady = 10)

    button1 = Button(gui, text = "Send me a reminder", bg = "white", 
                     fg = "green", command = scheduleReminder)
    button1.grid(row = 7, rowspan = 2, column =1, columnspan = 2)

    gui.mainloop()
    