# Библиотеки и фреймворки, используемые в приложении
import json
import webbrowser

import customtkinter as ctk
from pyairtable import Api
from pyairtable.formulas import match


class RoundedButton(ctk.CTkButton):  # Класс, создающий кнопку
    def __init__(self, parent, bg_color='white', fg_color='black', text='', radius=10, command=None,
                 font_btn='13', bg_color_new='black',
                 rel_btn='groove', width=30, border_color='black', height=30, corner_radius=5,
                 state='normal'):  # задаются параметры
        # parent - родительский виджет, в котором будет размещена кнопка
        # bg_color - цвет фона кнопки
        # fg_color - цвет текста кнопки
        # text - текст, отображаемый на кнопке
        # radius - радиус закругления углов кнопки
        # command - функция, вызываемая при нажатии кнопки
        font2 = str(font_btn)[-2] + str(font_btn)[-1]
        a = ctk.CTkFont(size=int(font2))
        hv_color = '#AFEEEE'
        # Инициализация кнопки с заданными параметрами
        ctk.CTkButton.__init__(self, parent, text=text, command=command, width=width, fg_color=bg_color,
                               text_color=fg_color,
                               border_width=1, border_color=border_color, hover_color=hv_color, font=a,
                               corner_radius=corner_radius,
                               height=height, state=state)


class CLabel(ctk.CTkLabel):  # Класс, создающий текстовую надпись
    def __init__(self, parent, text='', fg='black', bg='white', font=13, relief='groove', justify='left',
                 width=30, corner_radius=5, height=30, border_color='#1A1A1D'):
        # parent - родительский виджет, в котором будет размещена метка
        # text - текст, отображаемый на метке
        # fg - цвет текста метки (не используется в коде, заменено на bg)
        # bg - цвет фона метки
        # font - шрифт текста метки
        # relief - стиль границы метки (не используется в коде)
        # justify - выравнивание текста в метке
        font2 = str(font)[-2] + str(font)[-1]
        a = ctk.CTkFont(size=int(font2))
        ctk.CTkLabel.__init__(self, parent, text=text, fg_color=bg, text_color=fg, width=width,
                              corner_radius=corner_radius, justify=justify,
                              font=a, height=height, bg_color='#1A1A1D')


class App(ctk.CTk):  # Класс, создающий окно приложения
    def __init__(self, width=1280, height=720):
        super().__init__()
        # Создание окна root
        self.title('Информатор')  # Название приложения
        self.geometry(f'{width}x{height}')  # Его размеры
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.finish)
        # Создание виджета frame
        self.frame = ctk.CTkFrame(self, fg_color='#1A1A1D')
        self.frame.place(relwidth=1, relheight=1)
        # Размер шрифта
        self.font = 15

    def clean_frame(self):  # Очистка страницы
        for widget in self.frame.winfo_children():
            # Уничтожение (destroy) каждого виджета в рамке
            widget.destroy()

    def finish(self):  # Выход из приложения
        self.destroy()  # Закрытие окна


