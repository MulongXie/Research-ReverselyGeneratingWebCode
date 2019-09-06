from MODEL import CNN

# build model
model = CNN()
# model.train(data)
# model.evaluate(data)
model.predict(['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png'], show=True)