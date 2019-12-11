# leetcode-reminder-bot

## Setup

### Forking and cloning

Fork the repository (https://help.github.com/en/github/getting-started-with-github/fork-a-repo). A fork is a personal copy of the repository.

Go to your repositories and clone your fork of this repository (https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository). Cloning is synonymous with downloading in this context.

### Configuring the Facebook API

Navigate to the root directory for the project, `leetcode-reminder-bot`. Create a copy of `secret_example.yaml` called `secret.yaml`.

#### Page Access Token

1. Navigate to https://developers.facebook.com/.
2. Go to `My Apps` (top-right) and click on `Leetcode Reminder Bot`.
3. On the left panel under `Products`, click on `Messenger` and then `Settings`.
4. Now focusing on the center of the page, scroll down to the section titled `Access Tokens`.
5. Hit `Generate Token`. In `secret.yaml`, for `PAGE_ACCESS_TOKEN: Get_From_FB_API` replace `Get_From_FB_API` with the token. Don't close this page, we'll return to it shortly.

#### `ngrok` Part 1 / 2

1. Download `ngrok` from https://ngrok.com/download.
2. Open a separate terminal window and navigate to where the `ngrok` program is. Run `./ngrok http 5000`, which will run `ngrok` continuously. We'll return to this after the next section.

#### Run them jewels fast, run them, run them jewels fast

We're going to fucking it run it now.

1. Make sure you have Python 3.6.8 installed.
2. Go back to the root of the directory.
3. Run `pip3 install -r requirements.txt` to install the requirements.
4. Run `python3 app.py`.

Leave it running in the background

#### `ngrok` Part 2 / 2

1. In `secret.yaml`, for `VERIFY_TOKEN: Made_Up_Phrase_You_Set_In_The_FB_API_When_You_Set_Your_Endpoint`, replace the filler string with your token.
2. Go back to the terminal running `ngrok`. The output should expose a URL, for example `Forwarding http://d59cf242.ngrok.io -> http://localhost:5000`. COPY THE `HTTPS` URL NOT THE `HTTP` URL (they're basically identical but only https will work).
3. Go back to the FB Dev page you were on. Directly below the `Access Tokens` section should be the `Webhooks` section.
4. Hit `Edit URL` and paste your exposed URL, such as `https://dbf2d510.ngrok.io` into the `Callback URL` field. In the `Verify Token` field, make up some token, e.g. `AndrewLiIsBetterThanAndrewDing`. Save.

What's happening here is you're exposing an IP, which should be `5000` (remember `http://localhost:5000` from the `ngrok` output?) by default, for external access, however this is IP is local and can only be used internally on your computer. `ngrok` forwards or maps that IP to a random URL owned by their company, such as `http://d59cf242.ngrok.io`, which can be accessed externally by people, such as Facebook.

### Setting Up the Database

We need a database to store our users.

#### Homebrew

Navigate to https://brew.sh/ and read about Homebrew, I'm too lazy to explain it lol. Follow the installation steps in a new terminal window. We need this to install some shit.

#### Postgresql

`Postgres`, `psql`, `postgresql`, or whatever the fuck you want to call it is a kind of database management system, similar to `MySQL` for example. Run `brew install postgresql` to install it.

#### Bash Aliases

What is an `alias`? If you find yourself typing the same long ass command a million times, you can make an `alias` that runs the command, which saves you time. For example, `alias run-that-shit='python3 main.py --arg1 flag1 --arg2 flag2 --arg420 flag420'` means you can run `run-that-shit` instead of `python3 main.py --arg1 flag1 --arg2 flag2 --arg420 flag420`. Time. Saved.

Use `emacs` or `vi` to edit your `~/.bashrc` file to contain the following lines:

```
alias psql-start='pg_ctl -D /usr/local/var/postgres start'
alias psql-stop='pg_ctl -D /usr/local/var/postgres stop'
```

Run `psql-start` to start postgres. It runs in the backgorund until you run `psql-stop`.

#### Docker

In a nutshell, have you ever run something your personal laptop and had it work and then had it fail on a school lab machine because of a different operating system? `docker` allows us to run a "containerized environment", which means you can specify the operating system and versions of technology you are using, ensuring that the same code works across different machines.

1. Run `brew install docker docker-compose docker-machine xhyve docker-machine-driver-xhyve` to install `docker` and friends.
2. Install Docker Desktop from here: https://www.docker.com/products/docker-desktop.
3. Run Docker Desktop (probably just called Docker in your applications) and wait for its status to change to "Running" which can monitored from the drop down from clicking on the whale on the OS X task bar.

#### Configuring PSQL

1. Open a new terminal window and navigate to `leetcode-reminder-bot/pg`.
2. Run `docker-compose up -d`. This uses the `docker-compose.yaml` file to create a new container running a PSQL image specified to run version 10 on port 5433 with username `admin` and password `password`. This is only available locally, so it's not a security threat.
3. Run `./seed-db.sh` to create the appropriate columns and rows in the database.
4. Download http://www.psequel.com/. To connect to the database, `Host` should be `localhost`, `User` should be `admin`, `Password` should be `password`. `Database` should be `postgres`. `Port` should be `5433` `Use SSL`and `Use SSH Tunneling` should both be unchecked. Connect and take a look around.

#### Testing

Open Facebook messenger from your phone. You can't do it from the desktop version because you're an admin for the page and if you try to message the page, it just logs you in as the page. Message `Leetcode Reminder Bot` from your phone.

### Saving changes

Run `git add .` to add to current commit.

Run `git commit -m "message describing change here"` to stage change.

Run `git push` to push changes to GitHub.

Holy shit we're done. Finish my side-project now, Leah!