class Review:  # Класс, создающий страницу, с которой отправляется жалоба в базу данных
    def __init__(self):
        self.city = ''  # Город, к которому относится отзыв
        # Инициализация переменных, с помощью которых будет реализован ввод на странице
        self.entry_street = None
        self.entry_city = None
        self.entry_district = None
        self.entry_com = None
        self.entry_grade = None
        self.entry_com = None
        self.check_infr = None  # Переменная, отвечающая за наличие/не наличие проблем со слабой инфраструктурой
        self.check_big_pr = None  # Переменная, отвечающая за наличие/не наличие проблем с автомобильными пробками
        self.check_dm = None  # Переменная, отвечающая за наличие/не наличие проблем с задымлением воздуха
        self.check_garbage = None  # Переменная, отвечающая за наличие/не наличие проблем с мусором
        self.check_lake = None  # Переменная, отвечающая за наличие/не наличие проблем с загрязнением водоёмов
        self.check_weather = None  # Переменная, отвечающая за наличие/не наличие проблем с климатом и погодой
        # Переменная, отвечающая за наличие/не наличие проблем с плохой работой соц. служб
        self.check_bad_social_work = None
        self.check_population = None  # Переменная, отвечающая за наличие/не наличие проблем с население
        self.check_noise = None  # Переменная, отвечающая за наличие/не наличие проблем с громким шумом

    def problem(self):  # Страница, с которой отправляется жалоба
        app.clean_frame()  # Очистка окна
        # Вывод интерфейса страницы
        title = CLabel(app.frame, text='Добавление отзыва', width=1230, font=30, bg='#1A1A1D', fg='#FFE400',
                       justify='center')
        title.place(x=25, y=10)
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
        title_problem = CLabel(app.frame, text='Тип проблемы',
                               font=25, height=45, width=1230, corner_radius=15, fg='#EDFF21', bg='grey22')
        title_problem.place(x=25, y=150)
        self.check_infr = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем со слабой инфраструктурой
        # Переменная, отвечающая за наличие/не наличие проблем с автомобильными пробками
        self.check_big_pr = ctk.IntVar()
        self.check_dm = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с задымлением воздуха
        self.check_garbage = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с мусором
        self.check_lake = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с загрязнением водоёмов
        self.check_weather = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с климатом и погодой
        # Переменная, отвечающая за наличие/не наличие проблем с плохой работой соц. служб
        self.check_bad_social_work = ctk.IntVar()
        self.check_population = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с населением
        self.check_noise = ctk.IntVar()  # Переменная, отвечающая за наличие/не наличие проблем с громким шумом
        # Создание флажков, среди которых пользователь будет выбирать проблемы, присутствующие в конкретном месте
        # Флажок, отвечающий за слабую инфраструктуру
        check_btn_infr = ctk.CTkCheckBox(app.frame, text="Слабая инфраструктура", variable=self.check_infr, onvalue=1,
                                         offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                         font=('Arial', 25), border_width=2, fg_color='#EDFF21',
                                         checkmark_color='#1A1A1D')
        check_btn_infr.place(x=75, y=210)  # Размещение флажка
        # Флажок, отвечающий за автомобильные пробки
        check_btn_big_pr = ctk.CTkCheckBox(app.frame, text="Автомобильные пробки ", variable=self.check_big_pr,
                                           onvalue=1,
                                           offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                           font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                           checkmark_color='#1A1A1D')
        check_btn_big_pr.place(x=450, y=210)  # Размещение флажка
        # Флажок, отвечающий за задымление воздуха
        check_btn_dm = ctk.CTkCheckBox(app.frame, text="Задымление воздуха", variable=self.check_dm, onvalue=1,
                                       offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                       font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                       checkmark_color='#1A1A1D')
        check_btn_dm.place(x=875, y=210)  # Размещение флажка
        # Флажок, отвечающий за загрязнение территории
        check_btn_garbage = ctk.CTkCheckBox(app.frame, text="Загрязнение территории", variable=self.check_garbage,
                                            onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_garbage.place(x=75, y=250)  # Размещение флажка
        # Флажок, отвечающий за загрязнение водоёмов
        check_btn_lake = ctk.CTkCheckBox(app.frame, text="Загрязнение водоёмов", variable=self.check_lake, onvalue=1,
                                         offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                         font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                         checkmark_color='#1A1A1D')
        check_btn_lake.place(x=450, y=250)  # Размещение флажка
        # Флажок, отвечающий за климатические условия
        check_btn_weather = ctk.CTkCheckBox(app.frame, text="Суровый климат", variable=self.check_weather, onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_weather.place(x=875, y=250)  # Размещение флажка
        # Флажок, отвечающий за качество работы местных спец. служб
        check_btn_bad_soc = ctk.CTkCheckBox(app.frame, text="Плохая работа упр. служб",
                                            variable=self.check_bad_social_work,
                                            onvalue=1,
                                            offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                            font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                            checkmark_color='#1A1A1D')
        check_btn_bad_soc.place(x=75, y=290)  # Размещение флажка
        # Флажок, отвечающий за маргинальность населения
        check_btn_pop = ctk.CTkCheckBox(app.frame, text="Маргинальность населения", variable=self.check_population,
                                        onvalue=1,
                                        offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                        font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                        checkmark_color='#1A1A1D')
        check_btn_pop.place(x=450, y=290)  # Размещение флажка
        # Флажок, отвечающий за громкий шум
        check_btn_noise = ctk.CTkCheckBox(app.frame, text="Громкий шум", variable=self.check_noise, onvalue=1,
                                          offvalue=0, text_color='#EDFF21', border_color='#EDFF21', corner_radius=15,
                                          font=('Arial', 25), border_width=2, width=150, fg_color='#EDFF21',
                                          checkmark_color='#1A1A1D')
        check_btn_noise.place(x=875, y=290)  # Размещение флажка
        # Создание поля ввода для написания комментария
        # Создание заголовка
        title_com = CLabel(app.frame, text='Комментарий',
                           font=25, height=45, width=605, corner_radius=15, fg='#EDFF21', bg='grey22')
        title_com.place(x=25, y=340)
        self.entry_com = ctk.CTkTextbox(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2, width=1230,
                                        font=('Arial', 25), height=250, fg_color='#1A1A1D', text_color='#FFBD00')
        self.entry_com.place(x=25, y=390)  # Размещение поля ввода
        # Поле ввода оценки пользователя
        label_grade = CLabel(app.frame, text='Общая оценка', font=25, height=45, width=270,
                             corner_radius=15,
                             fg='#EDFF21', bg='grey22')
        label_grade.place(x=660, y=340)
        # Создание заголовка
        self.entry_grade = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                        width=315,
                                        font=('Arial', 25), height=45, fg_color='#1A1A1D', text_color='#FFBD00',
                                        placeholder_text='Ваша оценка от 1 до 10')
        self.entry_grade.place(x=940, y=340)  # Размещение этого поля ввода
        # Создание и размещение кнопки отправки жалобы
        btn_send = RoundedButton(app.frame, text='Отправить отзыв', fg_color='#FFBD00', bg_color='#1A1A1D',
                                 border_color='#FFBD00', corner_radius=15, width=255, font_btn=25, height=50,
                                 command=self.send)
        btn_send.place(x=1000, y=655)
        # Создание и размещение кнопки для выхода в главное меню
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=15, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=25, y=655)

    def send(self):  # Функция для отправки жалобы
        com = self.entry_com._textbox.get("1.0", "end-1c")  # Получаем текст от начала до конца
        city = self.entry_city.get()  # Получаем текст, введённый в поле ввода города
        distr = self.entry_district.get()  # Получаем текст, введённый в поле ввода района
        street = self.entry_street.get()  # Получаем текст, введённый в поле ввода улицы
        grade = self.entry_grade.get()  # Получаем текст, введённый в поле ввода оценки
        # Проверка правильности ввода
        if len(city) == 0 or city.count(" ") == len(city):
            self.entry_city.configure(border_color='red')  # Подсвечивание поля с некорректным вводом
        elif len(distr) == 0 or distr.count(" ") == len(distr):
            self.entry_district.configure(border_color='red')  # Подсвечивание поля с некорректным вводом
        elif len(street) == 0 or street.count(" ") == len(street):
            self.entry_street.configure(border_color='red')  # Подсвечивание поля с некорректным вводом
        elif len(grade) == 0 or grade.isdigit() == False or not (0 <= int(grade) <= 10):
            self.entry_grade.configure(border_color='red')  # Подсвечивание поля с некорректным вводом
        else:
            self.send_page()  # Вывод пользователю информации, что его жалоба отправляется
            if len(com) == 0 or len(com) == com.count(" "):
                com = ''
            # Формирование списка с жалобами
            sp_problem = [self.check_infr.get(), self.check_garbage.get(), self.check_bad_social_work.get(),
                          self.check_big_pr.get(),
                          self.check_lake.get(), self.check_population.get(), self.check_dm.get(),
                          self.check_weather.get(), self.check_noise.get()]
            all_problem = ''  # Строка, которая отправляется в бд
            for i in range(len(sp_problem)):  # Формирование строки, содержащей информацию о проблемах
                all_problem += str(sp_problem[i])  # Для экономии места в бд строка содержит только 0 или 1
            # Отправка жалобы в бд
            baza.create_record('Review', {'name': Reg.name, 'city': city, 'district': distr,
                                          'street': street, 'spproblem': all_problem, 'comment': com, 'grade': grade})
            self.page_res()  # Вывод пользователю информации, что его жалоба отправилась

    def send_page(self):
        app.clean_frame()  # Очистка окна
        # Вывод информации о текущем состоянии отправки
        title = CLabel(app.frame, text='Ваш отзыв отправляется', font=25, height=100, width=330,
                       corner_radius=15,
                       fg='#EDFF21', bg='grey22')
        title.place(x=505, y=100)

    def page_res(self):
        app.clean_frame()  # Очистка окна
        # Вывод информации о текущем состоянии отправки
        title = CLabel(app.frame, text='Ваш отзыв был отправлен', font=25, height=100, width=270,
                       corner_radius=15,
                       fg='#EDFF21', bg='grey22')
        title.place(x=505, y=100)
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=505, y=225)


