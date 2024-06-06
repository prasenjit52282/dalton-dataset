# Distributed Air quaLiTy mONitor (DALTON)
Sample Dataset for H1, H2, and H3 is shared in /SampleDataset folder

1. Merge replicas for a customer with
    * python merge_replicas.py --customer NAME

2. Preprocess for a customer with
    * python preprocess_data.py --customer NAME --workers #cpus

3. Mark BreakPoints in the data
    * python mark_breakpoints.py --customer NAME --workers #cpus  [--plot]

4. Mark breakpoints for annotation from MongoDB
    * python annotate.py --customer SP --date 2023/05/11 --DID 93
    #### Annotate multiple devices with bash script 
    bash annotPrev.sh CUSTOMER DAYAGO DID1 DID2 ... DIDN
    * bash annotPrev.sh SP 1 93 94  #(tag for 93 94 one day ago)

5. Tag Current Deployments
    * bash annotPrev.sh SP 1 93 94
    * bash annotPrev.sh Home 1 41 42 43 44 45
    * OR RUN
        - bash annotTask.sh

6. Plot motvation plots
    * python plot_motivation.py --export [png|pdf|eps|svg]

7. Compute Features
    * python compute_feat.py --customer NAME --workers #cpus

8. Compute HHI
    * python compute_hhi.py --customer NAME --DID d1 d2 d3

    python compute_hhi.py --customer CUST1 --DID 41 42 43 44 45
    python compute_hhi.py --customer CUST1 --DID 62 63 61
    python compute_hhi.py --customer CUST1 --DID 12 14 11 13 15 17