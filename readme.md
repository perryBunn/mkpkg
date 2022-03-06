# mkpkg

<!-- Brief description -->

This script serves to complete the menial task of creating tars for NOAA NESDIS
STAR algorithm deliveries. This interactive approach should make creating any
number of delivery files trivial and packages more concise.

## Features

<!-- More detailed description on what the program can do -->

## Installing

This script was written with Python 3.7 in mind, that being said there should
be no reason why new or older versions should not work. However support will
only be given for 3.7.*

1. `git clone https://github.com/perryBunn/mkpkg.git --depth 1`
2. `cd mkpkg`
3. `./configure`

### Dependencies

<!-- What is needed to install this for a user -->
Pip modules:
    pyyaml

## Usage

1. Interactive

    To start the script interactively all that is needed to do is to run `mkpkg`
    in the source directory.

    ```bash
    mkpkg
    ```

    <!-- TODO: Include gifs of it being used -->

2. Command Line Arguments

    This is an intended feature to be added. However it will not be fully
    implemented in the first revision

## Contributing

<!-- How should people contribute? -->

Getting the source for development is slightly different from getting the code
to run.

`git clone git@github.com:perryBunn/mkpkg.git`

If you have already downloaded the source then all you should need to do is
make sure that the git remote is set to use ssh.

For a more detailed view of how to contribute see the [contributing guide](contributing_guide.md)

### Dev Dependencies

Pip modules:
    pylint,
    pytest

### Style Guide

For all Python files PEP8 standards are to be followed. The pipeline will be
linting with pylint using this config: [pylintrc](pylintrc)

Shell files will use Google's [shellguide](https://google.github.io/styleguide/shellguide.html)

## Changelog

See [changelog.md](changelog.md)

## Credit

Perry Bunn - perry.bunn@noaa.gov

## License

See [license.md](license.md)
