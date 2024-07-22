# Watch Wave
Watch Wave is a backend REST API built with Flask that allows users to sign up, sign in, see a list of current movies and series, search for their favorite movies and series, add them to their watchlist, and mark them as watched or non-watched.

## Features
1. **User Authentication**
    - Sign up for a new account.
    - Sign in with an existing account.

2. **Movies and TV shows Management.**
    - View a list of current/popular movies and tv shows.
    - Search for movies and tv shows.

3. **Watchlist Management.**
    - Add movies or TV shows to own watchlist.
    - Mark items in watchlist as watched or non-watched.

## Getting Started
- Installation

```
git clone https://github.com/your-username/watch-wave.git
cd watch-wave
```

- Create and activate virtual environment

```
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

- Install Dependencies

```
pip install -r requirements.txt
```

- Set up the database

```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

- Run the application

```
Flask run
```