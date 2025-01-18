# DataTalks

## Generate private + public SSH keys
```bash
cd
mkdir .ssh
ssh-keygen -t rsa -f gcp -C jsrl
```

## Adding public key to GCP
Go to **Compute Engine -> Metadata -> SSH keys**

## Creating VM Instance
- **Name**: Specify a name
- **Region**: Choose your region
- **Machine-type**: e2-standard-4
- **OS**: Ubuntu
- **Disk**: 30GB

## Connecting via external IP
```bash
ssh -i ~/.ssh/gcp jsrl@external_ip
htop
gcloud --version
```

## Installing Conda on the instance
```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
```

## Local - Accessing easily via SSH
```bash
cd .ssh
touch config
```
Add the following content to `config`:
```plaintext
Host de-zoomcamp
    HostName external_ip
    User jsrl
    IdentityFile C:/Users/Home/.ssh/gcp
```
Connect via shorthand:
```bash
ssh de-zoomcamp
```

## Once Anaconda is installed
```bash
(base) which python
sudo apt-get update
sudo apt-get install docker.io
docker hello-world # (Permissions required)

sudo groupadd docker
sudo gpasswd -a $USER docker # Avoid using sudo with Docker
sudo service docker restart # Relogin required
docker hello-world # Should work
docker run -it ubuntu bash
```

## Install Docker Compose
```bash
wget https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -O docker-compose
chmod +x docker-compose
./docker-compose version
```
Edit `.bashrc` to add Docker Compose to PATH:
```bash
export PATH="${HOME}/bin:${PATH}"
```
Save and reload:
```bash
source .bashrc
which docker-compose
```
Change to the Docker bootcamp folder and run:
```bash
docker-compose up -d
docker ps
```

## Install and Use `pgcli`
```bash
pip install pgcli
pgcli -h localhost -U root -d ny_taxi # Password: root
\dt # Check schema
pip uninstall pgcli
conda install -c conda-forge pgcli
pip install -U mycli
pgcli -h localhost -U root -d ny_taxi # Password: root
```

## Forward ports to local machine
Forward:
- Port **5432** for PostgreSQL VM instance
- Port **8080** for pgAdmin

**pgAdmin Login**:
- Email: `admin@admin.com`
- Password: `root`

## Execute Jupyter Notebook
Navigate to the `02` folder in the repo and start the notebook:
```bash
jupyter notebook
```
Forward port **8888** to access the notebook.

## Install Terraform
```bash
wget https://releases.hashicorp.com/terraform/1.10.4/terraform_1.10.4_linux_amd64.zip
unzip terraform_1.10.4_linux_amd64.zip
sudo apt-get install unzip
terraform -version
```

## Create a Service Account for Terraform
1. Create a service account `terraform-runner` with the following roles:
    - Storage Admin
    - Compute Admin
    - BigQuery Admin
2. Download the key locally.

### Upload the key to the VM
```bash
sftp de-zoomcamp
ls
mkdir .gc
cd .gc
put my-creds.json
```

### Activate the key on the VM
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/my-creds.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
```

## Initialize Terraform
Navigate to the Terraform folder and run:
```bash
terraform init
terraform plan
terraform apply
```

## Shutdown the VM
```bash
sudo shutdown now
```

## Visual Studio Code Extension
Use the **Remote - SSH** extension to connect to the VM.

---
