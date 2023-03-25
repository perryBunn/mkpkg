import logging

# If the logger is not set in the main program don't log anything
logging.getLogger(__package__).addHandler(logging.NullHandler())