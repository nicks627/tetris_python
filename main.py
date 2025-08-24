import pygame
import sys

# 定数
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BLACK = (0, 0, 0)

def main():
    """
    メインのゲーム関数
    """
    pygame.init()

    # ウィンドウと画面の設定
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    running = True
    # メインゲームループ
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 画面の背景を黒にする
        screen.fill(BLACK)

        # 画面を更新
        pygame.display.flip()

    # Pygameを終了
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
