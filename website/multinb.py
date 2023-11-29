import numpy as np


class MultiNB:
    def __init__(self, alpha=1.0):
        self.prior = None
        self.jumlah_kata = None
        self.total_kata = None
        self.likelihood_kata = None
        self.predict_prob = None
        self.alpha = alpha
        
    def fit(self, x, y):
        '''
        Latih fitur dan label
        Menghitung hal-hal berikut :
            prior : Menghitung probabilitas banyaknya kelas c terhadap jumlah seluruh kelas dalam dokumen
            jumlah_kata : Menghitung jumlah kata yang muncul dalam dokumen pada kelas c terhadap kata unik
            likelihood_kata : likelihood dari setiap kata terhadap kelas c || P(Xi|y) = P(w1|y) * P(w2|y) ... * P(wn|y)
        '''
        jumlah_sample = x.shape[0]

        # Mengambil label unik dari y_train
        classes = np.unique(y)

        # Memisahkan x_train menjadi per kelas
        x_kelas = []
        for c in classes:
            x_kelas.append(x[y == c])

        x_per_kelas = np.array(x_kelas, dtype=object)

        # Menghitung prior
        # Menghitung jumlah kata
        prior = []
        jumlah_kata = []
        for x_kelas in x_per_kelas:
            prior.append(len(x_kelas) / jumlah_sample)
            jumlah_kata.append(x_kelas.sum(axis=0) + self.alpha)    # Laplace Smoothing dengan menambahkan alpha yaitu bernilai 1
        self.prior = np.array(prior)
        self.jumlah_kata = np.array(jumlah_kata)
        
        # Menghitung likelihood untuk setiap kata (likelihood_kata)
        self.total_kata = self.jumlah_kata.sum(axis=1).reshape(-1, 1)   # Menjumlahkan seluruh jumlah_kata
        self.likelihood_kata = self.jumlah_kata / self.total_kata       # Menghitung nilai likelihood || P(w1|y), ..., P(wn|y)
        
        return self
    
    def _get_class_numerators(self, x):
        '''
        Menghitung setiap kelas, likelihood seluruh teks kondisional pada teks bergantung pada kelas c (positif atau negatif)

        Menghitung hal-hal berikut:
            kata_muncul : kemunculan kata pada x_test
            likelihood_kata : likelihood dari setiap kata terhadap kelas c || P(Xi|y) = P(w1|y) * P(w2|y) ... * P(wn|y)
            likelihood_kata_kini : likelihood dari setiap kata terhadap kelas c yang sedang berlangsung dalam iterasi
            likelihood_teks : likelihood dari seluruh teks terhadap kelas c || P(x|y) = P(Xi|y)
            class_numerators : Perhitungan posterior untuk setiap kelas c
        '''
        n, m = x.shape[0], self.prior.shape[0]
        
        class_numerators = np.zeros(shape=(n, m))
        for i, kata in enumerate(x):
  
            kata_muncul = kata.astype(bool)     # Mengubah value kata menjadi boolean
            likelihood_kata_kini = self.likelihood_kata[:, kata_muncul] ** kata[kata_muncul]    # Mengambil likelihood dari kata muncul
            likelihood_teks = (likelihood_kata_kini).prod(axis=1)   # Mengalikan seluruh nilai dalam likelihood_kata_kini
            class_numerators[i] = likelihood_teks * self.prior      # Mengalikan likelihood dengan prior (posterior) || P(x|y) = P(y) * P(Xi|y)
        
        return class_numerators
    
    def _normalized_conditional_probs(self, class_numerators):
        '''
        Conditional probabilities = class_numerators / normalize_term
        '''
        # normalize term merupakan likelihood dari seluruh teks (penambahan dari seluruh kata dalam satu baris) || P(x)
        normalize_term = class_numerators.sum(axis=1).reshape(-1,1)
        conditional_probs = class_numerators / normalize_term
        
        return conditional_probs
    
    def predict_proba(self, x):
        '''
        Return the probabilities for each class (fake or real)
        Return probabilitas dari setiap kelas (positif atau negatif)
        '''
        class_numerators = self._get_class_numerators(x)
        conditional_probs = self._normalized_conditional_probs(class_numerators)
        self.predict_prob = conditional_probs

        return conditional_probs
    

    def predict(self, x):
        '''
        Return the answer with the highest probability (argmax)
        Return hasil nilai dengan probabilitas tertinggi (argmax)
        '''
        return self.predict_proba(x).argmax(axis=1)