curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql17
apt-get install unixodbc-dev --assume-yes
apt install python3-pip --assume-yes
pip3 install pyodbc --assume-yes
cp /etc/ssl/openssl.cnf /etc/ssl/openssl_bu.cnf
sed -i 's/MinProtocol = TLSv1.2/MinProtocol = TLSv1.0/g' /etc/ssl/openssl.cnf
sed -i 's/CipherString = DEFAULT@SECLEVEL=2/CipherString = DEFAULT@SECLEVEL=1/g' /etc/ssl/openssl.cnf