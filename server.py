from web_app import WebApp

if __name__ == "__main__":
    app = WebApp()

    # Start server to listen on some port
    app.start_server()
    app.run()