# run_server.py
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import ReviewServer
import logging

def main():
    """Запуск сервера"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Запуск сервера Информатор...")
        
        server = ReviewServer(host='0.0.0.0', port=8000)
        server.start()
        
    except Exception as e:
        logger.error(f"Ошибка запуска сервера: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()