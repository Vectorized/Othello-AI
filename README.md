50.021 Othello AI
=================

Main project for 50.021 Artificial Intelligence course in Singapore University of Technology and Design (SUTD). This is the winning entry for the othello AI competition during 50.021 summer 2015.

![Strong Othello AI screenshot](https://raw.githubusercontent.com/webby1111/Othello-AI/master/screenshot.png "Strong Othello AI screenshot")

<b>Features:</b>  
- Bitboard
- Negascout + transposition table
- Patten based leaf evaluation
- Accurate move ordering evaluation (High synergy with leaf evaluation) 
- Dynamic time allocation
- "Bit-vectorization" hacks (new hack to bypass Python's slow indirection)

Running
-------

1. Open a terminal window and change directory into the current folder.  
2. Launch the server.
 
        python runserver.py ['test'|'me'|'he']

  You can choose one out of the three options:  
  `'test'` : AI vs AI.  
  `'me'` : You start first. Used for challenging others online.  
  `'he'` : Opponent starts first. Used for challening others online.  

3. <b>If you have choosen `'test'`</b>, you need to open two more terminal windows to launch the two AI bots. In the 1st one, run:

        python runclientwhite.py
	
  In the 2nd window, run:

      python runclientblack.py
	
  <b>If you have choosen `'me'`</b>, you need to open one more terminal window to launch the AI (which will help you think of what you should do. You just have to do mirror what your opponent does to the AI game window. :P)

      python runclientwhite.py
	
  <b>If you have choosen `'he'`</b>, you need to open one more terminal window to launch the AI (which will help you think of what you should do. You just have to do mirror what your opponent does to the AI game window. :P)

      python runclientblack.py

Files that you may want to look at
----------------------------------

- `b78.py`: Most of the AI logic is contained here
- `b78player.py`: You can set the time allocation here
- `constants.py`: IP address and ports for hosting a game

Our bot's name is b78, hence the name of the files.

The other codes are either AI support code or the default game skeleton for all competitors.

Comments
--------

Feel free to edit or modify the code, learn from it, etc. 
If you find some way to make it even more awesome, or want to let me of how it has helped you in any AI othello contest, drop me a message using the contact form on my website. 

Also, if you are using an AI to vs a human player online, it's considered etiquette to let them know. ;)

This project was developed with the following limitations for the competition:
- Usage of Python 2.7
- No calls to external non-Python APIs. (Basically, we cannot write C/C++ code and call it from Python.)
- Code must be able run on opponent's computer with basic python installation. 
  This means we can't use numpy, Pypy, Cython, etc. Not everyone has these installed. As the "bit-vectorization" effectively pushes all the heavy-lifting to the inner C loops in Python to avoid indirection, the code should not see any siginificant improvements even with those extras. (Pypy is only ~10% faster) 
- 30 mins total CPU time per opponent.
- 80 MB max ram usage.