class Get_review:  # Класс, создающий страницу для получения информации о каком-то месте
    def __init__(self):
        self.search_city = None
        self.search_district = None
        self.search_street = None

    def page_search(self):
        app.clean_frame()  # Очистка окна
        # Вывод заголовка
        title = CLabel(app.frame, text='Поиск отзывов', width=1230, font=30, bg='#1A1A1D', fg='#FFE400',
                       justify='center')
        title.place(x=25, y=10)
        title_city = CLabel(app.frame, text='Город', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                            corner_radius=15, height=50, width=110)
        title_city.place(x=25, y=75)
        # Создание полей ввода
        # Поля ввода города
        self.search_city = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2, width=220,
                                        font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                        placeholder_text='Ваш город')
        self.search_city.place(x=150, y=75)
        title_district = CLabel(app.frame, text='Район', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                                corner_radius=15, height=50, width=110)
        title_district.place(x=25, y=150)
        # Поля ввода района
        self.search_district = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                            width=220,
                                            font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                            placeholder_text='Ваш район')
        self.search_district.place(x=150, y=150)
        title_street = CLabel(app.frame, text='Улица', font=30, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                              corner_radius=15, height=50, width=110)
        title_street.place(x=25, y=225)
        # Поля ввода улицы
        self.search_street = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                          width=220,
                                          font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                          placeholder_text='Ваша улица')
        self.search_street.place(x=150, y=225)
        # Создание кнопки для перехода к поиску
        btn_search = RoundedButton(app.frame, text='Поиск', bg_color='#1A1A1D', font_btn=25, height=45,
                                   corner_radius=15, width=345, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.search)
        btn_search.place(x=25, y=300)
        # Создание кнопки для возврата в главное меню
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=23, height=40,
                                 corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=925, y=670)

    def search(self):
        # Список жалоб, оставленных в городе, по которому введётся запрос
        sp_city = baza.get_record('Review', {'city': self.search_city.get()})
        # Список жалоб, оставленных в районе, по которому введётся запрос
        sp_district = list(filter(lambda x: x['fields']['district'] == self.search_district.get(), sp_city))
        # Список жалоб, оставленных в улице, по которому введётся запрос
        sp_street = list(filter(lambda x: x['fields']['street'] == self.search_street.get(), sp_district))[::-1]
        if sp_street != []:  # Если в БД есть информация о текущей улице
            problem = [i['fields']['spproblem'] for i in sp_street]  # Список проблем, получаемый из базы данных
            sp_problem = [['Слабая инфраструктура'], ['Загрязнение территории'],
                          ['Плохая работа упр. служб'],
                          ['Автомобильные пробки'], ['Загрязнение водоёмов'], ['Маргинальность населения'],
                          ['Задымление воздуха'], ['Суровый климат'], ['Громкий шум']]
            # Формирование списка проблем для вывода
            for i in range(len(problem[0])):
                k = 0
                for j in problem:
                    k += int(j[i])
                sp_problem[i].append(k)
            grade = round(sum([int(i['fields']['grade']) for i in sp_street]) / len(sp_street), 2)  # Оценка жильцов
            sp_problem = list(filter(lambda x: x[1] != 0, sorted(sp_problem, key=lambda x: x[1],
                                                                 reverse=True)))  # Список самых популярных проблем
            # Формирование строки с жалобами для вывода пользователю
            if not ([i[1] for i in sp_problem].count(0) == 9):  # Если есть жалобы
                show_problem = ''
                k = 1
                for i in sp_problem:
                    show_problem += f'{k}. {i[0]}{(27 - len(i[0])) * " "}Кол-во обращений: {i[1]}\n'
                    k += 1
                    if k > 5:
                        break
            else:
                show_problem = 'Жалоб по этому месту нет'
            # Вывод информации пользователю на экран
            title = CLabel(app.frame, text=f'{"  " * 15}Самые популярные жалобы\n\n{show_problem}\nОценка жильцов:'
                                           f' {grade}/10', font=23, width=855, bg='grey22',
                           fg='#FFE400', height=270, corner_radius=15)
            title.place(x=400, y=75)
            # Формирование строки комментария для вывода пользователю
            comments = ''
            for i in sp_street:
                i = i['fields']
                if 'comment' in i.keys():
                    comments += i['comment'] + '\n' + '=' * 101 + '\n'
            if len(comments):
                comments = 47 * '  ' + 'Отзывы\n' + 101 * '=' + '\n' + comments
            else:
                comments = 'Комментариев нет'
            # Вывод всех отзывов пользователю на экран
            textbox = ctk.CTkTextbox(app.frame, width=1230, corner_radius=5, height=300, border_color='#FFBD00',
                                     text_color='#FFBD00', fg_color='#1A1A1D', border_width=2, font=('Arial', 20))
            textbox.insert("0.0", comments)
            textbox.configure(state="disabled")
            textbox.place(x=25, y=365)

        elif sp_district != []:  # Если нет информации по конкретной улице, но есть информация по району поиска
            problem = [i['fields']['spproblem'] for i in sp_district]  # Список проблем, получаемый из базы данных
            # Список проблем, получаемый из базы данных
            sp_problem = [['Слабая инфраструктура'], ['Загрязнение территории'],
                          ['Плохая работа упр. служб'],
                          ['Автомобильные пробки'], ['Загрязнение водоёмов'], ['Маргинальность населения'],
                          ['Задымление воздуха'], ['Суровый климат'], ['Громкий шум']]
            # Формирование списка проблем для вывода
            for i in range(len(problem[0])):
                k = 0
                for j in problem:
                    k += int(j[i])
                sp_problem[i].append(k)
            grade = round(sum([int(i['fields']['grade']) for i in sp_district]) / len(sp_district), 2)  # Оценка жильцов
            sp_problem = list(filter(lambda x: x[1] != 0, sorted(sp_problem, key=lambda x: x[1],
                                                                 reverse=True)))  # Список самых популярных проблем
            # Формирование строки с жалобами для вывода пользователю
            if not ([i[1] for i in sp_problem].count(0) == 9):  # Если есть жалобы
                show_problem = ''
                k = 1
                for i in sp_problem:
                    show_problem += f'{k}. {i[0]}{(27 - len(i[0])) * " "}Кол-во обращений: {i[1]}\n'
                    k += 1
                    if k > 5:
                        break
            else:
                show_problem = 'Жалоб по этому месту нет'
            # Вывод информации пользователю на экран
            title = CLabel(app.frame,
                           text=f'По запрашиваемой улице не было найдено результатов\nОбщие сведения о районе:\n\n'
                                f'{"  " * 15}Самые популярные жалобы\n{show_problem}\nОценка жильцов:'
                                f' {grade}/10', font=20, width=855, bg='grey22',
                           fg='#FFE400', height=270, corner_radius=15)
            title.place(x=400, y=75)
            # Формирование строки комментария для вывода пользователю
            comments = ''
            for i in sp_district:
                i = i['fields']
                if 'comment' in i.keys():
                    comments += i['comment'] + '\n' + '=' * 101 + '\n'
            if len(comments):
                comments = 47 * '  ' + 'Отзывы\n' + 101 * '=' + '\n' + comments
            else:
                comments = 'Комментариев нет'
            # Вывод всех отзывов пользователю на экран
            textbox = ctk.CTkTextbox(app.frame, width=1230, corner_radius=5, height=300, border_color='#FFBD00',
                                     text_color='#FFBD00', fg_color='#1A1A1D', border_width=2, font=('Arial', 20))
            textbox.insert("0.0", comments)
            textbox.configure(state="disabled")
            textbox.place(x=25, y=365)
        else:  # Если ничего не было найдено
            # Вывод заголовка
            title = CLabel(app.frame, text='По вашему запросу ничего не найдено', width=830, font=30, bg='grey22',
                           fg='#FFE400',
                           justify='center', height=270, corner_radius=15)
            bg = CLabel(app.frame, text='', bg='#1A1A1D', fg='#1A1A1D', border_color='#1A1A1D', width=1230, height=300)
            title.place(x=400, y=75)
            bg.place(x=25, y=365)


