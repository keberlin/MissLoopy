import logging

logger = logging.getLogger('missloopy')
logging.basicConfig(format='%(asctime)-15s %(message)s', filename='/var/log/missloopy/log', level=logging.DEBUG)
