[Return to Documentation home](/README.md)

# Running the Server
**These are the instructions to start your own instance of the server for this site. This is NOT NECESSARY for use unless you want to create a new instance with your own stored data. (Judges should not need to use this.)**

## Clone
1. Clone this repository.
2. Navigate to the project directory.

## Database
1. Create a MongoDB database.
2. Copy the connection URI (`mongodb://...` or `mongodb+srv://...`).
3. Set the `DB_URI` environment variable to your connection URI.

## Secret Key
1. Generate a secure secret key for the app.
2. Set the `SECRET_KEY` environment variable to your secret key.

## Start
1. Run the app with `python3 main.py`.