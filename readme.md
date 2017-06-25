A voice convertion demo based on the paper  
[VOICE CONVERSION USING DEEP BIDIRECTIONAL LONG SHORT-TERM MEMORYBASED RECURRENT NEURAL NETWORKS]()

### Dependencies
* [STRAIGHT](https://github.com/petronny/STRAIGHT)
* [SPTK](http://sp-tk.sourceforge.net/)
* [Keras](https://github.com/fchollet/keras)
* [Theano](https://github.com/Theano/Theano)
* wget

### Usage

* Clone the repository
```
git clone https://github.com/petronny/vc-icassp2015
```
* Initialize submodules
```
cd vc-icassp2015
git submodule init
```
* Clean up
```
./run.sh 0
```
* Download the corpus
```
./run.sh 1
```
* Extract features
```
./run.sh 2 3
```
* Dynamic time wrapping
```
./run.sh 4
```
* Split datasets
```
./run.sh 5
```
* Concatenating features for neural networks
```
./run.sh 6
```
* Train the models
```
./run.sh 7 10
```
* Test the models
```
./run.sh 11
```
* Run all steps above
```
./run.sh 0 11
```
