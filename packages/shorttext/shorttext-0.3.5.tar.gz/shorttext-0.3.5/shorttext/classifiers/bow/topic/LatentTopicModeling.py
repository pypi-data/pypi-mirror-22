
#gensim_topic_model_dict = {'lda': LdaModel, 'lsi': LsiModel, 'rp': RpModel}
from shorttext.generators.bow.GensimTopicModeling import gensim_topic_model_dict

# abstract class
from generators.bow.LatentTopicModeling import LatentTopicModeler
# class LatentTopicModeler:
#     """
#     Abstract class for various topic modeler.
#     """
#     def __init__(self,
#                  preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                  normalize=True):
#         """ Initialize the modeler.
#
#         :param preprocessor: function that preprocesses the text. (Default: `shorttext.utils.textpreprocess.standard_text_preprocessor_1`)
#         :param normalize: whether the retrieved topic vectors are normalized. (Default: True)
#         :type preprocessor: function
#         :type normalize: bool
#         """
#         self.preprocessor = preprocessor
#         self.normalize = normalize
#         self.trained = False
#
#     def generate_corpus(self, classdict):
#         """ Calculate the gensim dictionary and corpus, and extract the class labels
#         from the training data. Called by :func:`~train`.
#
#         :param classdict: training data
#         :return: None
#         :type classdict: dict
#         """
#         self.dictionary, self.corpus, self.classlabels = gc.generate_gensim_corpora(classdict,
#                                                                                     preprocess_and_tokenize=lambda sent: tokenize(self.preprocessor(sent)))
#
#     def train(self, classdict, nb_topics, *args, **kwargs):
#         """ Train the modeler.
#
#         This is an abstract method of this abstract class, which raise the `NotImplementedException`.
#
#         :param classdict: training data
#         :param nb_topics: number of latent topics
#         :param args: arguments to be passed into the wrapped training functions
#         :param kwargs: arguments to be passed into the wrapped training functions
#         :return: None
#         :raise: NotImplementedException
#         :type classdict: dict
#         :type nb_topics: int
#         """
#         self.nb_topics = nb_topics
#         raise e.NotImplementedException()
#
#     def retrieve_bow(self, shorttext):
#         """ Calculate the gensim bag-of-words representation of the given short text.
#
#         :param shorttext: text to be represented
#         :return: corpus representation of the text
#         :type shorttext: str
#         :rtype: list
#         """
#         return self.dictionary.doc2bow(tokenize(self.preprocessor(shorttext)))
#
#     def retrieve_bow_vector(self, shorttext, normalize=True):
#         """ Calculate the vector representation of the bag-of-words in terms of numpy.ndarray.
#
#         :param shorttext: short text
#         :param normalize: whether the retrieved topic vectors are normalized. (Default: True)
#         :return: vector represtation of the text
#         :type shorttext: str
#         :type normalize: bool
#         :rtype: numpy.ndarray
#         """
#         bow = self.retrieve_bow(shorttext)
#         vec = np.zeros(len(self.dictionary))
#         for id, val in bow:
#             vec[id] = val
#         if normalize:
#             vec /= np.linalg.norm(vec)
#         return vec
#
#     def retrieve_topicvec(self, shorttext):
#         """ Calculate the topic vector representation of the short text.
#
#         This is an abstract method of this abstract class, which raise the `NotImplementedException`.
#
#         :param shorttext: short text
#         :return: topic vector
#         :raise: NotImplementedException
#         :type shorttext: str
#         :rtype: numpy.ndarray
#         """
#         raise e.NotImplementedException()
#
#     def get_batch_cos_similarities(self, shorttext):
#         """ Calculate the cosine similarities of the given short text and all the class labels.
#
#         This is an abstract method of this abstract class, which raise the `NotImplementedException`.
#
#         :param shorttext: short text
#         :return: topic vector
#         :raise: NotImplementedException
#         :type shorttext: str
#         :rtype: numpy.ndarray
#         """
#         raise e.NotImplementedException()
#
#     def __getitem__(self, shorttext):
#         return self.retrieve_topicvec(shorttext)
#
#     def __contains__(self, shorttext):
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         return True
#
#     def loadmodel(self, nameprefix):
#         """ Load the model from files.
#
#         This is an abstract method of this abstract class, which raise the `NotImplementedException`.
#
#         :param nameprefix: prefix of the paths of the model files
#         :return: None
#         :raise: NotImplementedException
#         :type nameprefix: str
#         """
#         raise e.NotImplementedException()
#
#     def savemodel(self, nameprefix):
#         """ Save the model to files.
#
#         This is an abstract method of this abstract class, which raise the `NotImplementedException`.
#
#         :param nameprefix: prefix of the paths of the model files
#         :return: None
#         :raise: NotImplementedException
#         :type nameprefix: str
#         """
#         raise e.NotImplementedException()


