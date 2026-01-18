# client.py
import json
import webbrowser
import requests
import customtkinter as ctk
from threading import Thread

# Настройка сервера
SERVER_URL = "http://localhost:8000"

class RoundedButton(ctk.CTkButton):
    def __init__(self, parent, bg_color='white', fg_color='black', text='', radius=10, command=None,
                 font_btn='13', bg_color_new='black',
                 rel_btn='groove', width=30, border_color='black', height=30, corner_radius=5,
                 state='normal'):
        font2 = str(font_btn)[-2] + str(font_btn)[-1]
        a = ctk.CTkFont(size=int(font2))
        hv_color = '#AFEEEE'
        ctk.CTkButton.__init__(self, parent, text=text, command=command, width=width, fg_color=bg_color,
                               text_color=fg_color,
                               border_width=1, border_color=border_color, hover_color=hv_color, font=a,
                               corner_radius=corner_radius,
                               height=height, state=state)

class CLabel(ctk.CTkLabel):
    def __init__(self, parent, text='', fg='black', bg='white', font=13, relief='groove', justify='left',
                 width=30, corner_radius=5, height=30, border_color='#1A1A1D'):
        font2 = str(font)[-2] + str(font)[-1]
        a = ctk.CTkFont(size=int(font2))
        ctk.CTkLabel.__init__(self, parent, text=text, fg_color=bg, text_color=fg, width=width,
                              corner_radius=corner_radius, justify=justify,
                              font=a, height=height, bg_color='#1A1A1D')

class App(ctk.CTk):
    def __init__(self, width=1280, height=720):
        super().__init__()
        self.title('Информатор')
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.finish)
        
        self.frame = ctk.CTkFrame(self, fg_color='#1A1A1D')
        self.frame.place(relwidth=1, relheight=1)
        self.font = 15
        
        # Текущий пользователь
        self.current_user = None
        
    def clean_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
    
    def finish(self):
        self.destroy()

class API:
    """Класс для работы с API сервера"""
    
    @staticmethod
    def register(username, password, city):
        """Регистрация пользователя"""
        try:
            response = requests.post(
                f"{SERVER_URL}/api/user/register",
                json={
                    'username': username,
                    'password': password,
                    'city': city
                },
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}
    
    @staticmethod
    def login(username, password):
        """Вход пользователя"""
        try:
            response = requests.post(
                f"{SERVER_URL}/api/user/login",
                json={
                    'username': username,
                    'password': password
                },
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}
    
    @staticmethod
    def get_user_profile(username):
        """Получение профиля пользователя"""
        try:
            response = requests.get(
                f"{SERVER_URL}/api/user/profile?username={username}",
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}
    
    @staticmethod
    def update_user(username, current_password, updates):
        """Обновление данных пользователя"""
        try:
            response = requests.post(
                f"{SERVER_URL}/api/user/update",
                json={
                    'username': username,
                    'current_password': current_password,
                    'updates': updates
                },
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}
    
    @staticmethod
    def create_review(data):
        """Создание отзыва"""
        try:
            response = requests.post(
                f"{SERVER_URL}/api/reviews/create",
                json=data,
                timeout=5
            )
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}
    
    @staticmethod
    def search_reviews(city='', district='', street=''):
        """Поиск отзывов"""
        try:
            params = []
            if city:
                params.append(f'city={city}')
            if district:
                params.append(f'district={district}')
            if street:
                params.append(f'street={street}')
            
            url = f"{SERVER_URL}/api/reviews/search"
            if params:
                url += '?' + '&'.join(params)
            
            response = requests.get(url, timeout=5)
            return response.json()
        except Exception as e:
            return {'error': f'Ошибка соединения: {str(e)}'}

