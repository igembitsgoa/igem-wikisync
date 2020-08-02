import logging

# LEVELS

# CRITICAL: Failed to login / SystemExit worthy
# ERROR:    Failed to connect
# Invalid credentials
# Coudln't upload
# Filename too large
# File too large
# Unsupported filetype
# Couldn't read/write file
# WARNING:  File not found/broken link
# INFO:     Uploaded
# Changed URL
# Logged in


# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console logger
console_handler = logging.StreamHandler()
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)
console_handler.setLevel(logging.WARNING)
logger.addHandler(console_handler)

# Create file logger
file_handler = logging.FileHandler('wikisync.log', mode='w')
file_format = logging.Formatter('%(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
file_handler.setFormatter(file_format)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
