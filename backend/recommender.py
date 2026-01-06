def recommend_classes(user_style, user_level, classes):
    recommendations = []

    for c in classes:
        score = 0

        if c.style.lower() == user_style.lower():
            score += 2

        if c.level.lower() == user_level.lower():
            score += 1

        if score > 0:
            recommendations.append({
                "title": c.title,
                "style": c.style,
                "level": c.level,
                "score": score
            })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return recommendations
