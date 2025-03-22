from chaos import Order
import json


text = """
- This is a basic example of using the Chaos entropy analyzer package.
- With Chaos, you can analyze the entropy of text data and gain insights.
- With these insights, you can improve your data processing pipelines.
- With improved data processing, you can build better machine learning models.
- With better machine learning models, you can make more accurate predictions.
- With accurate predictions, you can make better decisions.
- With better decisions, you can achieve your goals faster.
- By achieving your goals faster, you can unlock new opportunities.
- By unlocking new opportunities, you can improve your revenue and save costs.
- By improving your revenue and saving costs, you can grow your business.
- By growing your business, you can create value for your customers.
- By creating value for your customers, you can build a successful company.
"""

if __name__ == "__main__":
    print("Initializing Chaos (Order) in few seconds...")
    chaos = Order()
    print("Chaos Version:", chaos.version())
    print(f"Analyzing text data entropy of {len(text)} characters.")
    stats = chaos.get_stats(text)
    print(json.dumps(stats, indent=4))
