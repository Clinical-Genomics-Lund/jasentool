# Jasentool: A mongodb validation tool for comparing pipeline outputs
## Disclaimer: Jasentool was developed for the integration of [JASEN](https://github.com/Clinical-Genomics-Lund/jasentool) into [Clinical Genomics Lund](https://github.com/Clinical-Genomics-Lund). Jasentool's submethods are used as follows:
* Mongodb commands: `find`, `insert`, `remove`.
* Validate: Search old CGL bacterial pipeline database and compare results to JASEN results. 
* Missing: Search old CGL bacterial pipeline database and find sample results missing from JASEN output dir.
* Convert: Convert cgmlst.org target loci files to bed files.
* Converge: Converge tuberculosis mutation catlogues in order to add FoHM and tbdb catalogues to the WHO catalogue.
* Fix: Fix internal software's (bjorn's) generation of nextflow input csvs.
* QC: Create post alignment qc output.

## Dependencies (latest)
* python=3.11
* pymongo

## Using Jasentool
### Use the help argument for information regarding the Jasentool's methods
```
jasentool -h
```

### Use the method help argument for information regarding the input for each of Jasentool's methods (`find`, `insert`, `remove`, `validate`, `missing`, `fix`, `convert`, `converge`, `qc`)
```
jasentool <method> -h
```

### Validate pipeline data
```
jasentool validate (-i INPUT_FILE [INPUT_FILE ...] | --input_dir INPUT_DIR) --db_name DB_NAME --db_collection DB_COLLECTION -o OUTPUT_FILE [--address ADDRESS] [-h]
```

### Find missing samples
```
jasentool missing --db_name <db_name> --db_collection <db_collection> --analysis_dir <jasen_analysis_results_dir> --restore_dir <restore_dir> --restore_file <restore_file.sh> -o <output_file.csv>
```

### Fix bjorn csv
```
jasentool fix --csv_file /data/tmp/multi_microbiology.csv --sh_file /data/tmp/multi_microbiology.sh -o <flow_cell_id>_jasen.csv --remote_dir /fs1/ryan/pipelines/jasen/bjorn/ --remote
```

### Convert cgmlst.org target files to bed files
```
jasentool convert [-i INPUT_FILE [INPUT_FILE ...]] -o OUTPUT_FILE [-f OUT_FORMAT] [-a ACCESSION] [-h]
```

### Converge tuberculosis mutation catlogues
```
jasentool converge --output_dir OUTPUT_DIR [--save_dbs]
```

### Extract QC values after alignment
```
jasentool qc --sample_id SAMPLE_ID --bam_file BAM_FILE --reference REFERENCE -o OUTPUT_FILE [--bed_file BED_FILE] [--baits_file BAITS_FILE] [--cpus CPUS] [-h]
```
