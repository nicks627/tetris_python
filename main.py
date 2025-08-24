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

def valid_space(piece, grid):
    """
    ピースがグリッド内の有効な位置（壁や他のブロックと衝突しない）にいるかチェックする
    """
    # グリッド上の空いているマスを全件取得して、ピースのブロックがそこに含まれるかチェック
    # ただし、画面より上にはみ出している場合は有効とみなす
    accepted_positions = [[(j, i) for j in range(GRID_WIDTH) if grid[i][j] == (0,0,0)] for i in range(GRID_HEIGHT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_game_over(grid):
    """グリッドの最上段にブロックがあればゲームオーバーと判定する"""
    for x in range(len(grid[0])):
        if grid[0][x] != (0,0,0):
            return True
    return False

def lock_piece(piece, grid):
    """着地したピースをグリッドに固定する"""
    shape_pos = convert_shape_format(piece)
    for pos in shape_pos:
        x, y = pos
        # グリッド内にピースの形状を書き込む
        if y > -1:
            grid[y][x] = piece.color
    return grid

def clear_lines(grid):
    """満たされた行をクリアし、新しい空の行を上部に追加する。消した行数を返す。"""
    lines_cleared = 0
    # 下から上にチェック
    y = GRID_HEIGHT - 1
    while y >= 0:
        row = grid[y]
        if (0,0,0) not in row: # この行が埋まっている
            lines_cleared += 1
            # この行を削除
            del grid[y]
            # 上に新しい空の行を追加
            grid.insert(0, [(0,0,0) for _ in range(GRID_WIDTH)])
        else:
            y -= 1
    return lines_cleared

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

    # ゲームクロックと重力設定
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.3 # 秒 / 1ライン落下

    running = True
    # メインゲームループ
    while running:
        fall_time += clock.get_rawtime()
        clock.tick()

        # 重力処理
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                grid = lock_piece(current_piece, grid)
                clear_lines(grid) # ライン消去を呼び出す
                current_piece = next_piece
                next_piece = get_shape()

                if check_game_over(grid):
                    running = False

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    grid = lock_piece(current_piece, grid)
                    clear_lines(grid) # ライン消去を呼び出す
                    current_piece = next_piece
                    next_piece = get_shape()
                    if check_game_over(grid):
                        running = False


        # 描画処理
        draw_window(screen, grid, current_piece)
        pygame.display.flip()

    # Pygameを終了
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
