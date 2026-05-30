#!/usr/bin/env python3
"""
Interactive game runner - Play Cubed with command input
"""

import sys
from engine.game import Game

def main():
    game = Game()
    
    print("\n" + "="*60)
    print("CUBED - Interactive Mode")
    print("="*60)
    print("Type 'help' for commands or 'quit' to exit\n")
    
    game.render()
    game.handle_input()
    
    # Game loop
    while game.running:
        game.tick()
        game.render()
        game.handle_input()

if __name__ == "__main__":
    main()
