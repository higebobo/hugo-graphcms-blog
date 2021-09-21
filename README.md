# hugo-grapchms-blog


## Set up

* requirements
    * Hugo

### By clone

Clone this repository including submodules

```shell
git clone --recursive https://github.com/higebobo/hugo-graphcms-blog
```

### From scratch

Create a new site

```shell
hugo new site hugo-graphcms-blog
```

Create a git repository

```shell
cd hugo-graphcms-blog
git init
echo '*~' >> .gitignore
echo '*.bak' >> .gitignore
echo '*.orig' >> .gitignore
echo '.env' >> .gitignore
echo 'public' >> .gitignore
echo 'resources' >> .gitignore
```

Install [Ananke](https://github.com/theNewDynamic/gohugo-theme-ananke) theme

```shell
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
```

Copy config file from the theme directory

```shell
cp -pr themes/blonde/exampleSite/config.toml .
```

## Run server

```shell
hugo serve
```