from shorttext.generators.bow.GensimTopicModeling import GensimTopicModeler
# class GensimTopicModeler(LatentTopicModeler):
#     """
#     This class facilitates the creation of topic models (options: LDA (latent Dirichlet Allocation),
#     LSI (latent semantic indexing), and Random Projections
#     with the given short text training data, and convert future
#     short text into topic vectors using the trained topic model.
#
#     No compact model I/O available for this class. Refer to
#     :class:`LDAModeler` and :class:`LSIModeler`.
#
#     This class extends :class:`LatentTopicModeler`.
#     """
#     def __init__(self,
#                  preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                  algorithm='lda',
#                  toweigh=True,
#                  normalize=True):
#         """ Initialize the topic modeler.
#
#         :param preprocessor: function that preprocesses the text. (Default: `utils.textpreprocess.standard_text_preprocessor_1`)
#         :param algorithm: algorithm for topic modeling. Options: lda, lsi, rp. (Default: lda)
#         :param toweigh: whether to weigh the words using tf-idf. (Default: True)
#         :param normalize: whether the retrieved topic vectors are normalized. (Default: True)
#         :type preprocessor: function
#         :type algorithm: str
#         :type toweigh: bool
#         """
#         LatentTopicModeler.__init__(self, preprocessor=preprocessor, normalize=normalize)
#         self.algorithm = algorithm
#         self.toweigh = toweigh
#
#     def train(self, classdict, nb_topics, *args, **kwargs):
#         """ Train the topic modeler.
#
#         :param classdict: training data
#         :param nb_topics: number of latent topics
#         :param args: arguments to pass to the `train` method for gensim topic models
#         :param kwargs: arguments to pass to the `train` method for gensim topic models
#         :return: None
#         :type classdict: dict
#         :type nb_topics: int
#         """
#         self.nb_topics = nb_topics
#         self.generate_corpus(classdict)
#         if self.toweigh:
#             self.tfidf = TfidfModel(self.corpus)
#             normcorpus = self.tfidf[self.corpus]
#         else:
#             self.tfidf = None
#             normcorpus = self.corpus
#
#         self.topicmodel = gensim_topic_model_dict[self.algorithm](normcorpus,
#                                                                   num_topics=self.nb_topics,
#                                                                   *args,
#                                                                   **kwargs)
#         self.matsim = MatrixSimilarity(self.topicmodel[normcorpus])
#
#         # change the flag
#         self.trained = True
#
#     def retrieve_corpus_topicdist(self, shorttext):
#         """ Calculate the topic vector representation of the short text, in the corpus form.
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param shorttext: text to be represented
#         :return: topic vector in the corpus form
#         :raise: ModelNotTrainedException
#         :type shorttext: str
#         :rtype: list
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         bow = self.retrieve_bow(shorttext)
#         return self.topicmodel[self.tfidf[bow] if self.toweigh else bow]
#
#     def retrieve_topicvec(self, shorttext):
#         """ Calculate the topic vector representation of the short text.
#
#         This function calls :func:`~retrieve_corpus_topicdist`.
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param shorttext: text to be represented
#         :return: topic vector
#         :raise: ModelNotTrainedException
#         :type shorttext: str
#         :rtype: numpy.ndarray
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         topicdist = self.retrieve_corpus_topicdist(shorttext)
#         topicvec = np.zeros(self.nb_topics)
#         for topicid, frac in topicdist:
#             topicvec[topicid] = frac
#         if self.normalize:
#             topicvec /= np.linalg.norm(topicvec)
#         return topicvec
#
#     def get_batch_cos_similarities(self, shorttext):
#         """ Calculate the score, which is the cosine similarity with the topic vector of the model,
#         of the short text against each class labels.
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param shorttext: short text
#         :return: dictionary of scores of the text to all classes
#         :raise: ModelNotTrainedException
#         :type shorttext: str
#         :rtype: dict
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         simdict = {}
#         similarities = self.matsim[self.retrieve_corpus_topicdist(shorttext)]
#         for label, similarity in zip(self.classlabels, similarities):
#             simdict[label] = similarity
#         return simdict
#
#     def loadmodel(self, nameprefix):
#         """ Load the topic model with the given prefix of the file paths.
#
#         Given the prefix of the file paths, load the corresponding topic model. The files
#         include a JSON (.json) file that specifies various parameters, a gensim dictionary (.gensimdict),
#         and a topic model (.gensimmodel). If weighing is applied, load also the tf-idf model (.gensimtfidf).
#
#         :param nameprefix: prefix of the file paths
#         :return: None
#         :type nameprefix: str
#         """
#         # load the JSON file (parameters)
#         parameters = json.load(open(nameprefix+'.json', 'rb'))
#         self.nb_topics = parameters['nb_topics']
#         self.toweigh = parameters['toweigh']
#         self.algorithm = parameters['algorithm']
#         self.classlabels = parameters['classlabels']
#
#         # load the dictionary
#         self.dictionary = Dictionary.load(nameprefix+'.gensimdict')
#
#         # load the topic model
#         self.topicmodel = gensim_topic_model_dict[self.algorithm].load(nameprefix + '.gensimmodel')
#
#         # load the similarity matrix
#         self.matsim = MatrixSimilarity.load(nameprefix+'.gensimmat')
#
#         # load the tf-idf modek
#         if self.toweigh:
#             self.tfidf = TfidfModel.load(nameprefix+'.gensimtfidf')
#
#         # flag
#         self.trained = True
#
#     def savemodel(self, nameprefix):
#         """ Save the model with names according to the prefix.
#
#         Given the prefix of the file paths, save the corresponding topic model. The files
#         include a JSON (.json) file that specifies various parameters, a gensim dictionary (.gensimdict),
#         and a topic model (.gensimmodel). If weighing is applied, load also the tf-idf model (.gensimtfidf).
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param nameprefix: prefix of the file paths
#         :return: None
#         :raise: ModelNotTrainedException
#         :type nameprefix: str
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         parameters = {}
#         parameters['nb_topics'] = self.nb_topics
#         parameters['toweigh'] = self.toweigh
#         parameters['algorithm'] = self.algorithm
#         parameters['classlabels'] = self.classlabels
#         json.dump(parameters, open(nameprefix+'.json', 'wb'))
#
#         self.dictionary.save(nameprefix+'.gensimdict')
#         self.topicmodel.save(nameprefix+'.gensimmodel')
#         self.matsim.save(nameprefix+'.gensimmat')
#         if self.toweigh:
#             self.tfidf.save(nameprefix+'.gensimtfidf')


