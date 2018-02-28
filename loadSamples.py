from glob import glob
from os.path import basename
from numpy import append
from scipy.sparse import vstack
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_svmlight_file

def loadSamples(folder_path, file_wildcard, size=None):
    ''' Method that loads all the samples from the files in folder_path whose filename corresponds to file_wildcard.
        The size parameter can be used to load a uniformly sampled subset of the overall samples in the current folder.
        Parameters
        ----------
        folder_path : string
                    path to the folder that contains the sample files
        file_wildcard : string
                    file name wildcard
        size : float, int, or None, default None
        If float, should be between 0.0 and 1.0 and represent the
        proportion of the dataset to include in the train split. If
        int, represents the absolute number of train samples. If None,
        the value is automatically set to the complement of the test size.
        
        Returns
        -------
        samples : tuple (samples, class labels, file labels)
                Returns the loaded samples with relative class labels and 
                the file labels (PDB ids).        
    '''
    X = y = None
    labels = []
    files = glob(folder_path + file_wildcard)
    for f in sorted(files):
        print "Loading %s..." % basename(f) 
        X_f, y_f = load_svmlight_file(f, zero_based=False)
        if size is not None :
            X_f, _, y_f, _ = train_test_split(X_f, y_f, train_size=size, stratify = y_f)
        if X is None:
            X = X_f
            y = y_f
        else :
            X = vstack([X, X_f], "csr")
            y = append(y, y_f)
        current_label = basename(f)[:4]
        labels += [current_label] * y_f.size
    return (X, y, labels)
