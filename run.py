import uvicorn

from settings import DATABASES


def main():
    # инициализируем фабрику
    # db_session.global_init(**DATABASES)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    main()