# lda_suffices =  ['.json', '.gensimdict', '.gensimmodel.state',
#                    '.gensimtfidf', '.gensimmodel', '.gensimmat']
# if gensim.__version__ >= '1.0.0':
#     lda_suffices += ['.gensimmodel.expElogbeta.npy', '.gensimmodel.id2word']

from shorttext.generators.bow.GensimTopicModeling import LDAModeler
# @cio.compactio({'classifier': 'ldatopic'}, 'ldatopic', lda_suffices)
# class LDAModeler(GensimTopicModeler):
#     """
#     This class facilitates the creation of LDA (latent Dirichlet Allocation) topic models,
#     with the given short text training data, and convert future
#     short text into topic vectors using the trained topic model.
#
#     This class extends :class:`GensimTopicModeler`.
#     """
#     def __init__(self,
#                  preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                  toweigh=True,
#                  normalize=True):
#         GensimTopicModeler.__init__(self,
#                                     preprocessor=preprocessor,
#                                     algorithm='lda',
#                                     toweigh=toweigh,
#                                     normalize=normalize)

# lsi_suffices = ['.json', '.gensimdict', '.gensimtfidf', '.gensimmodel.projection',
#                 '.gensimmodel', '.gensimmat', ]

from shorttext.generators.bow.GensimTopicModeling import LSIModeler
# @cio.compactio({'classifier': 'lsitopic'}, 'lsitopic', lsi_suffices)
# class LSIModeler(GensimTopicModeler):
#     """
#     This class facilitates the creation of LSI (latent semantic indexing) topic models,
#     with the given short text training data, and convert future
#     short text into topic vectors using the trained topic model.
#
#     This class extends :class:`GensimTopicModeler`.
#     """
#     def __init__(self,
#                  preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                  toweigh=True,
#                  normalize=True):
#         GensimTopicModeler.__init__(self,
#                                     preprocessor=preprocessor,
#                                     algorithm='lsi',
#                                     toweigh=toweigh,
#                                     normalize=normalize)

