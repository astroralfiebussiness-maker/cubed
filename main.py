#!/usr/bin/env python3
"""
Cubed - Main entry point for the game
"""

from engine.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
