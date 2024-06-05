import sympy as sp

def solve_equations(equations):
    # Parse the equations and extract the variables
    parsed_equations = [sp.sympify(eq) for eq in equations]
    variables = list(set().union(*[eq.free_symbols for eq in parsed_equations]))

    # Solve the system of equations
    solutions = sp.solve(parsed_equations, variables)

    return solutions

# Main function to take input from the user and solve the equations
if __name__ == "__main__":
    equations = []

    # Input the number of equations
    num_equations = int(input("Enter the number of equations: "))

    # Input each equation
    for i in range(num_equations):
        eq = input(f"Enter equation {i + 1}: ")
        equations.append(eq)

    # Solve the equations
    solutions = solve_equations(equations)

    # Print the solutions
    if solutions:
        print("Solutions:")
        # Check the type of the solutions and handle accordingly
        if isinstance(solutions, dict):
            for var, val in solutions.items():
                print(f"{var} = {val}")
        elif isinstance(solutions, list):
            for sol in solutions:
                if isinstance(sol, dict):
                    for var, val in sol.items():
                        print(f"{var} = {val}")
                else:
                    print(sol)
        else:
            print(solutions)
    else:
        print("No solution found or infinite solutions exist.")
