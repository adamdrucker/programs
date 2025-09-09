#!/usr/bin/ruby

winning_num = rand(1..10)

print "Guess a number: "
guess = gets

if guess == winning_num
  puts "Correct!"
else
  puts "Incorrect!"
end
