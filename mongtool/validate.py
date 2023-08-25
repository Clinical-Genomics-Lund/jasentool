import json
from mongtool.database import Database

class Validate(object):
    def get_sample_id(self, results):
        return results["sample_id"]

    def get_species_name(self, results):
        return results["species_prediction"][0]["scientific_name"]

    def search(self, search_query, search_kw, search_list):
        return [element for element in search_list if element[search_kw] == search_query]

    def get_virulence_results(self, results):
        return self.search("VIRULENCE", "type", results["element_type_result"])

    def get_pvl(self, results):
        virulence_results = self.get_virulence_results(results)
        return (True if self.search("lukS-PV", "gene_symbol", virulence_results[0]["result"]["genes"]) else False)

    def get_mlst(self, results):
        return self.search("mlst", "type", results["typing_result"])

    def get_cgmlst(self, results):
        return self.search("cgmlst", "type", results["typing_result"])

    def get_mdb_cgv_data(self, db_collection, sample_id):
        mdb_pvl = list(Database.get_pvl(db_collection, {"id": sample_id}))
        mdb_mlst = list(Database.get_mlst(db_collection, {"id": sample_id}))
        mdb_cgmlst = list(Database.get_cgmlst(db_collection, {"id": sample_id}))
        mdb_pvl_present = int(mdb_pvl[0]["aribavir"]["lukS_PV"]["present"])
        mdb_mlst_seqtype = int(mdb_mlst[0]["mlst"]["sequence_type"])
        mdb_mlst_alleles = mdb_mlst[0]["mlst"]["alleles"]
        mdb_cgmlst_alleles = mdb_cgmlst[0]["alleles"]
        return {"pvl": mdb_pvl_present, "mlst_seqtype": mdb_mlst_seqtype, "mlst_alleles": mdb_mlst_alleles, "cgmlst_alleles": mdb_cgmlst_alleles}
    
    def get_fin_data(self, sample_json):
        fin_pvl_present = self.get_pvl(sample_json)
        fin_mlst = self.get_mlst(sample_json)
        fin_cgmlst = self.get_cgmlst(sample_json)
        fin_mlst_seqtype = fin_mlst[0]["result"]["sequence_type"]
        fin_mlst_alleles = fin_mlst[0]["result"]["alleles"]
        fin_cgmlst_alleles = list(fin_cgmlst[0]["result"]["alleles"].values())
        return {"pvl": fin_pvl_present, "mlst_seqtype": fin_mlst_seqtype, "mlst_alleles": fin_mlst_alleles, "cgmlst_alleles": fin_cgmlst_alleles}
    
    def compare_mlst_alleles(self, old_mlst_alleles, new_mlst_alleles):
        match_count, total_count = 0, 0
        for allele in old_mlst_alleles:
            if str(old_mlst_alleles[allele]) == str(new_mlst_alleles[allele]):
                match_count += 1
            total_count += 1
        return 100*(match_count/total_count)

    def compare_cgmlst_alleles(self, old_cgmlst_alleles, new_cgmlst_alleles):
        match_count, total_count = 0, 0
        for allele in range(0, len(old_cgmlst_alleles)):
            if str(old_cgmlst_alleles[allele]) == str(new_cgmlst_alleles[allele]):
                match_count += 1
            total_count += 1
        return 100*(match_count/total_count)

    def compare_data(self, old_data, new_data):
        pvl_comp = int(old_data["pvl"] == new_data["pvl"])
        mlst_seqtype_comp = int(old_data["mlst_seqtype"] == new_data["mlst_seqtype"])
        mlst_alleles = self.compare_mlst_alleles(old_data["mlst_alleles"], new_data["mlst_alleles"])
        cgmlst_alleles = self.compare_cgmlst_alleles(old_data["cgmlst_alleles"], new_data["cgmlst_alleles"])
        return f"pvl,mlst_seqtype,mlst_allele_matches(%),cgmlst_allele_matches(%)\n{pvl_comp},{mlst_seqtype_comp},{mlst_alleles},{cgmlst_alleles}"

    def run(self, input_files, output_fpaths, db_collection):
        for input_idx, input_file in enumerate(input_files):
            with open(input_file, 'r') as fin:
                sample_json = json.load(fin)
                sample_id = self.get_sample_id(sample_json)
                mdb_data_dict = self.get_mdb_cgv_data(db_collection, sample_id)
                species_name = self.get_species_name(sample_json)
                fin_data_dict = self.get_fin_data(sample_json)
                compared_data_output = self.compare_data(mdb_data_dict, fin_data_dict)
            with open(f"{output_fpaths[input_idx]}.csv", 'w+') as fout:
                fout.write(compared_data_output)
