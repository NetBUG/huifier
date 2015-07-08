#coding=utf-8
def huify(string)
	out = string
	if out.length > 2
		out[0] = "х"
		out[1] = "у"
	end
	out
end

def test
	text=File.open('xxx.txt').read
	text.gsub!(/\r\n?/, "\n")
	text.each_line do |line|
		line.strip!
		parts = line.split('-')
		h = line.huify(parts[0])
		if line == h
			print "✔: #{h}"
		else
			print "✘: #{line} vs #{h}"
		end
	end
end