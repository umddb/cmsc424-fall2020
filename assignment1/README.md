# Assignment 1: Computing Environment

Over the course of the semester, you will work with a variety of software packages, including PostgreSQL, Apache Spark, Python Django, and others. Installing those
packages and getting started can often be a hassle, because of software dependencies. You have two choices.

* Install the different software packages on your own machine (most of these packages should have tutorials to install them on different OSs). If you have a Linux box or a Mac, this should be possible; it may be more difficult with Windows. In any case, although we will try our best, we would likely not be able to help you with any problems.
* (**Preferred Option**) Use Vagrant with Virtual Box (as discussed below). If you have a reasonably modern machine (within last 3-4 years), VirtualBox should generally work fine, but with older laptops, the performance may not be as good. See below for more details on this.

---

### Git & Github

Git is one of the most widely used version control management systems today, and invaluable when working in a team. GitHub is a web-based hosting service built around git --
it supports hosting git repositories, user management, etc. There are other similar services, e.g., bitbucket.

We will use GitHub to distribute the assignments, and other class materials. Our use of git/github for the class will be minimal; however, we encourage you to use it for
collaboration for your class project, or for other classes. 

#### Just Cloning the Class Repository
You don't need a GitHub account for just cloning the class repository. Just do:

`git clone https://github.com/umddb/cmsc424-fall2020.git`

You can do `git pull` (from within the `cmsc424-fall2020` directory) to fetch the newly added material. 

*NOTE*: If you are having trouble installing `git`, you can just download the files instead (as a zipfile), although updating may become tedious. 

#### Setting up a GitHub Account 
Repositories hosted on github for free accounts are public; however, you can easily sign up for an educational account which allows you to host 5 private repositories. More
details: https://education.github.com/

- Create an account on Github: https://github.com
- Generate and associate an SSH key with your account
    - Instructions to generate SSH Keys: https://help.github.com/articles/generating-ssh-keys#platform-linux
        - Make sure to remember the passphrase
    - Go to Profile: https://github.com/settings/profile, and SSH Keys (or directly: https://github.com/settings/ssh)
    - Add SSH Key
- Clone the class repository:
    - In Terminal: `git clone git@github.com:umddb/cmsc424-fall2020.git`
    - The master branch should be checked out in a new directory 
- Familiarize yourself with the basic git commands
    - At a minimum, you would need to know: `clone`, `add`, `commit`, `push`, `pull`, `status`
    - But you should also be familiar with how to use **branches**
- You can't push to the main class repository, but feel free to do *pull requests* on the main class repository if you spot any errors or if you think something could be improved.

---

### Vagrant + Virtual Box

[Virtual Box](https://www.virtualbox.org/) is a virtualization software package (similar to VMWare or Parallels), which allows you to construct and run virtual machines on your computer. [Vagrant](https://www.vagrantup.com/) enables users to create and configure lightweight, reproducible, and portable development environments using VirtualBox. We will provide `VagrantFiles` for different assignments, that will help you start the VMs with the requisite packages installed.

- In order to use this option, you have to first install Vagrant and VirtualBox on your machine (called `Host` henceforth). See the instructions on the two websites above to do that.
- Vagrant makes things **super-easy**. We will provide you with appropriate setup files -- all you need to do is `vagrant up` to start the virtual machine.
- More specifically: in the git sub-directory `assignment1`, run `vagrant up`. This will start the virtual machine in the background. 
- By default, vagrant only provides **ssh** access into the virtual machine (called `Guest VM` henceforth), using `vagrant ssh`. This will work as if you are doing `ssh` into a remote machine.
- The Guest VM will have access to the files in the current directory in the host machine (i.e., the files in the `assignment1` directory and its subdirectories). These are mounted in the guest VM at `/vagrant`. It would be best if you only make edits to that directory -- since those edits will survive a `vagrant destroy`. In fact, you can continue using your favorite text editor (in the host machine) to edit files, and only use the VM for running specific programs (like `postgres`, `psql`, or `ipython notebook` below).
- If the Guest VM has a program (e.g., a Web Server) running and listening on a specific port (e.g., 80), you can access those ports from the host machine by adding them to the `VagrantFile`. The provided VagrantFile has two such mappings: for port 8888, used by iPython (mapped to port 8888 on the host machine), and for port 80, used by a Web server (mapped to port 8080 on the host machine).
- If you just exist `ssh`, then the VM continues running in the background.
- Some other vagrant commands that you would need to be familiar with:
    - `vagrant destroy`: will remove all traces of the guest machine from your system. It'll stop the guest machine, power it down, and remove all of the guest hard disks. Any data stored on the VM will be deleted (except in `/vagrant/`). When you are ready to work again, just do `vagrant up`.
    - `vagrant suspend`: will save the current running state of the machine and stop it. When you do `vagrant up` again, it will restart with that state.
    - `vagrant halt`: will shutdown the machine.

- You now have a virtual machine with PostgreSQL, Python 3, Jupyter notebooks and the required dependencies completely setup. To access them, simply `ssh` into your virtual machine by using `vagrant ssh` and running the required commands (listed in the following sections).

---

### PostgreSQL

PostgreSQL is a full-fledged and powerful relational database system, and will be used for several assignments. 

PostgreSQL is already installed on your virtual machine. To get started, start the virtual machine using `vagrant up`. 

The current version of PostgreSQL is 12.1. However, the version installed on the VMs is 10.10, the one available through `apt-get` right now. You will find the detailed documentation at: https://www.postgresql.org/docs/10/index.html

Following steps will get you started with creating a database and populating it with the `University` dataset provided on the book website: http://www.db-book.com

* You will be using PostgreSQL in the client-server mode. Recall that the server is a continuously running process that listens on a specific port (the actual port would differ, and you can usually choose it when starting the server). In order to connect to the server, the client will need to know the port. The client and server are often on different machines, but for you, it may be easiest if they are on the same machine (i.e., the virtual machine). 

* Using the **psql** client is the easiest -- it provides a command-line access to the database. But there are other clients too, including a GUI (although that would require starting the VM in a GUI mode, which is a bit more involved). We will assume **psql** here. If you really want to use the graphical interfaces, we recommend trying to install PostgreSQL directly on your machine.

* Important: The server should be already started on your virtual machine -- you do not need to start it. However, the following two help pages discuss how to start the
   server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html) and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

