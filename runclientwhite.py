import client, b78player 

#replace randomPlayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'W'
whitePlayer = b78player.Player('W')

whiteClient = client.Client(whitePlayer)
whiteClient.run()
