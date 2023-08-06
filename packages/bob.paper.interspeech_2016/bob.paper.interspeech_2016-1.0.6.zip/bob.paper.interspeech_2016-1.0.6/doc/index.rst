.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Thu 23 Jun 13:43:22 2016

=================================================
 Reproducing paper published in Interspeech 2016
=================================================

This package is part of the Bob_ toolkit, which allows to reproduce the results experiments published in the following paper::

    @inproceedings{KorshunovInterspeech2016,
        author = {P. Korshunov AND S. Marcel},
        title = {Cross-database evaluation of audio-based spoofing detection systems},
        year = {2016},
        month = sep,
        booktitle = {Interspeech},
        pages={1705--1709},
        address = {San Francisco, CA, USA},
    }


Installation
------------

Follow our `installation`_ instructions for installing ``conda`` and core Bob_ packages.

Also, install ``bob.bio.*``, ``bob.pad.*``, and database packages by running::

    $ conda install bob.bio.base bob.bio.spear bob.bio.gmm bob.pad.base bob.pad.voice bob.db.avspoof bob.db.asvspoof

Then, using the Python from the installed conda environment, bootstrap and buildout this package::

    $ python bootstrap-buildout.py
    $ ./bin/buildout


Running all experiments from scratch
------------------------------------

This package contains basic scripts to run Presentation Attack Detection (PAD) speech experiments presented in the paper.
It uses ``bob.bio.*`` and ``bob.pad.*`` packages from Bob framework, as well as, Bob's database interfaces for AVspoof_
and ASVspoof_ databases that are defined in ``bob.db.avspoof`` and ``bob.db.asvspoof`` packages. All these packages are
assumed to be installed using ``conda`` environment or built using ``buildout``.

The provided experimental pipeline scripts take several parameters, including:

* A database and its evaluation protocol
* A data preprocessing algorithm
* A feature extraction algorithm
* A classifier (to train or evaluate)

All these steps of the PAD system are given as configuration files.

To run all the experiments, two databases need to be downloaded: AVspoof_ and ASVspoof_.

Once the databases are downloaded, please specify the paths to these databases by creating/editing file
``~/.bob_bio_databases.txt`` and writing in it the following two lines:

    $ [YOUR_AVSPOOF_WAV_DIRECTORY]=/absolute/path/to/avspoof/database/
    $ [YOUR_ASVSPOOF_WAV_DIRECTORY]=/absolute/path/to/asvspoof/database/

By using ``~/.bob_bio_databases.txt`` file, where path placeholders are replaced with real paths, bob's framework
packages can find the data needed for the experiments.

GMM models for ``real`` and ``spoofed`` data are trained as per this generic command::

    $ ./bin/train_gmm.py -d DB_NAME -p Preprocessor -e Feature_Extractor -a Classifier -s Folder_Name --groups world --skip-enroller-training -vv --parallel 6

This training may take a long time and as the results, it will generate GMM model and write it into ``Projector.hdf5``
file. You can check all possible options by running ``$ ./bin/train_gmm.py --help``.

Here is the generic command for tuning the trained system on developing set and evaluate on the test set::

    $ ./bin/spoof.py -d DB_NAME -p Preprocessor -e Feature_Extractor -a Classifier --projector-file Projector_spoof.hdf5 -s Folder_Name --groups dev eval --skip-projector-training -vv

For example, to train and evaluate a GMM-based PAD system using MFCC-based features computed for
``licit`` and ``spoof`` protocols of the ASVspoof database, the following commands need to be run::

    $ ./bin/train_gmm.py -d asvspoof-licit -p mod-4hz -e mfcc20 -a gmm-tomi -s temp --groups world --projector-file Projector_licit.hdf5 --skip-enroller-training -vv --parallel 6
    $ ./bin/train_gmm.py -d asvspoof-spoof -p mod-4hz -e mfcc20 -a gmm-tomi -s temp --groups world --projector-file Projector_spoof.hdf5 --skip-enroller-training -vv --parallel 6
    $ ./bin/spoof.py -d asvspoof -p mod-4hz -e mfcc20 -a gmm --projector-file Projector_spoof.hdf5 -s temp --groups dev eval --skip-projector-training -vv
    
Here, ``./bin/train_gmm.py`` produces two GMM models, one for ``licit`` protocol (real data only) and one for ``spoof``
protocol (spoofed data only). Then, ``./bin/spoof.py`` is used to project all data from ``dev`` and ``eval`` sets onto
these two GMM models and compute corresponding scores.

Once the scores are obtained, error rates and DET curves can be computed using the following script::

    $ ./bin/plot_pad_results.py -t scores_path/dev-attack -d scores_path/dev-real -f scores_path/eval-attack -e scores_path/eval-real -o plots"

Also, it is possible to reproduce the experiments presented in the paper using the following bash scripts that run for all
PAD systems used in the paper (note that these scripts assume SGE grid to be available and will take a few days on 50
parallel machines)::

    $ ./train_gmms.sh avspoof 20  # train for AVspoof database
    $ ./train_gmms.sh asvspoof 20  # train for ASVspoof database
    $ ./project_on_gmms.sh avspoof 20  # evaluate for AVspoof database
    $ ./project_on_gmms.sh asvspoof 20  # evaluate for ASVspoof database


Generate results from pre-computed scores
-----------------------------------------

If you want to avoid training all PAD systems and computing scores, we are providing the score files obtained for all the PAD systems presented in the paper. Hence, the error rates can be computed, as per Tables 1, 2, and 3 of the paper, and additional DET curves can be plotted by simply performing the following::

    $ #You should be inside the package directory bob.paper.interspeech_2016
    $ wget http://www.idiap.ch/resource/biometric/data/interspeech_2016.tar.gz #Download the scores
    $ tar -xzvf interspeech_2016.tar.gz  
    $ ./evaluate_scores.sh # compute error rates and plot the DET curves for each PAD system

The script will create folders for each different PAD system (it contains computed error rates and DET curves)
and one ``stats.txt`` file with error rates from all systems in one LaTeX table.

To plot combined DET curves for different systems as per Figure 2 of the paper, the following script can be run::

    $ ./plot_pad_diff_methods.sh  # plot DET curves for selected PAD systems as in Figure 2

This script will plot several DET curves in a single PDF file inside the folder ``plots_compare_pads``.

.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _AVspoof: https://www.idiap.ch/dataset/avspoof
.. _ASVspoof: http://datashare.is.ed.ac.uk/handle/10283/853

