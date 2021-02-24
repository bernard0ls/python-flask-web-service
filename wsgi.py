from application import init_app
import os

app = init_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=port)
