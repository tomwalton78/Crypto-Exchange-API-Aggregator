from api.api_server.api_server import app

# Run API server
app.run(host='0.0.0.0', port=80, debug=True)