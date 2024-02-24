// Import ml5.js library
const ml5 = require('ml5');

// Create a classifier
const classifier = ml5.textClassifier('NaiveBayes');

// Train the classifier
function trainClassifier() {
    // Load training data
    const trainingData = [
        { text: 'This website is safe', label: 'safe' },
        { text: 'This website contains malware', label: 'malicious' },
        // Add more training data here
    ];

    // Train the classifier
    classifier.train(trainingData, () => {
        console.log('Training complete');
    });
}

// Make a prediction
function predictWebsiteContent(content) {
    classifier.classify(content, (err, result) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log('Prediction:', result);
    });
}

// Train the classifier
trainClassifier();

// Example usage
const websiteContent = 'This website is safe';
predictWebsiteContent(websiteContent);
