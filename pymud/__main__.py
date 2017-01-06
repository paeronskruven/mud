from . import core


def main():
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s'
    )

    core.server.run()

if __name__ == '__main__':
    main()
