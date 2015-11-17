---------------------------------------------------------
Journalling Trial for LAS CoyWolf team
Setup Instructions, last updated by PJ/PMS Jul 25th, 2015
Any problems, e-mail pjones@ncsu.edu
---------------------------------------------------------

------------------ INSTALLATION ------------------

* Install Chrome - download and install from: google.com/chrome
* Install Chrome Journaling plugin:
** Go to 'https://las-skylr.oscar.ncsu.edu/#/' and click 'Chrome Extension'
** In the browser, select Settings, Extensions, and drag the extension onto the page.

*** NOTE REQUIREMENT TO BE LOGGED INTO SHIBBOLETH, OTHERWISE YOU'LL SEE 'ERR' STATUS ON EXTENSION!

* Install OSXInstrumenter v0.4.5 or newer, from e-mail or posting in LAS-G group.

* Install other pre-requisites:

(from brew.sh)
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install wget

$ brew install tag
$ sudo easy_install pip

* Unpack the tarball provided by e-mail in your home directory:
$ cd ~; tar xvzf dashboard-osx.tgz
$ cd dashboard-osx
$ sudo pip install -r requirements.txt

* Add your Unity ID to your environment - open ~/.bashrc and add a line similar to:
export UNITYID=<my_unity_id>

* Ensure that your .bashrc file gets sourced every time bash is started - add this line to ~/.bash_profile (create this file if it doesn't exist):
[[ -s ~/.bashrc ]] && source ~/.bashrc

--------------------- TO RUN ---------------------

* Start the dashboard server from OSXInstrumenter (recommended), or manually using:
$ python ./server.py

* Go to localhost:5000 in Chrome and make sure your dashboard is displaying a welcome message (including your UnityID).

----------------- WHILE WORKING -------------------

* Please record as many goal tags on files and URLs as you can.
* Set the dashboard as your Chrome home page.
* When opening the browser, go to a Shiboleth-enabled page to clear the Extension ERR message!
* Download and view as many course files from within the Ubuntu VM as possible.

* View your events here: 'https://las-skylr.oscar.ncsu.edu/#/query' and select your UserId.

------------------ FEEDBACK ------------------------

* E-mail pjones@ncsu.edu with any bugs/issues.

* Submit feedback and questions on the whole process and the dashboard, through the CoyWolf Yammer group.
