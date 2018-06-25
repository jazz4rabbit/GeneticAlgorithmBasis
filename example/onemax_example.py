from ga_pkg import ga
from ga_pkg import problem

if __name__ == "__main__":
    model = problem.onemax.from_setting(n=20, IND_SIZE=10)
    run_model, logbook = ga.run(model, 5)

    if not __debug__: # if not debug mode
        print(logbook)
