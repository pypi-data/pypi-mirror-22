from functools import partial
from concurrent.futures import ThreadPoolExecutor
from BCBio import GFF
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation


def write_cluster(clusters, header, output_path, reference_fasta=None, blastdb=None, sample='sample', threads=1):
    """Write clusters as GFF entries."""
    with open(output_path, "w") as out_handle:
        tp = ThreadPoolExecutor(threads)
        futures = []
        records = {tid: SeqRecord(Seq(""), header['SQ'][tid]['SN']) for tid in range(len(header['SQ']))}
        for i, cluster in enumerate(clusters):
            func = partial(get_feature, cluster, sample, i)
            futures.append(tp.submit(func))
        for future in futures:
            tid, feature = future.result()
            records[tid].features.append(feature)
        GFF.write(records.values(), out_handle)
        tp.shutdown(wait=True)


def get_feature(cluster, sample, i):
    """Turn a cluster into a biopython SeqFeature."""
    genotype = cluster.genotype_likelihood()
    qualifiers = {"source": "findcluster",
                  "score": cluster.score,
                  "left_support": cluster.left_support,
                  "right_support": cluster.right_support,
                  "non_support": genotype.nref,
                  "genotype": genotype.genotype,
                  "genotype_likelihoods": [genotype.reference, genotype.heterozygous, genotype.homozygous],
                  "left_insert": [v for pair in enumerate(cluster.left_contigs) for v in pair],
                  "right_insert": [v for pair in enumerate(cluster.right_contigs) for v in pair],
                  "ID": "%s_%d" % (sample, i),
                  "valid_TSD": cluster.valid_tsd}
    if cluster.reference_name:
        qualifiers['insert_reference'] = cluster.reference_name
    feature = SeqFeature(FeatureLocation(cluster.start, cluster.end), type=cluster.reference_name or "TE", strand=1, qualifiers=qualifiers)
    if cluster.feature_args:
        seqfeature_args = cluster.feature_args
        base_args = {'location': FeatureLocation(cluster.start, cluster.end), 'strand': 1}
        subfeatures = []
        for feature_args in seqfeature_args:
            args = base_args.copy()
            args.update(feature_args)
            subfeatures.append(SeqFeature(**args))
        feature.sub_features = subfeatures
    return cluster.tid, feature