class Review:
    def __init__(self):
        self.entry_street = None
        self.entry_city = None
        self.entry_district = None
        self.entry_com = None
        self.entry_grade = None
        self.check_infr = None
        self.check_big_pr = None
        self.check_dm = None
        self.check_garbage = None
        self.check_lake = None
        self.check_weather = None
        self.check_bad_social_work = None
        self.check_population = None
        self.check_noise = None

    def problem(self):
        app.clean_frame()
        
        title = CLabel(app.frame, text='Добавление отзыва', width=1230, font=30, bg='#1A1A1D', fg='#FFE400',
                       justify='center')
        title.place(x=25, y=10)
        
        # Поля ввода
        title_city = CLabel(app.frame, text='Город', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                            corner_radius=15, height=50, width=110)
        title_city.place(x=25, y=75)
        self.entry_city = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2, width=220,
                                       font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                       placeholder_text='Ваш город')
        self.entry_city.place(x=150, y=75)
        
        title_district = CLabel(app.frame, text='Район', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                                corner_radius=15, height=50, width=110)
        title_district.place(x=400, y=75)
        self.entry_district = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                           width=270,
                                           font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                           placeholder_text='Ваш район')
        self.entry_district.place(x=525, y=75)
        
        title_street = CLabel(app.frame, text='Улица', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                              corner_radius=15, height=50, width=110)
        title_street.place(x=825, y=75)
        self.entry_street = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                         width=305,
                                         font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                         placeholder_text='Ваша улица')
        self.entry_street.place(x=950, y=75)
        
        # Типы проблем
        title_problem = CLabel(app.frame, text='Тип проблемы',
                               font=25, height=45, width=1230, corner_radius=15, fg='#EDFF21', bg='grey22')
        title_problem.place(x=25, y=150)
        
        self.check_infr = ctk.IntVar()
        self.check_big_pr = ctk.IntVar()
        self.check_dm = ctk.IntVar()
        self.check_garbage = ctk.IntVar()
        self.check_lake = ctk.IntVar()
        self.check_weather = ctk.IntVar()
        self.check_bad_social_work = ctk.IntVar()
        self.check_population = ctk.IntVar()
        self.check_noise = ctk.IntVar()
        
        # Флажки проблем
        check_btn_infr = ctk.CTkCheckBox(app.frame, text="Слабая инфраструктура", variable=self.check_infr, onvalue=1,
                                         offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                         font=('Arial', 25), border_width=2, fg_color='#EDFF21',
                                         checkmark_color='#1A1A1D')
        check_btn_infr.place(x=75, y=210)
        
        check_btn_big_pr = ctk.CTkCheckBox(app.frame, text="Автомобильные пробки ", variable=self.check_big_pr,
                                           onvalue=1,
                                           offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                           font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                           checkmark_color='#1A1A1D')
        check_btn_big_pr.place(x=450, y=210)
        
        check_btn_dm = ctk.CTkCheckBox(app.frame, text="Задымление воздуха", variable=self.check_dm, onvalue=1,
                                       offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                       font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                       checkmark_color='#1A1A1D')
        check_btn_dm.place(x=875, y=210)
        
        check_btn_garbage = ctk.CTkCheckBox(app.frame, text="Загрязнение территории", variable=self.check_garbage,
                                            onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_garbage.place(x=75, y=250)
        
        check_btn_lake = ctk.CTkCheckBox(app.frame, text="Загрязнение водоёмов", variable=self.check_lake, onvalue=1,
                                         offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                         font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                         checkmark_color='#1A1A1D')
        check_btn_lake.place(x=450, y=250)
        
        check_btn_weather = ctk.CTkCheckBox(app.frame, text="Суровый климат", variable=self.check_weather, onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_weather.place(x=875, y=250)
        
        check_btn_bad_soc = ctk.CTkCheckBox(app.frame, text="Плохая работа упр. служб",
                                            variable=self.check_bad_social_work,
                                            onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_bad_soc.place(x=75, y=290)
        
        check_btn_pop = ctk.CTkCheckBox(app.frame, text="Маргинальность населения", variable=self.check_population,
                                        onvalue=1,
                                        offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                        font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                        checkmark_color='#1A1A1D')
        check_btn_pop.place(x=450, y=290)
        
        check_btn_noise = ctk.CTkCheckBox(app.frame, text="Громкий шум", variable=self.check_noise, onvalue=1,
                                          offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                          font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                          checkmark_color='#1A1A1D')
        check_btn_noise.place(x=875, y=290)
        
        # Комментарий
        title_com = CLabel(app.frame, text='Комментарий',
                           font=25, height=45, width=605, corner_radius=15, fg='#EDFF21', bg='grey22')
        title_com.place(x=25, y=340)
        self.entry_com = ctk.CTkTextbox(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2, width=1230,
                                        font=('Arial', 25), height=250, fg_color='#1A1A1D', text_color='#FFBD00')
        self.entry_com.place(x=25, y=390)
        
        # Оценка
        label_grade = CLabel(app.frame, text='Общая оценка', font=25, height=45, width=270,
                             corner_radius=15,
                             fg='#EDFF21', bg='grey22')
        label_grade.place(x=660, y=340)
        self.entry_grade = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                        width=315,
                                        font=('Arial', 25), height=45, fg_color='#1A1A1D', text_color='#FFBD00',
                                        placeholder_text='Ваша оценка от 1 до 10')
        self.entry_grade.place(x=940, y=340)
        
        # Кнопки
        btn_send = RoundedButton(app.frame, text='Отправить отзыв', fg_color='#FFBD00', bg_color='#1A1A1D',
                                 border_color='#FFBD00', corner_radius=15, width=255, font_btn=25, height=50,
                                 command=self.send)
        btn_send.place(x=1000, y=655)
        
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=15, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=25, y=655)
    
    def send(self):
        """Отправка отзыва через API"""
        com = self.entry_com.get("1.0", "end-1c")
        city = self.entry_city.get()
        distr = self.entry_district.get()
        street = self.entry_street.get()
        grade = self.entry_grade.get()
        
        # Валидация на клиенте
        if not city or city.isspace():
            self.entry_city.configure(border_color='red')
            return
        if not distr or distr.isspace():
            self.entry_district.configure(border_color='red')
            return
        if not street or street.isspace():
            self.entry_street.configure(border_color='red')
            return
        if not grade or not grade.isdigit() or not (0 <= int(grade) <= 10):
            self.entry_grade.configure(border_color='red')
            return
        
        # Формирование строки проблем
        problems = [
            self.check_infr.get(),
            self.check_garbage.get(),
            self.check_bad_social_work.get(),
            self.check_big_pr.get(),
            self.check_lake.get(),
            self.check_population.get(),
            self.check_dm.get(),
            self.check_weather.get(),
            self.check_noise.get()
        ]
        
        spproblem = ''.join(str(p) for p in problems)
        
        # Подготовка данных
        review_data = {
            'name': app.current_user['username'] if app.current_user else 'Гость',
            'city': city,
            'district': distr,
            'street': street,
            'spproblem': spproblem,
            'grade': grade,
            'comment': com if com and not com.isspace() else ''
        }
        
        # Показ экрана загрузки
        self.send_page()
        
        # Отправка в отдельном потоке
        def send_thread():
            result = API.create_review(review_data)
            app.after(0, lambda: self.handle_send_result(result))
        
        Thread(target=send_thread, daemon=True).start()
    
    def send_page(self):
        app.clean_frame()
        title = CLabel(app.frame, text='Ваш отзыв отправляется', font=25, height=100, width=330,
                       corner_radius=15,
                       fg='#EDFF21', bg='grey22')
        title.place(x=505, y=100)
    
    def handle_send_result(self, result):
        if 'success' in result and result['success']:
            self.page_res()
        else:
            app.clean_frame()
            error_msg = result.get('error', 'Неизвестная ошибка')
            title = CLabel(app.frame, text=f'Ошибка: {error_msg}', font=25, height=100, width=330,
                           corner_radius=15, fg='red', bg='grey22')
            title.place(x=505, y=100)
            btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                     corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                     command=home_page)
            btn_home.place(x=505, y=225)
    
    def page_res(self):
        app.clean_frame()
        title = CLabel(app.frame, text='Ваш отзыв был отправлен', font=25, height=100, width=270,
                       corner_radius=15,
                       fg='#EDFF21', bg='grey22')
        title.place(x=505, y=100)
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=505, y=225)

