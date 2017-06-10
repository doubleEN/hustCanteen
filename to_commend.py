from math import sqrt


def euclidean_distance(data_dict, canteen1, canteen2):
    '''
    :param data_dict: the dict including comments from user about canteen
    :param canteen1: the string index of one cantenn. 
    :param canteen2: the string index of another cantenn.
    :return: the euclidean distance of the two canteens.
    '''
    si = {}

    # find the common user of two canteens.
    for user in data_dict[canteen1]:
        if user in data_dict[canteen2]:
            si[user] = 1
    # if two canteens have no ratings in common, return 0
    if len(si) == 0:
        return 0

    # calculate the euclidean distance
    sum_of_squares = sum([pow(data_dict[canteen1][user] - data_dict[canteen2][user], 2)
                          for user in data_dict[canteen1] if user in data_dict[canteen2]])
    # let the distance be in 0.0 to 1.0
    return 1 / (1 + sum_of_squares)


def sim_pearson(data_dict, canteen1, canteen2):
    '''
    :param data_dict: the dict including comments from user about canteen
    :param canteen1: the string index of one cantenn. 
    :param canteen2: the string index of another cantenn.
    :return: the pearson correlation coefficient  of the two canteens value in(-1,1).
    '''
    si = {}
    for item in data_dict[canteen1]:
        if item in data_dict[canteen2]: si[item] = 1

    # if they are no ratings in common, return 0
    if len(si) == 0: return 0

    # Sum calculations
    n = len(si)

    # Sums of all the preferences
    sum1 = sum([data_dict[canteen1][it] for it in si])
    sum2 = sum([data_dict[canteen2][it] for it in si])

    # Sums of the squares
    sum1Sq = sum([pow(data_dict[canteen1][it], 2) for it in si])
    sum2Sq = sum([pow(data_dict[canteen2][it], 2) for it in si])

    # sum of the products
    pSum = sum([data_dict[canteen1][it] * data_dict[canteen2][it] for it in si])

    # Calculate  pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r


def matchers(data_dict, canteen, n=5, similarity=sim_pearson):
    '''
    :param data_dict: the dict including comments from user about canteen
    :param canteen: the target canteen
    :param n: the number of similar cantten of target canteen
    :param similarity: the function of distance
    :return: the list of top n canteens
    '''
    scores = [(similarity(data_dict, canteen, other), other)
              for other in data_dict if other != canteen]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def recommendations(data_dict, canteen, similarity=sim_pearson):
    '''
    :param data_dict: the dict including comments from user about canteen
    :param canteen: the target canteen
    :param similarity: the function of distance
    :return: the scores of every users to the target canteen
    '''
    totals = {}
    simSums = {}
    # other canteens
    for other in data_dict:
        # don't compare  itself
        if other == canteen:
            continue
        sim = similarity(data_dict, canteen, other)
        # ignore scores of zero or lower(the pearson value may be negative)
        if sim <= 0:
            continue

        for user in data_dict[other]:
            if user not in data_dict[canteen] or data_dict[canteen][user] == 0:
                # Similarity * Score
                totals.setdefault(user, 0)
                totals[user] += data_dict[other][user] * sim
                # Sum of similarities
                simSums.setdefault(user, 0)
                simSums[user] += sim
    # Create the normalized list
    rankings = [(total / simSums[user], user) for user, total in totals.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def calculate_similar_canteen(data_dict, n=10):
    '''
    :param data_dict: the dict including comments from user about canteen
    :param n: the n most similar canteen
    :return: the similarity of every canteen
    '''
    result = {}
    c = 0
    for canteen in data_dict:
        c += 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(data_dict)))
        scores = matchers(data_dict, canteen, n=n, similarity=euclidean_distance)
        result[canteen] = scores
    return result


if __name__ == "__main__":
    import handle_data

    print("mian")
    data_comments = handle_data.comments

    sim_canteens = matchers(data_comments, "华中科技大学东教工食堂")
    print(sim_canteens)
    # print(calculate_similar_canteen(data_comments))
