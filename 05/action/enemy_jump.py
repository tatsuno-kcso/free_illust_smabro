import pygame

class EnemyJump():
    def __init__(self, screen, joystick, stage, player_pos):
        self.joystick = joystick
        self.screen = screen
        self.stage = stage
        self.player_pos = player_pos

        # ジャンプ
        self.jumping = False
        self.ground = self.screen.get_height() / 4 * 3
        self.vel = 0 # y方向の速度
        self.acc = 1 # 重力加速度
        self.jump_second = False
        
        self.before_jump_frame_count = 0
        self.jump_frame_count = None
        self.short_jump_flg = False
        self.VEL_CONST = 15
        self.ACC_CONST = 2

    def jump_input(self, events):
        # print(self.before_jump_frame_count)
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                # print("pygame.JOYBUTTONDOWN")
                # flg初期化
                self.short_jump_flg = False
                if not self.jumping and self.player_pos.colliderect(self.stage):
                    self.before_jump_frame_count = 4
                elif not self.jump_second:
                    self.jump_second = True
                    self.jump_frame_count = 0
                    # print("二段ジャンプしました")
            # ショートジャンプ入力受付
            if event.type == pygame.JOYBUTTONUP and event.button == 5 and 1 <= self.before_jump_frame_count and self.before_jump_frame_count <= 4:
                self.short_jump_flg = True
                # print("pygame.JOYBUTTONUP")
        if self.joystick and self.joystick.get_axis(1) > 0.9 and self.vel > 0:
            self.vel = 1 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
            print("急降下")
        
        # ジャンプ踏切フレーム
        if 1 <= self.before_jump_frame_count:
            self.before_jump_frame_count -= 1
            self.jump_frame_count = 0
            return 
        
        # ジャンプ中フレーム
        if self.jump_frame_count == None:
            return
        self.jump_frame_count+=1
        if self.short_jump_flg:
            self.set_short_jump_param()
        else:
            self.set_jump_param()

    def set_short_jump_param(self):
        if 0 == self.jump_frame_count:
            self.jumping = True
            self.vel = -1.35 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 1 == self.jump_frame_count:
            self.vel = -0.72 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 2 == self.jump_frame_count:
            self.vel = -0.69 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 3 == self.jump_frame_count:
            self.vel = -0.69 * self.VEL_CONST
            self.acc = 0.4 * self.ACC_CONST
        elif 4 <= self.jump_frame_count:
            if 0.6 * self.VEL_CONST < self.vel:
                self.acc = 0

    def set_jump_param(self):
        if 0 == self.jump_frame_count:
            self.jumping = True
            self.vel = -2 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 1 == self.jump_frame_count:
            self.vel = -3 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 2 == self.jump_frame_count:
            self.vel = -2 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 3 == self.jump_frame_count:
            self.vel = -1.6 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 4 == self.jump_frame_count:
            self.vel = -1.05 * self.VEL_CONST
            self.acc = 0 * self.ACC_CONST
        elif 5 == self.jump_frame_count:
            self.vel = -0.75 * self.VEL_CONST
            self.acc = 0.4 * self.ACC_CONST
        elif 6 <= self.jump_frame_count:
            if 0.6 * self.VEL_CONST < self.vel:
                self.acc = 0

    def fall_action(self):
        self.vel += self.acc
        self.player_pos.y += self.vel
        if self.player_pos.colliderect(self.stage):
            self.player_pos.y = self.screen.get_height() / 4 * 3 - 100 + 1
            self.vel = 0
            self.acc = 1
            self.jumping = False
            self.jump_second = False
        # if self.vel >= 20:
        #     self.acc = 0
        if 0.6 * self.VEL_CONST < self.vel:
            self.acc = 0
    def update(self, events):
        self.jump_input(events)
        self.fall_action()