class Get_review:
    def __init__(self):
        self.search_city = None
        self.search_district = None
        self.search_street = None
    
    def page_search(self):
        app.clean_frame()
        
        title = CLabel(app.frame, text='Поиск отзывов', width=1230, font=30, bg='#1A1A1D', fg='#FFE400',
                       justify='center')
        title.place(x=25, y=10)
        
        # Поля поиска
        title_city = CLabel(app.frame, text='Город', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                            corner_radius=15, height=50, width=110)
        title_city.place(x=25, y=75)
        self.search_city = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2, width=220,
                                        font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                        placeholder_text='Ваш город')
        self.search_city.place(x=150, y=75)
        
        title_district = CLabel(app.frame, text='Район', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                                corner_radius=15, height=50, width=110)
        title_district.place(x=25, y=150)
        self.search_district = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                            width=220,
                                            font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                            placeholder_text='Ваш район')
        self.search_district.place(x=150, y=150)
        
        title_street = CLabel(app.frame, text='Улица', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                              corner_radius=15, height=50, width=110)
        title_street.place(x=25, y=225)
        self.search_street = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                          width=220,
                                          font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                          placeholder_text='Ваша улица')
        self.search_street.place(x=150, y=225)
        
        # Кнопки
        btn_search = RoundedButton(app.frame, text='Поиск', bg_color='#1A1A1D', font_btn=25, height=45,
                                   corner_radius=15, width=345, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.search)
        btn_search.place(x=25, y=300)
        
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=23, height=40,
                                 corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=925, y=670)
    
    def search(self):
        """Поиск отзывов через API"""
        city = self.search_city.get()
        district = self.search_district.get()
        street = self.search_street.get()
        
        # Поиск в отдельном потоке
        def search_thread():
            result = API.search_reviews(city, district, street)
            app.after(0, lambda: self.display_search_results(result, city, district, street))
        
        Thread(target=search_thread, daemon=True).start()
    
    def display_search_results(self, result, city, district, street):
        app.clean_frame()
        
        if 'error' in result:
            title = CLabel(app.frame, text=f'Ошибка: {result["error"]}', font=25, height=100, width=330,
                           corner_radius=15, fg='red', bg='grey22')
            title.place(x=505, y=100)
            btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                     corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                     command=home_page)
            btn_home.place(x=505, y=225)
            return
        
        reviews = result.get('reviews', [])
        statistics = result.get('statistics', {})
        
        if reviews:
            # Отображение статистики
            stats_text = f"Найдено отзывов: {statistics['total_reviews']}\n"
            stats_text += f"Средняя оценка: {statistics['average_grade']}/10\n\n"
            stats_text += "Топ проблем:\n"
            
            for i, problem in enumerate(statistics['top_problems'], 1):
                stats_text += f"{i}. {problem['name']}: {problem['count']} жалоб\n"
            
            title = CLabel(app.frame, text=stats_text, font=20, width=1230, bg='grey22',
                           fg='#FFE400', height=320, corner_radius=15)
            title.place(x=25, y=25)
            
            # Отображение комментариев
            comments_text = "Отзывы:\n" + "="*100 + "\n"
            for comment in statistics.get('comments', []):
                if comment:
                    comments_text += comment + "\n" + "="*100 + "\n"
            
            if len(comments_text) > 100:
                textbox = ctk.CTkTextbox(app.frame, width=1230, corner_radius=5, height=300, border_color='#FFBD00',
                                         text_color='#FFBD00', fg_color='#1A1A1D', border_width=2, font=('Arial', 20))
                textbox.insert("0.0", comments_text)
                textbox.configure(state="disabled")
                textbox.place(x=25, y=365)
        else:
            title = CLabel(app.frame, text='По вашему запросу ничего не найдено', width=830, font=30, bg='grey22',
                           fg='#FFE400', justify='center', height=270, corner_radius=15)
            title.place(x=400, y=75)
        
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=23, height=40,
                                 corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=925, y=670)