* PostgreSQL server has a default superuser called **postgres**. You can do everything under that username, or you can create a different username for yourself. If you run a command (say `createdb`) without any options, it uses the same username that you are logged in under (i.e., `vagrant`). However, if you haven't created a PostgreSQL user with that name, the command will fail. You can either create a user (by logging in as the superuser), or run everything as a superuser (typically with the option: **-U postgres**).

* For our purposes, we will create a user with superuser privileges. 
	```
	sudo -u postgres createuser -s vagrant
	```

* After the server has started, the first step is to **create** a database, using the **createdb** command. PostgreSQL automatically creates one database for its own purpose, called **postgres**. It is preferable you create a different database for your data. Here are more details on **createdb**: 
   http://www.postgresql.org/docs/current/static/tutorial-createdb.html

* We will create a database called **university**.
	```
	createdb university
	```
* Once the database is created, you can connect to it. There are many ways to connect to the server. The easiest is to use the commandline tool called **psql**. Start it by:
	```
	psql university
	```
	**psql** takes quite a few other options: you can specify different user, a specific port, another server etc. See documentation: http://www.postgresql.org/docs/current/static/app-psql.html

* Note: you don't need a password here because PostgreSQL uses what's called `peer authentication` by default. You would typically need a password for other types of connections to the server (e.g., through JDBC).

Now you can start using the database. 
    
   - The psql program has a number of internal commands that are not SQL commands; such commands are often client and database specific. For psql, they begin with the
   backslash character: `\`. For example, you can get help on the syntax of various PostgreSQL SQL commands by typing: `\h`.

   - `\d`: lists out the tables in the database.

   - All commands like this can be found at:  http://www.postgresql.org/docs/current/static/app-psql.html. `\?` will also list them out.

   - To populate the database using the provided university dataset, use the following: `\i DDL.sql`, followed by 
	   ```
	   \i smallRelationsInsertFile.sql
	   ``` 

   - For this to work, the two .sql files must be in the same directory as the one where you started psql. The first command creates the tables, and the
   second one inserts tuples in it. 
	
   - Create a different database ```university_large``` for the larger dataset provided (`largeRelationsInsertFile.sql`). Since the table names
   are identical, we need a separate database. You would need this for the reading homework.

---

### Python and Jupyter/IPython

We will be using Python for most of the assignments; you wouldn't typically use Python for systems development, but it works much better as an instructional tool. Python is easy to pick up, and we will also provide skeleton code for most of the assignments. 

IPython is an enhanced command shell for Python, that offers enhanced introspection, rich media, additional shell syntax, tab completion, and rich history. 

**IPython Notebook** started as a web browser-based interface to IPython, and proved especially popular with Data Scientists. A few years ago, the Notebook functionality was forked off as a separate project, called [Jupyter](http://jupyter.org/). Jupyter provides support for many other languages in addition to Python. 

* Start the VM using `vagrant up`. Python, IPython, and Jupyter are already loaded.

* To use Python, you can just do `python` (or `ipython`), and it will start up the shell.

* To use Jupyter Notebook, do `cd /vagrant` followed by: 
	```
	jupyter-notebook --port=8888 --no-browser --ip=0.0.0.0
	``` 
This will start a server on the VM, listening on port 8888. We will access it from the **host** (as discussed above, the VagrantFile maps the 8888 port on the guest VM to the 8888 port on the host VM). To do that, simply start the browser, and point it to: http://127.0.0.1:8888

* You should see the Notebooks in the `assignment1/` directory. Click to open the "Jupyter Getting Started" Notebook, and follow the instruction therein.

* The second Notebook ("Basics of SQL") covers basics of SQL, by connecting to your local PostgreSQL instance. The Notebook also serves as an alternative mechanism to run queries. However, in order to use that, you must set up a password in `psql` using `\password` (set the password to be `vagrant`).

#### Common errors / FAQs

Q. Hyper-V error while running `vagrant up`. (Stderr: VBoxManage.exe: error: Not in a hypervisor partition (HVP=0) (VERR\_NEM\_NOT\_AVAILABLE).)

  * Hardware virtualization is often not enabled by default. Enable virtualization in your system. You can follow instructions listed [here](https://www.howtogeek.com/213795/how-to-enable-intel-vt-x-in-your-computers-bios-or-uefi-firmware/).

Q. Can't find jupyter / python / psql.

  * Please ensure that you are running the command after you ssh into your vagrant box using `vagrant ssh`.