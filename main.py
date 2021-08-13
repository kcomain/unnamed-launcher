import os
import logging

logging_mapping = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}
logging.basicConfig(
    format='[%(asctime)s %(levelname)s unnamed.%(module)s %(name)s thread %(thread)d] %(message)s',
    level=logging_mapping.get(os.environ.get('LOGGING', 'info'), logging.INFO)
)
logging.debug(f'current log level: {logging.root.level}')

# for some reason pyside _might_ be initializing another logger causing the above code to be as useful as padding
# sorry pep8
from unnamed.main import main

if __name__ == "__main__":
    main()