class Registration:
    def __init__(self):
        self.label_nic = None
        self.label_password = None
        self.city = None
    
    def main_page(self):
        app.clean_frame()
        
        bg = RoundedButton(app.frame, text='', height=260, width=350, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=465, y=120)
        
        title = CLabel(app.frame, text='Выполните вход', font=27, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=300)
        title.place(x=490, y=150)
        
        btn_entrance = RoundedButton(app.frame, text='Войти', bg_color='#1A1A1D', font_btn=25, height=50,
                                     corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                     command=self.entrance)
        btn_entrance.place(x=515, y=225)
        
        btn_reg = RoundedButton(app.frame, text='Регистрация', bg_color='#1A1A1D', font_btn=25, height=50,
                                corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                command=self.registration)
        btn_reg.place(x=515, y=300)
        
        # Проверка быстрого входа из файла
        if self.fast_entrance():
            bg2 = RoundedButton(app.frame, text='', height=120, width=350, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                                border_color='#EDFF21', corner_radius=25, state='disabled')
            bg2.place(x=465, y=400)
            
            title2 = CLabel(app.frame, text='Быстрый вход', font=20, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                            corner_radius=15, height=40, width=300)
            title2.place(x=490, y=410)
            
            user_data = self.fast_entrance()
            btn_fast_entrance = RoundedButton(app.frame, text=user_data['username'],
                                              bg_color='#1A1A1D', font_btn=25, height=50,
                                              corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                              command=lambda: self.fast_login(user_data['username'], user_data['password']))
            btn_fast_entrance.place(x=515, y=460)
    
    def fast_entrance(self):
        """Проверка сохраненных данных для быстрого входа"""
        try:
            with open('user_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except:
            return None
    
    def fast_login(self, username, password):
        """Быстрый вход"""
        result = API.login(username, password)
        if 'success' in result and result['success']:
            app.current_user = result['user']
            # Сохранение данных для быстрого входа
            with open('user_data.json', 'w', encoding='utf-8') as file:
                json.dump({
                    'username': username,
                    'password': password
                }, file)
            home_page()
        else:
            error_msg = result.get('error', 'Ошибка входа')
            self.show_error(error_msg)
    
    def entrance(self):
        app.clean_frame()
        
        bg = RoundedButton(app.frame, text='', height=335, width=400, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=440, y=120)
        
        label = CLabel(app.frame, text='Вход', font=25, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=350, justify='center')
        label.place(x=465, y=150)
        
        self.label_nic = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=350,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text='Введите никнейм',
                                      justify='center')
        self.label_password = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                           width=350,
                                           font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                           placeholder_text='Введите пароль',
                                           justify='center', show='*')
        self.label_nic.place(x=465, y=225)
        self.label_password.place(x=465, y=300)
        
        next_btn = RoundedButton(app.frame, text='Продолжить', bg_color='#1A1A1D', font_btn=20, height=50,
                                 corner_radius=15, width=350, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=self.get_entrance)
        next_btn.place(x=465, y=375)
        
        btn_return = RoundedButton(app.frame, text='Вернуться назад', bg_color='#1A1A1D', font_btn=25, height=50,
                                   corner_radius=25, width=300, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.main_page)
        btn_return.place(x=960, y=645)
    
    def get_entrance(self):
        """Вход через API"""
        username = self.label_nic.get()
        password = self.label_password.get()
        
        if not username or username.isspace():
            self.show_error('Введите имя пользователя')
            return
        if not password:
            self.show_error('Введите пароль')
            return
        
        # Вход в отдельном потоке
        def login_thread():
            result = API.login(username, password)
            app.after(0, lambda: self.handle_login_result(result, username, password))
        
        Thread(target=login_thread, daemon=True).start()
    
    def handle_login_result(self, result, username, password):
        if 'success' in result and result['success']:
            app.current_user = result['user']
            # Сохранение данных для быстрого входа
            with open('user_data.json', 'w', encoding='utf-8') as file:
                json.dump({
                    'username': username,
                    'password': password
                }, file)
            home_page()
        else:
            error_msg = result.get('error', 'Ошибка входа')
            self.show_error(error_msg)
    
    def registration(self):
        app.clean_frame()
        
        bg = RoundedButton(app.frame, text='', height=410, width=400, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=440, y=120)
        
        title = CLabel(app.frame, text='Регистрация', font=25, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=350)
        title.place(x=465, y=150)
        
        self.label_nic = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=350,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text='Введите ваш никнейм', justify='center')
        self.label_nic.place(x=465, y=225)
        
        self.label_password = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                           width=350,
                                           font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                           placeholder_text='Придумайте пароль', justify='center', show='*')
        self.label_password.place(x=465, y=300)
        
        self.city = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                 width=350,
                                 font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                 placeholder_text='Введите город проживания', justify='center')
        self.city.place(x=465, y=375)
        
        next_btn = RoundedButton(app.frame, text='Зарегистрироваться', bg_color='#1A1A1D', font_btn=20, height=50,
                                 corner_radius=15, width=350, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=self.get_reg)
        next_btn.place(x=465, y=450)
        
        btn_return = RoundedButton(app.frame, text='Вернуться назад', bg_color='#1A1A1D', font_btn=25, height=50,
                                   corner_radius=25, width=400, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.main_page)
        btn_return.place(x=440, y=550)
    
    def get_reg(self):
        """Регистрация через API"""
        username = self.label_nic.get()
        password = self.label_password.get()
        city = self.city.get()
        
        # Базовая валидация на клиенте
        if not username or username.isspace():
            self.show_error('Введите имя пользователя')
            return
        if not password:
            self.show_error('Введите пароль')
            return
        if len(password) < 4:
            self.show_error('Пароль должен содержать минимум 4 символа')
            return
        if ' ' in password:
            self.show_error('Пароль не должен содержать пробелы')
            return
        if not city or city.isspace():
            self.show_error('Введите город')
            return
        
        # Регистрация в отдельном потоке
        def register_thread():
            result = API.register(username, password, city)
            app.after(0, lambda: self.handle_register_result(result, username, password))
        
        Thread(target=register_thread, daemon=True).start()
    
    def handle_register_result(self, result, username, password):
        if 'success' in result and result['success']:
            # Автоматический вход после регистрации
            login_result = API.login(username, password)
            if 'success' in login_result and login_result['success']:
                app.current_user = login_result['user']
                # Сохранение данных для быстрого входа
                with open('user_data.json', 'w', encoding='utf-8') as file:
                    json.dump({
                        'username': username,
                        'password': password
                    }, file)
                home_page()
        else:
            error_msg = result.get('error', 'Ошибка регистрации')
            self.show_error(error_msg)
    
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        error_label = CLabel(app.frame, text=message, bg='grey22', fg='red', font=20, height=50,
                             width=350, corner_radius=25, justify='center')
        error_label.place(x=465, y=500)

