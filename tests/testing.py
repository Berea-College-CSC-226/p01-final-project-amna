from shark_tester import SharkTester

def check(name, condition):
    print(f"{name}: {'PASSED' if condition else 'FAILED'}")


# MOVEMENT TESTS
def test_shark_moves_right():
    shark = SharkTester(800, 600)
    old = shark.x
    shark.direction = 1
    shark.update()
    check("Shark moves right", shark.x == old + shark.speed)

def test_shark_moves_left():
    shark = SharkTester(800, 600)
    old = shark.x
    shark.direction = -1
    shark.update()
    check("Shark moves left", shark.x == old - shark.speed)

# BOUNDARY TESTS
def test_left_boundary():
    shark = SharkTester(800, 600)
    shark.x = 0
    shark.direction = -1
    shark.update()
    check("Shark left boundary", shark.x == 90)

def test_right_boundary():
    shark = SharkTester(800, 600)
    shark.x = 900
    shark.direction = 1
    shark.update()
    check("Shark right boundary", shark.x == 800 - 90)

def run_all_tests():
    test_shark_moves_right()
    test_shark_moves_left()
    test_left_boundary()
    test_right_boundary()


if __name__ == "__main__":
    run_all_tests()
