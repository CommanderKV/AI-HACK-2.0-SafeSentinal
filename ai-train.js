// Import TensorFlow.js library
// Create a sequential model
const model = tf.sequential();

const safeText = "This website is safe. proceed";
const susText = "This website is sus. proceed with caution";
const unsafeText = "This website is unsafe. do not proceed";

// Training data
const trainOnMe = [
    {
        text: safeText,
        threat: 0
    },
    {
        text: susText,
        threat: 1
    },
    {
        text: unsafeText,
        threat: 2
    }
];

// Add more training data to make it 50 in length
for (let i = 0; i < 97; i++) {
    trainOnMe.push({
        text: safeText,
        threat: 0
    });
    if (i > 30) {
        trainOnMe.push({
            text: susText,
            threat: 1
        });
    }
    trainOnMe.push({
        text: unsafeText,
        threat: 2
    });
}

function scaleData(data) {
    const maxThreat = Math.max(...data.map(text => text.threat));
    const scaledData = data.map(text => {
        const scaledThreat = text.threat / (maxThreat + 1); // Add 1 to avoid division by zero
        return {
            text: text.text,
            threat: scaledThreat
        };
    });
    return scaledData;
}


// Scale the training data
const scaledData = scaleData(trainOnMe);
const scaledTrainingData = tf.tensor2d(scaledData.map(item => {
    const textToNumber = item.text.split('').map(char => char.charCodeAt(0));
    return [...textToNumber, item.threat];
}), [scaledData.length, 3]); // Reshape the tensor to have shape [scaledData.length, 3]

// Add layers to the model
model.add(tf.layers.dense({
    units: 3,
    activation: 'relu',
    inputShape: [3]
}));
model.add(tf.layers.dense({
    units: 3,
    activation: 'relu'
}));
model.add(tf.layers.dense({
    units: 3,
    activation: 'relu'
}));
model.add(tf.layers.dense({
    units: 3, // Change the number of units to 3
    activation: 'sigmoid' // Change the activation function to 'sigmoid'
}));

// Compile the model
model.compile({
    optimizer: "sgd",
    loss: 'meanSquaredError',
    metrics: ['accuracy']
});

const targetData = tf.tensor2d([
    [1, 0, 0], // Safe
    [0, 1, 0], // Sus
    [0, 0, 1], // Unsafe
    [0, 0, 0]  // Unknown
]);

// Adjust the target data to match the number of input samples
const adjustedTargetData = tf.tile(targetData, [scaledTrainingData.shape[0] / targetData.shape[0], 1]);

// Train the model
const trainingOptions = {
    epochs: 5,
    batchSize: 32,
    validationSplit: 0.2,
    shuffle: true
};

model.fit(scaledTrainingData, adjustedTargetData, trainingOptions)
    .then((info) => {
        console.log('Training completed');
        predictWebsiteContent();
        console.log(`Final accuracy${info.history.acc}`);
    })
    .catch((error) => {
        console.error('Training failed:', error);
    });

// Make a prediction
function predictWebsiteContent() {
    var testData = [
        {
            text: safeText
        }
    ];
    const content = tf.tensor2d(scaleData(testData));
    const predictions = model.predict(content);
    predictions.print();

    const predictionValues = predictions.arraySync()[0];
    const predictionLabels = ['Safe', 'Sus', 'Unsafe'];
    const maxPredictionIndex = predictionValues.indexOf(Math.max(...predictionValues));
    const predictedLabel = predictionLabels[maxPredictionIndex];
    console.log(`Predicted label: ${predictedLabel}`);
}

console.log(model.summary());
