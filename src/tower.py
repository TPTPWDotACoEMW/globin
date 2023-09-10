from dataclasses import dataclass

@dataclass
class Ball:
    ball_type:    str
    x_pos:        float
    y_pos:        float
    x_momentum:   float
    y_momentum:   float
    in_structure: bool

@dataclass
class Strand:
    strand_type:         str
    first_ball:          Ball
    second_ball:         Ball
    connection_strength: float
    length:              float
    ball_used:           bool

class Tower:
    def __init__(self, tower_str):
        if tower_str[0] == '_':
            tower_str = tower_str[1:]

        self.balls   = []
        self.strands = []

        self.used_strand_balls = 0
        self.total_balls       = 0

        tower_separator = ":"
        token_ball      = "b"
        token_strand    = "s"

        tower_tokens = tower_str.split(tower_separator)
        try:
            token_index = 0
            while token_index < len(tower_tokens):
                ball_type = tower_tokens[token_index]
                token_index += 1

                if ball_type == token_ball:
                    ball_type = tower_tokens[token_index]
                    token_index += 1
                    
                    x_pos = float(tower_tokens[token_index])
                    token_index += 1

                    y_pos = float(tower_tokens[token_index])
                    token_index += 1
                    
                    x_momentum = float(tower_tokens[token_index])
                    token_index += 1
                    
                    y_momentum = float(tower_tokens[token_index])
                    token_index += 1
                    
                    self.balls.append(Ball(ball_type, x_pos, y_pos, x_momentum, y_momentum, in_structure=False))
                    self.total_balls += 1

                elif ball_type == token_strand:
                    strand_type = tower_tokens[token_index]
                    token_index += 1

                    first_ball = self.balls[int(tower_tokens[token_index])]
                    first_ball.in_structure  = True
                    token_index += 1

                    second_ball = self.balls[int(tower_tokens[token_index])]
                    second_ball.in_structure = True
                    token_index += 1

                    connection_strength = float(tower_tokens[token_index])
                    token_index += 1

                    length = float(tower_tokens[token_index])
                    token_index += 1

                    ball_used = (tower_tokens[token_index] == "1")
                    token_index += 1

                    if ball_used:
                        self.used_strand_balls += 1
                        self.total_balls       += 1

                    self.strands.append(Strand(strand_type, first_ball, second_ball, connection_strength, length, ball_used))

                else:
                    raise IOError("Invalid tower element type " + ball_type)
                
        except (IndexError, IOError):
            #Can't parse tower string
            self.used_strand_balls = 0
            self.total_balls       = 0

        self.tower_height    = 0
        self.used_node_balls = 0

        for ball in self.balls:
            if ball.in_structure:
                self.used_node_balls += 1
                self.tower_height = max(ball.y_pos, self.tower_height)

        self.tower_height /= 100