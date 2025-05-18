import logging
from logging import Logger

from app import App
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
        log.error(f'Exception found while running application: {ex}')
    finally:
        log.info('Application stopped')
        logging.shutdown()
