// Import TensorFlow.js library
// Create a sequential model
const model = tf.sequential();

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
    units: 1,
    activation: 'sigmoid'
}));

// Compile the model
model.compile({
    optimizer: 'adam',
    loss: 'binaryCrossentropy',
    metrics: ['accuracy']
});




// Training data
const trainOnMe = [
    {
        text: "This website is safe",
        threat: 0
    },
    {
        text: "This website is not sus",
        threat: 1
    },
    {
        text: "This website is unsafe",
        threat: 2
    }
]



const trainingData = tf.tensor2d(trainOnMe.map(text => [
    text.threat === 0 ? 1 : 0,
    text.threat === 1 ? 1 : 0,
    text.threat === 2 ? 1 : 0
]));
const targetData = tf.tensor2d([
    [0],
    [1],
    [2]
]);

// Train the model
const trainingOptions = {
    epochs: 32,
    batchSize: 4
};

model.fit(trainingData, targetData, trainingOptions)
    .then(() => {
        console.log('Training completed');
        predictWebsiteContent();
    })
    .catch((error) => {
        console.error('Training failed:', error);
    });

// Make a prediction
function predictWebsiteContent() {
    var testData = [{
        text: "This website is not sus",
        threat: 1
    }];
    const content = tf.tensor2d(
        testData.map(text => [
            text.threat === 0 ? 1 : 0,
            text.threat === 1 ? 1 : 0,
            text.threat === 2 ? 1 : 0
        ])
    );
    const predictions = model.predict(content);
    predictions.print();
}
