require 'json'
a = JSON.parse(File.read("docs/feed.json"))
a.each do |am|
    am["read_more"] = 0
    am["read_more"] = ""
end
File.delete("docs/feed.json")
File.open("docs/feed.json", "a") { |file| file.write(JSON.generate(a)) }
