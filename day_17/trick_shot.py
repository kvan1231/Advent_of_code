# https://adventofcode.com/2021/day/17

import re

"""
We're solving a projectile here and we can do P1 without any complex coding

P1. What is the highest y position possible?

A1. Since the projectile starts at (0, 0) and there is a gravity force
pulling the projectile down by a_y = -1, the maximum height depends only on the
initial y velocity. The y velocity is bounded by the constraint that if the
probe is moving too fast then it does not appear in the ocean trench in any
step so our y velocity has a maximum value.

Due to the projectile motion in this problem, when the probe comes back down
and crosses through y=0, its velocity will be v_y0 = -v_i, or it will be moving
downards at the same speed as when we launched it up. The very next step will
have a velocity of v_y1 = v_y0 - 1 since the gravitational force in this
problem tries to pull our probe downwards. This velocity can only be so
large so that it remains bounded by our landing zone when it makes this
change, so putting this all together, the maximum height is given by:

h_max = abs(y_min) * abs(y_min + 1) // 2

"""

input_file = "input.txt"
with open("input.txt") as f:
    input_data = f.read()

x_min, x_max, y_min, y_max = [
    int(num) for num in re.findall(r'[-\d]+', input_data)
]

h_max = abs(y_min) * abs(y_min + 1) // 2


"""
To find every intial velocity that remains bounded to the box we can follow a
similar logic to above where we found the maximum height, we know that the
probe must be bounded by the landing zone. There is horizontal drag so
a_x = -1 and again, due to gravity a_y = -1. For our y velocity we know
it must be smaller than the velocity used to calculate h_max, and our x
velocity must be small enough to not overshoot the trench while being large
enough to reach the trench.
"""


def find_valid_velocities(x_min, x_max, y_min, y_max):
    """
    The bounds for our velocities should be:

        x direction
        ===========
        The lower bound is given by the initial velocity where we reach the
        target location and then stop. This can be solved by the equation
        
            v_f^2 = v_i^2 + 2 a (x_f - x_i)

        Solving for v_i
            v_i = sqrt(v_f^2 - 2 a [x_f - x_i])

        Our final variables are:
            v_f = 0
            a = -1
            x_f = x_min
            x_i = 0

            v_i = sqrt(2 * 235)
            v_i ~ 22

        The upper bound will be the initial velocity where we reach the
        target locations upper bound in a single step.

            22 <= v_x <= xmax

        y direction
        ===========
        The lower bound is the velocity where we shoot the projectile downwards
        at the target. This still works as long as the x velocity is high
        enough so the projectile enters the box in one step. The upper bound is
        the one that represents the maximum height.

            -abs(ymin) <= v_y <= abs(ymin)
    """

    # with these bounds known, lets loop through all combinations
    # of v_x and v_y and check if they're in the limits

    v_count = 0
    # all of our initial x velocities
    for init_x_vel in range(22, x_max + 1):
        # all of our initial y velocities
        for init_y_vel in range(y_min, abs(y_min)):

            x_vel = init_x_vel
            y_vel = init_y_vel

            x_pos = 0
            y_pos = 0

            while y_pos > y_min:
                # move the position
                x_pos += x_vel
                y_pos += y_vel

                # if the x velocity is greater than 0,
                # apply drag
                if x_vel > 0:
                    x_vel -= 1

                # apply gravity to the y velocity
                y_vel -= 1

                # check if our position is in the target
                x_pos_check = (x_min <= x_pos <= x_max)
                y_pos_check = (y_min <= y_pos <= y_max)

                # if we are
                if x_pos_check and y_pos_check:
                    # add to velocity count
                    v_count += 1
                    break

    return v_count


v_count = find_valid_velocities(x_min, x_max, y_min, y_max)

print("part 1 solution:", h_max)
print("part 2 solution:", v_count)