# rp_suffices = ['.json', '.gensimtfidf', '.gensimmodel', '.gensimmat', '.gensimdict']

from shorttext.generators.bow.GensimTopicModeling import RPModeler
# @cio.compactio({'classifier': 'rptopic'}, 'rptopic', rp_suffices)
# class RPModeler(GensimTopicModeler):
#     """
#     This class facilitates the creation of RP (random projection) topic models,
#     with the given short text training data, and convert future
#     short text into topic vectors using the trained topic model.
#
#     This class extends :class:`GensimTopicModeler`.
#     """
#     def __init__(self,
#                  preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                  toweigh=True,
#                  normalize=True):
#         GensimTopicModeler.__init__(self,
#                                     preprocessor=preprocessor,
#                                     algorithm='rp',
#                                     toweigh=toweigh,
#                                     normalize=normalize)


# autoencoder_suffices = ['.gensimdict', '_encoder.json', '_encoder.h5', '_classtopicvecs.pkl',
#                         '_decoder.json', '_decoder.h5', '_autoencoder.json', '_autoencoder.h5',
#                         '.json']

from generators.bow.AutoEncodingTopicModeling import AutoencodingTopicModeler, load_autoencoder_topicmodel
# @cio.compactio({'classifier': 'kerasautoencoder'}, 'kerasautoencoder', autoencoder_suffices)
# class AutoencodingTopicModeler(LatentTopicModeler):
#     """
#     This class facilitates the topic modeling of input training data using the autoencoder.
#
#     A reference about how an autoencoder is written with keras by Francois Chollet, titled
#     `Building Autoencoders in Keras
#     <https://blog.keras.io/building-autoencoders-in-keras.html>`_ .
#
#     This class extends :class:`LatentTopicModeler`.
#     """
#     def train(self, classdict, nb_topics, *args, **kwargs):
#         """ Train the autoencoder.
#
#         :param classdict: training data
#         :param nb_topics: number of topics, i.e., the number of encoding dimensions
#         :param args: arguments to be passed to keras model fitting
#         :param kwargs: arguments to be passed to keras model fitting
#         :return: None
#         :type classdict: dict
#         :type nb_topics: int
#         """
#         self.nb_topics = nb_topics
#         self.generate_corpus(classdict)
#         vecsize = len(self.dictionary)
#
#         # define all the layers of the autoencoder
#         input_vec = Input(shape=(vecsize,))
#         encoded = Dense(self.nb_topics, activation='relu')(input_vec)
#         decoded = Dense(vecsize, activation='sigmoid')(encoded)
#
#         # define the autoencoder model
#         autoencoder = Model(input=input_vec, output=decoded)
#
#         # define the encoder
#         encoder = Model(input=input_vec, output=encoded)
#
#         # define the decoder
#         encoded_input = Input(shape=(self.nb_topics,))
#         decoder_layer = autoencoder.layers[-1]
#         decoder = Model(input=encoded_input, output=decoder_layer(encoded_input))
#
#         # compile the autoencoder
#         autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
#
#         # process training data
#         embedvecs = np.array(reduce(add,
#                                     [map(lambda shorttext: self.retrieve_bow_vector(shorttext, normalize=True),
#                                          classdict[classtype])
#                                      for classtype in classdict]
#                                     )
#                              )
#
#         # fit the model
#         autoencoder.fit(embedvecs, embedvecs, *args, **kwargs)
#
#         # store the autoencoder models
#         self.autoencoder = autoencoder
#         self.encoder = encoder
#         self.decoder = decoder
#
#         # flag setting
#         self.trained = True
#
#         # classes topic vector precomputation
#         self.classtopicvecs = {}
#         for label in classdict:
#             self.classtopicvecs[label] = self.precalculate_liststr_topicvec(classdict[label])
#
#     def retrieve_topicvec(self, shorttext):
#         """ Calculate the topic vector representation of the short text.
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param shorttext: short text
#         :return: encoded vector representation of the short text
#         :raise: ModelNotTrainedException
#         :type shorttext: str
#         :rtype: numpy.ndarray
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         bow_vector = self.retrieve_bow_vector(shorttext)
#         encoded_vec = self.encoder.predict(np.array([bow_vector]))[0]
#         if self.normalize:
#             encoded_vec /= np.linalg.norm(encoded_vec)
#         return encoded_vec
#
#     def precalculate_liststr_topicvec(self, shorttexts):
#         """ Calculate the summed topic vectors for training data for each class.
#
#         This function is called while training.
#
#         :param shorttexts: list of short texts
#         :return: average topic vector
#         :raise: ModelNotTrainedException
#         :type shorttexts: list
#         :rtype: numpy.ndarray
#         """
#         sumvec = sum(map(self.retrieve_topicvec, shorttexts))
#         sumvec /= np.linalg.norm(sumvec)
#         return sumvec
#
#     def get_batch_cos_similarities(self, shorttext):
#         """ Calculate the score, which is the cosine similarity with the topic vector of the model,
#         of the short text against each class labels.
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param shorttext: short text
#         :return: dictionary of scores of the text to all classes
#         :raise: ModelNotTrainedException
#         :type shorttext: str
#         :rtype: dict
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#         simdict = {}
#         for label in self.classtopicvecs:
#             simdict[label] = 1 - cosine(self.classtopicvecs[label], self.retrieve_topicvec(shorttext))
#         return simdict
#
#     def savemodel(self, nameprefix, save_complete_autoencoder=True):
#         """ Save the model with names according to the prefix.
#
#         Given the prefix of the file paths, save the model into files, with name given by the prefix.
#         There are files with names ending with "_encoder.json" and "_encoder.h5", which are
#         the JSON and HDF5 files for the encoder respectively. They also include a gensim dictionary (.gensimdict).
#
#         If `save_complete_autoencoder` is True,
#         then there are also files with names ending with "_decoder.json" and "_decoder.h5".
#
#         If neither :func:`~train` nor :func:`~loadmodel` was run, it will raise `ModelNotTrainedException`.
#
#         :param nameprefix: prefix of the paths of the file
#         :param save_complete_autoencoder: whether to store the decoder and the complete autoencoder (Default: True; but False for version <= 0.2.1)
#         :return: None
#         :type nameprefix: str
#         :type save_complete_autoencoder: bool
#         """
#         if not self.trained:
#             raise e.ModelNotTrainedException()
#
#         parameters = {}
#         parameters['nb_topics'] = self.nb_topics
#         parameters['classlabels'] = self.classlabels
#         json.dump(parameters, open(nameprefix+'.json', 'wb'))
#
#         self.dictionary.save(nameprefix+'.gensimdict')
#         kerasio.save_model(nameprefix+'_encoder', self.encoder)
#         if save_complete_autoencoder:
#             kerasio.save_model(nameprefix+'_decoder', self.decoder)
#             kerasio.save_model(nameprefix+'_autoencoder', self.autoencoder)
#         pickle.dump(self.classtopicvecs, open(nameprefix+'_classtopicvecs.pkl', 'w'))
#
#     def loadmodel(self, nameprefix, load_incomplete=False):
#         """ Save the model with names according to the prefix.
#
#         Given the prefix of the file paths, load the model into files, with name given by the prefix.
#         There are files with names ending with "_encoder.json" and "_encoder.h5", which are
#         the JSON and HDF5 files for the encoder respectively.
#         They also include a gensim dictionary (.gensimdict).
#
#         :param nameprefix: prefix of the paths of the file
#         :param load_incomplete: load encoder only, not decoder and autoencoder file (Default: False; put True for model built in version <= 0.2.1)
#         :return: None
#         :type nameprefix: str
#         :type load_incomplete: bool
#         """
#         # load the JSON file (parameters)
#         parameters = json.load(open(nameprefix+'.json', 'rb'))
#         self.nb_topics = parameters['nb_topics']
#         self.classlabels = parameters['classlabels']
#
#         self.dictionary = Dictionary.load(nameprefix + '.gensimdict')
#         self.encoder = kerasio.load_model(nameprefix+'_encoder')
#         self.classtopicvecs = pickle.load(open(nameprefix+'_classtopicvecs.pkl', 'r'))
#         if not load_incomplete:
#             self.decoder = kerasio.load_model(nameprefix+'_decoder')
#             self.autoencoder = kerasio.load_model(nameprefix+'_autoencoder')
#         self.trained = True

