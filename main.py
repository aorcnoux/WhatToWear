import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame as pg
from datetime import datetime
import requests 
import random
import certifi 
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) 
API_KEY = os.getenv("CWA_API_KEY")


# Set application icon
im = Image.open('outfit.png')
im.save('outfit.ico')

# Fetch weather data from CWA API
url = (f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0003-001"
       f"?Authorization={API_KEY}"
       f"&StationName=臺北,新北,基隆,桃園,宜蘭,花蓮,臺東,新竹,苗栗,臺中,南投,"
       f"田中,古坑,嘉義,臺南,高雄,屏東,金門,馬祖,澎湖"
       f"&WeatherElement=&GeoInfo=CountyName")

# Fetch API JSON / Check data validity
def fetch_weather_data():
    try:
        response = requests.get(url, timeout=15, verify=False)
        response.raise_for_status()
        data = response.json()

        # Check if API returned valid data
        if not data or data.get("success") != "true":
            raise ValueError("API returned invalid data")

        return data

    except Exception as e:
        print("API Error:", e)
        # Fallback data for demonstration
        return {
            "records": {
                "Station": [
                    {
                        "StationName": "臺北",
                        "WeatherElement": {
                            "AirTemperature": "25",
                            "Weather": "晴"
                        }
                    }
                ]
            }
        }

# Extract station names for the Combobox
def extract_station_list(api_json):
    if not api_json:  
        return []
    try:
        stations = api_json["records"]["Station"]
        station_names = [s.get("StationName") for s in stations if s.get("StationName")]
        return sorted(station_names)  
    except:
        return []

# Extract specific weather data for each station
def extract_station_weather(api_json):
    result = {}
    if not api_json:
        return result
    try:
        stations = api_json["records"]["Station"]
        for s in stations:
            name = s.get("StationName")
            elements = s.get("WeatherElement", {})
            temp = elements.get("AirTemperature", "—")
            weather = elements.get("Weather", "—")
            result[name] = {
                "temp": temp,
                "weather": weather
            }
        return result
    except:
        return result
    
# Build main window (Startup window)
win1 = tk.Tk()
win1.title('WhatToWear')
win1.geometry('300x200')
win1.iconbitmap('assets/outfit.ico')
win1.resizable(False, False)

# Background Music Setup
pg.mixer.init()
pg.mixer.music.load('assets/BGM1.mp3')
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(-1)  
music_paused = False  

# Toggle music
def toggle_music():
    global music_paused
    if not music_paused:
        pg.mixer.music.pause()
        btn2.config(image=speaker0)
        music_paused = True
    else:
        pg.mixer.music.unpause()
        btn2.config(image=speaker1)
        music_paused = False

# Button click sound
def clickSound():
    s = pg.mixer.Sound('button.wav')
    s.set_volume(0.9)
    s.play()

# Set Main Window Background
canvas1 = tk.Canvas(win1, width=300, height=200)  
canvas1.place(relwidth=1, relheight=1)
img1 = Image.open('BG1.PNG')
tk_img1 = ImageTk.PhotoImage(img1.resize((300, 200)))
canvas1.create_image(0, 0, anchor='nw', image=tk_img1)
canvas1.create_text(150, 30, text='Outfit Guide', anchor='n', fill='#312E24', font=('Arial', 17, 'bold'))

