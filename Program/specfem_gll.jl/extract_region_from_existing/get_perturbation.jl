using ArgParse
include("../scripts/perturbation_bin_file.jl")
include("../src/utils/readfiles.jl")

function parse_command_line()
    s = ArgParseSettings()

    @add_arg_table s begin
        "--target_basedir"
            help = "the target gll directory"
        "--reference_basedir"
            help = "the reference gll directory"
        "--output_basedir"
            help = "the output gll directory for perturbation"
        "--nproc"
            help = "number of processors the gll directory correspons to"
    end
    return parse_args(s)
end

function main()
    # parse args
    parsed_args = parse_command_line()
    @show parsed_args["target_basedir"]
    target_basedir = parsed_args["target_basedir"]
    reference_basedir = parse_args["reference_basedir"]
    output_basedir = parsed_args["output_basedir"]
    nproc = parsed_args["nproc"]
    # get nspec
    mesh_info = sem_mesh_read(target_basedir, 0)
    nspec = mesh_info.nspec
    # run generate_perturbation
    generate_perturbation(target_basedir, reference_basedir, output_basedir, nproc, nspec)
end

main()