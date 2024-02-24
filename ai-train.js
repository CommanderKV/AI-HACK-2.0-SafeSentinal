// Import ml5.js library
//const ml5 = require('ml5js');

// Create a classifier
const options = {
    inputs: ["content", "threat"],
    outputs: [0, 1, 2],
    task: "classification",
    debug: true
}
const neuralNetwork = ml5.neuralNetwork(options);

// Training data
trainingData = [
    {
        "content": "This website is safe",
        "threat": 0
    },
    {
        "content": "This website is unsafe",
        "threat": 2
    },
    {
        "content": "This website is suspicious",
        "threat": 1
    },
    {
        "content": "This website is safe",
        "threat": 0
    },
    {
        "content": "This website is unsafe",
        "threat": 2
    },
    {
        "content": "This website is suspicious",
        "threat": 1
    },
    {
        "content": "This website is safe",
        "threat": 0
    },
    {
        "content": "This website is unsafe",
        "threat": 2
    },
    {
        "content": "This website is suspicious",
        "threat": 1
    },
    {
        "content": "This website is safe",
        "threat": 0
    },
    {
        "content": "This website is unsafe",
        "threat": 2
    },
    {
        "content": "This website is suspicious",
        "threat": 1
    },
    {
        "content": "This website is safe",
        "threat": 0
    },
    {
        "content": "This website is unsafe",
        "threat": 2
    },
    {
        "content": "This website is suspicious",
        "threat": 1
    }
]

neuralNetwork.addData(trainingData);

// Train the classifier
neuralNetwork.train(trainingData, () => {
    console.log('Training complete');
});

// Make a prediction
function predictWebsiteContent(content) {
    neuralNetwork.classify(content, (err, result) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log('Prediction:', result);
    });
}


// Example usage
const websiteContent = 'This website is safe';
predictWebsiteContent(websiteContent);