class Bd:  # Класс, создающий экземпляр для взаимодействия с БД
    # Используется база данных AirTable
    def __init__(self):
        # Токен бд
        airtable_token = 'patYjQ9sO59UNzN6O.eb1dfe59a1837740f4ccffc6e96f38cd8d8539fe6422707b2b1aaf8691ca4083'
        # Ид бд
        self.base_id = 'appXgwqUNM4KLAqcY'
        self.api = Api(airtable_token)

    def create_record(self, table_name: str, record: dict) -> dict:  # Создание записи в бд
        table = self.api.table(self.base_id, table_name)
        result = table.create(record)
        return result

    def get_record(self, table_name: str, filter: dict) -> dict:  # Получение информации о бд
        formula = match(filter)
        table = self.api.table(self.base_id, table_name)
        result = table.all(formula=formula)
        return result

    def update_record(self, table_name: str, filter: dict, update: dict) -> dict:  # Изменение информации в бд
        formula = match(filter)
        table = self.api.table(self.base_id, table_name)
        records = table.all(formula=formula)
        if len(records) > 0:
            record_id = records[0]['id']
            result = table.update(record_id, update)
            return result
        else:
            return []


baza = Bd()  # Создание экземпляра класса Bd


class Registration:  # Класс, создающий окно регистрации/входа в приложение
    def __init__(self):
        self.label_nic = None
        self.label_password = None
        self.city = None
        self.name = None

    def main_page(self):
        app.clean_frame()  # Очистка окна
        bg = RoundedButton(app.frame, text='', height=260, width=350, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=465, y=120)  # Вывод заднего фона, жёлтой обводки кнопок
        title = CLabel(app.frame, text='Выполните вход', font=27, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=300)
        title.place(x=490, y=150)  # Создание и вывод заголовка "Выполните вход"
        # Создание и размещение кнопки, с помощью которой пользователь может войти в свой аккаунт
        btn_entrance = RoundedButton(app.frame, text='Войти', bg_color='#1A1A1D', font_btn=25, height=50,
                                     corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                     command=self.entrance)
        btn_entrance.place(x=515, y=225)
        # Создание и размещение кнопки, с помощью которой пользователь может создать аккаунт
        btn_reg = RoundedButton(app.frame, text='Регистрация', bg_color='#1A1A1D', font_btn=25, height=50,
                                corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                command=self.registration)
        btn_reg.place(x=515, y=300)
        if self.fast_entrance():  # Если можно реализовать быстрый вход
            bg2 = RoundedButton(app.frame, text='', height=120, width=350, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                                border_color='#EDFF21', corner_radius=25, state='disabled')
            bg2.place(x=465, y=400)  # Вывод заднего фона, жёлтой обводки кнопок
            title2 = CLabel(app.frame, text='Быстрый вход', font=20, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                            corner_radius=15, height=40, width=300)
            title2.place(x=490, y=410)  # Создание и вывод заголовка "Быстрый вход"
            name = self.fast_entrance()['name']
            btn_fast_entrance = RoundedButton(app.frame, text=name,
                                              bg_color='#1A1A1D', font_btn=25, height=50,
                                              corner_radius=25, width=250, fg_color='#FFBD00', border_color='#FFBD00',
                                              command=home_page)
            btn_fast_entrance.place(x=515, y=460)

    def fast_entrance(self):  # Функция для быстрого входа в приложение
        try:  # Проверка есть ли информация о предыдущем входе
            with open('bd.py', 'r', encoding='utf-8') as file:
                data = json.load(file)
                if baza.get_record('rp', {'username': data['name']})[0]['fields']['password'] == data['password']:
                    self.name = data['name']
                    # Если есть, то можно реализовать быстрый вход
                    return data
                else:
                    # Иначе нет
                    return False
        except:
            return False

    def entrance(self):  # Функция, с помощью которой пользователь может войти в свой аккаунт
        app.clean_frame()  # Очистка окна
        bg = RoundedButton(app.frame, text='', height=335, width=400, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=440, y=120)  # Вывод заднего фона, жёлтой обводки кнопок
        label = CLabel(app.frame, text='Вход', font=25, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=350, justify='center')
        label.place(x=465, y=150)  # Создание и вывод заголовка "Вход"
        # Создание поле ввода, в которое пользователь будет вводить свой никнейм
        self.label_nic = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=350,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text='Введите никнейм',
                                      justify='center')
        # Создание поле ввода, в которое пользователь будет вводить пароль от аккаунта
        self.label_password = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                           width=350,
                                           font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                           placeholder_text='Введите пароль',
                                           justify='center')
        self.label_nic.place(x=465, y=225)  # Размещение этих виджетов
        self.label_password.place(x=465, y=300)
        # Создание и размещение кнопки, отвечающей за проверку никнейма и пароля, которые ввёл пользователь
        next_btn = RoundedButton(app.frame, text='Продолжить', bg_color='#1A1A1D', font_btn=20, height=50,
                                 corner_radius=15, width=350, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=self.get_entrance)
        next_btn.place(x=465, y=375)
        # Создание и размещение кнопки, которая возвращает пользователя на предыдущую страницу
        btn_return = RoundedButton(app.frame, text='Вернуться назад', bg_color='#1A1A1D', font_btn=25, height=50,
                                   corner_radius=25, width=300, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.main_page)
        btn_return.place(x=960, y=645)

    def get_entrance(self):  # Функция для проверки имени и пароля пользователя
        nic = self.label_nic.get()  # Получаем имя, которое ввёл пользователь
        password = self.label_password.get()  # Получаем пароль, который ввёл пользователь
        if len(baza.get_record('rp', {'username': nic})) != 0:  # Если такой никнейм существует
            # Сравнение паролей и проверка на наличие аккаунта
            if baza.get_record('rp', {'username': nic})[0]['fields']['password'] == password:
                home_page()  # Если пароль, введённый пользователем, совпал с паролем из базы данных
                # Сохранение в локальный файл пароля и имени пользователя, для быстрого входа
                data = {'password': password, 'name': nic}
                self.write_info('bd.py', data)
            else:  # Иначе выводится предупреждение "Неверный пароль"
                label_error = CLabel(app.frame, text='Неверный пароль', bg='grey22', fg='#FFBD00', font=25, height=50,
                                     width=350, corner_radius=25)
                label_error.place(x=860, y=300)  # Размещение виджета с предупреждением
        else:  # Если никнейма, который ввёл пользователь, не было найдено в базе данных
            label_error = CLabel(app.frame, text='Данного имени не существует', bg='grey22', fg='#FFBD00', font=25,
                                 height=50,
                                 width=350, corner_radius=25)
            label_error.place(x=860,
                              y=225)  # Создание и размещение виджета с предупреждением "Данного имени не существует"

    def registration(self):  # Регистрация пользователя
        app.clean_frame()  # Очистка окна
        # Вывод заднего фона
        bg = RoundedButton(app.frame, text='', height=410, width=400, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=440, y=120)
        # Вывод заголовка
        title = CLabel(app.frame, text='Регистрация', font=25, fg='#EDFF21', bg='grey22', border_color='#EDFF21',
                       corner_radius=15, height=50, width=350)
        title.place(x=465, y=150)
        # Вывод полей ввода
        # Поле ввода имени
        self.label_nic = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=350,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text='Введите ваш никнейм', justify='center')
        self.label_nic.place(x=465, y=225)
        # Поле ввода пароля
        self.label_password = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                           width=350,
                                           font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                           placeholder_text='Придумайте пароль', justify='center')
        self.label_password.place(x=465, y=300)
        # Поле ввода города проживания
        self.city = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                 width=350,
                                 font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                 placeholder_text='Введите город проживания', justify='center')
        self.city.place(x=465, y=375)
        # Кнопка регистрации
        next_btn = RoundedButton(app.frame, text='Зарегистрироваться', bg_color='#1A1A1D', font_btn=20, height=50,
                                 corner_radius=15, width=350, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=self.get_reg)
        next_btn.place(x=465, y=450)
        # Создание и размещение кнопки, которая возвращает пользователя на предыдущую страницу
        btn_return = RoundedButton(app.frame, text='Вернуться назад', bg_color='#1A1A1D', font_btn=25, height=50,
                                   corner_radius=25, width=400, fg_color='#FFBD00', border_color='#FFBD00',
                                   command=self.main_page)
        btn_return.place(x=440, y=550)

    def get_reg(self):  # Функция для регистрации
        nic = self.label_nic.get()  # Получение ника
        # Проверка ввода на корректность
        # Проверка имени на корректность
        if len(nic) == 0 or nic.count(" ") == len(nic):
            label_error = CLabel(app.frame, text='Некорректный ввод', bg='grey22', fg='#FFBD00', font=25,
                                 height=50,
                                 width=350, corner_radius=25, justify='center')
            label_error.place(x=855, y=225)
        # Проверка пароля на корректность
        elif len(self.label_password.get()) == 0 or ' ' in self.label_password.get():
            label_error = CLabel(app.frame, text='Введите пароль без пробелов', bg='grey22', fg='#FFBD00', font=25,
                                 height=50,
                                 width=350, corner_radius=25, justify='center')
            label_error.place(x=855, y=300)
        # Проверка ввода города на корректность
        elif len(self.city.get()) == 0 or ' ' in self.city.get():
            label_error = CLabel(app.frame, text='Введите название города\n без пробелов', bg='grey22', fg='#FFBD00',
                                 font=25,
                                 height=50,
                                 width=350, corner_radius=25, justify='center')
            label_error.place(x=855, y=375)
        # Дополнительная проверка пароля на корректность
        elif len(self.label_password.get()) < 4:
            label_error = CLabel(app.frame, text='Пароль должен содержать\n хотя бы 4 символа', bg='grey22',
                                 fg='#FFBD00', font=25, height=50,
                                 width=350, corner_radius=25, justify='center')
            label_error.place(x=855, y=300)
        # Если проблем с вводом не было обнаружено, то
        else:
            # Проверка имени на индивидуальность
            if len(baza.get_record('rp', {'username': nic})) > 0:
                label_error = CLabel(app.frame, text='Пользователь с таким ником\n уже существует', bg='grey22',
                                     fg='#FFBD00', font=25, height=50,
                                     width=350, corner_radius=25, justify='center')
                label_error.place(x=855, y=225)
            # Если имя индивидуально
            else:
                # Создание записи в бд
                baza.create_record('rp',
                                   {'username': nic, 'password': self.label_password.get(), 'city': self.city.get(),
                                    'Complaints': '0'})
                # Сохранение в локальный файл пароля и имени пользователя, для быстрого входа
                data = {'password': self.label_password.get(), 'name': nic}
                self.write_info('bd.py', data)  # Запись в локальную бд
                home_page()  # Вывод домашней страницы

    def write_info(self, file_name, data):  # Запись в локальную бд
        data = json.dumps(data)  # конвертируем data в json
        data = json.loads(str(data))
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)


