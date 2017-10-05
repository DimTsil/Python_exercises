import requests  # https://github.com/requests/requests
import json


def get_response(city):  # Retrieving data for a specific town
    url = 'https://api.teleport.org/api/cities/?search=' + city
    response = requests.get(url).json()
    return response


def correct_city(response): # Checking if the user's input town exists and returning its link in order to fetch its ratings
    while True:
        data = response['_embedded']['city:search-results']
        count = response['count']
        if count == 0:
            print('No such city, try again\n')
            city = input('Give a city again: ')
            response = get_response(city)
        elif count > 1:
            print('--------------------------------')
            for i in range(0, count):
                print(data[i]['matching_full_name'])
            print('--------------------------------')
            print('Plenty of cities with the same name, specify state and/or country by comma\n')
            print('Example: Athens, Attica, Greece\n')
            city = input('Give the name of the city again: ')
            response = get_response(city)
        else:
            href = data[0]['_links']['city:item']['href']
            if exist_rating(href):
                return href, response
            else:
                print("There are not any ratings for {} city".format(data[0]['matching_full_name']))
                exit(0)


def exist_rating(href):         # There are towns that they don't have any ratings, thus this functions search for it
    link = requests.get(href).json()
    if 'city:urban_area' in link['_links']:
        return True
    return False


def get_city_score(href):       # Fetching the data which consist of the score that a town has
    link = requests.get(href).json()
    link2scores = link['_links']['city:urban_area']['href'] + 'scores'
    list_of_scores = requests.get(link2scores).json()
    return list_of_scores


def compare_cities(score_1, score_2): # Counting on how many categories the towns surpass each other
    count1 = 0
    count2 = 0
    max_len = len(scores_1['categories'])
    for i in range(0, max_len):
        if score_1['categories'][i]['score_out_of_10'] > score_2['categories'][i]['score_out_of_10']:
            count1 += 1
        elif score_1['categories'][i]['score_out_of_10'] < score_2['categories'][i]['score_out_of_10']:
            count2 += 1
        else:
            pass
    return count1, count2


if __name__ == '__main__':
    city_1 = input('Give the name of a city: ')
    response_1 = get_response(city_1)
    href_city_1, response_1 = correct_city(response_1)
    # Taking the full name of the first city e.g. Athens, Attica, Greece and putting it in a list
    city_name_1 = str(response_1['_embedded']['city:search-results'][0]['matching_full_name']).split(", ")
    city_2 = input('Give the name of the other city: ')
    print('\n')
    response_2 = get_response(city_2)
    href_city_2, response_2 = correct_city(response_2)
    # Taking the full name of the second city e.g. Athens, Attica, Greece and putting it in a list
    city_name_2 = str(response_2['_embedded']['city:search-results'][0]['matching_full_name']).split(", ")
    scores_1 = get_city_score(href_city_1)
    scores_2 = get_city_score(href_city_2)

    #  Comparing the cities by their score on each category and printing the results

    if scores_1['teleport_city_score'] > scores_2['teleport_city_score']:
        count_1, count_2 = compare_cities(scores_1, scores_2)

        # Printing on how many categories the first town surpasses the second one
        print('{} surpasses {} in {} out of 17 categories\n'.format(
            city_name_1[0],
            city_name_2[0],
            count_1))
        # Printing on how many categories the second town surpasses the first one
        print('{} surpasses {} in {} out of 17 categories\n'.format(
            city_name_2[0],
            city_name_1[0],
            count_2))
        # Printing which town has overall the better score
        print('Generally, {}({},{}) surpasses {}({},{})'.format(
            city_name_1[0], city_name_1[1], city_name_1[2],
            city_name_2[0], city_name_2[1], city_name_2[2]))
    else:
        count_2, count_1 = compare_cities(scores_2, scores_1)

        # Printing on how many categories the second town surpasses the first one
        print('{} surpasses {} in {} out of 17 categories\n'.format(
            city_name_2[0],
            city_name_1[0],
            count_2))

        # Printing on how many categories the first town surpasses the second one
        print('{} surpasses {} in {} out of 17 categories\n'.format(
            city_name_1[0],
            city_name_2[0],
            count_1))
        # Printing which town has overall the better score
        print('Generally, {}({},{}) surpasses {}({},{})'.format(
            city_name_2[0], city_name_2[1], city_name_2[2],
            city_name_1[0], city_name_1[1], city_name_1[2]))
