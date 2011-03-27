cd webapps/stud2dotoh/stud2dotoh
sh_scripts/remove_pyc.sh ~/webapps/stud2dotoh/stud2dotoh
git status
git stash
git pull
git stash pop
cd ..
./apache2/bin/restart
echo "Instance Restarted"