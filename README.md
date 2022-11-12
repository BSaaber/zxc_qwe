# Documentation
****
## install, build & up
- install git repository
```shell
    git clone https://github.com/BSaaber/zxc_qwe.git
```
- install front submodule (in project folder)
```shell
    git submodule update --init --recursive
```
- install and run [docker desktop](https://www.docker.com/products/docker-desktop/) or install docker [by cli](https://docs.docker.com/engine/install/ubuntu/)
- build project (in project folder)
```shell
    docker-compose build
```
- run (in project folder)
```shell
    docker-compose up
```
## scripts
### how to execute script:
1. open ``web`` (backend) container cli
2. ``python -m app.scripts.<name_of_script>`` \
    Notice that you **must not** use write ``.py`` at the end of the command

### filling the database
1. run parse_spgz_table script
```shell
    python -m app.scripts.parse_spgz_table
```
2. run parse_tsn script
```shell
    python -m app.scripts.parse_tsn
```
3. run parse_sn script
```shell
    python -m app.scripts.parse_sn
```
4. run make_sn_mapping script
```shell
    python -m app.scripts.make_sn_mapping
```
5. run make_tsn_mapping script
```shell
    python -m app.scripts.make_tsn_mapping
```