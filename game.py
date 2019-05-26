from game_objects.window import GameWindow

if __name__ == "__main__":
    window = GameWindow(cell_size=20, length=40, height=30, aps=20)
    window.run_game_loop()
