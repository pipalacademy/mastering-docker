# Mastering Docker

Resources for _Mastering Docker_ course by Pipal Academy.

## How to build

The website is built using [mkdocs for material][1].

[1]: https://squidfunk.github.io/mkdocs-material/

Follow the following steps to build the website.

**Step 1: clone the repo**

```
$ git clone https://github.com/pipalacademy/mastering-docker
$ cd mastering-docker
```

**Step 2: Install dependencies**

```
$ pip install -r requirements.txt
```

You may want to do this in a vitualenv.

**Step 3: Build the docs**

```
$ mkdocs build
```

The generated site will be in `site/` directory.


