#!/usr/bin/env bash
git pull
python scripts/update_datasets.py
git add datasets/ images/

 # Only commit and push if changes were made
if $(git status | grep -q "nothing to commit")
then
    echo "No changes to commit."
else
    git commit -m "Manual Update"
    git push
fi
