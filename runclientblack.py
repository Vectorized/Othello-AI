import client, b78player

#replace randomplayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'B'
blackPlayer = b78player.Player('B')

blackClient = client.Client(blackPlayer)
blackClient.run()
