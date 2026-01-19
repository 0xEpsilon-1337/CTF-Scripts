#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

jmp_buf env[5];
int launched[5];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

int read_int(char *prompt) {
    int x;
    printf("%s > ", prompt);
    scanf("%d", &x);
    for (;getchar() != '\n';);
    return x;
}

void notepad() {
    void *_[99]; // padding
    char *buf = malloc(0x1000);//pointer on stack
    if (buf == NULL) {
        return;
    }
    if (setjmp(env[1]) != 0) {
        printf("saved content: %s\n", buf);//read
    }
    for (;;) {
        int q = read_int("1: edit, 0: save and quit");
        if (q == 0) {
            longjmp(env[0], 1);
        } else {
            printf("enter the content > ");
            fgets(buf, 0x1000, stdin);//arbitrary write using this
        }
    }
}

void pwquiz() {
    void *_[100]; // padding
    char *hints[3] = {
        "Hint 1: an English word",
        "Hint 2: length is 8",
        "Hint 3: the most used password in the world"
    };//pointer on stack

    setjmp(env[2]);

    for (;;) {
        int q = read_int("1~3: hint, 4: answer, 0: quit");
        if (q == 0) {
            longjmp(env[0], 1);
        } else if (1 <= q && q <= 3) {
            printf("%s\n", hints[q-1]);//read
        } else if (q == 4) {
            char buf[16];
            printf("answer > ");
            scanf("%15s", buf);//can be used to change notepad buffer address
            if (strcmp("password", buf) == 0) {
                puts("Congraturations!!!");
                longjmp(env[0], 123456);
            } else {
                puts("...");
            }
        }
    }
}

struct board {
    int board[16];
    int sx;
    int sy;
};

void move(struct board *b, char m) {
    if (b->sx < 0 || 3 < b->sx || b->sy < 0 || 3 < b->sy) {
        return;
    }
    switch (m) { // left, down, up, right
        case 'a': // left
            if (b->sx < 3) {
                b->board[b->sy*4 + b->sx] = b->board[b->sy*4 + b->sx + 1];
                b->sx++;
            }
            break;
        case's': // down
            if (b->sy > 0) {
                b->board[b->sy*4 + b->sx] = b->board[(b->sy-1)*4 + b->sx];
                b->sy--;
            }
            break;
        case 'w': // up
            if (b->sy < 3) {
                b->board[b->sy*4 + b->sx] = b->board[(b->sy+1)*4 + b->sx];
                b->sy++;
            }
            break;
        case 'd': // right
            if (b->sx > 0) {
                b->board[b->sy*4 + b->sx] = b->board[b->sy*4 + b->sx - 1];
                b->sx--;
            }
            break;
        default:
            break;
    }
}

void print_board(struct board *b) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (i == b->sy && j == b->sx) {
                printf("[] ");
            } else {
                printf("%02d ", b->board[i*4+j]);
            }
        }
        puts("");
    }
}

int judge(struct board *b) {
    for (int i = 0; i < 15; i++) {
        if (b->board[i] != i) {
            return 0;
        }
    }
    return 1;
}

void slide_puzzle() {
    srand(time(NULL));
    void *_[100]; // padding
    struct board b = {{}, 3, 3};
    for (int i = 0; i < 16; i++) {
        b.board[i] = i;
    }

    // randomize board
    for (int i = 0; i < 100; i++) {
         move(&b, "aswd"[rand()%4]);
    }

    // move space to bottom-right
    move(&b, 'a');
    move(&b, 'a');
    move(&b, 'a');
    move(&b, 'w');
    move(&b, 'w');
    move(&b, 'w');

    setjmp(env[3]);

    for (;;) {
        print_board(&b);
        printf("a: left, s: down, w: up, d: right, q: save and quit > ");
        char c = getchar();
        if (c == 'q') {
            longjmp(env[0], 1);
        } else if (c != '\n') {
            move(&b, c);
            if (judge(&b)) {
                print_board(&b);
                puts("Congraturations!");
                launched[3] = 0;
                longjmp(env[0], 1);
            }
        }
    }
}

void int_float_translater() {
    void *_[94]; // padding
    unsigned long num;//pointer on stack
    char *__ = alloca(100); // padding 2

    setjmp(env[4]);

    for (;;) {
        int q = read_int("1: uint64 to float64, 2: float64 to uint64, 0: quit");
        switch (q) {
            case 1:
                printf("num(uint64) > ");
                scanf("%ld", &num);
                for (;getchar() != '\n';);
                printf("%1$ld = %2$f = %2$e\n", num, *(double *)&num);
                break;
            case 2:
                printf("num(float64) > ");
                scanf("%lf", (double *)&num);
                for (;getchar() != '\n';);
                printf("%1$f = %2$ld = 0x%2$lx\n", *(double *)&num, num);
                break;
            case 0:
                longjmp(env[0], 1);
            default:
                break;
        }
    }
}

void *apps[5] = {NULL, notepad, pwquiz, slide_puzzle, int_float_translater};

void print_desktop() {
    puts("...");
    puts("1: notepad.exe");
    puts("2: password ate quiz ~returns~");
    puts("3: 4x4 slide puzzle");
    puts("4: int float translater");
    puts("0: exit TSG LAND");
}

int main() {
    init();
    puts("Welcome to TSG LAND!!!");
    int res = setjmp(env[0]);
    if (res == 123456) {
        puts("You are pw-ate-quiz m@ster!");
    } else if (res != 0) {
        puts("Welcome back!");
    }

    for (;;) {
        print_desktop();
        int q = read_int("May I help you?");
        if (q <= -1 || 5 <= q) {
            puts("invalid command");
        } else if (q == 0) {
            puts("bye");
            exit(0);
        } else {
            if (launched[q]) {
                longjmp(env[q], 1);
            } else {
                launched[q] = 1;
                ((void(*)())apps[q])();
            }
        }
    }
}
