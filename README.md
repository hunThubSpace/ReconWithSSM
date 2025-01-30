# Recon with SSM

## bb_urlrecon
```bash
# install requirement tools
$ git clone https://github.com/hunThubSpace/ReconVPS.git; cd ReconVPS; bash reconVPS.sh

# append content of following file into ~/.zshrc file
$ git clone https://github.com/hunThubSpace/BB-BugBountyBash.git; cd BB-BugBountyBash; $ cat zshfile.txt >> ~/.zshrc; source ~/.zshrc

# optional: you can use following command to generate wordlists for dns bruteforces
$ bb_wlgen_4char; bb_wlgen_alljhaddix; bb_wlgen_assetnote; bb_wlgen_nokovo; bb_wlgen_chaos

# optional: you can add following command to add valid dns servers as resolvers
$ bb_resfile_gen

# install SSM (database for managing assets)
$ cd /opt/others; git clone https://github.com/hunThubSpace/SSM-SubScopeMongo.git && cd SSM-SubScopeMongo
$ echo "export ssm_cred=user:pass" >> ~/.zshrc
$ source ~/.zshrc
$ python3 -r requirements.txt --break-system-package 
$ python3 setup.py; python3 ssm.py; dos2unix ssm.py
$ ln -s /opt/others/SSM-SubScopeMongo/ssm.py /opt/others/bb_subscope; chmod +x /opt/others/bb_subscope; source ~/.zshrc

# cloning recon framework (urlsRecon)
$ cd /opt/others; git clone https://github.com/hunThubSpace/ReconWithSSM.git && cd ReconWithSSM
$ dos2unix urlsRecon.py
$ ls -s /opt/others/ReconWithSSM/urlsRecon.py /opt/bb_urlrecon; chmod +x bb_urlrecon
source ~/.zshrc

# For starting recon, you need following steps

## 1. Create a program into database (ex. tesla_company)
$ bb_subscope program add tesla_company

## 2. Add domains into program (ex. tesla.com)
$ bb_subscope domain add tesla.com tesla_company

## 3. Crate a directory for program data (recommended)
$ mkdir -p ~/recon/tesla_company; cd ~/recon/tesla_company

## 4. Open bb_urlrecon and change your requirements (program_name, passive methods, reolve methods)
$ nano bb_urlrecon

## 5. Start
bb_urlrecon
```

## bb_iprecon
```bash
# install requirement tools
$ git clone https://github.com/hunThubSpace/ReconVPS.git; cd ReconVPS; bash reconVPS.sh

# append content of following file into ~/.zshrc file
$ git clone https://github.com/hunThubSpace/BB-BugBountyBash.git; cd BB-BugBountyBash; $ cat zshfile.txt >> ~/.zshrc; source ~/.zshrc

# optional: you can use following command to generate wordlists for dns bruteforces
$ bb_wlgen_4char; bb_wlgen_alljhaddix; bb_wlgen_assetnote; bb_wlgen_nokovo; bb_wlgen_chaos

# optional: you can add following command to add valid dns servers as resolvers
$ bb_resfile_gen

# install SSM (database for managing assets)
$ cd /opt/others; git clone https://github.com/hunThubSpace/SSM-SubScopeMongo.git && cd SSM-SubScopeMongo
$ echo "export ssm_cred=user:pass" >> ~/.zshrc
$ source ~/.zshrc
$ python3 -r requirements.txt --break-system-package 
$ python3 setup.py; python3 ssm.py; dos2unix ssm.py
$ ln -s /opt/others/SSM-SubScopeMongo/ssm.py /opt/others/bb_subscope; chmod +x /opt/others/bb_subscope; source ~/.zshrc

# cloning recon framework (urlsRecon)
$ cd /opt/others; git clone https://github.com/hunThubSpace/ReconWithSSM.git && cd ReconWithSSM
$ dos2unix ipRecon.py
$ ls -s /opt/others/ReconWithSSM/ipRecon.sh /opt/bb_iprecon; chmod +x bb_iprecon
source ~/.zshrc

# For starting recon, you need following steps

## 1. Create a program into database (ex. tesla_company)
$ bb_subscope program add tesla_company

# 3. Crate a directory for program data (recommended)
$ mkdir -p ~/recon/tesla_company; cd ~/recon/tesla_company

## 4. Open bb_iprecon and change your requirements (program_name, ASN)
$ nano bb_iprecon

## 5. make sure you have shodan api
$ shodan init <shodan-api-key>

## 5. Start
bb_iprecon
```
