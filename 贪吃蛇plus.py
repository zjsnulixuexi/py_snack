#######################################引用库#########################################
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque
######################################初始化界面#######################################
# 初始化 Pygam
#test_by_zjs
pygame.init()
# 设置窗口尺寸和标题
SCREEN_WIDTH = 889
SCREEN_HEIGHT = 717
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('贪吃蛇')

# 加载链接图片和开始按钮图片
link_image = pygame.image.load('背景图.jpg')
start_button_image = pygame.image.load('按钮(1).jpg')

# 定义打印文本函数
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    img_text = font.render(text, True, fcolor)
    screen.blit(img_text, (x, y))

# 初始化字体
font = pygame.font.Font(None, 36)

# 显示链接图片和开始按钮
screen.blit(link_image, (0, 0))  # 根据实际需求设置图片的位置
screen.blit(start_button_image, (10, 10))  # 根据实际需求设置按钮的位置

# 渲染界面
pygame.display.flip()

def tanchi():
#########################################初始化参数########################################
    SCREEN_WIDTH = 889
    SCREEN_HEIGHT = 717
    SIZE = 20


    def print_text(screen, font, x, y, text, fcolor=(0, 0, 0)):
        imgText = font.render(text, True, fcolor)
        screen.blit(imgText, (x, y))


    def main():
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('背景音乐.mp3')  # 音乐
        pygame.mixer.music.play(-1)  # 音乐循环
        eat_sound = pygame.mixer.Sound('吃食物音效.mp3')  # 吃食物时的音效
        game_over_sound = pygame.mixer.Sound('失败音效.wav')  # 失败音效
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('贪吃蛇')
        light = (255, 30, 30)  # 蛇的颜色
        dark = (0, 0, 0)  # 食物颜色

        font1 = pygame.font.SysFont('SimHei', 24)  # 得分的字体
        font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
        red = (200, 30, 30)  # GAME OVER 的字体颜色
        fwidth, fheight = font2.size('GAME OVER')
        line_width = 1  # 网格线宽度
        black = (0, 0, 0)  # 网格线颜色
        bgcolor = (135, 206, 235)  # 背景色
        # 方向，起始向右
        pos_x = 1
        pos_y = 0
        # 如果蛇正在向右移动，那么快速点击向下向左，由于程序刷新没那么快，向下事件会被向左覆盖掉，导致蛇后退，直接GAME OVER
        # b 变量就是用于防止这种情况的发生
        b = True
        # 范围
        scope_x = (0, SCREEN_WIDTH // SIZE - 1)
        scope_y = (2, SCREEN_HEIGHT // SIZE - 1)
        # 蛇
        snake = deque()
        # 食物
        food_x = 0
        food_y = 0

        # 初始化蛇
        def _init_snake():
            nonlocal snake
            snake.clear()
            snake.append((2, scope_y[0]))
            snake.append((1, scope_y[0]))
            snake.append((0, scope_y[0]))

        # 食物
        def _create_food():
            nonlocal food_x, food_y
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
            while (food_x, food_y) in snake:
                # 为了防止食物出到蛇身上
                food_x = random.randint(scope_x[0], scope_x[1])
                food_y = random.randint(scope_y[0], scope_y[1])
#######################################游戏逻辑主体##################################################
        _init_snake()
        _create_food()
        game_over = True
        start = False  # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
        score = 0  # 得分
        orispeed = 0.1  # 原始速度
        speed = orispeed
        last_move_time = None
        pause = False  # 暂停

        while True : # 蛇的移动逻辑和键盘监听
            for event in pygame.event.get():
                if event.type == QUIT: # 监听退出键
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if game_over: # 监听游戏结束时重新开始的回车键
                            start = True
                            game_over = False
                            b = True
                            _init_snake()
                            _create_food()
                            pos_x = 1
                            pos_y = 0
                            # 得分
                            score = 0
                            last_move_time = time.time()
                    elif event.key == K_SPACE: # 监听空格暂停键
                        if not game_over:
                            pause = not pause
                    elif event.key in (K_w, K_UP): # 四个方向逻辑
                        # 这个判断是为了防止蛇向上移时按了向下键，导致直接 GAME OVER
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = -1
                            b = False
                    elif event.key in (K_s, K_DOWN):
                        if b and not pos_y:
                            pos_x = 0
                            pos_y = 1
                            b = False
                    elif event.key in (K_a, K_LEFT):
                        if b and not pos_x:
                            pos_x = -1
                            pos_y = 0
                            b = False
                    elif event.key in (K_d, K_RIGHT):
                        if b and not pos_x:
                            pos_x = 1
                            pos_y = 0
                            b = False

            # 填充背景色
            screen.fill(bgcolor)
            # 画网格线 竖线
            for x in range(SIZE, SCREEN_WIDTH, SIZE):
                pygame.draw.line(screen, black, (x, scope_y[0] * SIZE), (x, SCREEN_HEIGHT), line_width)
            # 画网格线 横线
            for y in range(scope_y[0] * SIZE, SCREEN_HEIGHT, SIZE):
                pygame.draw.line(screen, black, (0, y), (SCREEN_WIDTH, y), line_width)
            # 游戏结束提示语
            if game_over:
                pygame.mixer.music.play(-1)  # 音乐循环
                if start:
                    print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER',
                               red)
                    print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2 + fheight,
                               'Your score:' + str(score), red)
            else:
                curTime = time.time()
                if curTime - last_move_time > speed:
                    if not pause:
                        b = True
                        last_move_time = curTime
                        next_s = (snake[0][0] + pos_x, snake[0][1] + pos_y)
                        if next_s[0] == food_x and next_s[1] == food_y:
                            # 吃到了食物
                            _create_food()
                            snake.appendleft(next_s)
                            score += 10
                            speed = orispeed - 0.03 * (score // 100)
                            eat_sound.play()
                        else:
                            if scope_x[0] <= next_s[0] <= scope_x[1] and scope_y[0] <= next_s[1] <= scope_y[1] \
                                    and next_s not in snake:
                                snake.appendleft(next_s)
                                snake.pop()
                            else:
                                game_over = True
                                # 停止背景音乐
                                pygame.mixer.music.stop()
                                # 播放失败音效
                                game_over_sound.play()

            # 画食物
            if not game_over:
                # 避免 GAME OVER 的时候把 GAME OVER 的字给遮住了
                pygame.draw.rect(screen, light, (food_x * SIZE, food_y * SIZE, SIZE, SIZE), 0)

            # 画蛇
            for s in snake:
                pygame.draw.rect(screen, dark, (s[0] * SIZE + line_width, s[1] * SIZE + line_width,
                                                SIZE - line_width * 2, SIZE - line_width * 2), 0)
            print_text(screen, font1, 30, 7, f'速度: {score // 100}')
            print_text(screen, font1, 450, 7, f'得分: {score}')
            pygame.display.update()


    if __name__ == '__main__':
        main()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # 监听退出键

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 监听鼠标左键
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_button_rect = start_button_image.get_rect()
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    tanchi()  # 启动贪吃蛇游戏

pygame.quit()