if __name__ == '__main__':
    from server.app import app
    app.run(host='0.0.0.0', port=8000, workers=4)
