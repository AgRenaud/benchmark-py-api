


```bash
/ #root
├─ opt/
│  ├─ src/ # Application source code
│  ├─ venv/ # Application's python virtualenv
├─ /
├─ run/ # Application sockets
├─ etc/ 
│  ├─ apache2/ # Application Apache2 configuration files
│  ├─ nginx/   # Application Nginx configuration files
│  ├─ systemd/ # Application Service files
```

To run a benchmark, first ensure that all the service are shutdown.
```bash
sudo -u theuser systemctl ...
```  

Then run the following depending on your service to bench


```
sudo systemctl 
```