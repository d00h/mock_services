from mock_services.api import create_app
from mock_services.config import MockServicesConfig as config

app = create_app()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
