# PasswordSaver
Version: 1.00

Local encrypted database application designed for storing website usernames and passwords. Supports mulitple user login.

This application uses bcrypt to store hashed passwords for user login.
Once logged in, information is encrypted with PBKDF2 before it enters the database.

## Getting Started

### Prerequisites

* visidata
* bcrypt
* cryptography
* sqlalchemy


### Installing

```
git clone https://github.com/mattmurch/PasswordSaver.git
python setup.py install
```

## Usage

Run this line to start the application

```
password_saver.py
```

### Commands

Once logged in, normal visidata commands will work.
Listed below are the commands specific to this application.

Commands are case-sensitive:
* 'A' - Add a new row. Will ask for Site, Username, and Password.
* 'd' - Delete entire row.
* 'e' - Edit the current value.
* 'q' - Quit.


## Built With

* [VisiData](https://github.com/saulpw/visidata/) - User Interface

## Contributing

If you would like to contribute, please send a pull request against the master branch.


## Authors

* **Matt Murch** - *Initial work* - [Matt Murch](https://github.com/mattmurch)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Acknowledgments

* Saul Pwanson
* AJ Jordan (Strugee)
