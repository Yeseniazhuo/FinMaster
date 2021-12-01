# FinMaster

Financial Time Management Tool

## Author

This project is built and maintained by @cheryl-mxd and @Yeseniazhuo. Private repository addresses are https://github.com/cheryl-mxd/FinMaster.git and https://github.com/Yeseniazhuo/FinMaster.git. Please check both repositories for commits' details and the final versions of the two repositories are exactly the same. 

The pull requests between repositories are not properly executed because of the security alert brought by the private key of _newsapi_.

## Execute Instructions

Please check `requirements.txt`  for project dependencies.

First, git clone the project repository.

```shell
git clone https://github.com/Yeseniazhuo/FinMaster.git
```

Second, run the server in the `FinMaster/backend` folder (remember to change your localhost url in `/backend/backend/settings.py` to `INTERNAL_IPS = [ "127.0.0.1", ]` ).

```shell
python manage.py runserver
```

Then you should be able to access the website at `127.0.0.1:8000/`.

<u>Warning: all functions are only available to logged-in users. You can easily create a new user and enjoy your journey with **FinMaster**!</u>