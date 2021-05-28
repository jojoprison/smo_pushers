import numpy as np

""" Draws a random number from given probability density function.
Parameters ---------- 
pdf -- the function pointer to a probability density function of form P = pdf(x)
interval -- the resulting random number is restricted to this interval
pdfmax -- the maximum of the probability density function
integers -- boolean, indicating if the result is desired as integer
max_iterations -- maximum number of 'tries' to find a combination of
random numbers (rand_x, rand_y) located below the function value
calc_y = pdf(rand_x). returns a single random number according the
pdf distribution. """


def draw_random_number_from_pdf(interval, integers=False, max_iterations=10000):
    for i in range(max_iterations):
        if integers:
            rand_x = np.random.randint(interval[0], interval[1])
        else:
            rand_x = (interval[1] - interval[0]) * np.random.random(1) + interval[0]

        print(rand_x)

        # (b - a) * random_sample() + a rand_y = pdfmax * np.random.random(1)
        # calc_y = pdf(rand_x)
        # if(rand_y <= calc_y ):
        # return rand_x
        # raise Exception("Could not find a matching random number within pdf in " + max_iterations + " iterations.")


if __name__ == '__main__':
    draw_random_number_from_pdf([0, 1])
