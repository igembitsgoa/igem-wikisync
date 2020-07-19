import logging

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console logger
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Create file logger
file_handler = logging.FileHandler('igemwiki-upload.log', mode='w')
file_format = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(funcName)s : %(message)s')
file_handler.setFormatter(file_format)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
