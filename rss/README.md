This code does not include the needed packages from `pip`. In order for this code to work, please install the required python packages according to [this](https://medium.freecodecamp.org/escaping-lambda-function-hell-using-docker-40b187ec1e48) blog post. Currently, the needed python packages are:

1. `pip install googletrans -t .`
1. `pip install newspaper -t .`

These packages _need_ to be installed via docker:
1. `docker run -v /Users/iacutone/lambda-functions/rss:/working -it --rm ubuntu`

__TODO__

1. Find a way to automate zipping the files together
  - Currently, I need to run:
      1. `zip lambda.zip lambda_function.py` for files
      1. `zip -r lambda.zip newspaper/` for file directories
