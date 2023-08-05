import click
from readtagger import findcluster
from readtagger import VERSION


@click.command()
@click.option('--input_path',
              help='Find cluster in this BAM file.',
              type=click.Path(exists=True))
@click.option('--region',
              help='Find clusters in this Region (Format is chrX:2000-1000).',
              default=None,)
@click.option('--output_bam',
              help='Write out BAM file with cluster information to this path. '
                   'Reads will have an additional "CD" tag to indicate the cluster number',
              type=click.Path(exists=False))
@click.option('--output_gff',
              help='Write out GFF file with cluster information to this path.',
              type=click.Path(exists=False))
@click.option('--output_fasta',
              help='Write out supporting evidence for clusters to this path.',
              type=click.Path(exists=False))
@click.option('--sample_name',
              default=None,
              help='Sample name to use when writing out clusters in GFF file. '
                   'Default is to infer the name from the input filename.',
              )
@click.option('--include_duplicates/--no-include_duplicates',
              help='Include reads marked as duplicates when finding clusters.',
              default=False)
@click.option('--reference_fasta',
              help='Blast cluster contigs against this fasta file',
              default=None)
@click.option('--blastdb',
              help='Blast cluster contigs against this blast database',
              default=None)
@click.option('--bwa_index',
              help='align cluster contigs against this bwa index',
              default=None)
@click.option('--threads', help='Threads to use for cap3 assembly step', default=1, type=click.IntRange(1, 100))
@click.option('--shm_dir', envvar="SHM_DIR", help='Path to shared memory folder', default=None, type=click.Path(exists=True))
@click.version_option(version=VERSION)
def cli(**kwds):
    """Find clusters of reads that support a TE insertion."""
    return findcluster.ClusterManager(**kwds)
