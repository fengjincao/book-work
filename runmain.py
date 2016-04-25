# -*- coding: utf-8 -*-

from bookhouse.main import create_app_main

app = create_app_main()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
