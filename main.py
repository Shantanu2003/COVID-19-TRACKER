import requests   #pip install requests
import bs4        #pip install beautifulsoup4
import tkinter as tk
import plyer       #pip install plyer
import time
import datetime
import threading
import tracestack

def get_html_data(url):           #function to request the html from the website
    data= requests.get(url)
    return data

def get_covid_detail():          # to get the covid details from the website
    url="https://www.mygov.in/covid-19/"
    html_data=get_html_data(url)
    bs=bs4.BeautifulSoup(html_data.text,'html.parser') #to get the html in text form and to make is look good using beautiful soup
    info_div=bs.find("div" ,class_="information_row",id="dashboard").find_all("div",class_="iblock_text") # to get only the particular section of the website
    vs=bs.find("div",class_="information_row",id="dashboard").find_all("div",class_="active-case")  #to get active cases
    all_details=" "
    for block in vs:  #to get the active cases from website
       count= block.find("span",class_="icount").get_text()   # to get no of active cases
       text=block.find("div", class_="info_label").get_text()  # to get the label
       all_details=all_details + text+ " : " + count+ "\n"
    for block in info_div[0:2]:
       count= block.find("span",class_="icount").get_text()
       text=block.find("div", class_="info_label").get_text()
       all_details=all_details + text+ " : " + count+ "\n"
    return all_details
def refresh():    #Fuction to refresh the info
    newData=get_covid_detail()
    print("Refreshing..")
    mainLabel['text']=newData

#for notification
def main():
    while True:
     plyer.notification.notify(title="COVID 19 TRACKER INDIA",
                               message=get_covid_detail(),
                               timeout=15,
     )
     time.sleep(30)
     main()

# GUI making
root = tk.Tk()   #root is the name for a tkinter class
root.geometry("900x800")  #size of the window
root.iconbitmap("logo.ico")   #to add logo
root.title("COVID-19 CASES TRACKER-INDIA")  #heading
root.configure(background='pink')  #bg colour
f= ["Algerian", 25, "bold"]  #font of text
ban=tk.PhotoImage(file="ban.png")  # to add banner at centre
banLabel=tk.Label(root, image=ban)
banLabel.pack()
mainLabel=tk.Label(root,text=get_covid_detail(),font=f,background='skyblue')   #calling the data
mainLabel.pack()
#for refresh button
g=("Algerian",15,"bold")
reBtn=tk.Button(root,text="REFRESH",font=g,bg='red',relief='solid',command=refresh)
reBtn.pack()

#new thread creating
t1 = threading.Thread(target=main)  # to call the function in another thread
t1.setDaemon(True)  #to make service provider thread and stop notification when application is closed
t1.start() #to start the function

root.mainloop()

