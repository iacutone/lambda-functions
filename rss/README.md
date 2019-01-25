This code does not include the needed packages from `pip`. In order for this code to work, please install the required python packages according to [this](https://medium.freecodecamp.org/escaping-lambda-function-hell-using-docker-40b187ec1e48) blog post. Currently, the needed python packages are:

1. `pip install googletrans -t .`
1. `pip3 install newspaper3k -t .`

These packages _need_ to be installed via docker:
1. `docker run -v /Users/iacutone/lambda-functions/rss:/working -it --rm ubuntu`
1. `apt-get update`
1. `apt-get install python-pip`
1. `apt-get install python3-pip`
1. `apt-get install zip`
1. `cd working`

__TODO__

1. Find a way to automate zipping the files together
  - Currently, I need to run:
      1. find . -maxdepth 1 -type d | zip -r lambda.zip *
      1. find . -maxdepth 1 -type f | zip lambda.zip *

  - Write an ansible script?
