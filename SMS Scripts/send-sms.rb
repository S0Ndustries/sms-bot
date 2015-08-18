require 'rubygems'
require 'twilio-ruby'
 
account_sid = "AC164a87fb536f9ead23575f129196c639"
auth_token = "45f2016a23a6629ecc9df46ad2f3212a"
client = Twilio::REST::Client.new account_sid, auth_token
 
from = "+12264003340" # Your Twilio number
 
friends = {
"+16477450709" => "Alex",
"+16477467048" => "Josh"
}
friends.each do |key, value|
  client.account.messages.create(
    :from => from,
    :to => key,
    :body => "Hey #{value}, Monkey party at 6PM. Bring Bananas!"
  )
  puts "Sent message to #{value}"
end
