This code does not include the needed packages from `pip`. In order for this code to work, please install the required python packages according to [this](https://medium.freecodecamp.org/escaping-lambda-function-hell-using-docker-40b187ec1e48) blog post.


*Install these libraries in Docker*

1. `docker run -v /Users/iacutone/lambda-functions/rss:/working -it --rm ubuntu`
1. `apt-get update`
1. `apt-get install python-pip`
2. `apt-get install python3-pip`
3. `apt-get install zip`
4. `cd working`
5. `pip3 install newspaper3k -t .`
7. `pip3 install googletrans==4.0.0-rc1`

*Zip the files*

1. `find . -maxdepth 1 -type d | zip -r lambda.zip *`
2. `find . -maxdepth 1 -type f | zip lambda.zip *`

- Upload lambda.zip to AWS
