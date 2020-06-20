from models.collaborative import DependencyFinder


class RecommendationGenerator:

    def get_generated_recommendations(self):
        pass


class CollaborativeRecommendationGenerator(RecommendationGenerator):

    def __init__(self, products, sessions):
        self.generated_recommendation = None
        self.dependency_finder = DependencyFinder(products)
        self.sessions = sessions

    def generate_recommendation(self, session):
        self.dependency_finder.parse_sessions_to_find_dependencies(self.sessions)
        dependencies = self.dependency_finder.dependencies