class Cabinet:  # Класс, создающий страницу личного кабинета
    def __init__(self):
        # Получение информации с локальной бд
        with open('bd.py', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.password = data['password']  # Получение пароля
        self.name = data['name']  # Получение имени
        self.nic_entry = None
        self.pas_entry = None
        self.city_entr = None

    def page(self):  # Открытие страницы
        app.clean_frame() # Очистка окна
        inf = baza.get_record('rp', {'username': self.name})
        # Вывод заднего фона, жёлтой обводки кнопок
        bg = RoundedButton(app.frame, text='', height=375, width=620, bg_color='#1A1A1D', bg_color_new='#1A1A1D',
                           border_color='#EDFF21', corner_radius=25, state='disabled')
        bg.place(x=330, y=170)
        # Вывод заголовка
        title = CLabel(app.frame, text='Профиль', font=27, bg='grey22', fg='#EDFF21', corner_radius=25,
                       justify='center', width=600, height=60)
        title.place(x=340, y=185)
        title_nic = CLabel(app.frame, text='Ваше имя:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                           justify='center', width=290, height=50)
        title_nic.place(x=340, y=250)
        # Вывод полей ввода
        # Поле ввода с именем
        self.nic_entry = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text=self.name, justify='center')
        self.nic_entry.place(x=650, y=250)
        # Поле ввода с паролем
        title_password = CLabel(app.frame, text='Ваш пароль:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                                justify='center', width=290, height=50)
        title_password.place(x=340, y=305)
        self.pas_entry = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text=self.password, justify='center')
        self.pas_entry.place(x=650, y=305)
        title_city = CLabel(app.frame, text='Город проживания:', font=25, bg='grey22', fg='#EDFF21', corner_radius=15,
                            justify='center', width=290, height=50)
        title_city.place(x=340, y=360)
        # Поле ввода с городом
        self.city_entr = ctk.CTkEntry(app.frame, corner_radius=15, border_color='#FFBD00', border_width=2,
                                      width=290,
                                      font=('Arial', 25), height=50, fg_color='#1A1A1D', text_color='#FFBD00',
                                      placeholder_text=inf[0]['fields']['city'], justify='center')
        self.city_entr.place(x=650, y=360)
        # Кнопка для сохранения изменений
        btn_changes = RoundedButton(app.frame, text='Сохранить изменения', bg_color='#1A1A1D', font_btn=25, height=50,
                                    corner_radius=25, width=600, fg_color='#FFBD00', border_color='#FFBD00',
                                    command=self.changes_personal_data)
        btn_changes.place(x=340, y=415)
        # Кнопка для выхода в главное меню
        btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=50,
                                 corner_radius=25, width=600, fg_color='#FFBD00', border_color='#FFBD00',
                                 command=home_page)
        btn_home.place(x=340, y=475)

    def changes_personal_data(self): # Изменение данных
        data = baza.get_record('rp', {'username': self.name})
        # Изменение данных в д
        if self.nic_entry.get() != '':
            data[0]['fields']['username'] = self.nic_entry.get()
        if self.pas_entry.get() != '':
            data[0]['fields']['password'] = self.pas_entry.get()
        if self.city_entr.get() != '':
            data[0]['fields']['city'] = self.city_entr.get()
        # Сохранение информации в бд
        baza.update_record('rp', {'username': self.name}, data[0]['fields'])


