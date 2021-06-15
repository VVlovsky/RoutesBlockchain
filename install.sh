sudo apt install git python3 python3-pip

git clone https://github.com/VVlovsky/RoutesBlockchain.git
cd RoutesBlockchain

pip install -r requirements.txt

IP=$(curl ifconfig.me)

IPPORT=$(echo $IP:8000)

python manage.py runserver $IPPORT