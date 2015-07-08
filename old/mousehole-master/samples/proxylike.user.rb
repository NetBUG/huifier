require 'open-uri'
require 'resolv'

class Array
  def to_h
    self.inject({}) do |hash, value|
      hash[value.first] = value.last ; hash
    end
  end
end

class ProxyLike < MouseHole::App
  title 'ProxyLike'
  namespace 'http://whytheluckystiff.net/mouseHole/'
  description %{
    Run pages through the proxy by passing them in on the URL.
    For example, to view Boing Boing through the proxy, use:
    http://127.0.0.1:3704/http://boingboing.net/
  }
  version '2.1'
 
  mount "http:" do |page|
    page.status = 200 # OK
    proxyAddr = URI("http://#{ page.headers['host'] }/")
    addresses = Resolv.getaddresses(proxyAddr.host)
    if (address = addresses.find { |a| a =~ /([0-9]+\.){3}[0-9]+/ }) # stupid ip address detect
      mH = "http://#{ address }:#{proxyAddr.port}/"
    else
      mH = proxyAddr.to_s
    end
    uri = URI(page.location.to_s[1..-1])
    options = {:proxy => mH}.merge(page.headers.to_h)
    options.delete_if { |k,v| %w(host accept-encoding).include? k }
    page.document =
      uri.open(options) do |f|
      base_uri = uri.dup
      base_uri.path = '/'
      base_href f.read, base_uri, mH
    end
  end

  def self.base_href( html, uri, mh )
    html.gsub( /((href|action|src)\s*=\s*["']?)(#{ uri }|\/+)/, "\\1#{ mh }#{ uri }" ).
      sub( /<html/i, %(<base href="#{ uri }" /><html) )
  end
end
