# Makefile
# makefile for the maintenance of the git repository

pull:
	git pull origin main

add:
	git add -A

commit: add
	git commit -a

push: commit
	git push

