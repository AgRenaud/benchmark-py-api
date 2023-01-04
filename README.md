# Benchmark Py-API

In this project you'll find several production like implementation of a simple Veterinary service.

The project aim to bench several proxy, web-server, application configuration in python.

# Running a Benchmark 

> **Requirements**
> - [Vagrant](https://www.vagrantup.com/) (With vagrant scp `vagrant plugin install vagrant-scp`)
> - [Poetry](https://python-poetry.org/) (with [multi-project plugin](https://pypi.org/project/poetry-multiproject-plugin/))
> - [VirtualBox](https://www.virtualbox.org/)

## Setting Up VM
After running the following command, you'll have Virtual machine up for the benchmark.
The initial VM has 2 CPU cores and 2048 MB of memory

To start with the installation you'll want to build the archive or `wheel` for the application to test with `poetry build-project` command.
```shell
poetry env use </path-to-your-python-exe>
poetry install
poetry shell

cd flask-example && poetry build-project
cd ..
cd fastapi-example && poetry build-project
cd ..

vagrant up # The provision script need the above command to be executed
```
The virtual Machine has a user Bench that you will use to install the applications.
Here is how the file system will be used:

```bash
/ #root
├─ home/
│  ├─ bench/ # we will put application wheel here
├─ opt/
│  ├─ src/ # Applications config files (.wsgi files)
│  ├─ venv/ # Application's python virtualenv
├─ etc/ 
│  ├─ apache2/ # Apache2 configuration files
│  ├─ nginx/   # Nginx configuration files
│  ├─ systemd/ # Service files
│  ├─ hosts # DNS configuration
├─ run/ # Application sockets
├─ var/ # Application storage (sqlite)
```

Now that everything is ready, we'll install the services for the different configuration we want to test.


## Setting up applications
Now we've got the minimal files to create all our needed configuration at `/home/bench` in the VM.

For each of the below configurations we will create a python virtualenv and the required configuration files.

```bash
vagrant ssh

su -l bench # password: bench
python --version # Make sure you are using python 3.10.4
```

> When needed make sure the required modules are installed for `apache2` :
> - mod_proxy: `sudo a2enmod proxy proxy_http`

### flask-example
#### flask-mod-wsgi (`Apache` + `mod_wsgi`)

First you need to make sure that `mod_wsgi` is installed for the python version of the application (`3.10`).

```sh
sudo apt-get install apache2-dev

./setup.sh flask-mod-wsgi
python -m venv /opt/venv/flask-mod-wsgi # Make sure you're using python3.10
source /opt/venv/flask-mod-wsgi/bin/activate
pip install /home/bench/dist/flask_example-0.1.0-py3-none-any.whl
pip install mod_wsgi # activate your python 3.10

sudo /opt/venv/flask-mod-wsgi/bin/mod_wsgi-express install-module | sudo tee /etc/apache2/mods-available/wsgi.load

sudo a2enmod wsgi
sudo service apache2 restart
```

Then write a `.wsgi` configuration file :

```
cd /opt/src/flask-mod-wsgi/
touch application.wsgi
```
```python
# /opt/src/flask-mod-wsgi/application.wsgi
from flask_example.client import create_application

application = create_application()
```

Then we'll create a virtual host for the application...

`sudo vim /etc/apache2/sites-available/flask-mod-wsgi.conf`
```apache
<VirtualHost *:80>
    ServerName flask-mod-wsgi.app

    WSGIDaemonProcess flask-mod-wsgi\
        user=bench\
        group=bench\
        python-home=/opt/venv/flask-mod-wsgi

    WSGIScriptAlias / /opt/src/flask-mod-wsgi/application.wsgi

    <Directory /opt/src/flask-mod-wsgi>
        WSGIProcessGroup flask-mod-wsgi
        WSGIApplicationGroup %{GLOBAL}
        
        Require all granted
    </Directory>

</VirtualHost>
```

Now you can enable it with `sudo a2ensite flask-mod-wsgi.app`

...and configure the proxy in order to expose the service outside the VM.

Add the following line to `/etc/apache2/sites-available/000-default.conf`
```apache
<VirtualHost *:80>
    ...
    ProxyPreserveHost On
    ProxyPass        "/bench" "http://flask-mod-wsgi.app/"
    ProxyPassReverse "/bench" "http://flask-mod-wsgi.app/"
    ...
<VirtualHost/>
```
and add this line to `/etc/hosts`
```
127.0.0.1   flask-mod-wsgi.app
```

And restart apache with `sudo systemctl restart apache2` and everything is ready !


You'll notice in the chart below that the server does not need a service manager like `systemd`.
`apache2` and `mod_wsgi` manage the WSGI server.

```mermaid
flowchart TB

    subgraph VM
        Proxy["Proxy (Apache2)"] --> VirtualHost["VirtualHost (Apache2)"]
        VirtualHost --> WSGIServer["WSGI Server (mod_wsgi)"]
        WSGIServer --> |call| Application["Application"]

    subgraph Web server
        Proxy
        VirtualHost
    end
    subgraph Application server
        WSGIServer
        Application
    end
    end
```

#### flask-a2 (`Apache` + `gunicorn`)
For this example, setting up the application will be easier since the WSGI configuration can remains the same for this example and `nginx + gunicorn` example. That's because application is completely decoupled from proxy.

```bash
source /opt/venv/flask-a2/bin/activate
pip install /home/bench/dist/flask_example-0.1.0-py3-none-any.whl
pip install gunicorn
```

```mermaid
flowchart TB
    subgraph VM
        Proxy["Proxy (Apache2)"] --> |redirect| Socket["Application Socket"]
        WSGIServer["WSGI Server (Gunicorn)"] --> |listen| Socket
        WSGIServer --> |call| Application

    ServiceManager["systemd"] -.-> |manage| WSGIServer

    subgraph Web server
        Proxy
    end

    subgraph Application server
        WSGIServer
        Application
    end

    end
```

#### flask-nginx (`Nginx` + `gunicorn`)

```bash
source /opt/venv/flask-nginx/bin/activate
pip install /home/bench/dist/flask_example-0.1.0-py3-none-any.whl
pip install gunicorn
```

```mermaid
flowchart TB
    subgraph VM
        Proxy["Proxy (Apache2)"] --> |redirect| Socket["Application Socket"]
        WSGIServer["WSGI Server (Gunicorn)"] --> |listen| Socket
        WSGIServer --> |call| Application

        ServiceManager["systemd"] -.-> |manage| WSGIServer

        subgraph Web server
            Proxy
        end

        subgraph Application server
            WSGIServer
            Application
        end
    end
```

### fastapi-example
#### fastapi-a2 (`Apache`  + `gunicorn` + `uvicorn`)
```bash
source /opt/venv/fastapi-a2/bin/activate
pip install /home/bench/dist/fastapi_example-0.1.0-py3-none-any.whl
pip install gunicorn
```

```mermaid
flowchart TB
    subgraph VM
        Proxy["Proxy (Apache2)"] --> |redirect| Socket["Application Socket"]
        WSGIServer["WSGI Server (Gunicorn)"] --> |listen| Socket
        WSGIServer --> |call| ASGIServer["ASGI Server (Uvicorn)"]
        ASGIServer --> |call| Application

        ServiceManager["systemd"] -.-> |manage| WSGIServer

        subgraph Web server
            Proxy
        end

        subgraph Application server
            WSGIServer
            ASGIServer
            Application
        end
    end
```

#### fastapi-nginx (`Nginx`  + `gunicorn` + `uvicorn`)
```bash
source /opt/venv/fastapi-nginx/bin/activate
pip install /home/bench/dist/fastapi_example-0.1.0-py3-none-any.whl
pip install gunicorn
```

```mermaid
flowchart TB
    subgraph VM
        Proxy["Proxy (Nginx)"] --> |redirect| Socket["Application Socket"]
        WSGIServer["WSGI Server (Gunicorn)"] --> |listen| Socket
        WSGIServer --> |redirect| ASGIServer["ASGI Server (Uvicorn)"]
        ASGIServer --> |run| Application

        ServiceManager["systemd"] -.-> |manage| WSGIServer

        subgraph Web server
            Proxy
        end

        subgraph Application server
            WSGIServer
            ASGIServer
            Application
        end
    end
```
