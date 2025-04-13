## Info

- Convolutional Neural Network (ResNet50 architecture)
- Custom Colorado plant dataset using iNaturalist API (CC BY-NC)
  - Open source if used non commercially
-  434 classes (species) and ~180,000 features (images)
  - Each class ranges from 400-600 images per
- 80/20 training/validation split
- Final performance metrics on validation dataset for model after initial training and two stages of gradual fine tuning:
  - val_accuracy: 0.9223 (92.2%)
  - val_loss: 0.3364
- Dataset available (raw or .tfrecord) upon request
- If using model for custom tests, a good photo for identification is one that is close to the plant so that other plants are limited or removed from the image