def about_app():  # Страница осуществляющая вывод информации о приложении
    app.clean_frame()  # Очистка окна
    # Вывод заголовка
    label = CLabel(app.frame,
                   text='С помощью этого приложения вы всегда будете своевременно информированы о происходящем'
                        ' рядом\nс вами,' +
                        'обеспечивая себя и своих близких безопасностью, также вы сможете оставлять своё мнение'
                        '\n о конкретном городе, районе этого города.'
                   , font=25, fg='#EDFF21', bg='#1A1A1D',
                   justify='center')
    label.place(x=20, y=25)

    # Демонстрационный пример перемещения пользователя на сайт с видео-инструкцией
    def open_youtube():
        url = 'https://youtube.com/live/3NO5s59qxxY'
        webbrowser.open(url)

    # Создание кнопок для перемещения на сайты
    btn_youtube = RoundedButton(app.frame, text='Ссылка на наш youtube', bg_color='#1A1A1D', font_btn=25, height=70,
                                corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                command=open_youtube)
    btn_youtube.place(x=20, y=200)
    btn_rutube = RoundedButton(app.frame, text='Ссылка на наш rutube', bg_color='#1A1A1D', font_btn=25, height=70,
                               corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00')
    btn_rutube.place(x=475, y=200)
    btn_vk = RoundedButton(app.frame, text='Ссылка на наш vk video', bg_color='#1A1A1D', font_btn=25, height=70,
                           corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00')
    btn_vk.place(x=930, y=200)
    # Создание кнопки для выхода в меню
    btn_home = RoundedButton(app.frame, text='Вернуться на главную', bg_color='#1A1A1D', font_btn=25, height=70,
                             corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00', command=home_page)
    btn_home.place(x=930, y=625)


def home_page():  # Функция для создания домашней страницы, главного меню
    app.clean_frame()  # Очистка окна
    # Инициализация объектов классов, отвечающих за личный кабинет, отправку жалобы и получения информации
    # о каком-то месте
    problem = Review()
    search = Get_review()
    cabinet = Cabinet()
    # Вывод заголовка
    title_name = CLabel(app.frame, text='Информатор', font=50, bg='#1A1A1D', fg='#FFE400', width=340, height=60,
                        corner_radius=25)  # 66FCF1
    title_name.place(x=470, y=10)
    # Вывод кнопок главного меню
    # Кнопка, открывающая страницу для формирования отзыва пользователя
    btn_problem = RoundedButton(app.frame, text='Оставить отзыв', bg_color='#1A1A1D', font_btn=25, height=70,
                                corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                                command=problem.problem)
    btn_problem.place(x=25, y=150)
    # Кнопка, открывающая страницу для просмотра информации о конкретном месте
    btn_static = RoundedButton(app.frame, text='Посмотреть статистику', bg_color='#1A1A1D', font_btn=25, height=70,
                               corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                               command=search.page_search)
    btn_static.place(x=25, y=250)
    # Кнопка для перехода в личный кабинет
    btn_cab = RoundedButton(app.frame, text='Профиль', bg_color='#1A1A1D', font_btn=25, height=70,
                            corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00',
                            command=cabinet.page)
    btn_cab.place(x=25, y=350)
    # Кнопка для просмотра информации о личном кабинете
    btn_info = RoundedButton(app.frame, text=f'О приложении', bg_color='#1A1A1D', font_btn=25, height=70,
                             corner_radius=25, width=330, fg_color='#FFBD00', border_color='#FFBD00', command=about_app)
    btn_info.place(x=25, y=450)


app = App()  # Создание окна
Reg = Registration()  # Создание окна регистрации
Reg.main_page()
app.mainloop()
