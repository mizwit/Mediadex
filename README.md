# Mediadex

**Mediadex** is a personal movie-tracking web application built using Django, HTML5/CSS3, JavaScript, Bootstrap, and The Movie Database (TMDB) API. It allows users to:
- Create an account, log in, and manage their profile.
- Search for movies using the TMDB API.
- View detailed information about a movie.
- Organize movies into personal collections: **Watched**, **Watchlist**, and **Favorites**.
- Sort and browse these collections based on metadata like release date, popularity, and rating.

## Installation
To run this project locally, follow these steps:

1. Clone the project and move into the project folder
```bash
git clone https://github.com/manasauriz/Mediadex.git
cd Mediadex
```

2. Set Up the `.env` File. In the root directory, create a file named `.env` with the following contents:
```env
DEBUG=on
SECRET_KEY=your-secret-key
TMDB_API=your-tmdb-api-key
ADMIN_NAME=admin-name
ADMIN_EMAIL=admin-email
EMAIL_HOST=smtp-domain-name
EMAIL_HOST_USER=your-sender-email
EMAIL_HOST_PASSWORD=your-sender-password
```
- You can generate a Django secret key using online tools.
- Sign up for a TMDB account and generate an API key.
- Error notifications will be sent to Admin Name and Email
- Use your SMTP provider's credentials for sending emails

3. Execute Build Commands
```bash
./build.sh
```

4. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

5. Run the Server and visit the app on your browser
```bash
python manage.py runserver  # Development Server
```
```bash
gunicorn Mediadex.wsgi:application  # Production Server
```

## Acknowledgements

The concept and design of Mediadex draws inspiration from existing media tracking platforms, namely **Letterboxd** and **Serializd**.

This project makes use of several public services:
- **TMDB API** – for fetching movie data.
- **Bootstrap Icons** – for UI icons throughout the site.
- **Google Fonts** – specifically the Audiowide font.

**ChatGPT** was used throughout the project for the following:
- Designing visual assets like the logo, favicon, and error images.
- Assisting in bug resolution and providing code suggestions.
- Proofreading documentation, including this README.