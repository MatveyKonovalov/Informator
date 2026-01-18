# server.py
import json
import logging
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from data_base import Bd
# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Security:
    """Класс для работы с безопасностью"""
    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return Security.hash_password(password) == hashed_password

# Инициализация подключения к базе данных
airtable_token = os.getenv('airtable_token')
base_id = os.getenv('base_id')

# Проверка загрузки переменных окружения
if not airtable_token or not base_id:
    logging.error("ОШИБКА: Переменные окружения не загружены!")
    logging.error(f"airtable_token: {airtable_token}")
    logging.error(f"base_id: {base_id}")
    logging.error("Проверьте наличие файла .env в той же папке, что и server.py")
    logging.error("Содержимое .env должно быть:")
    logging.error("airtable_token=patYOUR_TOKEN_HERE")
    logging.error("base_id=appYOUR_BASE_ID_HERE")
    exit(1)

# Создаем экземпляр Bd
try:
    db_instance = Bd(airtable_token, base_id)
    logging.info(f"Подключение к Airtable установлено с base_id: {base_id}")
except Exception as e:
    logging.error(f"Ошибка подключения к Airtable: {e}")
    exit(1)

class RequestHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов"""
    
    def __init__(self, *args, **kwargs):
        # Используем глобальный экземпляр Bd
        self.db = db_instance
        self.security = Security()
        super().__init__(*args, **kwargs)
    
    def _set_headers(self, status_code=200, content_type='application/json'):
        """Установка заголовков ответа"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """Обработка CORS preflight запросов"""
        self._set_headers(200)
    
    def do_GET(self):
        """Обработка GET запросов"""
        try:
            if self.path.startswith('/api/reviews/search'):
                self._handle_search_reviews()
            elif self.path.startswith('/api/user/profile'):
                self._handle_get_user_profile()
            elif self.path == '/api/health':
                self._set_headers(200)
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        except Exception as e:
            logging.error(f"Error in GET request: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_POST(self):
        """Обработка POST запросов"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/reviews/create':
                self._handle_create_review(data)
            elif self.path == '/api/user/register':
                self._handle_register_user(data)
            elif self.path == '/api/user/login':
                self._handle_login_user(data)
            elif self.path == '/api/user/update':
                self._handle_update_user(data)
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Not found'}).encode())
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Invalid JSON'}).encode())
        except Exception as e:
            logging.error(f"Error in POST request: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_create_review(self, data):
        """Создание нового отзыва"""
        try:
            required_fields = ['name', 'city', 'district', 'street', 'spproblem', 'grade']
            for field in required_fields:
                if field not in data or not str(data[field]).strip():
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': f'Missing required field: {field}'}).encode())
                    return
            
            # Проверка оценки
            try:
                grade = int(data['grade'])
                if not (0 <= grade <= 10):
                    raise ValueError
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Grade must be integer between 0 and 10'}).encode())
                return
            
            # Создание записи
            record_data = {
                'name': str(data['name']).strip(),
                'city': str(data['city']).strip(),
                'district': str(data['district']).strip(),
                'street': str(data['street']).strip(),
                'spproblem': str(data['spproblem']).strip(),
                'grade': str(grade)
            }
            
            if 'comment' in data and data['comment']:
                record_data['comment'] = str(data['comment']).strip()
            
            result = self.db.create_record('Review', record_data)
            
            self._set_headers(201)
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'Отзыв успешно создан',
                'id': result.get('id')
            }).encode())
        except Exception as e:
            logging.error(f"Error creating review: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_search_reviews(self):
        """Поиск отзывов"""
        try:
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            filter_dict = {}
            if 'city' in params:
                filter_dict['city'] = params['city'][0]
            if 'district' in params:
                filter_dict['district'] = params['district'][0]
            if 'street' in params:
                filter_dict['street'] = params['street'][0]
            
            reviews = self.db.get_record('Review', filter_dict)
            
            if reviews:
                processed_reviews = []
                problems_summary = [0] * 9  # 9 типов проблем
                total_grade = 0
                comments = []
                
                for review in reviews:
                    fields = review['fields']
                    processed_review = {
                        'id': review['id'],
                        'name': fields.get('name', ''),
                        'city': fields.get('city', ''),
                        'district': fields.get('district', ''),
                        'street': fields.get('street', ''),
                        'grade': int(fields.get('grade', 0))
                    }
                    
                    # Анализ проблем
                    if 'spproblem' in fields:
                        problems = fields['spproblem']
                        for i in range(min(9, len(problems))):
                            if problems[i] == '1':
                                problems_summary[i] += 1
                    
                    # Сбор комментариев
                    if 'comment' in fields and fields['comment']:
                        comments.append(fields['comment'])
                    
                    total_grade += processed_review['grade']
                    processed_reviews.append(processed_review)
                
                # Расчет средней оценки
                average_grade = round(total_grade / len(processed_reviews), 2) if processed_reviews else 0
                
                # Названия проблем
                problem_names = [
                    'Слабая инфраструктура',
                    'Загрязнение территории',
                    'Плохая работа упр. служб',
                    'Автомобильные пробки',
                    'Загрязнение водоёмов',
                    'Маргинальность населения',
                    'Задымление воздуха',
                    'Суровый климат',
                    'Громкий шум'
                ]
                
                # Топ-5 проблем
                top_problems = []
                for i, count in enumerate(problems_summary):
                    if count > 0:
                        top_problems.append({
                            'name': problem_names[i],
                            'count': count
                        })
                
                top_problems.sort(key=lambda x: x['count'], reverse=True)
                top_problems = top_problems[:5]
                
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'success': True,
                    'reviews': processed_reviews,
                    'statistics': {
                        'total_reviews': len(processed_reviews),
                        'average_grade': average_grade,
                        'top_problems': top_problems,
                        'comments': comments
                    }
                }).encode())
            else:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'success': True,
                    'reviews': [],
                    'statistics': {
                        'total_reviews': 0,
                        'average_grade': 0,
                        'top_problems': [],
                        'comments': []
                    }
                }).encode())
        except Exception as e:
            logging.error(f"Error searching reviews: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_register_user(self, data):
        """Регистрация пользователя"""
        try:
            required_fields = ['username', 'password', 'city']
            for field in required_fields:
                if field not in data or not str(data[field]).strip():
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': f'Отсутствует обязательное поле: {field}'}).encode())
                    return
            
            username = str(data['username']).strip()
            password = str(data['password']).strip()
            city = str(data['city']).strip()
            
            # Проверка имени пользователя
            if len(username) < 3 or ' ' in username:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Имя пользователя должно содержать минимум 3 символа без пробелов'}).encode())
                return
            
            # Проверка пароля
            if len(password) < 4 or ' ' in password:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Пароль должен содержать минимум 4 символа без пробелов'}).encode())
                return
            
            # Проверка существования пользователя
            existing_users = self.db.get_record('rp', {'username': username})
            if existing_users:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Пользователь с таким именем уже существует'}).encode())
                return
            
            # Хеширование пароля
            hashed_password = self.security.hash_password(password)
            
            # Создание пользователя
            user_data = {
                'username': username,
                'password': hashed_password,
                'city': city,
                'Complaints': '0'
            }
            
            result = self.db.create_record('rp', user_data)
            
            self._set_headers(201)
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'Пользователь успешно зарегистрирован',
                'user': {
                    'username': username,
                    'city': city
                }
            }).encode())
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_login_user(self, data):
        """Вход пользователя"""
        try:
            required_fields = ['username', 'password']
            for field in required_fields:
                if field not in data or not str(data[field]).strip():
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': f'Отсутствует обязательное поле: {field}'}).encode())
                    return
            
            username = str(data['username']).strip()
            password = str(data['password']).strip()
            
            # Поиск пользователя
            users = self.db.get_record('rp', {'username': username})
            
            if not users:
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'Пользователь не найден'}).encode())
                return
            
            user = users[0]['fields']
            hashed_password = user.get('password', '')
            
            # Проверка пароля на сервере
            if not self.security.verify_password(password, hashed_password):
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'Неверный пароль'}).encode())
                return
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'Вход выполнен успешно',
                'user': {
                    'username': user['username'],
                    'city': user.get('city', ''),
                    'complaints': user.get('Complaints', '0')
                }
            }).encode())
        except Exception as e:
            logging.error(f"Error logging in user: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_get_user_profile(self):
        """Получение профиля пользователя"""
        try:
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            if 'username' not in params:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Требуется параметр username'}).encode())
                return
            
            username = params['username'][0]
            users = self.db.get_record('rp', {'username': username})
            
            if not users:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Пользователь не найден'}).encode())
                return
            
            user = users[0]['fields']
            
            # Не возвращаем пароль
            user_profile = {
                'username': user['username'],
                'city': user.get('city', ''),
                'complaints': user.get('Complaints', '0')
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                'success': True,
                'user': user_profile
            }).encode())
        except Exception as e:
            logging.error(f"Error getting user profile: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def _handle_update_user(self, data):
        """Обновление данных пользователя"""
        try:
            required_fields = ['username', 'current_password', 'updates']
            for field in required_fields:
                if field not in data:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({'error': f'Отсутствует обязательное поле: {field}'}).encode())
                    return
            
            username = data['username']
            current_password = data['current_password']
            updates = data['updates']
            
            # Поиск пользователя и проверка текущего пароля
            users = self.db.get_record('rp', {'username': username})
            if not users:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Пользователь не найден'}).encode())
                return
            
            user = users[0]['fields']
            
            # Проверка текущего пароля
            if not self.security.verify_password(current_password, user['password']):
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'Неверный текущий пароль'}).encode())
                return
            
            # Подготовка обновлений
            update_data = {}
            if 'password' in updates and updates['password']:
                update_data['password'] = self.security.hash_password(updates['password'])
            
            if 'city' in updates and updates['city']:
                update_data['city'] = updates['city']
            
            if not update_data:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Нет данных для обновления'}).encode())
                return
            
            result = self.db.update_record('rp', {'username': username}, update_data)
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'Данные пользователя обновлены'
            }).encode())
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Многопоточный HTTP сервер"""
    daemon_threads = True

class ReviewServer:
    """Сервер для обработки отзывов о городах"""
    
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server = None
    
    def start(self):
        """Запуск сервера"""
        server_address = (self.host, self.port)
        self.server = ThreadedHTTPServer(server_address, RequestHandler)
        
        logging.info(f"Запуск сервера на {self.host}:{self.port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logging.info("Сервер остановлен пользователем")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка сервера"""
        if self.server:
            self.server.shutdown()
            logging.info("Сервер остановлен")

def run_server():
    """Запуск сервера"""
    # Добавьте отладочный вывод при запуске
    print("=" * 50)
    print("Запуск сервера Информатор...")
    print(f"Переменные окружения загружены:")
    print(f"  airtable_token: {'Да' if airtable_token else 'Нет'}")
    print(f"  base_id: {'Да' if base_id else 'Нет'}")
    if base_id and len(base_id) > 10:
        print(f"  base_id (первые 10 символов): {base_id[:10]}...")
    print("=" * 50)
    
    server = ReviewServer(host='0.0.0.0', port=8000)
    server.start()

if __name__ == '__main__':
    run_server()