import pygame
import sys

# 定数
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
BLACK = (0, 0, 0)
GRID_COLOR = (128, 128, 128) # グレー

# プレイフィールドの定数
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
PLAYFIELD_WIDTH = GRID_WIDTH * BLOCK_SIZE
PLAYFIELD_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# プレイフィールドを画面中央に配置するための座標
TOP_LEFT_X = (SCREEN_WIDTH - PLAYFIELD_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAYFIELD_HEIGHT - 50 # 画面下部に少し余白を設ける

def draw_grid(surface):
    """プレイフィールドのグリッド線と枠線を描画する"""
    # 枠線を描画
    pygame.draw.rect(surface, GRID_COLOR, (TOP_LEFT_X, TOP_LEFT_Y, PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT), 2)

    # グリッド線を描画
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def main():
    """
    メインのゲーム関数
    """
    pygame.init()

    # ウィンドウと画面の設定
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # グリッドの状態を保持する2次元リストを作成
    # 0は空のセルを表す（色は黒）
    grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    running = True
    # メインゲームループ
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 画面の背景を黒にする
        screen.fill(BLACK)

        # グリッドを描画
        draw_grid(screen)

        # 画面を更新
        pygame.display.flip()

    # Pygameを終了
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
