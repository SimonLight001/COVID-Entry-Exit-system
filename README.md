# Location COVID 

This is a small project that picks up device count, and displays a screen that describes whether it is safe or not to enter.

This is updated every 5 seconds.

## Dependencies

Python3 (as well as pip of course)

Python packages:

These are all shown in the import list for each use case (I usually do this at the top of each file)

- requests
- pyjwt
- cryptography (a dependency of pyjwt)
- Flask

## How to run

Firstly, clone/download the git repo.

Then install Python 3 (if not done already).

Then we need to install the dependencies - `pip3 install requests pyjwt cryptography Flask`

This may require admin permissions - `sudo pip3 install requests pyjwt cryptography Flask`

Then navigate to the correct folder - `cd Location_COVID`

IT IS KEY TO RUN THE WEB SERVER FIRST!

Firstly start the web server with the command - `python3 web_server.py`

In another terminal or tab, run the application with - `python 3 index.py`

You will be asked to enter a token. This is done by adding a partner app to a spaces dashboard (can be added to the sandbox dashboard found on the partner site).

When creating a new application, its key that the application sends Device Count information, as well as simulation data is turned on if using a sandbox.

When the app is added to the dashboard, you will be asked to generate a token, this token can then be copied and pasted into the terminal.

Once this is done, the demo will validate the app (meaning it will now show as Active in the spaces dashboard).

The demo will then begin to send data around a location, showing how many users are in that spaces as well as if the space is safe to enter (current limit is hard set at 630, but looking to improve this).

To view the dashboard, navigate to your private IP (This can be found in wifi settings, or option click the wifi icon on a mac)

Here you can find a link to a video of me starting fresh and installing. (https://youtu.be/2YWrqjDHbFY)

This is done on a mac so should be similar experience for Linux, Windows of course may be slightly different.
