from app import app, db
from app.models import User, Score, Waste_category, Income_category, Waste, Income

@app.shell_context_processor
def make_shell_context():
	return {
	'db': db, 
	'User': User,
	'Score': Score,
	'Waste_category': Waste_category,
	'Income_category': Income_category.
	'Waste': Waste,
	'Income': Income
	}