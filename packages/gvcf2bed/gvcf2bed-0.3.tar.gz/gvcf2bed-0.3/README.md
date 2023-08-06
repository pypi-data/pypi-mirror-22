GVCF2BED
========

This is a small tool to convert a gVCF file to BED.
This is useful for extracting regions that pass a certain genotype quality threshold.
 

## Installation

gvcf2bed is now available through pypi with: 
`pip install gvcf2bed` 


## Requirements

* Python 3.4+
* pyvcf
* cyvcf2

### For developers

* pytest
* pytest-cov

## Changelog

### 0.3 

* Use `cyvcf2` by default in tool. This results in a speed-up of approximately
8-10x. Existing API has not changed, and will still work with `pyvcf`.
* Add separate filter for non-variants, as GQ scores may have a different
distribution on non-variant records than on variant records.


## Usage

```
usage: gvcf2bed [-h] -I INPUT -O OUTPUT [-s SAMPLE] [-q QUALITY]
                [-nq NON_VARIANT_QUALITY] [-b]

Create a BED file from a gVCF. Regions are based on a minimum genotype
quality. The gVCF file must contain a GQ field in its FORMAT fields. GQ scores
of non-variants records have a different distribution from the GQ score
distribution of variant records. Hence, an option is provided to set a
different threshold for non-variant positions.

optional arguments:
  -h, --help            show this help message and exit
  -I INPUT, --input INPUT
                        Input gVCF
  -O OUTPUT, --output OUTPUT
                        Output bed file
  -s SAMPLE, --sample SAMPLE
                        Sample name in VCF file to use. Will default to first
                        sample (alphabetically) if not supplied
  -q QUALITY, --quality QUALITY
                        Minimum genotype quality (default 20)
  -nq NON_VARIANT_QUALITY, --non-variant-quality NON_VARIANT_QUALITY
                        Minimum genotype quality for non-variant records
                        (default 20)
  -b, --bedgraph        Output in bedgraph mode

```