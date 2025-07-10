FROM ghcr.io/ewatercycle/remotebmi-julia:0.1.0

LABEL org.opencontainers.image.source="https://github.com/eWaterCycle/ewatercycle-wflowjl"

# chmod central depot path so all users can access it
RUN chmod 777 ${JULIA_DEPOT_PATH}

# Install Wflow
RUN julia -e 'using Pkg; Pkg.add(PackageSpec(name="Wflow", version="0.8.1"))'
RUN julia -e 'import Pkg; Pkg.add("PackageCompiler")'

RUN apt update
RUN apt install build-essential -y

# https://words.yuvi.in/post/pre-compiling-julia-docker/
# https://github.com/docker-library/julia/issues/79
# note that the -cx16 flag allows it to run on more cpus but can cause performance and stability problems
ENV JULIA_CPU_TARGET="generic;sandybridge,-xsaveopt,clone_all;haswell,-rdrnd,base(1)"

# Write run file
RUN echo "using Wflow" > run.jl
RUN echo "import RemoteBMI.Server: run_bmi_server" >> run.jl
RUN echo "port = parse(Int, get(ENV, \"BMI_PORT\", \"50051\"))" >> run.jl
RUN echo "run_bmi_server(Wflow.Model, \"0.0.0.0\", port)" >> run.jl

# Write precompile file
RUN echo "using Wflow" > compile.jl
RUN echo "using RemoteBMI" >> compile.jl
RUN echo "import RemoteBMI.Server: run_bmi_server" >> compile.jl
RUN echo "port = parse(Int, get(ENV, \"BMI_PORT\", \"50051\"))" >> compile.jl

RUN julia -e 'using PackageCompiler; create_sysimage(["Wflow", "RemoteBMI"], sysimage_path="wflow.so", precompile_execution_file="compile.jl")'

# Expose port and start server
EXPOSE 50051
CMD ["julia", "-J", "wflow.so", "run.jl"]
