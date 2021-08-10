import mdptoolbox
import numpy as np

IRRELEVANT, RELEVANT, ACTIVE = 0, 1, 2

ADOPT, OVERRIDE, WATI, MATCH = 0, 1, 2, 3


def get_index(a, h, f, rounds, fork_states_num):
    # A * rounds * fork_states_num + H * fork_states_num + F
    return a * rounds * fork_states_num + h * fork_states_num + f


def generate_probability_matrix(states_num, action_num, rounds, fork_states_num):

    P = np.zeros([states_num, states_num, action_num])
    # the structure of probability is (A, H, F)
    # irrelevant = 0, relevant =1, active = 2
    # (0, 0, 0)
    # (0, 0, 1)
    # (0, 0, 2)
    # (0, 1, 0)
    # (0, 1, 1)
    # (0, 1, 2)
    # ...
    # (0, 75, 2)
    # (1, 0, 0)

    # probability under action adopt.
    # with probablity alpha to (1, 0, IRRELEVANT) position
    adversary_height, honest_height = 1, 0
    index_column_current = get_index(adversary_height, honest_height,
                                     IRRELEVANT, rounds, fork_states_num)
    P[:, index_column_current, ADOPT] = alpha
    # with probablity 1 - alpha to (0, 1, IRRELEVANT) I am not sure if it should be (0, 1, RELEVANT)
    # 可能是错的。
    adversary_height, honest_height = 0, 1
    index_column_current = get_index(adversary_height, honest_height,
                                     IRRELEVANT, rounds, fork_states_num)
    P[:, index_column_current, ADOPT] = 1-alpha

    # probability under action override.
    # only works for a > h.
    # I am wrong at the first attempt. PLZ remember it !!!
    for a in range(0, rounds-1):
        for h in range(0, rounds-1):
            if a > h:
                index_row_begin = get_index(
                    a, h, IRRELEVANT, rounds, fork_states_num)
                index_row_end = get_index(
                    a, h, ACTIVE, rounds, fork_states_num)

                # with probablity alpha to ((a - h), 0, 0).
                index_column_current = get_index(
                    (a-h), 0, IRRELEVANT, rounds, fork_states_num)
                P[index_row_begin:index_row_end+1,
                    index_column_current, OVERRIDE] = alpha

                # with probablity alpha to ((a - h - 1), 1, 1).
                index_column_current = get_index(
                    (a-h-1), 1, RELEVANT, rounds, fork_states_num)
                P[index_row_begin:index_row_end+1,
                    index_column_current, OVERRIDE] = 1-alpha

    # probability under action wait.
    for a in range(0, rounds-1):
        for h in range(0, rounds-1):
            # IRRELEVANT
            index_row = get_index(
                a, h, IRRELEVANT, rounds, fork_states_num)
            P[index_row, get_index(
                a+1, h, IRRELEVANT, rounds, fork_states_num), WATI] = alpha
            P[index_row, get_index(
                a, h+1, RELEVANT, rounds, fork_states_num), WATI] = 1-alpha

            # RELEVANT
            index_row += 1
            P[index_row, get_index(
                a+1, h, IRRELEVANT, rounds, fork_states_num), WATI] = alpha
            P[index_row, get_index(
                a, h+1, RELEVANT, rounds, fork_states_num), WATI] = 1-alpha

            # ACTIVE
            index_row += 1
            P[index_row, get_index(
                a+1, h, ACTIVE, rounds, fork_states_num), WATI] = alpha
            #  这里错了，要注意。
            P[index_row, get_index(
                a-h, 1, RELEVANT, rounds, fork_states_num), WATI] = gamma*(1-alpha)
            P[index_row, get_index(
                a, h+1, RELEVANT, rounds, fork_states_num), WATI] = (1-gamma)*(1-alpha)

    # probability under action match.
    for a in range(0, rounds-1):
        for h in range(0, rounds-1):
            if a >= h:
                index_row = get_index(
                    a, h, RELEVANT, rounds, fork_states_num)
                P[index_row, get_index(
                    a+1, h, ACTIVE, rounds, fork_states_num), MATCH] = alpha
                P[index_row, get_index(
                    a-h, 1, RELEVANT, rounds, fork_states_num), MATCH] = gamma*(1-alpha)
                P[index_row, get_index(
                    a, h+1, RELEVANT, rounds, fork_states_num), MATCH] = (1-gamma)*(1-alpha)
    return P


def generate_reward_matrix(states_num, action_num, rounds, fork_states_num, rho):
    R = np.zeros([states_num, states_num, action_num])
    # reward under action adopt.
    
    # reward under action override.
    # reward under action wait.
    # reward under action match.


if __name__ == "__main__":
    low, high, epsilon = 0, 1, pow(10, -5)
    rounds = 76
    # There are three different fork for the sanme height combination.
    states_num = rounds*rounds*3
    action_num = 4
    alpha, gamma = 0.45, 0.5
    rho = (low+high)/2
    fork_states_num = 3
    # generate P.
    # four actions: adopt, override, wait, match.

    P = generate_probability_matrix(
        states_num, action_num, rounds, fork_states_num)
    R = generate_reward_matrix(
        states_num, action_num, rounds, fork_states_num)
    # while high-low > epsilon:
    #     rho = (low+high)/2

    #     # generate Reward with different rho.

    # rewaird under action adopt.
    # rewaird under action override.
    # rewaird under action wait.
    # rewaird under action match.
    #     R = np.array([[5, 10], [-1, 2]])

    #     max_iter = 1000
    #     vi = mdptoolbox.mdp.RelativeValueIteration(P, R, max_iter=max_iter)
    #     vi.run()
    #     print(vi.policy)