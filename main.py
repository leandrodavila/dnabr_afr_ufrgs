"""
DNABR_AFR - Main entry point
"""

import vcf

def main():
    """Main function"""
    print("DNABR_AFR project initialized!")

    vcf_reader = vcf.Reader(open('VCFs\\1001.vcf', 'r'))
    for record in vcf_reader:

        if record.POS <= 16569:
            print(record)    

            for sample in record.samples:
                print(sample.sample, sample['GT'])    


if __name__ == "__main__":
    main()
