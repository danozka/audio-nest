import logging
import sys
from logging import Logger

from api.app import App
from container import Container


log: Logger = logging.getLogger(__name__)


if __name__ == '__main__':
    container: Container = Container()
    container.logging.init()
    log.info('Starting application...')
    try:
        app: App = App(container)
        app.run()
    except Exception as ex:
        log.error(f'Exception found while starting application: {ex}')
        sys.exit(1)
    finally:
        log.info('Application stopped')
