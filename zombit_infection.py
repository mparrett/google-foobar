"""
Zombit infection
================

Dr. Boolean continues to perform diabolical studies on your fellow rabbit kin,
and not all of it is taking place in the lab. Reports say the mad doctor has
his eye on infecting a rabbit in a local village with a virus that transforms
rabbits into zombits (zombie-rabbits)!

Professor Boolean is confident in the virus's ability to spread, and he will
only infect a single rabbit. Unfortunately, you and your fellow resistance
agents have no idea which rabbit will be targeted. You've been asked to predict
how the infection would spread if uncontained, so you decide to create a
simulation experiment. In this simulation, the rabbit that Dr. Boolean will
initially infect will be called "Patient Z".

So far, the lab experts have discovered that all rabbits contain a property
they call "Resistance", which is capable of fighting against the infection. The
virus has a particular "Strength" which Dr. Boolean needs to make at least as
large as the rabbits' Resistance for it to infect them.

You will be provided with the following information:
population = A 2D non-empty array of positive integers. (The dimensions of the
array are not necessarily equal.) Each cell represents one rabbit, and the
value of the cell represents that rabbit's Resistance. All cells contain a
rabbit.
x = The X-Coordinate (column) of "Patient Z" in the population array.
y = The Y-Coordinate (row) of "Patient Z" in the population array.
strength = A constant integer value representing the Strength of the virus.

Here are the rules of the simulation: First, the virus will attempt to infect
Patient Z. Patient Z will only be infected if the infection's Strength equals
or exceeds Patient Z's Resistance. From then on, any infected rabbits will
attempt to infect any uninfected neighbors (cells that are directly - not
diagonally - adjacent in the array). They will succeed in infecting any
neighbors with a Resistance lower than or equal to the infection's Strength.
This will continue until no further infections are possible (i.e., every
uninfected rabbit adjacent to an infected rabbit has a Resistance greater than
the infection's Strength.)

You will write a function answer(population, x, y, strength), which outputs a
copy of the input array representing the state of the population at the end of
the simulation, in which any infected cells value has been replaced with -1.
The Strength and Resistance values will be between 0 and 10000. The population
grid will be at least 2x2 and no larger than 50x50. The x and y values will be
valid indices in the population arrays, with numbering beginning from 0.
"""


def will_infect(population, x, y, strength):
  """
  Returns whether x, y can be infected with given infection strength
  Selects from 2D array by row, col
  """
  return strength >= population[y][x] and population[y][x] != -1


def infect(population, x, y, strength):
  """
  Returns a list of newly infected cells or an empty list
  Attempts to infect the existing population at x, y with
  given infection strength
  """

  infected = []
  if x > 0:
    if will_infect(population, x-1, y, strength):
      infected.append((x-1, y))

  if x < len(population[y]) - 1:
    if will_infect(population, x+1, y, strength):
      infected.append((x+1, y))

  if y > 0:
    if will_infect(population, x, y-1, strength):
      infected.append((x, y-1))

  if y < len(population) - 1:
    if will_infect(population, x, y+1, strength):
      infected.append((x, y+1))

  return infected


def simulate_infection(population, x, y, strength):
  """
  Returns the resulting population after multiple
  rounds of infection simulation starting at x, y
  with given infection strength
  """

  # Infect a 2D population array
  # Keep track of all infected cells
  infected = []

  # Starting with patient Z at x, y
  # Select from 2D array by row, col
  resistance = population[y][x]

  # Initial infection fails
  if strength < resistance:
    return population

  # Patient z infected
  population[y][x] = -1
  infected.append((x, y))

  # A cell can infect 0-4 of its neighbors
  # Loop and check all infected for new infections.
  # When there are no new infections we are done

  while True:
    newly_infected_count = 0

    # For all infected, possibly infect each neighbor
    for check_x, check_y in infected:
      newly_infected = infect(population, check_x, check_y, strength)
      # Keep track of how many infected this round
      newly_infected_count += len(newly_infected)

      # Flag as infected / prepare for output
      for infected_x, infected_y in newly_infected:
        population[infected_y][infected_x] = -1

      # Concatenate newly infected for subsequent check
      infected = infected + newly_infected

    # When no new infections happen we are done
    if newly_infected_count == 0:
      break

  # Return final state of population
  return population


def test_case_1():
  population = [[1, 2, 3], [2, 3, 4], [3, 2, 1]]
  x = 0
  y = 0
  strength = 2

  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[-1, -1, 3], [-1, 3, 4], [3, 2, 1]])


def test_case_2():
  population = [[6, 7, 2, 7, 6], [6, 3, 1, 4, 7], [0, 2, 4, 1, 10], [8, 1, 1, 4, 9], [8, 7, 4, 9, 9]]
  x = 2
  y = 1
  strength = 5

  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[6, 7, -1, 7, 6], [6, -1, -1, -1, 7], [-1, -1, -1, -1, 10], [8, -1, -1, -1, 9], [8, 7, -1, 9, 9]])


def test_case_3():
  """Test non-square population"""
  population = [[7, 2, 7, 6], [3, 1, 4, 7]]
  x = 1
  y = 1
  strength = 5
  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[7, -1, 7, 6], [-1, -1, -1, 7]])

  population = [[7, 2], [7, 6], [3, 1], [4, 7]]
  x = 0
  y = 0
  strength = 8
  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[-1, -1], [-1, -1], [-1, -1], [-1, -1]])


def test_case_4():
  """Test initial infection fails"""
  population = [[7, 2, 7, 6], [3, 1, 4, 7]]
  x = 1
  y = 1
  strength = 0
  final_population = simulate_infection(population, x, y, strength)
  assert(final_population != [[7, -1, 7, 6], [-1, -1, -1, 7]])


def test_case_5():
  """Test second infection fails"""
  population = [[9, 9, 9, 9], [9, 8, 9, 9]]
  x = 1
  y = 1
  strength = 8
  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[9, 9, 9, 9], [9, -1, 9, 9]])


def test_case_6():
  """Test 1x1 grid"""
  population = [[2]]
  x = 0
  y = 0
  strength = 8
  final_population = simulate_infection(population, x, y, strength)

  assert(final_population == [[-1]])

  population = [[2]]
  strength = 1
  final_population = simulate_infection(population, x, y, strength)
  assert(final_population == [[2]])


def test_case_7():
  """
  Create NxN array
  Attempt to infect all
  """
  N = 50

  x = 0
  y = 0
  strength = 10000
  population = [[0 for i in range(N)] for j in range(N)]
  final_population = simulate_infection(population, x, y, strength)

  assert sum([len([i for i in row if i == -1]) for row in final_population]) == N * N


def run_all_tests():
  test_case_1()
  test_case_2()
  test_case_3()
  test_case_4()
  test_case_5()
  test_case_6()
  test_case_7()


def answer(population, x, y, strength):
  return simulate_infection(population, x, y, strength)
