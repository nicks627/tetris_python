import pygame
import sys
import random

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

# --- テトリミノの形状定義 ---

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# --- グローバル変数 ---
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] # Green, Red, Cyan, Yellow, Orange, Blue, Purple


# --- Pieceクラス ---
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def convert_shape_format(piece):
    """
    Pieceオブジェクトの形状と回転に応じて、
    グリッド上のブロックの座標リストを返す
    """
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        # テンプレートのオフセットを補正
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def get_shape():
    """
    ランダムな形状の新しいPieceオブジェクトを生成して返す
    """
    return Piece(5, 0, random.choice(shapes))

def draw_window(surface, grid, piece):
    """ウィンドウ全体を描画する（背景、グリッド、固定されたブロック、現在のピース）"""
    surface.fill(BLACK)

    # グリッド線を描画
    draw_grid(surface)

    # 固定されたブロックを描画
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != (0,0,0):
                pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    # 落下中のピースを描画
    shape_pos = convert_shape_format(piece)
    for pos in shape_pos:
        x, y = pos
        if y > -1:
            pygame.draw.rect(surface, piece.color, (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

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
    grid = [[(0,0,0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # 最初のピースを生成
    current_piece = get_shape()
    next_piece = get_shape() # 次のピースも用意しておく

    running = True
    # メインゲームループ
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 描画処理
        draw_window(screen, grid, current_piece)
        pygame.display.flip()

    # Pygameを終了
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