class Cabinet:
    def __init__(self):
        self.nic_entry = None
        self.pas_entry = None
        self.city_entr = None
        self.current_password_entry = None
        
    def page(self):
        app.clean_frame()
        
        if not app.current_user:
            title = CLabel(app.frame, text='Вы не авторизованы', font=27, bg='grey22', fg='red', corner_radius=25,
                           justify='center', width=600, height=60)
            title.place(x=340, y=250)
            btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                     corner_radius=25, width=600, fg_color='#FFBD00', border_color='#FFBD00',
                                     command=home_page)
            btn_home.place(x=340, y=350)
            return
        
        # Получение профиля через API
        result = API.get_user_profile(app.current_user['username'])
        if 'error' in result:
            title = CLabel(app.frame, text=f'Ошибка: {result["error"]}', font=27, bg='grey22', fg='red', corner_radius=25,
                           justify='center', width=600, height=60)
            title.place(x=340, y=250)
            return
        
        user_profile = result.get('user', {})
        
        # Отображение профиля
        bg = RoundedButton(app.frame, text='', height=500, width=620, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=330, y=100)
        
        title = CLabel(app.frame, text='Профиль', font=27, bg='grey22', fg='#EDFF21', corner_radius=25,
                       justify='center', width=600, height=60)
        title.place(x=340, y=115)
        
        # Поля для редактирования
        title_nic = CLabel(app.frame, text='Ваше имя:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                           justify='center', width=290, height=50)
        title_nic.place(x=340, y=180)
        self.nic_entry = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text=user_profile.get('username', ''),
                                      justify='center')
        self.nic_entry.place(x=650, y=180)
        
        title_city = CLabel(app.frame, text='Город проживания:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                            justify='center', width=290, height=50)
        title_city.place(x=340, y=240)
        self.city_entr = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text=user_profile.get('city', ''),
                                      justify='center')
        self.city_entr.place(x=650, y=240)
        
        title_password = CLabel(app.frame, text='Новый пароль:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                                justify='center', width=290, height=50)
        title_password.place(x=340, y=300)
        self.pas_entry = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text='Оставьте пустым, чтобы не менять',
                                      justify='center', show='*')
        self.pas_entry.place(x=650, y=300)
        
        title_current_password = CLabel(app.frame, text='Текущий пароль:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                                        justify='center', width=290, height=50)
        title_current_password.place(x=340, y=360)
        self.current_password_entry = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                                   width=290,
                                                   font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                                   placeholder_text='Для подтверждения изменений',
                                                   justify='center', show='*')
        self.current_password_entry.place(x=650, y=360)
        
        btn_changes = RoundedButton(app.frame, text='Сохранить изменения', bg_color='#1A1A1D', font_btn=25, height=50,
                                    corner_radius=25, width=600, fg_color='#FFBD00', border_color='#FFBD00',
                                    command=self.changes_personal_data)
        btn_changes.place(x=340, y=420)
        
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=25, width=600, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=340, y=480)
    
    def changes_personal_data(self):
        """Обновление данных пользователя через API"""
        if not app.current_user:
            return
        
        current_password = self.current_password_entry.get()
        if not current_password:
            self.show_error('Введите текущий пароль для подтверждения')
            return
        
        updates = {}
        new_username = self.nic_entry.get()
        new_city = self.city_entr.get()
        new_password = self.pas_entry.get()
        
        if new_username and new_username != app.current_user['username']:
            updates['username'] = new_username
        
        if new_city and new_city != app.current_user.get('city', ''):
            updates['city'] = new_city
        
        if new_password:
            if len(new_password) < 4:
                self.show_error('Новый пароль должен содержать минимум 4 символа')
                return
            if ' ' in new_password:
                self.show_error('Новый пароль не должен содержать пробелы')
                return
            updates['password'] = new_password
        
        if not updates:
            self.show_error('Нет изменений для сохранения')
            return
        
        # Обновление в отдельном потоке
        def update_thread():
            result = API.update_user(app.current_user['username'], current_password, updates)
            app.after(0, lambda: self.handle_update_result(result, updates))
        
        Thread(target=update_thread, daemon=True).start()
    
    def handle_update_result(self, result, updates):
        if 'success' in result and result['success']:
            # Обновление данных текущего пользователя
            if 'username' in updates:
                app.current_user['username'] = updates['username']
            if 'city' in updates:
                app.current_user['city'] = updates['city']
            
            self.show_success('Данные успешно обновлены')
        else:
            error_msg = result.get('error', 'Ошибка обновления')
            self.show_error(error_msg)
    
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        error_label = CLabel(app.frame, text=message, bg='grey22', fg='red', font=20, height=50,
                             width=600, corner_radius=25, justify='center')
        error_label.place(x=340, y=540)
    
    def show_success(self, message):
        """Показ сообщения об успехе"""
        success_label = CLabel(app.frame, text=message, bg='grey22', fg='green', font=20, height=50,
                               width=600, corner_radius=25, justify='center')
        success_label.place(x=340, y=540)

