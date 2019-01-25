require 'json'
require 'logger'
require 'url_validator'

def lambda_handler(event:, context:)
  logger = Logger.new(STDOUT)
  logger.level = Logger::INFO

  logger.info(event)

  url = event.dig('queryStringParameters', 'url')
  valid = UrlValidator.valid?(url)

  {statusCode: 200, body: JSON.generate({valid: valid})}
end
