### Install Vagrant
Download and install from here: [http://www.vagrantup.com/downloads](http://www.vagrantup.com/downloads)

    $ cd tecnocial
    $ vagrant up
    $ vagrant ssh # You're now inside the VM.

### Compile styles

    $ vagrant ssh
    $ cd tecnocial
    $ grunt less # grunt watch to keep polling for changes

### Run django
    $ vagrant ssh
    $ workon tecnocial
    $ cd tecnocial/src
    $ python manage.py runserver 0.0.0.0:8000 # Now you can open your browser
                                              # and go to localhost:8000
![http://reactiongifs.me/wp-content/uploads/2013/08/shia-labeouf-magic-gif.gif](http://reactiongifs.me/wp-content/uploads/2013/08/shia-labeouf-magic-gif.gif)