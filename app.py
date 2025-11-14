from app import create_app

# create app instance
app = create_app()

if __name__ == '__main__':
    # run in dev mode
    app.run(debug=True, host='0.0.0.0', port=5001)

