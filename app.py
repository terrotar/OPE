
from app import create_app, config


app = create_app(config)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)