from shorttext.generators import load_gensimtopicmodel
# def load_gensimtopicmodel(name,
#                           preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                           compact=True):
#     """ Load the gensim topic modeler from files.
#
#     :param name: name (if compact=True) or prefix (if compact=False) of the file path
#     :param preprocessor: function that preprocesses the text. (Default: `shorttext.utils.textpreprocess.standard_text_preprocessor_1`)
#     :param compact: whether model file is compact (Default: True)
#     :return: a topic modeler
#     :type name: str
#     :type preprocessor: function
#     :type compact: bool
#     :rtype: GensimTopicModeler
#     """
#     if compact:
#         modelerdict = {'ldatopic': LDAModeler, 'lsitopic': LSIModeler, 'rptopic': RPModeler}
#         classifier_name = str(cio.get_model_classifier_name(name))
#
#         topicmodeler = modelerdict[classifier_name](preprocessor=preprocessor)
#         topicmodeler.load_compact_model(name)
#         return topicmodeler
#     else:
#         topicmodeler = GensimTopicModeler(preprocessor=preprocessor)
#         topicmodeler.loadmodel(name)
#         return topicmodeler

from shorttext.generators import load_autoencoder_topicmodel as load_autoencoder_topic
# def load_autoencoder_topic(name,
#                            preprocessor=textpreprocess.standard_text_preprocessor_1(),
#                            compact=True):
#     """ Load the autoencoding topic model from files.
#
#     :param name: name (if compact=True) or prefix (if compact=False) of the paths of the model files
#     :param preprocessor: function that preprocesses the text. (Default: `shorttext.utils.textpreprocess.standard_text_preprocessor_1`)
#     :param compact: whether model file is compact (Default: True)
#     :return: an autoencoder as a topic modeler
#     :type name: str
#     :type preprocessor: function
#     :type compact: bool
#     :rtype: AutoencodingTopicModeler
#     """
#     autoencoder = AutoencodingTopicModeler(preprocessor=preprocessor)
#     if compact:
#         autoencoder.load_compact_model(name)
#     else:
#         autoencoder.loadmodel(name)
#     return autoencoder
