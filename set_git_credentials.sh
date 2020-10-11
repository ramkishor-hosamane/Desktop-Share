echo "Github Configuration"
echo "--------------------"
sleep 1
echo
read -p "Enter your name : " name
read -p "Enter your email id (one which is configured with github) : " email
git config --global user.email "$email"
git config --global user.name "$name"

echo "[+] Configured your account's default identity"


read -p "Enter your github username : " username
read -p "Enter your github password : " password

read -p "Enter remote github repository username : " git_repo_username
read -p "Enter remote github repository name : " repository


git remote set-url origin https://$username:$password@github.com/$git_repo_username/$repository.git
echo "[+] Configured remote Repository"

echo "Done!!!!"
