# soul

soul api client

## Install

```bash
pip3 install soulapi
```

## Usage

In a terminal:

1. get help

```bash
soul -h             # get help and available module, method, property
soul -h use         # get help for `use` api
soul -h post       # get help for `post` module
soul -h post like  # get help for `post.like` method
```

2. login: most api need to authorization, so, you should login at first

```bash
soul login PHONE PASSWORD AREA  # use mobile or email to login

soul use SECRET                     # use token directly
```

3. use api

```bash
soul post recommended
```

## LICENSE

MIT
