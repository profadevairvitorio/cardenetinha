import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=os.environ.get('APPLICATION_HOST'),
        port=os.environ.get('APPLICATION_PORT'),
        debug=os.environ.get('APPLICATION_DEBUG')
    )