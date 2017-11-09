tell application "QuickTime Player"
	open "sun-chang.mp4"
	tell front document
		present
		set looping to true
		play
	end tell
end tell