# PasswordSaver
Version: 1.0.0

Local encrypted database application designed for storing website usernames and passwords. Supports mulitple user login.

### Security Specs
* This application uses bcrypt to store hashed passwords for user login.
* Once logged in, information is encrypted with PBKDF2 before it enters the database.
* Encryption key is derived from your login password.
* Salts are generated randomly and stored along with your login username and password.
* Currently, there is no way to change your login password, as it is used to encrypt your data.

![PasswordSaverExample](https://user-images.githubusercontent.com/13307633/27192135-35fe1be4-51c8-11e7-8c02-33936d9b4d21.png)

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
./password_saver.py
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
