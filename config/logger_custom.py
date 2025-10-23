import logging

logger = logging.getLogger(__name__)  # cria logger para este módulo
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