def about_app():
    app.clean_frame()
    
    label = CLabel(app.frame,
                   text='С помощью этого приложения вы всегда будете своевременно информированы о происходящем'
                        ' рядом\nс вами,' +
                        'обеспечивая себя и своих близких безопасностью, также вы сможете оставлять своё мнение'
                        '\n о конкретном городе, районе этого города.'
                   , font=25, fg='#EDFF21', bg='#1A1A1D',
                   justify='center')
    label.place(x=20, y=25)
    
    def open_youtube():
        url = 'https://youtube.com/live/3NO5s59qxxY'
        webbrowser.open(url)
    
    btn_youtube = RoundedButton(app.frame, text='Ссылка на наш youtube', bg_color='#1A1A1D', font_btn=25, height=70,
                                corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                command=open_youtube)
    btn_youtube.place(x=20, y=200)
    
    btn_vk = RoundedButton(app.frame, text='Ссылка на наш vk video', bg_color='#1A1A1D', font_btn=25, height=70,
                           corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00')
    btn_vk.place(x=930, y=200)
    
    btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=70,
                             corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00', command=home_page)
    btn_home.place(x=930, y=625)

def home_page():
    app.clean_frame()
    
    problem = Review()
    search = Get_review()
    cabinet = Cabinet()
    
    title_name = CLabel(app.frame, text='Информатор', font=50, bg='#1A1A1D', fg='#FFE400', width=340, height=60,
                        corner_radius=25)
    title_name.place(x=470, y=10)
    
    
    btn_problem = RoundedButton(app.frame, text='Оставить отзыв', bg_color='#1A1A1D', font_btn=25, height=70,
                                corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                command=problem.problem)
    btn_problem.place(x=25, y=150 if not app.current_user else 200)
    
    btn_static = RoundedButton(app.frame, text='Посмотреть статистику', bg_color='#1A1A1D', font_btn=25, height=70,
                               corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                               command=search.page_search)
    btn_static.place(x=25, y=250 if not app.current_user else 300)
    
    btn_cab = RoundedButton(app.frame, text='Профиль', bg_color='#1A1A1D', font_btn=25, height=70,
                            corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                            command=cabinet.page)
    btn_cab.place(x=25, y=350 if not app.current_user else 400)
    
    btn_info = RoundedButton(app.frame, text=f'О приложении', bg_color='#1A1A1D', font_btn=25, height=70,
                             corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00', command=about_app)
    btn_info.place(x=25, y=450 if not app.current_user else 500)
    
    # Кнопка выхода
    if app.current_user:
        btn_logout = RoundedButton(app.frame, text='Выйти', bg_color='#1A1A1D', font_btn=25, height=70,
                                   corner_radius=25, width=330, fg_color='red', border_color='red',
                                   command=logout)
        btn_logout.place(x=25, y=600)

def logout():
    """Выход из системы"""
    app.current_user = None
    # Удаление сохраненных данных
    try:
        import os
        if os.path.exists('user_data.json'):
            os.remove('user_data.json')
    except:
        pass
    Reg.main_page()

# Запуск приложения
if __name__ == '__main__':
    app = App()
    Reg = Registration()
    Reg.main_page()
    app.mainloop()