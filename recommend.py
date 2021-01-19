def find_match(places_crosstab,place):
    a = places_crosstab.loc[:,place]
    similar_to_Tortas = places_crosstab.corrwith(a)
    recommendations = similar_to_Tortas.sort_values()
    return recommendations

def SuggestSmilar(recommendations):
    recommendations = recommendations[recommendations>0.5]
    return recommendations.sample(n = 1)

def SuggestDifferent(recommendations):
    recommendations = recommendations[recommendations<0.5]
    return recommendations.sample(n = 1)