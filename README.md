# Spotify to YouTube Music Playlist Migration Tool

Welcome to the Spotify to YouTube Music Playlist Migration Tool, a project designed to seamlessly transfer playlists from Spotify to YouTube Music using Python.

## Introduction

This project serves as an educational endeavor to explore the functionalities of Spotify's API and YouTube Music's API while honing Python skills. Although still in its developmental phase, the tool currently offers the following features:

- **Spotify Authentication**: Securely authenticates with Spotify.
- **Playlist Retrieval**: Fetches all user playlists from Spotify, including public, private, and collaborative ones.
- **Local Storage**: Stores playlists locally in a pickled migrator object for seamless migration.
- **YouTube Authentication**: Authenticates with YouTube for playlist migration.
- **Migration Process**: Transfers playlists from Spotify to YouTube Music, attempting to maintain song order and state across runs.
- **Song Selection Algorithm**: Utilizes a rudimentary algorithm to search YouTube Music for songs, based on the song and artist name.
- **State Management**: Capable of resuming from failures or interruptions by storing and retrieving current migration state locally.

## Dependencies

This project is managed using Poetry. To install the necessary dependencies, run:

```bash
poetry install
```

## Authentication

### Spotify

To use the Spotify implementation, you need to obtain access credentials for your application following the steps documented [here](https://spotipy.readthedocs.io/en/2.22.1/#authorization-code-flow). Prior to running the script, set the following environment variables:

```bash
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

### YouTube

For YouTube Music, follow the steps outlined [here](https://ytmusicapi.readthedocs.io/en/stable/setup/oauth.html) to authorize your application for OAuth use. This will generate an **oauth.json** file, which the code references. Run the following command once:

```bash
ytmusicapi oauth
```

To execute the script, use:

```bash
python main.py
```

## State Management and Retries

The project is designed to resume from failure or interruption by storing the current state in a pickled file locally. It operates in two states:

- **State: None**: Playlist metadata needs to be fetched from Spotify. The script won't proceed until all playlists are processed in a single run.
- **State: Populated**: Spotify playlists are saved, and migration is underway. If errors occur, they are logged, and migration failures are recorded.

To delete the state, remove the `migrator_data.db` file.

## Known Limitations

- Due to differences between Spotify and YouTube Music, a 1:1 mapping isn't guaranteed.
- The song selection algorithm may not be optimal for all cases, but it works for most scenarios.
- YouTube Music has playlist creation limits, which may affect the migration process.

## Development

Development tasks are managed with Poetry:

- Run code formatter (Black):

```bash
poetry run black .
```

- Run type check (PyType):

```bash
poetry run pytype
```

- Run tests (pytest):

```bash
poetry run pytest
```

- Run autoflake (removes unused imports):

```bash
autoflake --remove-unused-variables --remove-all-unused-imports --in-place --recursive service dao model adaptor tests
```

Feel free to reach out with questions or contribute through pull requests for new features or improvements. Your feedback is highly valued.