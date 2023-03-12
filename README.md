# Keebo

Keebo a small python utility for analyzing your keyboard habits. It keeps track of the keys you press and produces a summary of how many times you pressed each key.

I wrote Keebo because I was curious about which keys I used the most and which ones I didn't use at all.

## Usage

Start the db (requires docker/podman-compose)
```
podman-compose up -d
```

Then start keebo (assuming you're in a virtualenv and have installed the requirements)
```
sudo python src/keebo.py
```

## Gotcha

- Keebo requires to be run with `sudo` in order to be able to listen to key press.
- It was only tested to work on Linux.
- Keebo is not a keylogger, it only stores the count of the key presses for each key (nonetheless it's a good habit to be mindful when typing passwords and other sensitive stuff).
- The database is not thought to be used anywhere else than your local machine. It's unsecure by design and it shouldn't be used in production. 
