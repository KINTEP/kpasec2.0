from app import app
import os


if __name__ == '__main__':
	server = int(os.environ.get("PORT", 8080))
	#app.run(host="0.0.0.0", port=server)
	app.run(debug=True, host="0.0.0.0", port=server)