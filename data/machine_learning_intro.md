# Introduction to Machine Learning

## What is Machine Learning?

Machine Learning (ML) is a subset of artificial intelligence that enables
systems to learn and improve from experience without being explicitly
programmed. Instead of writing rules, we feed data to algorithms that
learn patterns automatically.

## Types of Machine Learning

### Supervised Learning

The model learns from **labeled data** - input-output pairs where the correct
answer is known.

- **Classification**: Predicting a category (spam vs not spam)
- **Regression**: Predicting a number (house price, temperature)

Common algorithms: Linear Regression, Decision Trees, Random Forests,
Support Vector Machines, Neural Networks.

### Unsupervised Learning

The model learns from **unlabeled data** - finding hidden patterns without
predefined answers.

- **Clustering**: Grouping similar items (customer segments)
- **Dimensionality Reduction**: Simplifying data while keeping structure

Common algorithms: K-Means, DBSCAN, PCA, Autoencoders.

### Reinforcement Learning

An agent learns by **trial and error**, receiving rewards or penalties for
its actions. Used in game playing, robotics, and autonomous driving.

## The ML Workflow

1. **Collect data** - Gather relevant examples
2. **Clean data** - Handle missing values, remove outliers
3. **Feature engineering** - Select and transform input variables
4. **Choose a model** - Pick an algorithm suitable for the problem
5. **Train the model** - Feed data and let it learn patterns
6. **Evaluate** - Test on unseen data to measure performance
7. **Tune** - Adjust parameters to improve results
8. **Deploy** - Put the model into production

## Neural Networks

Inspired by the human brain, neural networks are layers of connected nodes
(neurons) that process information.

- **Input layer**: Receives raw features
- **Hidden layers**: Transform data through weighted connections
- **Output layer**: Produces the prediction

**Deep learning** uses networks with many hidden layers. It powers modern
AI breakthroughs like image recognition, natural language processing, and
generative AI (including LLMs like Gemini).

## Common Metrics

- **Accuracy**: Percentage of correct predictions
- **Precision**: Of predicted positives, how many are actually positive
- **Recall**: Of actual positives, how many did we find
- **F1 Score**: Harmonic mean of precision and recall
- **RMSE**: Root Mean Squared Error (for regression)

## Popular Python Libraries

- **NumPy** - Numerical computing and array operations
- **Pandas** - Data manipulation and analysis
- **Scikit-learn** - Traditional ML algorithms
- **TensorFlow** - Deep learning by Google
- **PyTorch** - Deep learning by Meta
- **Matplotlib** - Data visualization
