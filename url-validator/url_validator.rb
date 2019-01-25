require 'net/http'
require 'openssl'
require 'url_formatter'

class UrlValidator

  attr_reader :url

  def initialize(url)
    @url = UrlFormatter.new(url.strip).remove_extra_words
  end

  def self.valid?(url)
    return false if url.to_s.empty?

    new(url).valid?
  end

  def send_request
    Net::HTTP.start uri.host, uri.port, use_ssl: uri.scheme == 'https' do |http|
      req = Net::HTTP::Get.new uri

      req['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
      req['Accept-Encoding'] = 'gzip, deflate, br'
      req['Accept-Language'] = 'en-US,en;q=0.9'
      req['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

      http.request req
    end
  end

  def valid?(retries: 5)
    return false if retries < 0

    begin
      response = send_request
    rescue Errno::ECONNREFUSED => e
      if e.message == 'Failed to open TCP connection to :80 (Connection refused - connect(2) for nil port 80)'
        return UrlValidator.new(force_https).valid?(retries: retries - 1)
      elsif e.message.include? '443'
        return UrlValidator.new(remove_https).valid?(retries: retries - 1)
      end
      return valid?(retries: retries - 1)
    rescue Net::OpenTimeout
      return valid?(retries: retries - 1)
    rescue OpenSSL::SSL::SSLError
      puts "OpenSSL error for url: #{url}"
      return UrlValidator.new(remove_https).valid?(retries: retries - 1)
    rescue SocketError, URI::InvalidURIError
      return false
    end

    case response
    when Net::HTTPSuccess, Net::HTTPTooManyRequests, Net::HTTPRedirection
      true
    when Net::HTTPNotFound
      new_url = UrlFormatter.new(url).remove_path
      return UrlValidator.new(new_url).valid?(retries: retries - 1)
    else
      false
    end
  end

  private

  def force_https
    "https://#{url}"
  end

  def remove_https
    url.sub(%r{\Ahttps://}, 'http://')
  end

  def uri
    @uri = URI(url)
  end
end
