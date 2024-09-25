import curses
import redis
import time

REDIS_HOST = 'localhost'

def display_leaderboard(stdscr, redis_client):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)

    while True:
        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(1, 2, "Real-Time Leaderboard", curses.A_BOLD)

        leaderboard = redis_client.zrevrange('leaderboard', 0, -1, withscores=True)

        if not leaderboard:
            stdscr.addstr(3, 2, "No data available yet.", curses.A_DIM)
        else:
            for rank, (student_name, score) in enumerate(leaderboard, start=1):
                stdscr.addstr(3 + rank, 2, f"{rank}. {student_name.decode('utf-8')}: {int(score)}")

        stdscr.addstr(15, 2, "Press 'q' to quit.", curses.A_BOLD)
        key = stdscr.getch()
        if key == ord('q'):
            break

        stdscr.refresh()
        time.sleep(0.2)

def main(stdscr):
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    try:
        display_leaderboard(stdscr, redis_client)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    curses.wrapper(main)
