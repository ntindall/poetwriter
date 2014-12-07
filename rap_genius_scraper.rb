require 'rapgenius'


num = ARGV[0]
title = ARGV[1]

seed_song = RapGenius::Song.find(num) # song, seed
artist = seed_song.artist
puts artist.name
puts ""
y = 1
while true do
	songs = artist.songs(page: y)
	if songs.empty? 
		puts "Done here!"
		break
	end
	
	for x in 0..artist.songs.length-1 #only twenty songs for now
		array = Array.new
		song = songs[x]
		if !song.nil?
			puts song.title
			length = song.lines.length
			
			for i in 0..length-1
			    line = song.lines[i]
				array[i] = line.lyric
			end

			newfile = File.open(title, "a")
			for i in 0..array.length-1
				newfile.puts "#{array[i]}"
			end
			newfile << "\n"
		end
	end
	y += 1
end