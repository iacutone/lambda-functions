class UrlFormatter
  attr_reader :url

  def initialize(url)
    @url = url
  end

  def remove_extra_words
    ensure_protocol[/(\S+)/]
  end

  def remove_path
    if has_https_protocol?
      "https://#{extract_domain_name}"
    else
      "http://#{extract_domain_name}"
    end
  end

  private

  def ensure_protocol
    if has_https_protocol? || has_http_protocol?
      url
    else
      "http://#{url}"
    end
  end

  def has_https_protocol?
    url.match(%r{\Ahttps://})
  end

  def has_http_protocol?
    url.match(%r{\Ahttp://})
  end

  def extract_domain_name
    ensure_protocol.split('/')[2]
  end

end