# Open User Preferences Window
def createNewWindow():
    global win2, btn3, combo_location, location_var, weather_label, STATION_WEATHER
    win2 = tk.Toplevel()
    win2.title('WhatToWear')
    win2.geometry('1000x700')
    win2.iconbitmap('outfit.ico')
    win2.resizable(False, False)
    btn1.config(state="disabled", cursor='arrow')

    def on_close():  
        btn1.config(state="normal")
        win2.destroy()
    win2.protocol("WM_DELETE_WINDOW", on_close)

    canvas2 = tk.Canvas(win2, width=1000, height=700)
    canvas2.pack()
    img2 = Image.open('BG2.PNG')
    tk_img2 = ImageTk.PhotoImage(img2.resize((1000, 700)))
    canvas2.background = tk_img2
    canvas2.create_image(0, 0, anchor='nw', image=tk_img2)

    # Frame 3 (Weather + Color Palette) - Bottom Right
    frame3 = tk.Frame(win2, width=350, height=120, bg="#FCF7EE", relief='groove')
    frame3.place(x=576, y=524)

    tk.Label(frame3, text='Color Palette_', font=('Arial', 16, 'bold'),
            bg='#FCF7EE', fg='#312E24').place(x=200, y=20, anchor='w')

    tk.Label(frame3, text='Weather_', font=('Arial', 16, 'bold'),
            bg='#FCF7EE', fg='#312E24').place(x=15, y=20, anchor='w')

    # Load Weather Icons
    def load_icon(path):
        img = Image.open(path).resize((50, 50))
        return ImageTk.PhotoImage(img)

    weather_icons = {
        "sunny": load_icon("sunny.png"),
        "cloudy": load_icon("cloudy.png"),
        "overcast": load_icon("overcast.png"),
        "rain": load_icon("rain.png"),
    }

    # Weather Icon & Text Area
    weather_icon_label = tk.Label(frame3, bg="#FCF7EE")
    weather_icon_label.place(x=125, y=48)
    weather_label = tk.Label(frame3, text="", font=('Arial', 12, 'bold'),
                            bg='#FCF7EE', fg='#312E24', justify="left")
    weather_label.place(x=15, y=75, anchor='w')
    
    # Recommended Colors Config
    default_color = "#FCF7EE"

    def show_color_window(color):
        win_color = tk.Toplevel(win2)
        win_color.title("Palette")
        win_color.geometry("200x200")
        win_color.resizable(False, False)
        tk.Label(win_color, text=color, font=('Arial', 12, 'bold')).pack(pady=10)
        canvas_color = tk.Canvas(win_color, width=150, height=150, bg=color)
        canvas_color.pack()

    color_1 = ['#F2E4EC', "#2B4AA9", "#5082DF", '#F2DEA0', '#212326', '#6F7372', "#FFFFFF", "#979797"]
    color_2 = ['#B57114', '#7B9E89', '#706513', '#520120', '#BD2A2E', '#3B3936', '#B2BEBF', '#486966', '#212326', "#FFFFFF", '#2B4AA9', "#335130"]
    color_3 = ['#D9B8B8', '#D0E5F2', '#A6977B', '#BFA18F', '#212326', '#6F7372', "#FFFFFF", "#979797", '#706513', "#511213", "#B15C5C", "#335130"]
    color_4 = ['#283618', '#606C38', '#F2E8CF', '#BC6C25', '#4A403A', '#C9ADA7', '#F2E3E1', '#9A8C8C', "#A980C0", "#FFFFFF", '#D9B8B8', "#DCD16B"]
    
    all_colors = {'Scheme 1': color_1, 'Scheme 2': color_2, 'Scheme 3': color_3, 'Scheme 4': color_4}
        
    color_btns = []    
    positions = [(220, 45), (260, 45), (220, 75), (260, 75)]

    for i in range(4):
        x, y = positions[i]
        
        # 1. 改用 tk.Label，完美破解 Mac 無法顯示按鈕顏色的問題
        lbl = tk.Label(frame3, text="   ", font=('Arial', 10, 'bold'),
                       bg="#FCF7EE", cursor="hand2",
                       width=5, height=2, borderwidth=0)
        lbl.place(x=x, y=y)
        
        # 2. 綁定「滑鼠左鍵點擊」事件 (<Button-1>)，讓它擁有按鈕的功能
        lbl.bind("<Button-1>", lambda event, idx=i: show_color_window(color_btns[idx]["bg"]))
        
        color_btns.append(lbl) 

    def update_color_buttons():
        selected = random.choice(list(all_colors.values()))
        random.shuffle(selected)
        selected = selected[:4]
        for btn, c in zip(color_btns, selected):
            btn.config(bg=c, borderwidth=1)

    # Frame 4 (Current Time) - Top Right
    frame4 = tk.Frame(win2, width=180, height=25, bg="#E3DFD3", relief='groove')
    frame4.place(x=842, y=25) 
    time_label = tk.Label(frame4, text="", font=('Arial', 12, 'bold'), bg="#E3DFD3", fg="#312E24")
    time_label.pack()

    def update_time():
        now = datetime.now()
        time_str = now.strftime("%Y/%m/%d  %H:%M")
        time_label.config(text=time_str)
        frame4.after(1000, update_time)
    update_time() 
    
    # Frame 1 (User Settings) - Top Left
    frame1 = tk.Frame(win2, width=445, height=315, bg="#FCF7EE", relief='groove')
    frame1.place(x=37, y=52)

    tk.Label(frame1, text='Please select settings_', font=('Arial', 17, 'bold'),
             bg='#FCF7EE', fg='#312E24').place(x=20, y=25, anchor='w')

    for i in range(4):
        pos_y = 50 + i*50
        tk.Label(frame1, bitmap='gray12', font=('Arial', 14, 'bold'),
                 bg='#FCF7EE', fg='#312E24', justify="left").place(x=20, y=pos_y)

    # Gender Radio Buttons
    tk.Label(frame1, text='Category:', font=('Arial', 16, 'bold'), bg='#FCF7EE', fg='#312E24').place(x=50, y=45)
    val_gender = tk.StringVar(value="male") 
    radio_gander1 = tk.Radiobutton(frame1, text='Men', variable=val_gender, value="male",
                                 font=('Arial', 14, 'bold'), bg='#FCF7EE', fg='#312E24',
                                 command=clickSound, selectcolor="#D7D4CB", cursor='hand2')
    radio_gander1.place(x=130, y=45)
    radio_gander1.select()

    radio_gander2 = tk.Radiobutton(frame1, text='Women', variable=val_gender, value="female",
                                 font=('Arial', 14, 'bold'), bg='#FCF7EE', fg='#312E24',
                                 command=clickSound, selectcolor="#D7D4CB", cursor='hand2')
    radio_gander2.place(x=210, y=45)

    # Style Combobox
    tk.Label(frame1, text='Style:', font=('Arial', 16, 'bold'), bg='#FCF7EE', fg='#312E24').place(x=50, y=95)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.TCombobox", fieldbackground="#D7D4CB", background="#D7D4CB",
                    foreground="#312E24", selectbackground="#D7D4CB", selectforeground="#312E24")

    val_style = tk.StringVar(value='Casual')
    style_box = ttk.Combobox(frame1, font=('Arial', 14, 'bold'), state='readonly',
                                 textvariable=val_style, values=['Casual', 'Formal', 'Sporty'],
                                 style="Custom.TCombobox", cursor='hand2')
    style_box.place(x=130, y=97, width=150)

    # Location Combobox (with Chinese to English mapping)
    tk.Label(frame1, text='Location:', font=('Arial', 16, 'bold'), bg='#FCF7EE', fg='#312E24').place(x=50, y=146)
    location_var = tk.StringVar() 
    combo_location = ttk.Combobox(frame1, textvariable=location_var, font=('Arial', 14, 'bold'),
                                  state='readonly', style="Custom.TCombobox", cursor='hand2')
    
    api_json = fetch_weather_data()   
    raw_station_list = extract_station_list(api_json)
    raw_station_weather = extract_station_weather(api_json)

    # English Mapping for Cities
    eng_city_map = {
        "臺北": "Taipei", "台北": "Taipei", "新北": "New Taipei", "基隆": "Keelung",
        "桃園": "Taoyuan", "宜蘭": "Yilan", "花蓮": "Hualien", "臺東": "Taitung",
        "新竹": "Hsinchu", "苗栗": "Miaoli", "臺中": "Taichung", "台中": "Taichung",
        "南投": "Nantou", "田中": "Changhua", "古坑": "Yunlin", "嘉義": "Chiayi",
        "臺南": "Tainan", "台南": "Tainan", "高雄": "Kaohsiung", "屏東": "Pingtung",
        "金門": "Kinmen", "馬祖": "Matsu", "連江馬祖": "Matsu", "澎湖": "Penghu"
    }

    # Translate lists and dict keys to English
    station_list = [eng_city_map.get(name, name) for name in raw_station_list]
    
    # Remove duplicates from list just in case
    station_list = sorted(list(set(station_list))) 

    STATION_WEATHER = {
        eng_city_map.get(name, name): data for name, data in raw_station_weather.items()
    }

    if station_list:
        combo_location["values"] = station_list
        combo_location.set(station_list[0])
    else:
        combo_location["values"] = ["Load Failed"]
        combo_location.set("Load Failed")  
    
    combo_location.place(x=140, y=150, width=160)

    # Accessories Checkboxes
    tk.Label(frame1, text='Add:', font=('Arial', 16, 'bold'), bg='#FCF7EE', fg='#312E24').place(x=50, y=195)
    chk_acc_val = tk.IntVar()
    check_hat = tk.Checkbutton(frame1, text='Accessories', font=('Arial', 14, 'bold'),
                                 bg='#FCF7EE', fg='#312E24', command=clickSound,
                                 cursor='hand2', selectcolor="#D7D4CB", variable=chk_acc_val, onvalue=1, offvalue=0)
    check_hat.place(x=130, y=195)

    chk_outer_val = tk.IntVar()
    check_accessory = tk.Checkbutton(frame1, text='Outerwear', font=('Arial', 14, 'bold'),
                                     bg='#FCF7EE', fg='#312E24', command=clickSound,
                                     cursor='hand2', selectcolor="#D7D4CB", variable=chk_outer_val, onvalue=1, offvalue=0)
    check_accessory.place(x=260, y=195)
    
    # Generate Button
    btn3 = tk.Button(frame1, text='Generate', font=('Arial', 15, 'bold'),
                     command=lambda: [clickSound(), showInfo()],
                     bg='#D7D4CB', fg='#312E24', cursor='hand2')
    btn3.place(x=340, y=270, width=90, height=30)

    def showInfo():
        btn3.config(state="disabled", cursor='arrow')
        frame2 = tk.Frame(win2, width=480, height=210, bg="#FCF7EE", relief='flat')
        frame2.place(x=20, y=470)   

        canvas3 = tk.Canvas(frame2, width=480, height=210)
        canvas3.place(x=0, y=0)
        
        img_CAT = Image.open('CAT.PNG')
        tk_img_CAT = ImageTk.PhotoImage(img_CAT.resize((480, 210)))
        canvas3.img = tk_img_CAT
        canvas3.create_image(0, 0, anchor='nw', image=tk_img_CAT)

        # 1. 取得天氣資料 (Retrieve Weather Info)
        station = location_var.get()
        current_temp = "25" # 預設氣溫，防止沒抓到資料時出錯

        if station in STATION_WEATHER:
            w = STATION_WEATHER[station]
            current_temp = w.get("temp", "25")
            weather_chn = str(w.get("weather", "—"))

            if "雨" in weather_chn:
                icon = weather_icons["rain"]
                weather_eng = "Rainy"
            elif "陰" in weather_chn:
                icon = weather_icons["overcast"]
                weather_eng = "Overcast"
            elif "雲" in weather_chn:
                icon = weather_icons["cloudy"]
                weather_eng = "Cloudy"
            else:
                icon = weather_icons["sunny"]
                weather_eng = "Sunny"

            weather_label.config(text=f"Weather: {weather_eng}\nTemp: {current_temp}°C", fg="#312E24")
            weather_icon_label.config(image=icon)
            weather_icon_label.image = icon 
        else:
            weather_label.config(text=f"Weather: —\nTemp: —°C\n(No data)", fg="red")
            weather_icon_label.config(image='')

        update_color_buttons()  

        # 2. 顯示推薦文字
        label9 = tk.Label(frame2, text="Outfit recommended for you!", font=('Arial', 15, 'bold'), bg='#FCF7EE', fg='#312E24')
        label9.place(x=140, y=40, anchor='w')
        label10 = tk.Label(frame2, text="Outfit details:", font=('Arial', 15, 'bold'), bg='#FCF7EE', fg='#312E24', justify="left")
        label10.place(x=140, y=120, anchor='w')

        # 3. 紙娃娃系統設定 (Paper Doll System)
        global doll_label
        if 'doll_label' in globals() and doll_label.winfo_exists():
            doll_label.destroy()
        doll_label = tk.Label(win2, bg="#E3DFE3", borderwidth=0)
        doll_label.place(x=650, y=60)

        layer_order = ["shoes", "bottom", "top", "outer", "access"]

        def load_base_model():
            gender = val_gender.get()
            path = f"models/{gender}.png"
            base_img = Image.open(path).resize((225, 450)).convert("RGBA")
            return base_img

        def get_temp_folder(t_val):
            try:
                t = float(t_val)
            except:
                return "mild"
            if t <= 15: return "cold"
            elif t >= 26: return "hot"
            return "mild"

        def load_clothes(t_val):
            clothes_dict = {cat: [] for cat in layer_order}
            gender = val_gender.get()
            style = val_style.get()
            temp_folder = get_temp_folder(t_val)
            
            # --- 修正 root 定義與路徑拼接 ---
            root_path = os.path.join("clothes", gender, style, temp_folder)

            for cat in layer_order:
                folder = os.path.join(root_path, cat)
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if file.lower().endswith(".png"):
                            img = Image.open(os.path.join(folder, file)).resize((225, 450)).convert("RGBA")
                            clothes_dict[cat].append((img, file))
            return clothes_dict

        def update_doll():
            base = load_base_model()
            clothes = load_clothes(current_temp) 
            combined = base.copy()
            result_list = []

            for cat in layer_order:
                if cat == "outer" and chk_outer_val.get() == 0:
                    result_list.append(" ")
                    continue
                if cat == "access" and chk_acc_val.get() == 0:
                    result_list.append(" ")
                    continue

                items = clothes.get(cat, [])
                if items:
                    img, filename = random.choice(items)
                    combined = Image.alpha_composite(combined, img)
                    name_no_png = os.path.splitext(filename)[0]
                    result_list.append(name_no_png)
                else:
                    result_list.append(" ")

            photo = ImageTk.PhotoImage(combined)
            doll_label.config(image=photo)
            doll_label.image = photo 
            label10.config(text="Outfit details:\n" + "\n".join(f"- {x}" for x in result_list if x.strip()))

        update_doll()

        def restart_action():
            clickSound()
            if 'doll_label' in globals() and doll_label.winfo_exists():
                doll_label.config(image='', bg="#E3DFE3")   
                doll_label.image = None       

            for btn in color_btns:
                btn.config(bg=default_color, borderwidth=0)
            weather_label.config(text="")
            weather_icon_label.config(image="")
            frame2.destroy()
            btn3.config(state="normal", cursor='hand2')

        btn_restart = tk.Button(frame2, text='Remix', font=('Arial', 15, 'bold'),
                                command=restart_action, bg='#D7D4CB', fg='#312E24', cursor='hand2')
        btn_restart.place(x=280, y=155, width=80, height=30)

        btn_esc = tk.Button(frame2, text='Exit', font=('Arial', 15, 'bold'),
                            command=lambda: [clickSound(), win1.destroy()],
                            bg="#a63c3c", fg="#a63c3c", cursor='hand2')
        btn_esc.place(x=370, y=155, width=80, height=30)

# START / MUSIC buttons setup
btn1 = tk.Button(win1, text='START!', font=('Arial', 18, 'bold'),
                 command=lambda: [createNewWindow(), clickSound()],
                 background='#FCF7EE', foreground='#312E24', cursor='hand2', borderwidth=0)
btn1.place(x=102, y=135, width=95, height=35)

speaker1 = tk.PhotoImage(file='speaker1.PNG')
speaker0 = tk.PhotoImage(file='speaker0.PNG')
btn2 = tk.Button(win1, image=speaker1, command=lambda: [clickSound(), toggle_music()],
                 relief='flat', background='#FCF7EE', cursor='hand2')
btn2.place(x=10, y=10)

win1.mainloop()