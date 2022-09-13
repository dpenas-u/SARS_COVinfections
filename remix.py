import argparse, os, utils, mixtas, sys

# parse arguments (-B)
parser = argparse.ArgumentParser(description="Script to infer a potential co-infection")

parser.add_argument("tsv_file", help="tsv file to extract htz positions")
parser.add_argument("--out_dir", help="Output directory", default=".")
parser.add_argument("--file_sep", help="File separator", default="\t")

parser.add_argument("--include", help="Get SNPs from a certain lineage", 
                    default=[], required=False, action='append')
parser.add_argument("--episode", help="Extra recent episodes (samples) as fasta sequences", 
                    default=[], required=False, action='append')
parser.add_argument("--min_DP", help="minimum frequency (depth) to accept a SNP", default=15,
                    type=int)
parser.add_argument("--min_HOM", help="minimum proportion for homocigosis",
                    default=0.85, type=float)
parser.add_argument("--ambiguity", help="min value to segregate", default=0.56, type=float)
parser.add_argument("--min_SNP_pos", help="min value to segregate", default=15, type=int)
parser.add_argument("--min_SNP_percentage", help="min value to segregate", default=0.85, type=float)

parser.add_argument("--pangolin", help="pangolin annotation", 
                    action="store_true")
parser.add_argument("--snipit", help="snipit analysis", 
                    action="store_true")

# main
def main():

    # Script directory
    abs_path = os.path.abspath(sys.argv[0])
    script_dir = os.path.dirname(abs_path)

    # check arguments
    args = parser.parse_args()

    if utils.check_argmunets(args, script_dir):
        exit(1)

    else:

        # Check out dir
        utils.check_create_dir(args.out_dir)

        # tsv file (SNPs)
        name_tsv = os.path.basename(args.tsv_file).rstrip(".tsv")

        # Parse mutations.
        mut_dir = os.path.join(script_dir, "mutations")
        mutations = utils.parse_mut(mut_dir, args)

    # main function
    df = mixtas.get_lineage(args, name_tsv, mutations)

    # get HTZ/HOM positions
    HTZ_SNVs, HOM_SNVs = mixtas.get_HTZ(df, args, name_tsv, mutations)

    # get alingment
    mixtas.get_alingment(args, script_dir, name_tsv, HTZ_SNVs, HOM_SNVs, df, mutations)

    # include previous or post episodes
    if args.episode:
        mixtas.compare_episode(args, name_tsv, script_dir)
    
    # If all OK
    exit(0)

if __name__ == "__main__":
    main()
