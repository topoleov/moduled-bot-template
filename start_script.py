# -*- coding: utf-8 -*-
import logging


def main():
    print('hello')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
