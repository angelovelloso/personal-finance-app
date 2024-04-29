docker run -d \
    -p 3000:3000 \
    -v /mnt/c/Users/vello/OneDrive/my_git/financeiro-pessoal/data/db:/data \
    --name metabase metabase/metabase